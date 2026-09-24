"""M1 check: does the ink on each paired image agree with the transcription?

For every train pair in categories one_to_one / multi_column, fetch the 1200 px
rendition, measure parchment area and letter-sized ink blobs (method of
prior_work/ink.py), and compare with the preserved-letter count. Only the
numbers are stored: data/m1/ink_features.json.
"""
import json, io, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor
import numpy as np, cv2
from PIL import Image

D1 = 'data/m1'


def fetch(url, tries=4):
    for k in range(tries):
        try:
            r = urllib.request.Request(url.replace('http://', 'https://') + '=s1200',
                                       headers={'User-Agent': 'Mozilla/5.0'})
            return urllib.request.urlopen(r, timeout=60).read()
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(2 ** k)


def features(g, full_w):
    sc = full_w / g.shape[1]                      # full-res px per preview px
    # some images are underexposed; stretch so the brightest parchment is ~230
    hi = np.percentile(g, 99.9)
    if hi > 20:
        g = np.clip(g.astype(np.float32) * (230.0 / hi), 0, 255).astype(np.uint8)
    b = cv2.GaussianBlur(g, (0, 0), 1)
    fg = b > 40
    if fg.sum() < 200:
        return dict(parch=0, ink=0, blobs=0, rows=0, scale=sc)
    t = np.percentile(b[fg], 60)
    parch = (b > max(t * 0.8, 70)).astype(np.uint8)
    parch = cv2.morphologyEx(parch, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cnt, _ = cv2.findContours(parch, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    filled = np.zeros_like(parch)
    cv2.drawContours(filled, cnt, -1, 1, -1)
    ink = ((filled == 1) & (b < t * 0.55)).astype(np.uint8)
    n, _, st, _ = cv2.connectedComponentsWithStats(ink)
    area = st[1:, 4] * sc * sc if n > 1 else np.array([])
    # full-res letter strokes: roughly 150-10000 px^2 at ~1200 ppi
    blobs = int(((area >= 150) & (area <= 10000)).sum())
    return dict(parch=int(filled.sum() * sc * sc), ink=int(ink.sum() * sc * sc),
                blobs=blobs, scale=round(sc, 2))


def one(r):
    try:
        g = np.array(Image.open(io.BytesIO(fetch(r['url']))).convert('L'))
        return r['name'], features(g, r['w'])
    except Exception as e:
        return r['name'], dict(error=str(e))


if __name__ == '__main__':
    pairs = json.load(open(f'{D1}/pairs.json'))
    urls = {x['name']: x['url'] for x in json.load(open('data/m0/inventory_images.json'))}
    path = f'{D1}/ink_features.json'
    have = json.load(open(path)) if os.path.exists(path) else {}
    todo = [dict(name=r['name'], url=urls[r['name']], w=r['w']) for r in pairs
            if r['split'] == 'train' and r['category'] in ('one_to_one', 'multi_column')
            and r['name'] not in have]
    print(len(todo), 'to fetch', file=sys.stderr)
    with ThreadPoolExecutor(8) as ex:
        for k, (n, f) in enumerate(ex.map(one, todo)):
            have[n] = f
            if k % 500 == 499:
                json.dump(have, open(path, 'w'))
                print(k + 1, file=sys.stderr)
    json.dump(have, open(path, 'w'))
    print(len(have), 'images measured;', sum('error' in v for v in have.values()), 'errors')
