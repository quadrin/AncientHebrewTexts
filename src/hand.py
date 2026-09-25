"""Scribal-hand features per fragment, and a test of whether they find other
pieces of the same manuscript.

Features (on the dark ink of the M2 crop, half-resolution pyramid level):
  * contour-hinge: at each ink-contour point, the directions to the points
    HINGE_L steps back and forward along the contour, 12 bins each -> 144-bin
    joint histogram (Bulacu & Schomaker's writer feature)
  * contour directions: 12-bin histogram
  * stroke width: histogram of 2 x distance transform on the ink skeleton
  * ink run lengths, horizontal and vertical: log-binned histograms
  * letter size: median height and width of ink components, line pitch
Histograms are square-rooted (Hellinger), scalars standardised; distance is
cosine on the block-weighted vector.

Usage:
  python3 src/hand.py features           -> data/hand/features.npz (all processed crops)
  python3 src/hand.py retrieval          -> reports/M8_hand_retrieval.json
"""
import json, os, sys, collections
import numpy as np, cv2
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from prep import dark_ink  # noqa: E402

DH = 'data/hand'
HINGE_L = 6
NB = 12
RUN_BINS = np.array([1, 2, 3, 4, 6, 8, 11, 16, 23, 32, 45, 64, 1e9])
SW_BINS = np.array([0, 4, 6, 8, 10, 12, 14, 17, 20, 24, 30, 40, 1e9])
MIN_INK = 1500          # dark-ink pixels at half resolution: about 3+ letters


def skeleton(b):
    """Morphological skeleton (OpenCV has no thinning without contrib)."""
    b = b.copy()
    sk = np.zeros_like(b)
    k = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    while b.any():
        er = cv2.erode(b, k)
        sk |= b & ~cv2.dilate(er, k)
        b = er
    return sk


def runs(b, axis):
    """Lengths of ink runs along rows (axis=1) or columns (axis=0)."""
    a = b if axis == 1 else b.T
    a = np.pad(a.astype(np.int8), ((0, 0), (1, 1)))
    d = np.diff(a, axis=1)
    starts = np.argwhere(d == 1)
    ends = np.argwhere(d == -1)
    return ends[:, 1] - starts[:, 1]


