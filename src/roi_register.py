"""E2 step 1b: register the SQE letter polygons to the M2 crops.

The polygons are in SQE master-image coordinates (7216 x 5412, 1,215 ppi).
The Leon Levy photo of the same IAA plate/fragment/side (M0 join) is a
square crop of a capture. For each piece with an M2 crop:
  1. fetch the SQE infrared (direct light) image of that side at 1/8 scale
     (902 px wide; the IIIF server serves only its listed sizes), cached
     under data/ (local only, IAA rights)
  2. SIFT + RANSAC similarity from the SQE image to the Leon Levy raw image
     (half resolution, scaled to 1/8 of full)
  3. map every polygon: SQE full -> 1/8 -> Leon Levy 1/8 -> half resolution
     -> M2 deskew rotation -> crop offset
  4. checks: similarity scale (expected ~1; the angle may be 0 or +-90: some
     Leon Levy photos are turned), RANSAC inliers (>= 30),
     and the ink hit rate - share of mapped letter boxes that contain M2 dark
     ink, against the same boxes shifted by 2.5 letter heights (control)
Band: the M2 line band that contains the mapped letter centre (None if none).

Usage: python3 src/roi_register.py
Outputs: data/sqe_rois/registered.json, reports/E2_registration.json
"""
import json, os, sys, re, collections, urllib.request, time
import numpy as np, cv2

sys.path.insert(0, os.path.dirname(__file__))
from sqe_harvest import get  # noqa: E402

DR = 'data/sqe_rois'
D2 = 'data/m2'
UA = {'User-Agent': 'Mozilla/5.0 (research; AncientHebrewTexts)'}


def fetch_sqe(io, side):
    path = f'{DR}/img/{io.replace("/", "_")}_{side}.jpg'
    if os.path.exists(path):
        return cv2.imread(path, 0)
    d = get(f'/imaged-objects/{io}')
    ims = [im for im in d['images'] if im['type'] == 'infrared' and im['side'] == side
           and im.get('lightingType') == 'direct']
    if not ims:
        return None
    b = urllib.request.urlopen(urllib.request.Request(ims[0]['url'] + '/full/902,/0/default.jpg', headers=UA),
                               timeout=120).read()
    os.makedirs(f'{DR}/img', exist_ok=True)
    open(path, 'wb').write(b)
    return cv2.imread(path, 0)


def similarity(a, b):
    """Similarity transform mapping image a onto image b (2x3), inliers, n matches."""
    sift = cv2.SIFT_create(4000)
    ka, da = sift.detectAndCompute(a, None)
    kb, db = sift.detectAndCompute(b, None)
    if da is None or db is None or len(ka) < 10 or len(kb) < 10:
        return None, 0, 0
    m = cv2.BFMatcher().knnMatch(da, db, k=2)
    good = [x for x, y in (p for p in m if len(p) == 2) if x.distance < 0.75 * y.distance]
    if len(good) < 8:
        return None, 0, len(good)
    pa = np.float32([ka[x.queryIdx].pt for x in good])
    pb = np.float32([kb[x.trainIdx].pt for x in good])
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=2.0)
    return M, int(inl.sum()) if inl is not None else 0, len(good)


def pts_of(wkt):
    n = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', wkt)]
    return np.array(list(zip(n[0::2], n[1::2])), np.float64)


