"""M2: preprocessing of Leon Levy infrared fragment images.

For one image: fetch the half-resolution pyramid level, normalise exposure,
build a parchment mask (without tissue strips and neighbouring fragments),
binarise ink, deskew, and segment text lines with projection profiles.

Everything written goes under data/m2/ (never committed):
  data/m2/crop/{name}.png   deskewed grey crop of the fragment, outside mask = 0
  data/m2/ink/{name}.png    binarised ink (255 = ink) in the same frame
  data/m2/seg/{name}.json   angle, crop box, line bands, measurements
"""
import io, json, os, re, time, urllib.request
import numpy as np, cv2
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

D2 = 'data/m2'


# ---------------------------------------------------------------- fetch
def get(u, tries=4):
    for k in range(tries):
        try:
            r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            return urllib.request.urlopen(r, timeout=60).read()
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(2 ** k)


def fetch_level(url, inverse_scale=2):
    """Stitch one pyramid level. Returns (grey uint8 array, inverse_scale used)."""
    base = url.replace('http://', 'https://')
    x = get(base + '=g').decode()
    tw = int(re.search(r'tile_width="(\d+)"', x).group(1))
    lv = re.findall(r'num_tiles_x="(\d+)" num_tiles_y="(\d+)" inverse_scale="(\d+)" '
                    r'empty_pels_x="(\d+)" empty_pels_y="(\d+)"', x)
    lv = [tuple(map(int, v)) for v in lv]
    z = next((i for i, v in enumerate(lv) if v[2] == inverse_scale), len(lv) - 1)
    nx, ny, inv, ex, ey = lv[z]
    canvas = np.zeros((ny * tw, nx * tw), np.uint8)

    def tile(ab):
        a, b = ab
        im = Image.open(io.BytesIO(get(f'{base}=x{a}-y{b}-z{z}-nt0'))).convert('L')
        return a, b, np.array(im)
    with ThreadPoolExecutor(6) as pool:
        for a, b, t in pool.map(tile, [(a, b) for a in range(nx) for b in range(ny)]):
            canvas[b * tw:b * tw + t.shape[0], a * tw:a * tw + t.shape[1]] = t
    return canvas[:ny * tw - ey, :nx * tw - ex], inv


# ---------------------------------------------------------------- mask
def normalise(g):
    hi = np.percentile(g, 99.9)
    if hi > 20:
        g = np.clip(g.astype(np.float32) * (230.0 / hi), 0, 255).astype(np.uint8)
    return g