def features(name):
    g = cv2.imread(f'data/m2/crop/{name}.png', 0)
    ink = cv2.imread(f'data/m2/ink/{name}.png', 0)
    if g is None or ink is None:
        return name, None
    mask = (g > 0).astype(np.uint8)
    dk, contrast = dark_ink(g, (ink > 0).astype(np.uint8), mask)
    n_ink = int(dk.sum())
    if n_ink < MIN_INK:
        return name, None
    seg = json.load(open(f'data/m2/seg/{name}.json'))
    pitch = seg.get('pitch') or 0
    # contour hinge and directions
    cnts, _ = cv2.findContours(dk.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    hinge = np.zeros((NB, NB))
    dirs = np.zeros(NB)
    for c in cnts:
        c = c[:, 0, :].astype(np.float64)
        if len(c) < 2 * HINGE_L + 1:
            continue
        fwd = np.roll(c, -HINGE_L, axis=0) - c
        back = np.roll(c, HINGE_L, axis=0) - c
        a1 = (np.arctan2(fwd[:, 1], fwd[:, 0]) % (2 * np.pi)) / (2 * np.pi) * NB
        a2 = (np.arctan2(back[:, 1], back[:, 0]) % (2 * np.pi)) / (2 * np.pi) * NB
        i1, i2 = a1.astype(int) % NB, a2.astype(int) % NB
        np.add.at(hinge, (i1, i2), 1)
        np.add.at(dirs, i1, 1)
    # stroke width on the skeleton
    dt = cv2.distanceTransform(dk.astype(np.uint8), cv2.DIST_L2, 3)
    sk = skeleton(dk.astype(np.uint8)).astype(bool)
    sw = np.histogram(2 * dt[sk], SW_BINS)[0].astype(float)
    # run lengths
    rh = np.histogram(runs(dk, 1), RUN_BINS)[0].astype(float)
    rv = np.histogram(runs(dk, 0), RUN_BINS)[0].astype(float)
    # component size (letter-sized components only)
    n, _, st, _ = cv2.connectedComponentsWithStats(dk.astype(np.uint8))
    hs, ws = st[1:, 3], st[1:, 2]
    keep = st[1:, 4] >= 60
    ch = float(np.median(hs[keep])) if keep.any() else 0.0
    cw = float(np.median(ws[keep])) if keep.any() else 0.0
    vec = dict(hinge=hinge.ravel(), dirs=dirs, sw=sw, rh=rh, rv=rv,
               scal=np.array([ch, cw, pitch or 0.0, contrast or 0.0, np.median(2 * dt[sk]) if sk.any() else 0.0]))
    return name, dict(vec=vec, ink=n_ink)


def all_names():
    names = {}
    for f, kind in (('data/m2/batch_parchment.json', 'id'), ('data/m2/batch_shared.json', 'id'),
                    ('data/m2/batch_target.json', 'target')):
        for b in json.load(open(f)):
            if not b.get('error'):
                names[b['name']] = kind
    return names


def build():
    os.makedirs(DH, exist_ok=True)
    names = all_names()
    out = {}
    with ProcessPoolExecutor(4) as ex:
        for k, (n, f) in enumerate(ex.map(features, list(names), chunksize=16)):
            if f:
                out[n] = f
            if k % 1000 == 999:
                print(k + 1, len(out), file=sys.stderr, flush=True)
    keys = sorted(out)
    blocks = ['hinge', 'dirs', 'sw', 'rh', 'rv']
    arr = {b: np.array([out[k]['vec'][b] for k in keys]) for b in blocks + ['scal']}
    np.savez_compressed(f'{DH}/features.npz', names=np.array(keys), ink=np.array([out[k]['ink'] for k in keys]),
                        **arr)
    print(len(keys), 'pieces with features', file=sys.stderr)


def matrix(z, idx=None, weights=None):
    """Feature matrix: Hellinger histograms (each block unit length) + scaled scalars."""
    weights = weights or dict(hinge=1.0, dirs=0.5, sw=0.7, rh=0.5, rv=0.5, scal=0.7)
    parts = []
    for b in ('hinge', 'dirs', 'sw', 'rh', 'rv'):
        h = z[b][idx] if idx is not None else z[b]
        h = np.sqrt(h / np.maximum(h.sum(1, keepdims=True), 1))
        h = h - h.mean(0)
        h = h / np.maximum(np.linalg.norm(h, axis=1, keepdims=True), 1e-9)
        parts.append(weights[b] * h)
    s = z['scal'][idx] if idx is not None else z['scal']
    s = np.log1p(np.maximum(s, 0))
    s = (s - s.mean(0)) / np.maximum(s.std(0), 1e-9)
    s = s / np.sqrt(s.shape[1])
    parts.append(weights['scal'] * s)
    x = np.concatenate(parts, 1)
    return x / np.maximum(np.linalg.norm(x, axis=1, keepdims=True), 1e-9)


def retrieval():
    z = np.load(f'{DH}/features.npz')
    names = list(z['names'])
    inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
    kinds = all_names()
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    idx = [i for i, n in enumerate(names) if kinds[n] == 'id' and pairs[n]['material'] == 'Parchment']
    ms = [inv[names[i]]['manuscript'] for i in idx]
    plate = [inv[names[i]]['plate'] for i in idx]
    x = matrix(z, np.array(idx))
    sim = x @ x.T
    n = len(idx)
    res = collections.Counter()
    chance = []
    msarr, plarr = np.array(ms), np.array(plate)
    for i in range(n):
        # leave out the piece itself and every piece on the same IAA plate:
        # a plate is one photo session (lighting) and usually one manuscript
        valid = plarr != plarr[i]
        same = (msarr == msarr[i]) & valid
        if not same.any():
            continue
        s = np.where(valid, sim[i], -np.inf)
        order = np.argsort(-s)
        top = msarr[order[:10]]
        res['queries'] += 1
        res['top1'] += top[0] == msarr[i]
        res['top5'] += (top[:5] == msarr[i]).any()
        res['top10'] += (top == msarr[i]).any()
        chance.append(same.sum() / valid.sum())
    q = res['queries']
    ch = float(np.mean(chance))
    out = dict(pieces=n, manuscripts=len(set(ms)), queries=q,
               top1=round(res['top1'] / q, 3), top5=round(res['top5'] / q, 3), top10=round(res['top10'] / q, 3),
               chance_top1=round(ch, 4), chance_top10=round(1 - float(np.mean([(1 - c) ** 10 for c in chance])), 3),
               note='neighbours on the same IAA plate are excluded')
    json.dump(out, open('reports/M8_hand_retrieval.json', 'w'), indent=1)
    print(out)


if __name__ == '__main__':
    {'features': build, 'retrieval': retrieval}[sys.argv[1]]()
