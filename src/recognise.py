"""M4 inference: read the line bands of a preprocessed image with per-position
letter probabilities.

read_image(model, name) uses data/m2/crop/{name}.png and data/m2/seg/{name}.json
(run prep.process first) and returns, per band top to bottom:
  dict(band=i, text=best string (reading order), probs=[{letter: p, ...}, ...])
Positions come from the CTC best path: each emitted symbol's distribution is the
mean softmax over its frames with the blank removed and renormalised. Spaces
are dropped from probs (the matcher works on letters).
"""
import json, os, sys
import numpy as np, cv2, torch, torch.nn.functional as F

sys.path.insert(0, os.path.dirname(__file__))
from train import CRNN, ALPHABET, H, MAXW  # noqa: E402
from align import crop_line  # noqa: E402

D2 = 'data/m2'


def load_model(path):
    """Weights plus the line height the run was trained at (run.json, default 64)."""
    h = H
    rj = os.path.join(os.path.dirname(path), 'run.json')
    if os.path.exists(rj):
        h = json.load(open(rj))['args'].get('height', H)
    m = CRNN(height=h)
    m.load_state_dict(torch.load(path, map_location='cpu'))
    m.eval()
    m.height = h
    return m


def prep_line(g, H=H):
    inside = g > 0
    fill = np.median(g[inside]) if inside.any() else 200
    g = np.where(inside, g, fill).astype(np.uint8)
    s = H / g.shape[0]
    w = int(min(MAXW, max(8, round(g.shape[1] * s))))
    g = cv2.resize(g, (w, H), interpolation=cv2.INTER_AREA)
    w4 = int(np.ceil(w / 4) * 4)
    x = np.zeros((H, w4), np.float32)
    x[:, :w] = (255.0 - g) / 255.0
    return torch.from_numpy(x)[None, None]


def positions(probs, topk=5, min_p=0.01):
    """CTC best path -> list of (symbol, distribution) in network order (left to right)."""
    best = probs.argmax(1)
    segs, cur, prev = [], None, 0
    for t, k in enumerate(best):
        if k == 0:
            prev = 0
            continue
        if k != prev:
            cur = [int(k), [t]]
            segs.append(cur)
        else:
            cur[1].append(t)
        prev = k
    out = []
    for k, ts in segs:
        p = probs[ts, 1:].mean(0)
        p = p / p.sum()
        top = np.argsort(-p)[:topk]
        out.append((ALPHABET[k - 1], {ALPHABET[j]: round(float(p[j]), 4) for j in top if p[j] >= min_p}))
    return out


def read_line(model, g, topk=5):
    with torch.no_grad():
        lg = model(prep_line(g, getattr(model, 'height', H)))[0]
    probs = F.softmax(lg, -1).numpy()
    pos = positions(probs, topk)[::-1]           # to reading order (right to left)
    text = ''.join(s for s, _ in pos)
    letters = [d for s, d in pos if s != ' ']
    return dict(text=text, probs=letters)


def read_image(model, name, topk=5):
    seg = json.load(open(f'{D2}/seg/{name}.json'))
    g = cv2.imread(f'{D2}/crop/{name}.png', 0)
    pitch = seg.get('pitch')
    if not pitch and len(seg['lines']) > 1:
        pitch = float(np.median(np.diff([b['y'] for b in seg['lines']])))
    if not pitch and seg['lines']:
        pitch = max(seg['lines'][0]['bottom'] - seg['lines'][0]['top'], 40)
    out = []
    for i, b in enumerate(seg['lines']):
        c = crop_line(g, b, pitch)
        if c.size == 0 or c.shape[1] < 8:
            continue
        r = read_line(model, c, topk)
        r.update(band=i, y=b['y'], strength=b['strength'])
        out.append(r)
    return out
