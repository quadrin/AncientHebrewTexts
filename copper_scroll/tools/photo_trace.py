"""Clear images and letter tracings for the atlas photograph of strip 13 (column VII).

The atlas shows Osama Shukir Muhammed Amin's photograph of original strip 13 in
the Jordan Museum (Wikimedia Commons, CC BY-SA 4.0, 2467 x 4016). No infrared
image of 3Q15 exists (the scroll is metal; the Leon Levy library lists 3Q15
with no images). This tool makes two clearer versions of the open photograph
and turns the hand tracing of VII 7-11 into the reader's data.

    python copper_scroll/tools/photo_trace.py enhance PHOTO
    python copper_scroll/tools/photo_trace.py trace PHOTO [--update]
    python copper_scroll/tools/photo_trace.py review PHOTO PLATEDIR OUTDIR

PHOTO     the Commons original, full resolution (any format OpenCV reads)
PLATEDIR  output of tools/plate_extract.py for column 7; `review` uses
          07_radio2_1.png, the second exposure of Puech 2006 vol. II,
          pl. CCCXLVI (radiograph of strip 13). Copyrighted plate material:
          keep it and OUTDIR outside git.

Needs numpy, opencv-python-headless and scipy.

enhance  writes atlas/public/scroll/strip13.webp (the photograph, full size),
         strip13-grooves.webp (groove map) and strip13-relief.webp (relief).
trace    reads the hand tracing, registration/photo_tracing_strip13.json. Each
         stroke names its letter and is 'seen' (the photograph shows the
         groove) or 'inferred' (the radiograph shows it, the photograph does
         not). Seen strokes are snapped onto the groove map: a shift of up to
         4 units, then each vertex moves up to 2.5 units. The groove response
         of every stroke is printed. --update writes the paths, dashed paths
         and hit boxes into atlas/app/atlas-photo-data.json.
review   writes one sheet per word to OUTDIR: the photograph, the photograph
         with the tracing, and the radiograph carried into the same frame.

Coordinates are in the reader's 1000 x 1628 system (1 unit = 2.467 px of the
original).
"""
import argparse, json, os, sys
import numpy as np, cv2

HERE = os.path.dirname(os.path.abspath(__file__))
ATLAS = os.path.join(HERE, '..', 'atlas')
TRACING = os.path.join(HERE, '..', 'registration', 'photo_tracing_strip13.json')
DATA = os.path.join(ATLAS, 'app', 'atlas-photo-data.json')
UNITS_W = 1000
WORK_W = 1600          # the groove-map kernel sizes are defined at this width


def read_photo(photo, flags=cv2.IMREAD_COLOR):
    img = cv2.imread(photo, flags)
    if img is None:
        sys.exit(f'cannot read {photo}')
    return img


def groove_response(grey):
    """Black-hat groove response, normalised to about 0-1 (strokes high)."""
    s = grey.shape[1] / WORK_W
    k = int(round(21 * s)) | 1
    b = cv2.GaussianBlur(grey, (0, 0), 2.0 * s)
    bh = cv2.morphologyEx(b, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))).astype(np.float32)
    return bh / np.percentile(bh, 99.6)


