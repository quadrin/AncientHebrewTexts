"""M7: read the unidentified fragments and build a review queue.

For every preprocessed target image (prep_batch.py target):
  1. read all bands with the recogniser (per-position top-k probabilities)
  2. skip fragments with fewer than MIN_READ letters read (M5: no signal there)
  3. match against MT + all scrolls (a transcribed unidentified set leaves its
     own scroll out), with N_SHUF shuffled-reading controls per fragment
  4. p-value: share of control scores (this run's and M5's, same read-letter
     band) at or above the fragment's best score; E-value = p x fragments searched

Outputs (local): data/m7/readings.json, data/m7/results.json,
data/m7/crops/{name}.jpg (for the reviewer; never committed).
Committed: reports/M7_queue.md (names, readings, passages, scores, E-values).

Usage: python3 src/m7_run.py MODEL [--gapped] [--limit N]
"""
import argparse, json, os, re, sys, random, time, collections
import numpy as np, cv2

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from recognise import load_model, read_image  # noqa: E402

D7 = 'data/m7'
MIN_READ = 10
N_SHUF = 20
BANDS = [(10, 19), (20, 39), (40, 79), (80, 10 ** 6)]


def band(n):
    return next((b for b in BANDS if b[0] <= n <= b[1]), None)


def nms(s):
    return re.sub(r'[\s.^]', '', s).replace('_', '-').upper()


def shuffled(reading, rnd):
    out = []
    for l in reading:
        l = list(l)
        rnd.shuffle(l)
        out.append(l)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('model')
    ap.add_argument('--gapped', action='store_true')
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--m5', default='', help='M5 results file whose controls join the null pool')
    a = ap.parse_args()
    os.makedirs(f'{D7}/crops', exist_ok=True)
    batch = [b for b in json.load(open('data/m2/batch_target.json')) if not b['error']]
    ink = {r[0]: r[3] for r in json.load(open('prior_work/ink_rank.json'))}
    # 4Q9999 in ink_rank order first, then the other sets
    batch.sort(key=lambda b: (b['manuscript'] != '4Q9999', -ink.get(b['name'], 0)))
    if a.limit:
        batch = batch[:a.limit]
    etcbc_scrolls = {nms(s) for s, *_ in json.load(open('data/ref/dss_lines.json'))}

    model = load_model(a.model)
    rpath = f'{D7}/readings.json'
    readings = json.load(open(rpath)) if os.path.exists(rpath) else {}
    t0 = time.time()
    for k, b in enumerate(batch):
        if b['name'] not in readings:
            readings[b['name']] = read_image(model, b['name'])
        if k % 200 == 199:
            json.dump(readings, open(rpath, 'w'), ensure_ascii=False)
            print(k + 1, 'read', round(time.time() - t0), 's', file=sys.stderr)
    json.dump(readings, open(rpath, 'w'), ensure_ascii=False)

    todo = []
    for b in batch:
        rd = [l['probs'] for l in readings[b['name']] if l['probs']]
        n = sum(len(l) for l in rd)
        if n >= MIN_READ:
            todo.append((b, rd, n))
    print(f'{len(batch)} read; {len(todo)} with >= {MIN_READ} letters to match', file=sys.stderr)

    rnd = random.Random(0)
    corpora = {}
    results = []
    for k, (b, rd, n) in enumerate(todo):
        ex = nms(b['manuscript'])
        ex = ex if ex in etcbc_scrolls else None
        if ex not in corpora:
            corpora.clear()
            corpora[ex] = pmatch.Corpus(exclude={ex} if ex else (), mode='ex')
        c = corpora[ex]
        hits = c.search(rd, gapped=a.gapped)
        null = [c.search(shuffled(rd, rnd), gapped=a.gapped)[0][0] for _ in range(N_SHUF)]
        results.append(dict(name=b['name'], manuscript=b['manuscript'], read_letters=n, read_lines=len(rd),
                            reading=[l['text'] for l in readings[b['name']]],
                            hits=[(round(s, 2), d, ref, o) for s, d, ref, o in hits],
                            null=[round(x, 2) for x in null]))
        if k % 20 == 19:
            print(k + 1, 'matched', round(time.time() - t0), 's', file=sys.stderr)
            json.dump(results, open(f'{D7}/results.json', 'w'), ensure_ascii=False)
    json.dump(results, open(f'{D7}/results.json', 'w'), ensure_ascii=False)

    # ---- p-values from pooled controls in the same read-letter band
    pool = collections.defaultdict(list)
    for r in results:
        pool[band(r['read_letters'])] += r['null']
    if a.m5 and os.path.exists(a.m5):
        for r in json.load(open(a.m5)):
            bd = band(r['read_letters'])
            if bd:
                pool[bd] += [x for x in r['ex']['null'] if x is not None]
    pool = {k: np.sort(np.array(v)) for k, v in pool.items()}
    for r in results:
        nb = pool[band(r['read_letters'])]
        s = r['hits'][0][0]
        r['p'] = float((np.sum(nb >= s) + 1) / (len(nb) + 1))
        r['E'] = r['p'] * len(results)
    results.sort(key=lambda r: r['p'])
    json.dump(results, open(f'{D7}/results.json', 'w'), ensure_ascii=False)

    # ---- crops for the reviewer (local only)
    for r in results[:60]:
        g = cv2.imread(f'data/m2/crop/{r["name"]}.png', 0)
        if g is not None:
            cv2.imwrite(f'{D7}/crops/{r["name"]}.jpg', g, [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(json.dumps(dict(read=len(batch), matched=len(results),
                          E_below_1=sum(r['E'] < 1 for r in results),
                          p_below_001=sum(r['p'] < 0.01 for r in results)), indent=1))


if __name__ == '__main__':
    main()
