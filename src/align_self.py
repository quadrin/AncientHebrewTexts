"""M3b: more line labels, aligned with the recogniser's own reading.

Sources (train-split manuscripts only; test and validation stay untouched):
  * 'shared' and 'image_many' images (a text fragment over several pieces, or
    several text fragments on one piece): which transcription lines sit on
    which band is unknown
  * one-to-one images whose M3 width alignment rejected some lines
  * clean one-to-one papyrus images (M3 has not run on papyrus)
For each band, the recogniser's top-1 reading is searched as an approximate
substring of every candidate transcription line (visible letters only).
A band is labelled when
  - the reading has >= MIN_LEN letters,
  - edits / matched length <= MAX_ERR,
  - the best line beats the second best by >= MARGIN in error rate.
The label is the matched stretch of the editors' transcription, never the
model's reading. Output: data/m3/lines/{id}.png and data/m3/manifest_self.jsonl.

Usage: python3 src/align_self.py MODEL
"""
import json, os, sys, collections
import numpy as np, cv2

sys.path.insert(0, os.path.dirname(__file__))
from recognise import load_model, read_line  # noqa: E402
from align import visible, crop_line  # noqa: E402
from inventory import nms  # noqa: E402

MIN_LEN, MAX_ERR, MARGIN = 4, 0.35, 0.15
FIN = str.maketrans('ךםןףץ', 'כמנפצ')


def fold(s):
    return s.translate(FIN)


def semiglobal(a, b):
    """Best alignment of all of a (reading, letters only) to a substring of b.
    Returns (edits, start, end) in b."""
    n, m = len(a), len(b)
    prev = np.zeros(m + 1, int)                 # free start in b
    starts = np.arange(m + 1)
    for i in range(1, n + 1):
        cur = np.empty(m + 1, int)
        cst = np.empty(m + 1, int)
        cur[0], cst[0] = i, 0
        for j in range(1, m + 1):
            opts = ((prev[j - 1] + (a[i - 1] != b[j - 1]), starts[j - 1]),
                    (prev[j] + 1, starts[j]),
                    (cur[j - 1] + 1, cst[j - 1]))
            cur[j], cst[j] = min(opts)
        prev, starts = cur, cst
    j = int(np.argmin(prev))
    return int(prev[j]), int(starts[j]), j


def label_span(label, start, end):
    """Map a span over the label's letters (spaces removed) back to the label."""
    idx = [i for i, c in enumerate(label) if c != ' ']
    return label[idx[start]: idx[end - 1] + 1].strip() if end > start else ''


def main():
    model = load_model(sys.argv[1])
    split = json.load(open('reports/M4_split.json'))
    train_ms = set(split['train'])
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    et_lines = collections.defaultdict(list)
    for s, f, l, t, m in json.load(open('data/m0/etcbc_lines.json')):
        et_lines[(nms(s), f)].append(dict(line=l, text=t, marks=m))
    man = [json.loads(l) for l in open('data/m3/manifest.jsonl')]
    labelled = {(r['name'], r['band']) for r in man if r['tier']}

    names = []
    for f, cat in (('data/m2/batch_shared.json', 'shared'), ('data/m2/batch_parchment.json', 'misfit'),
                   ('data/m2/batch_papyrus.json', 'papyrus')):
        if os.path.exists(f):
            names += [(b['name'], cat) for b in json.load(open(f)) if not b.get('error')]
    out = open('data/m3/manifest_self.jsonl', 'w')
    stats = collections.Counter()
    letters = collections.Counter()
    for k, (name, cat) in enumerate(names):
        pr = pairs[name]
        if pr['manuscript'] not in train_ms or not os.path.exists(f'data/m2/seg/{name}.json'):
            continue
        cands = []
        for x in pr['links']:
            for l in et_lines[(nms(x['etcbc'][0]), x['etcbc'][1])]:
                v = visible(l)
                if v and v['letters'] >= MIN_LEN:
                    cands.append((f'{x["etcbc"][0]}|{x["etcbc"][1]}|{l["line"]}', v))
        if not cands:
            continue
        seg = json.load(open(f'data/m2/seg/{name}.json'))
        g = cv2.imread(f'data/m2/crop/{name}.png', 0)
        pitch = seg.get('pitch') or (float(np.median(np.diff([b['y'] for b in seg['lines']])))
                                     if len(seg['lines']) > 1 else None)
        if not pitch and seg['lines']:
            pitch = max(seg['lines'][0]['bottom'] - seg['lines'][0]['top'], 40)
        for i, b in enumerate(seg['lines']):
            if cat == 'misfit' and (name, i) in labelled:
                continue
            c = crop_line(g, b, pitch)
            if c.size == 0 or c.shape[1] < 8:
                continue
            rd = read_line(model, c)['text'].replace(' ', '')
            stats['bands'] += 1
            if len(rd) < MIN_LEN:
                continue
            scored = []
            for key, v in cands:
                lab = fold(v['label'].replace(' ', ''))
                e, s0, s1 = semiglobal(fold(rd), lab)
                scored.append((e / max(len(rd), 1), key, v, s0, s1))
            scored.sort(key=lambda t: t[0])
            err, key, v, s0, s1 = scored[0]
            second = scored[1][0] if len(scored) > 1 else 1.0
            if err > MAX_ERR or second - err < MARGIN:
                stats['rejected'] += 1
                continue
            lab = label_span(v['label'], s0, s1)
            n = sum(1 for ch in lab if ch != ' ')
            if n < MIN_LEN:
                continue
            lid = f'{name}_s{i}'
            cv2.imwrite(f'data/m3/lines/{lid}.png', c)
            out.write(json.dumps(dict(id=lid, name=name, manuscript=pr['manuscript'], period=pr['period'],
                                      band=i, line=key, label=lab, letters=n, uncertain=0,
                                      has_gap=v['has_gap'], width_misfit=0.0, tier='S', source=cat,
                                      read_err=round(err, 3), material=pr['material']),
                                 ensure_ascii=False) + '\n')
            stats[f'lines_{cat}'] += 1
            letters[cat] += n
        if k % 200 == 199:
            print(k + 1, dict(stats), file=sys.stderr, flush=True)
    out.close()
    res = dict(bands=dict(stats), letters=dict(letters))
    json.dump(res, open('reports/M8_selfalign_summary.json', 'w'), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == '__main__':
    main()
