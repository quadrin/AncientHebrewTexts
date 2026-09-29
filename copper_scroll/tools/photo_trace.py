"""Clear images and word tracings for the atlas photograph of strip 13 (column VII).

The atlas shows Osama Shukir Muhammed Amin's photograph of original strip 13 in
the Jordan Museum (Wikimedia Commons, CC BY-SA 4.0, 2467 x 4016). No infrared
image of 3Q15 exists (the scroll is metal; the Leon Levy library lists 3Q15
with no images). This tool makes two clearer versions of the open photograph
and traces the letters of VII 7-11 on it, with Puech's radiograph as the
reference for which strokes are letters.

    python copper_scroll/tools/photo_trace.py enhance PHOTO
    python copper_scroll/tools/photo_trace.py trace PHOTO PLATEDIR [--update]

PHOTO     the Commons original, full resolution (any format OpenCV reads)
PLATEDIR  output of tools/plate_extract.py for column 7; uses 07_radio2_1.png,
          the second exposure of the radiograph of strip 13, Puech 2006 vol. II,
          pl. CCCXLVI. Copyrighted plate material: it stays local and is never
          written into the atlas.

Needs numpy, opencv-python-headless, scipy and scikit-image.

enhance writes atlas/public/scroll/strip13.webp (the photograph, full size),
strip13-grooves.webp (groove map) and strip13-relief.webp (relief).

trace prints the candidate strokes and writes the curated tracing to
registration/photo_tracing_strip13.json; --update also writes the paths and
hit boxes into atlas/app/atlas-photo-data.json. Coordinates are in the
reader's 1000 x 1628 system (1 unit = 2.467 px of the original).

Method (trace):
 1. Groove map of the photograph at the 1600-px working size: grey, Gaussian
    blur 2 px, black-hat with a 21-px ellipse. Engraved strokes become dark
    lines; the relief lighting and the patina drop out.
 2. Stroke map of the radiograph: black-hat with a 13-px ellipse. Cracks are
    thin, very dark and long: they are found with a 7-px black-hat (top 0.8 %,
    components at least 70 px long) and removed.
 3. One affine transform radiograph -> photograph: three hand-picked points
    (the apex of the triangular mem in VII 8, the corrosion hole in VII 9, the
    first letter of VII 8's second word), refined by ECC on the two maps.
 4. Radiograph strokes are skeletonised and split into segments. Each word
    gets one shift (search +/- 20 units), each segment a further shift
    (+/- 6 units, small distance penalty), maximising the groove response of
    the photograph along the segment.
 5. Curation (CURATION below): a segment is kept only where the photograph
    shows its groove. A few grooves the transfer missed but the photograph
    shows clearly are drawn by hand (MANUAL). Strokes the photograph does not
    show are left out, even when the radiograph has them.
"""
import argparse, json, os, sys
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS = os.path.join(HERE, '..', 'atlas')
UNITS_W = 1000                      # reader coordinate width
WORK_W = 1600                       # working width for tracing
PX = WORK_W / UNITS_W               # working px per unit

# Radiograph word boxes (px of 07_radio2_1.png), checked against Puech's facsimile pl. CCCLXXII.
WORDS = {
    'VII-7-0': (295, 765, 458, 858),    # ככרין
    'VII-8-0': (183, 888, 465, 978),    # במערא
    'VII-9-0': (323, 1008, 458, 1092),  # בית
    'VII-9-1': (140, 1005, 322, 1105),  # הקץ
    'VII-10-0': (305, 1105, 462, 1192), # כדין
    'VII-10-1': (175, 1110, 300, 1190), # של
    'VII-11-0': (275, 1212, 465, 1308), # בדוק
    'VII-11-1': (68, 1212, 272, 1305),  # תחת
}
# Control points for the initial affine: radiograph px -> photograph units.
CONTROL = [((373, 905), (656, 628)), ((317.5, 1041), (567.5, 817.5)), ((171.7, 920), (255, 630))]
# Candidate segments kept after inspection on the groove map (indices printed by `trace`).
CURATION = {
    'VII-7-0': [2, 3, 6, 4, 7, 9],
    'VII-8-0': [0, 2, 3, 4, 13, 5, 8, 6, 7, 9, 14],
    'VII-9-0': [2, 4, 10],
    'VII-9-1': [0, 1, 9, 11, 13, 12, 5],
    'VII-10-0': [8, 7, 3, 5, 0, 6],
    'VII-10-1': [0, 1],
    'VII-11-0': [9, 8, 4, 5, 1, 2, 3, 6],
    'VII-11-1': [10, 11, 4, 0, 8],
}
# Grooves drawn by hand where the photograph shows them clearly (units).
MANUAL = {
    'VII-7-0': [[(697, 533), (712, 527), (728, 521)]],                          # right part of the base line
    'VII-8-0': [[(371, 619), (386, 642), (401, 663), (414, 680), (428, 694)]],  # long stroke of alef
    'VII-9-1': [[(458, 800), (495, 802), (533, 806)],                           # roof of he
                [(333, 830), (350, 817), (368, 803)]],                          # upper stroke of final tsade
    'VII-11-1': [[(387, 1111), (398, 1108), (411, 1110)]],                      # roof of het
}