def parchment_mask(g, close=45):
    """Bright parchment on black; tissue strips are mid-grey and textured.

    Returns (mask uint8 0/1 of the kept fragment, info dict).
    """
    b = cv2.GaussianBlur(g, (0, 0), 3)
    fg = b > 35
    info = {}
    if fg.sum() < 500:
        return np.zeros_like(g), dict(error='no foreground')
    vals = b[fg]
    # Otsu between tissue and parchment on the foreground only; tissue strips
    # are mid-grey, parchment bright
    t_otsu, _ = cv2.threshold(vals.reshape(-1, 1), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    upper, lower = vals[vals > t_otsu], vals[vals <= t_otsu]
    split = len(lower) > 0.03 * len(vals) and lower.mean() < 0.72 * upper.mean()
    t = t_otsu if split else max(0.5 * np.percentile(vals, 60), 45)
    info.update(t=float(t), split=bool(split))
    parch = (b > t).astype(np.uint8)
    # a small closing only, so that neighbouring fragments stay separate
    parch = cv2.morphologyEx(parch, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    parch = cv2.morphologyEx(parch, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    n, lab, st, cen = cv2.connectedComponentsWithStats(parch)
    if n < 2:
        return parch, dict(info, error='no parchment')
    areas = st[1:, 4]
    k = 1 + int(np.argmax(areas))
    # keep the main piece plus large pieces close to it (a cracked fragment);
    # drop neighbours at the frame edge and small far-away scraps
    keep = [k]
    H, W = g.shape
    diag = np.hypot(*st[k, 2:4])
    for i in range(1, n):
        if i == k or st[i, 4] < 0.15 * areas.max():
            continue
        x, y, w, h = st[i, :4]
        touches_edge = x <= 2 or y <= 2 or x + w >= W - 2 or y + h >= H - 2
        near = np.hypot(*(cen[i] - cen[k])) < 0.9 * diag
        if near and not touches_edge:
            keep.append(i)
    kept = np.isin(lab, keep).astype(np.uint8)
    # letters are dark and open notches at the edge: close the kept piece with
    # a kernel wider than a stroke, then fill holes (ink, cracks)
    kern = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (close, close))
    kept = cv2.morphologyEx(kept, cv2.MORPH_CLOSE, kern)
    cnt, _ = cv2.findContours(kept, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(kept)
    cv2.drawContours(filled, cnt, -1, 1, -1)
    mask = filled
    info.update(components=int(n - 1), kept=len(keep), area=int(mask.sum()),
                dropped_area=int(parch.sum() - (parch & mask).sum()))
    return mask, info


# ---------------------------------------------------------------- ink
def sauvola(g, win, k=0.25, R=128.0):
    f = g.astype(np.float64)
    m = cv2.boxFilter(f, -1, (win, win), borderType=cv2.BORDER_REFLECT)
    s = np.sqrt(np.maximum(cv2.boxFilter(f * f, -1, (win, win), borderType=cv2.BORDER_REFLECT) - m * m, 0))
    return m * (1 + k * (s / R - 1))


def binarise(g, mask, win=61):
    # fill outside with the parchment median so the edge does not read as ink
    med = np.median(g[mask == 1]) if mask.any() else 128
    h = np.where(mask == 1, g, med).astype(np.uint8)
    ink = (h < sauvola(h, win)) & (mask == 1)
    # the mask edge is dark (shadow, fraying): peel a thin border
    inner = cv2.erode(mask, np.ones((9, 9), np.uint8))
    ink &= inner == 1
    ink = cv2.morphologyEx(ink.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink)
    small = np.where(st[:, 4] < 12)[0]
    ink[np.isin(lab, small)] = 0
    return ink


# ---------------------------------------------------------------- deskew + lines
def _angle_scores(xs, ys, angles):
    cx, cy = xs.mean(), ys.mean()
    out = []
    for a in angles:
        r = np.deg2rad(a)
        yy = (-(xs - cx) * np.sin(r) + (ys - cy) * np.cos(r)).astype(int)
        h = np.bincount(yy - yy.min())
        out.append(float((h.astype(np.float64) ** 2).sum()))
    return np.array(out)


def best_angle(ink, wide=18.0, step=0.25, penalty=0.02):
    """Projection-profile deskew with a prior towards 0 degrees.

    Short texts give flat, unreliable score curves, so an angle a must raise
    the profile score over the 0-degree score by more than penalty*|a|
    (15 degrees needs +30%)."""
    ys, xs = np.nonzero(ink)
    if len(ys) < 50:
        return 0.0
    angles = np.arange(-wide, wide + 1e-9, step)
    sc = _angle_scores(xs, ys, angles)
    gain = sc / sc[np.argmin(np.abs(angles))]
    return float(angles[np.argmax(gain - penalty * np.abs(angles))])


def rotate(img, angle, interp=cv2.INTER_LINEAR):
    H, W = img.shape
    M = cv2.getRotationMatrix2D((W / 2, H / 2), angle, 1.0)
    return cv2.warpAffine(img, M, (W, H), flags=interp, borderValue=0)


def dark_ink(g, ink, mask, rel=0.6):
    """Ink components darker than rel x parchment median (cracks and shadows
    are grey in infrared, ink near black). Falls back to all ink when the dark
    part is under half the ink (faded fragments). Returns (ink, contrast)."""
    med = float(np.median(g[mask == 1])) if mask.any() else 128.0
    n, lab, st, _ = cv2.connectedComponentsWithStats(ink)
    if n < 2:
        return ink, None
    sums = np.bincount(lab.ravel(), weights=g.ravel().astype(np.float64), minlength=n)
    means = sums[1:] / np.maximum(st[1:, 4], 1) / max(med, 1)
    area = st[1:, 4]
    contrast = float(np.average(means, weights=area))
    dark = means < rel
    if area[dark].sum() < 0.5 * area.sum():
        return ink, contrast
    keep = np.concatenate([[False], dark])
    return keep[lab].astype(np.uint8), contrast


def lines_from_profile(ink, mask):
    """Text-line bands from the row profile of ink, normalised by mask width."""
    prof = ink.sum(1).astype(np.float64)
    width = np.maximum(mask.sum(1), 1)
    prof = prof / np.maximum(width, 0.15 * width.max())
    if prof.max() <= 0:
        return [], None
    # line pitch from the autocorrelation of the profile
    p = prof - prof.mean()
    ac = np.correlate(p, p, 'full')[len(p) - 1:]
    ac /= ac[0] if ac[0] else 1
    # first peak after the autocorrelation first dips below zero
    pitch = None
    neg = np.nonzero(ac[20:] < 0)[0]
    if len(neg):
        start = 20 + int(neg[0])
        hi = min(len(ac) - 1, 450)
        if hi > start + 2:
            cand = start + int(np.argmax(ac[start:hi]))
            if ac[cand] > 0.05 and 40 <= cand < hi - 1:
                pitch = cand
    sm = cv2.GaussianBlur(prof.reshape(-1, 1), (1, 0), (pitch or 60) / 6).ravel()
    # peaks at least 0.6 pitch apart, above 20% of the strongest peak
    d = int(0.6 * (pitch or 60))
    peaks = [i for i in range(1, len(sm) - 1) if sm[i] >= sm[i - 1] and sm[i] > sm[i + 1]
             and sm[i] > 0.2 * sm.max()]
    peaks.sort(key=lambda i: -sm[i])
    chosen = []
    for i in peaks:
        if all(abs(i - j) >= d for j in chosen):
            chosen.append(i)
    chosen.sort()
    bands = []
    for j, c in enumerate(chosen):
        top = (chosen[j - 1] + c) // 2 if j else max(0, c - (pitch or 60) // 2)
        bot = (c + chosen[j + 1]) // 2 if j + 1 < len(chosen) else min(len(sm) - 1, c + (pitch or 60) // 2)
        rows = ink[top:bot]
        cols = np.nonzero(rows.sum(0))[0]
        bands.append(dict(y=int(c), top=int(top), bottom=int(bot),
                          x0=int(cols.min()) if len(cols) else 0,
                          x1=int(cols.max()) if len(cols) else 0,
                          ink=int(rows.sum()), strength=round(float(sm[c] / sm.max()), 3)))
    return bands, pitch


# ---------------------------------------------------------------- one image
def load_raw(name, url):
    """Half-resolution level, cached in data/m2/raw/ (local only)."""
    path = f'{D2}/raw/{name}.png'
    if os.path.exists(path):
        return cv2.imread(path, 0), 2
    g, inv = fetch_level(url)
    os.makedirs(f'{D2}/raw', exist_ok=True)
    if inv == 2:
        cv2.imwrite(path, g)
    return g, inv


def process(name, url, save=True):
    g, inv = load_raw(name, url)
    g = normalise(g)
    mask, info = parchment_mask(g)
    if 'error' in info or mask.sum() < 2000:
        return dict(name=name, inverse_scale=inv, mask=info, error=info.get('error', 'tiny mask'))
    ink = binarise(g, mask)
    angle = best_angle(dark_ink(g, ink, mask)[0])
    g2, m2 = rotate(g, angle), rotate(mask * 255, angle, cv2.INTER_NEAREST) // 255
    i2 = rotate(ink * 255, angle, cv2.INTER_NEAREST) // 255
    ys, xs = np.nonzero(m2)
    pad = 10
    y0, y1 = max(0, ys.min() - pad), min(m2.shape[0], ys.max() + pad)
    x0, x1 = max(0, xs.min() - pad), min(m2.shape[1], xs.max() + pad)
    g2, m2, i2 = g2[y0:y1, x0:x1], m2[y0:y1, x0:x1], i2[y0:y1, x0:x1]
    dk, contrast = dark_ink(g2, i2, m2)
    bands, pitch = lines_from_profile(dk, m2)
    rec = dict(name=name, inverse_scale=inv, shape=list(g.shape), angle=angle,
               box=[int(x0), int(y0), int(x1), int(y1)], mask=info, pitch=pitch,
               ink_px=int(i2.sum()), dark_ink_px=int(dk.sum()),
               ink_contrast=round(contrast, 3) if contrast is not None else None,
               lines=bands)
    if save:
        for d in ('crop', 'ink', 'seg'):
            os.makedirs(f'{D2}/{d}', exist_ok=True)
        cv2.imwrite(f'{D2}/crop/{name}.png', np.where(m2 == 1, g2, 0).astype(np.uint8))
        cv2.imwrite(f'{D2}/ink/{name}.png', (i2 * 255).astype(np.uint8))
        json.dump(rec, open(f'{D2}/seg/{name}.json', 'w'))
    return rec


def overlay(name, out, maxw=900):
    """Debug view: crop with line bands and ink in red (local only)."""
    g = cv2.imread(f'{D2}/crop/{name}.png', 0)
    ink = cv2.imread(f'{D2}/ink/{name}.png', 0)
    rec = json.load(open(f'{D2}/seg/{name}.json'))
    v = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)
    v[ink > 0] = (0.5 * v[ink > 0] + [0, 0, 120]).astype(np.uint8)
    for i, b in enumerate(rec['lines']):
        cv2.line(v, (0, b['y']), (v.shape[1], b['y']), (0, 200, 0), 2)
        cv2.line(v, (0, b['top']), (v.shape[1], b['top']), (200, 120, 0), 1)
        cv2.putText(v, str(i + 1), (5, b['y'] - 4), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
    s = min(1.0, maxw / v.shape[1])
    v = cv2.resize(v, (int(v.shape[1] * s), int(v.shape[0] * s)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(out, v)
