"""M5: does recogniser -> matcher identify fragments of held-out manuscripts?

For every clean one-to-one parchment image of a test manuscript (reports/M4_split.json):
  1. ground truth: search the fragment's own transcription (preserved letters,
     longest line first) in the reference with the fragment's manuscript left
     out. A fragment is identifiable when a preserved run of >= 10 letters
     (>= 10 after dropping ו/י in skeleton mode) occurs exactly somewhere
     else; the place is the truth. Shorter runs hit by chance too often
     (brief: 9 letters, 5% exact / 30% skeleton).
  2. read the image with the recogniser (all detected bands; no transcription used)
  3. search the reading with the probabilistic matcher (same exclusion)
  4. controls: the same reading with positions shuffled within each line,
     N_SHUF times -> null distribution of best scores

Output: data/m5/results.json (local) and reports/M5_summary.json.
"""
import json, os, re, sys, collections, random, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from recognise import load_model, read_image  # noqa: E402

N_SHUF = 10
D5 = 'data/m5'
FIN = str.maketrans('ךםןףץ', 'כמנפצ')


def nms(s):
    return re.sub(r'[\s.^]', '', s).replace('_', '-').upper()


def truth(corpus, lines, min_len=10):
    """Exact (skeleton-aware) search of the transcription's preserved runs."""
    runs = []
    for l in lines:
        cur = ''
        for c, k in zip(l['text'], l['marks']):
            if k in '.u' and 'א' <= c <= 'ת':
                cur += c.translate(FIN)
            elif k != ' ':
                if len(cur) >= min_len:
                    runs.append(cur)
                cur = ''
        if len(cur) >= min_len:
            runs.append(cur)
    runs.sort(key=len, reverse=True)
    rev = {i: c for c, i in pmatch.IDX.items()}
    if not hasattr(corpus, '_text'):
        corpus._text = ''.join(rev.get(int(i), '|') for i in corpus.ids)
    for r in runs:
        if corpus.mode == 'sk':
            r = r.replace('ו', '').replace('י', '')
            if len(r) < min_len:
                continue
        hits = [m.start() for m in re.finditer('(?=' + re.escape(r) + ')', corpus._text)]
        if hits:
            return r, [(corpus.docs[h], corpus.refs[h], h) for h in hits[:20]]
    return None, []


def shuffled(reading, rnd):
    out = []
    for l in reading:
        l = list(l)
        rnd.shuffle(l)
        out.append(l)
    return out


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('model', nargs='?', default='data/m4/run1/best.pt')
    ap.add_argument('--gapped', action='store_true')
    ap.add_argument('--out', default=f'{D5}/results.json')
    a = ap.parse_args()
    model_path = a.model
    os.makedirs(D5, exist_ok=True)
    cache_path = f'{D5}/readings_{os.path.basename(os.path.dirname(model_path))}.json'
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    split = json.load(open('reports/M4_split.json'))
    test = set(split['test'])
    pairs = [r for r in json.load(open('data/m1/pairs.json'))
             if r['manuscript'] in test and r['category'] == 'one_to_one' and r['side'] == 'Recto'
             and r['material'] == 'Parchment' and 'ink' in r and not r['ink'].get('flag')
             and os.path.exists(f'data/m2/seg/{r["name"]}.json')]
    print(len(pairs), 'test images from', len({r['manuscript'] for r in pairs}), 'manuscripts', file=sys.stderr)
    model = load_model(model_path)
    rnd = random.Random(0)
    corpora = {}
    results = []
    t0 = time.time()
    for k, r in enumerate(sorted(pairs, key=lambda r: r['manuscript'])):
        ex = nms(r['manuscript'])
        if ex not in corpora:
            corpora.clear()     # one manuscript at a time keeps memory low
            corpora[ex] = {m: pmatch.Corpus(exclude={ex}, mode=m) for m in ('ex', 'sk')}
        cs = corpora[ex]
        tlines = list(r['lines'].values())[0]
        if r['name'] not in cache:
            cache[r['name']] = read_image(model, r['name'])
        reading = cache[r['name']]
        rd = [l['probs'] for l in reading if l['probs']]
        rec = dict(name=r['name'], manuscript=r['manuscript'], preserved=r['preserved'],
                   read_letters=sum(len(l) for l in rd), read_lines=len(rd),
                   reading=[l['text'] for l in reading])
        for mode, c in cs.items():
            run, where = truth(c, tlines)
            hits = c.search(rd, gapped=a.gapped) if rd else None
            null = []
            for _ in range(N_SHUF):
                h = c.search(shuffled(rd, rnd), gapped=a.gapped) if rd else None
                null.append(h[0][0] if h else None)
            rec[mode] = dict(truth_run=run, truth=[(d, ref) for d, ref, _ in where],
                             truth_pos=[p for _, _, p in where],
                             hits=[(round(s, 2), d, ref, o) for s, d, ref, o in (hits or [])],
                             null=[round(x, 2) if x is not None else None for x in null])
        results.append(rec)
        if k % 10 == 9:
            print(k + 1, 'done', round(time.time() - t0), 's', file=sys.stderr)
            json.dump(results, open(a.out, 'w'), ensure_ascii=False)
    json.dump(results, open(a.out, 'w'), ensure_ascii=False)
    json.dump(cache, open(cache_path, 'w'), ensure_ascii=False)


if __name__ == '__main__':
    main()