def blackhat(img, k, blur):
    b = cv2.GaussianBlur(img, (0, 0), blur) if blur else img
    h = cv2.morphologyEx(b, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    return h.astype(np.float32)


def enhance(photo):
    img = cv2.imread(photo)
    if img is None:
        sys.exit(f'cannot read {photo}')
    H, W = img.shape[:2]
    s = W / WORK_W
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    k = int(round(21 * s)) | 1
    bh = blackhat(grey, k, 2.0 * s)
    bh = np.clip(bh / np.percentile(bh, 99.6), 0, 1)
    grooves = (255 * (1 - bh ** 0.8)).astype(np.uint8)
    relief = cv2.createCLAHE(2.5, (10, 16)).apply(cv2.fastNlMeansDenoising(grey, None, 5, 7, 21))
    out = os.path.join(ATLAS, 'public', 'scroll')
    os.makedirs(out, exist_ok=True)
    for name, im, q in (('strip13.webp', img, 86), ('strip13-grooves.webp', grooves, 80), ('strip13-relief.webp', relief, 80)):
        path = os.path.join(out, name)
        cv2.imwrite(path, im, [cv2.IMWRITE_WEBP_QUALITY, q])
        print(path, im.shape[1], 'x', im.shape[0], os.path.getsize(path) // 1024, 'KB')


def segments(skel):
    from scipy import ndimage as ndi
    k = np.ones((3, 3), int); k[1, 1] = 0
    nb = ndi.convolve(skel.astype(int), k, mode='constant') * skel
    body = skel & ~ndi.binary_dilation(skel & (nb > 2), np.ones((3, 3)))
    lab, n = ndi.label(body, np.ones((3, 3)))
    segs = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < 6:
            continue
        pts = set(zip(xs.tolist(), ys.tolist()))
        nbrs = lambda p: [(p[0] + dx, p[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1)
                          if (dx or dy) and (p[0] + dx, p[1] + dy) in pts]
        start = next((p for p in pts if len(nbrs(p)) == 1), next(iter(pts)))
        path, seen, cur = [start], {start}, start
        while True:
            nx = [q for q in nbrs(cur) if q not in seen]
            if not nx:
                break
            cur = nx[0]; seen.add(cur); path.append(cur)
        if len(path) >= 6:
            segs.append(np.array(path, float))
    return segs


def trim_boxes(result):
    """Split overlapping hit boxes at the middle of the overlap. The words slope,
    so their axis-aligned boxes overlap slightly; the reader selects the first box hit."""
    ids = list(result)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ax, ay, aw, ah = result[a]['box']; bx, by, bw, bh = result[b]['box']
            ox = min(ax + aw, bx + bw) - max(ax, bx); oy = min(ay + ah, by + bh) - max(ay, by)
            if ox <= 0 or oy <= 0:
                continue
            if a.rsplit('-', 1)[0] == b.rsplit('-', 1)[0]:     # same line: split in x (a lies to the right)
                cut = round(max(ax, bx) + ox / 2)
                result[a]['box'] = [cut, ay, ax + aw - cut, ah]
                result[b]['box'] = [bx, by, cut - bx, bh]
            else:                                              # next line: split in y (a lies above)
                cut = round(max(ay, by) + oy / 2)
                result[a]['box'] = [ax, ay, aw, cut - ay]
                result[b]['box'] = [bx, cut, bw, by + bh - cut]


def trace(photo, platedir, update):
    from scipy import ndimage as ndi
    from skimage.filters import apply_hysteresis_threshold
    from skimage.morphology import skeletonize, remove_small_objects

    img = cv2.imread(photo, cv2.IMREAD_GRAYSCALE)
    rad = cv2.imread(os.path.join(platedir, '07_radio2_1.png'), cv2.IMREAD_GRAYSCALE)
    if img is None or rad is None:
        sys.exit('missing photograph or 07_radio2_1.png')
    P = cv2.resize(img, (WORK_W, round(img.shape[0] * WORK_W / img.shape[1])), interpolation=cv2.INTER_AREA)
    Sp = blackhat(P, 21, 2.0); Sp /= np.percentile(Sp, 99.5)
    Sr0 = blackhat(rad, 13, 1.0); Sr0 /= np.percentile(Sr0, 99.5)
    # remove cracks
    thin = blackhat(rad, 7, 0)
    m = cv2.morphologyEx((thin > np.percentile(thin, 99.2)).astype(np.uint8), cv2.MORPH_CLOSE,
                         cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m, 8)
    crack = np.isin(lab, [i for i in range(1, n) if max(st[i][2], st[i][3]) >= 70]).astype(np.uint8)
    Sr0 *= 1 - cv2.dilate(crack, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))
    Sr = np.zeros_like(Sp); Sr[:Sr0.shape[0], :Sr0.shape[1]] = Sr0
    # global affine (photo px -> radiograph px), ECC from the control points
    A = cv2.getAffineTransform(np.float32([c[0] for c in CONTROL]), np.float32([c[1] for c in CONTROL]) * PX)
    W = cv2.invertAffineTransform(A).astype(np.float32)
    mask = np.zeros(P.shape, np.uint8)
    x0, y0, x1, y1 = (int(v * PX) for v in (200, 380, 830, 1260))
    mask[y0:y1, x0:x1] = 255
    crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 300, 1e-6)
    for sig in (12, 8, 5, 3):
        cc, W = cv2.findTransformECC(cv2.GaussianBlur(Sp, (0, 0), sig), cv2.GaussianBlur(Sr, (0, 0), sig / 2.3),
                                     W, cv2.MOTION_AFFINE, crit, mask, 5)
    A0 = cv2.invertAffineTransform(W).astype(np.float64)
    print('affine radiograph -> photo units:', np.round(A0 / PX, 4).tolist(), 'ECC', round(cc, 3))
    # radiograph skeleton segments
    b = cv2.GaussianBlur(Sr0, (0, 0), 1.0)
    sk = skeletonize(remove_small_objects(apply_hysteresis_threshold(b, 0.22, 0.45), max_size=25))
    segs = segments(sk)
    G = cv2.GaussianBlur(Sp, (0, 0), 2.2)
    sample = lambda pts: ndi.map_coordinates(G, [pts[:, 1], pts[:, 0]], order=1, mode='constant')
    result = {}
    for wid, (bx0, by0, bx1, by1) in WORDS.items():
        mine = [s for s in segs if bx0 <= s[:, 0].mean() <= bx1 and by0 <= s[:, 1].mean() <= by1]
        photo_segs = [cv2.transform(s[None], A0)[0] for s in mine]
        L = np.array([len(s) for s in photo_segs], float)
        best = (-1, None)
        for dx in np.arange(-20, 21) * PX:
            for dy in np.arange(-20, 21) * PX:
                sc = sum(sample(s + (dx, dy)).mean() * l for s, l in zip(photo_segs, L)) / L.sum()
                if sc > best[0]:
                    best = (sc, np.array((dx, dy)))
        shift = best[1]
        cands = []
        for s, l in zip(photo_segs, L):
            if l / PX < 5:
                continue
            bb = (-1e9, None)
            for dx in np.arange(-6, 6.5) * PX:
                for dy in np.arange(-6, 6.5) * PX:
                    sc = sample(s + shift + (dx, dy)).mean() - 0.006 * np.hypot(dx, dy) / PX
                    if sc > bb[0]:
                        bb = (sc, (dx, dy))
            u = (s + shift + bb[1]) / PX
            k = max(1, min(4, len(u) // 5))
            us = np.array([u[max(0, i - k):i + k + 1].mean(0) for i in range(len(u))])
            us[0], us[-1] = u[0], u[-1]
            cands.append(cv2.approxPolyDP(us.astype(np.float32).reshape(-1, 1, 2), 1.2, False).reshape(-1, 2))
        print(wid, 'word shift (units)', np.round(shift / PX, 1).tolist())
        for i, c in enumerate(cands):
            print(f'   {i:2d}  {np.round(c[0], 1).tolist()} -> {np.round(c[-1], 1).tolist()}')
        strokes = [cands[i] for i in CURATION[wid]] + [np.array(m, float) for m in MANUAL.get(wid, [])]
        # hit box: the radiograph word box carried into the photograph, padded
        corners = cv2.transform(np.float32([[bx0, by0], [bx1, by0], [bx1, by1], [bx0, by1]])[None], A0)[0] + shift
        lo, hi = corners.min(0) / PX, corners.max(0) / PX
        result[wid] = {
            'box': [round(lo[0] - 6), round(lo[1] - 4), round(hi[0] - lo[0] + 12), round(hi[1] - lo[1] + 8)],
            'paths': ['M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in s) for s in strokes],
        }
    trim_boxes(result)
    out = os.path.join(HERE, '..', 'registration', 'photo_tracing_strip13.json')
    json.dump({'description': 'Curated word tracings of strip 13, VII 7-11, on the Jordan Museum photograph '
                              '(reader units, 1000 x 1628). Made by tools/photo_trace.py.',
               'words': result}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('wrote', os.path.normpath(out))
    if update:
        path = os.path.join(ATLAS, 'app', 'atlas-photo-data.json')
        data = json.load(open(path, encoding='utf-8'))
        for w in data['words']:
            w['box'] = result[w['id']]['box']
            w['paths'] = result[w['id']]['paths']
        json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        open(path, 'a').write('\n')
        print('updated', os.path.normpath(path))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('enhance'); e.add_argument('photo')
    t = sub.add_parser('trace'); t.add_argument('photo'); t.add_argument('platedir'); t.add_argument('--update', action='store_true')
    a = ap.parse_args()
    enhance(a.photo) if a.cmd == 'enhance' else trace(a.photo, a.platedir, a.update)
