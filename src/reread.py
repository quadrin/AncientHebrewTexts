"""Re-read a set of preprocessed images with another model (E4 step 0).

Usage: python3 src/reread.py MODEL OUT.json SET
  SET = m5test : the M5 held-out test images (keys of data/m5/readings_run2.json)
        m7target: the M7 target images (keys of data/m7/readings_run2.json)
        decoy_v4: identified images that can be v4 decoys (m5_decoy.py rules,
                  before the per-image run test)
"""
import json, os, sys, collections
sys.path.insert(0, os.path.dirname(__file__))
from recognise import load_model, read_image  # noqa: E402

model_path, out, which = sys.argv[1:4]
if which == 'm5test':
    names = list(json.load(open('data/m5/readings_run2.json')))
elif which == 'm7target':
    names = list(json.load(open('data/m7/readings_run2.json')))
else:
    from prior import load_meta, BOOKMAP
    ll, comp, etcbc = load_meta()
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    split = json.load(open('reports/M4_split.json'))
    held = set(split['test']) | set(split['val'])
    flagged = {r['name'] for r in json.load(open('data/audit/forward_flags.json'))
               if r['verdict2'] in ('other_frag', 'split_record', 'weak_elsewhere', 'no_fit')}
    mspar = json.load(open('data/m5/ms_parallel.json'))
    names = []
    for n in json.load(open('data/audit/readings.json')):
        ms = pairs[n]['manuscript']
        cm = comp.get(ms, comp.get(ms.split('-')[0], ms))
        if ms in held or cm in BOOKMAP or n in flagged:
            continue
        t = [mspar[x['etcbc'][0]] for x in pairs[n]['links'] if x['etcbc'][0] in mspar]
        if t and all(v['share'] <= 0.03 and v['longest'] <= 13 for v in t) and sum(v['shingles'] for v in t) >= 20:
            names.append(n)
res = json.load(open(out)) if os.path.exists(out) else {}
model = load_model(model_path)
for k, n in enumerate(names):
    if n not in res:
        res[n] = read_image(model, n)
    if k % 200 == 199:
        json.dump(res, open(out, 'w'), ensure_ascii=False)
json.dump(res, open(out, 'w'), ensure_ascii=False)
print(len(res), 'images read', file=sys.stderr)