def enhance(photo):
    img = read_photo(photo)
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grooves = (255 * (1 - np.clip(groove_response(grey), 0, 1) ** 0.8)).astype(np.uint8)
    relief = cv2.createCLAHE(2.5, (10, 16)).apply(cv2.fastNlMeansDenoising(grey, None, 5, 7, 21))
    out = os.path.join(ATLAS, 'public', 'scroll')
    os.makedirs(out, exist_ok=True)
    for name, im, q in (('strip13.webp', img, 86), ('strip13-grooves.webp', grooves, 80), ('strip13-relief.webp', relief, 80)):
        path = os.path.join(out, name)
        cv2.imwrite(path, im, [cv2.IMWRITE_WEBP_QUALITY, q])
        print(os.path.normpath(path), im.shape[1], 'x', im.shape[0], os.path.getsize(path) // 1024, 'KB')


class Grooves:
    def __init__(self, photo):
        grey = read_photo(photo, cv2.IMREAD_GRAYSCALE)
        self.u = grey.shape[1] / UNITS_W
        self.g = cv2.GaussianBlur(np.clip(groove_response(grey), 0, 1.5), (0, 0), 2.0)

    def resp(self, p):
        from scipy import ndimage as ndi
        p = np.asarray(p, float)
        pts = [p[0]]
        for a, b in zip(p[:-1], p[1:]):
            n = max(1, int(np.ceil(np.hypot(*(b - a)) / 0.7)))
            pts += [a + (b - a) * t for t in np.linspace(0, 1, n + 1)[1:]]
        q = np.array(pts) * self.u
        return ndi.map_coordinates(self.g, [q[:, 1], q[:, 0]], order=1, mode='nearest')

    def score(self, p):
        return self.resp(p).mean()

    def snap(self, p, shift=4.0, vert=2.5):
        p = np.asarray(p, float)
        best = (self.score(p), p)
        for dx in np.arange(-shift, shift + .01, .5):
            for dy in np.arange(-shift, shift + .01, .5):
                q = p + (dx, dy)
                s = self.score(q) - 0.004 * np.hypot(dx, dy)
                if s > best[0]:
                    best = (s, q)
        p = best[1].copy()
        steps = np.arange(-vert, vert + .01, .5)
        for _ in range(3):
            for i in range(len(p)):
                if i in (0, len(p) - 1):          # end points move across the stroke only
                    b = p[1] if i == 0 else p[-2]
                    t = (b - p[i]) / (np.hypot(*(b - p[i])) + 1e-9)
                    moves = [np.array([-t[1], t[0]]) * k for k in steps]
                else:
                    moves = [np.array((dx, dy)) for dx in steps for dy in steps]
                cur, pick = self.score(p), None
                for m in moves:
                    q = p.copy(); q[i] = q[i] + m
                    s = self.score(q) - 0.004 * np.hypot(*m)
                    if s > cur:
                        cur, pick = s, m
                if pick is not None:
                    p[i] = p[i] + pick
        return p


def path(p):
    return 'M ' + ' L '.join(f'{x:.1f} {y:.1f}' for x, y in p)


def trim_boxes(boxes):
    """Split overlapping hit boxes at the middle of the overlap (the reader selects the first box hit)."""
    ids = list(boxes)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            ax, ay, aw, ah = boxes[a]; bx, by, bw, bh = boxes[b]
            ox = min(ax + aw, bx + bw) - max(ax, bx); oy = min(ay + ah, by + bh) - max(ay, by)
            if ox <= 0 or oy <= 0:
                continue
            if a.rsplit('-', 1)[0] == b.rsplit('-', 1)[0]:      # same line: a lies to the right
                cut = round(max(ax, bx) + ox / 2)
                boxes[a] = [cut, ay, ax + aw - cut, ah]; boxes[b] = [bx, by, cut - bx, bh]
            else:                                               # next line: a lies above
                cut = round(max(ay, by) + oy / 2)
                boxes[a] = [ax, ay, aw, cut - ay]; boxes[b] = [bx, cut, bw, by + bh - cut]


def traced(photo):
    """The hand tracing with seen strokes snapped onto the photograph's grooves."""
    src = json.load(open(TRACING, encoding='utf-8'))
    g = Grooves(photo)
    words = {}
    for wid, w in src['words'].items():
        strokes = []
        for st in w['strokes']:
            p = np.asarray(st['points'], float)
            if st['status'] == 'seen':
                p = g.snap(p)
            r = g.resp(p)
            strokes.append({**st, 'points': p, 'response': float(r.mean())})
        words[wid] = strokes
    return src, words


def trace(photo, update):
    src, words = traced(photo)
    boxes = {}
    for wid, strokes in words.items():
        print(wid, src['words'][wid]['hebrew'])
        for i, st in enumerate(strokes):
            flag = '  <- weak for a seen stroke' if st['status'] == 'seen' and st['response'] < 0.25 else ''
            print(f"   {i:2d} {st['letter']} {st['status']:8s} groove {st['response']:.2f}{flag}")
        pts = np.vstack([st['points'] for st in strokes])
        lo, hi = pts.min(0) - (12, 12), pts.max(0) + (12, 12)
        boxes[wid] = [round(lo[0]), round(lo[1]), round(hi[0] - lo[0]), round(hi[1] - lo[1])]
    trim_boxes(boxes)
    if not update:
        return
    data = json.load(open(DATA, encoding='utf-8'))
    for w in data['words']:
        strokes = words[w['id']]
        w['box'] = boxes[w['id']]
        w['paths'] = [path(st['points']) for st in strokes if st['status'] == 'seen']
        w['inferred'] = [path(st['points']) for st in strokes if st['status'] == 'inferred']
    with open(DATA, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print('updated', os.path.normpath(DATA))


def review(photo, platedir, outdir):
    src, words = traced(photo)
    img = read_photo(photo)
    u = img.shape[1] / UNITS_W
    rad = cv2.imread(os.path.join(platedir, '07_radio2_1.png'), cv2.IMREAD_GRAYSCALE)
    if rad is None:
        sys.exit('missing 07_radio2_1.png')
    rad = cv2.createCLAHE(2.0, (8, 8)).apply(rad)
    A = np.array(src['radiograph']['affine_to_units'], float)
    os.makedirs(outdir, exist_ok=True)
    S = 4                                                  # output px per unit
    for wid, strokes in words.items():
        pts = np.vstack([st['points'] for st in strokes])
        (x0, y0), (x1, y1) = pts.min(0) - 20, pts.max(0) + 20
        W, H = int((x1 - x0) * S), int((y1 - y0) * S)
        crop = img[int(y0 * u):int(y1 * u), int(x0 * u):int(x1 * u)]
        crop = cv2.resize(crop, (W, H), interpolation=cv2.INTER_CUBIC)
        drawn = crop.copy()
        for st in strokes:
            q = ((st['points'] - (x0, y0)) * S).astype(np.int32)
            col = (160, 228, 255) if st['status'] == 'seen' else (40, 170, 255)
            cv2.polylines(drawn, [q], False, (32, 40, 20), 7, cv2.LINE_AA)
            cv2.polylines(drawn, [q], False, col, 3, cv2.LINE_AA)
        M = A.copy(); M[:, 2] += src['words'][wid]['radiograph_shift']
        M = M * S; M[0, 2] -= x0 * S; M[1, 2] -= y0 * S
        r = cv2.cvtColor(cv2.warpAffine(rad, M, (W, H), flags=cv2.INTER_CUBIC, borderValue=255), cv2.COLOR_GRAY2BGR)
        sheet = np.vstack([np.hstack([crop, np.full((H, 8, 3), 255, np.uint8), drawn]),
                           np.full((8, 2 * W + 8, 3), 255, np.uint8),
                           np.hstack([r, np.full((H, W + 8, 3), 255, np.uint8)])])
        out = os.path.join(outdir, f'{wid}.png')
        cv2.imwrite(out, sheet)
        print(out)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    e = sub.add_parser('enhance'); e.add_argument('photo')
    t = sub.add_parser('trace'); t.add_argument('photo'); t.add_argument('--update', action='store_true')
    r = sub.add_parser('review'); r.add_argument('photo'); r.add_argument('platedir'); r.add_argument('outdir')
    a = ap.parse_args()
    if a.cmd == 'enhance':
        enhance(a.photo)
    elif a.cmd == 'trace':
        trace(a.photo, a.update)
    else:
        review(a.photo, a.platedir, a.outdir)