def main():
    rois = json.load(open(f'{DR}/rois.json'))
    inv = json.load(open('data/m0/inventory_images.json'))
    key = {(f"IAA-{x['plate']}-{x['frag']}", x['side'].lower()): x for x in inv}
    by = collections.defaultdict(list)
    for r in rois:
        by[(r['imaged_object'], r['side'])].append(r)
    out, pieces = [], []
    t0 = time.time()
    for (io, side), rs in sorted(by.items()):
        x = key.get((io, side))
        if not x or not os.path.exists(f'{D2}/seg/{x["name"]}.json'):
            continue
        n = x['name']
        seg = json.load(open(f'{D2}/seg/{n}.json'))
        raw = cv2.imread(f'{D2}/raw/{n}.png', 0)
        ink = cv2.imread(f'{D2}/ink/{n}.png', 0)
        if raw is None or ink is None or seg.get('inverse_scale') != 2:
            continue
        try:
            sq = fetch_sqe(io, side)
        except Exception as e:
            pieces.append(dict(name=n, io=io, side=side, error=str(e)))
            continue
        if sq is None:
            continue
        fs = sq.shape[1] / 7216.0                       # SQE image scale (1/8)
        ll = cv2.resize(raw, None, fx=fs * 2, fy=fs * 2, interpolation=cv2.INTER_AREA)   # LL at the same scale
        M, inl, ng = similarity(sq, ll)
        rec = dict(name=n, io=io, side=side, rois=len(rs), matches=ng, inliers=inl)
        if M is None or inl < 12:
            rec['error'] = 'no registration'
            pieces.append(rec)
            continue
        scale = float(np.hypot(M[0, 0], M[1, 0]))
        ang = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
        rec.update(scale=round(scale, 4), angle=round(ang, 3))
        H, Wd = raw.shape
        R = cv2.getRotationMatrix2D((Wd / 2, H / 2), seg['angle'], 1.0)
        x0, y0 = seg['box'][0], seg['box'][1]
        dk = (ink > 0).astype(np.uint8)
        hits = ctrl = tot = 0
        for r in rs:
            p = pts_of(r['shape']) * fs                               # SQE 1/8
            p = p @ M[:, :2].T + M[:, 2]                              # LL 1/8
            p = p / (fs * 2)                                          # LL half resolution
            p = p @ R[:, :2].T + R[:, 2]                              # deskewed
            p = p - [x0, y0]                                          # crop
            bx = [float(p[:, 0].min()), float(p[:, 1].min()), float(p[:, 0].max()), float(p[:, 1].max())]
            cx, cy = (bx[0] + bx[2]) / 2, (bx[1] + bx[3]) / 2
            band = next((i for i, b in enumerate(seg['lines']) if b['top'] <= cy <= b['bottom']), None)
            h = max(bx[3] - bx[1], 8)

            def has_ink(dx, dy):
                a0, a1 = int(max(bx[0] + dx, 0)), int(min(bx[2] + dx, dk.shape[1]))
                b0, b1 = int(max(bx[1] + dy, 0)), int(min(bx[3] + dy, dk.shape[0]))
                if a1 <= a0 or b1 <= b0:
                    return None
                return dk[b0:b1, a0:a1].mean() > 0.03
            hi, hc = has_ink(0, 0), has_ink(2.5 * h, 0)
            if hi is not None and hc is not None:
                tot += 1
                hits += hi
                ctrl += hc
            out.append(dict(name=n, io=io, side=side, edition=r['edition'], text_fragment=r['text_fragment'],
                            line=r['line'], sign=r['sign'], char=r['char'], letter=r['letter'],
                            readability=r['readability'], reconstructed=r['reconstructed'],
                            crop_bbox=[round(v, 1) for v in bx], band=band))
        rec.update(ink_hit=round(hits / tot, 3) if tot else None, ink_hit_shifted=round(ctrl / tot, 3) if tot else None,
                   in_band=round(float(np.mean([o['band'] is not None for o in out if o['name'] == n])), 3))
        pieces.append(rec)
        if len(pieces) % 25 == 0:
            print(len(pieces), 'pieces', round(time.time() - t0), 's', file=sys.stderr, flush=True)
    json.dump(out, open(f'{DR}/registered.json', 'w'), ensure_ascii=False)
    ok = [p for p in pieces if 'error' not in p]
    good = [p for p in ok if abs(p['scale'] - 1) < 0.05 and p['inliers'] >= 30]
    summ = dict(pieces_tried=len(pieces), registered=len(ok), scale_about_1=len(good),
                letters_mapped=sum(1 for o in out if o['letter']),
                scale_median=float(np.median([p['scale'] for p in ok])) if ok else None,
                ink_hit_median=float(np.median([p['ink_hit'] for p in good if p['ink_hit'] is not None])) if good else None,
                ink_hit_shifted_median=float(np.median([p['ink_hit_shifted'] for p in good if p['ink_hit_shifted'] is not None])) if good else None,
                in_band_median=float(np.median([p['in_band'] for p in good])) if good else None,
                failures=collections.Counter(p.get('error', 'ok')[:40] for p in pieces).most_common(5),
                pieces=pieces)
    json.dump(summ, open('reports/E2_registration.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k != 'pieces'}, indent=1))


if __name__ == '__main__':
    main()
