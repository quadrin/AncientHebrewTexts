"""Idea 4 scoping: ink on the backs of fragments.

Leon Levy serves one infrared composite and one colour composite per photo;
the separate multispectral bands are not public, so this test runs on the
infrared image only. Every verso photo of a square-script manuscript (594)
goes through the M2 pipeline and the recogniser. Signals per photo:
  dark_ink - dark-ink pixels per parchment pixel (M2 filter)
  lines    - detected line bands
  conf     - letters the recogniser reads with top-1 probability >= 0.8
Ground truth: SQE links a verso photo to a text fragment when the back
carries text (the opisthographs). A signal that separates linked from
unlinked versos (AUC) can rank the unlinked ones; the top of that list is a
review queue for a specialist (crops stay local).

Usage: python3 src/verso_ink.py MODEL
Outputs: data/verso/readings.json, data/verso/rank.json, reports/M9_verso_ink.json
"""
import json, os, sys, collections
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from recognise import load_model, read_image  # noqa: E402

DV = 'data/verso'


def auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if not len(pos) or not len(neg):
        return None
    gt = (pos[:, None] > neg[None, :]).mean()
    eq = (pos[:, None] == neg[None, :]).mean()
    return round(float(gt + eq / 2), 3)


def main():
    os.makedirs(DV, exist_ok=True)
    inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    batch = [b for b in json.load(open('data/m2/batch_verso.json')) if not b.get('error')]
    model = load_model(sys.argv[1])
    rpath = f'{DV}/readings.json'
    readings = json.load(open(rpath)) if os.path.exists(rpath) else {}
    for b in batch:
        if b['name'] not in readings:
            readings[b['name']] = read_image(model, b['name'])
    json.dump(readings, open(rpath, 'w'), ensure_ascii=False)
    rows = []
    for b in batch:
        n = b['name']
        seg = json.load(open(f'data/m2/seg/{n}.json'))
        area = max(seg.get('mask', {}).get('area', 0), 1)
        probs = [d for l in readings[n] for d in l['probs']]
        conf = sum(1 for d in probs if max(d.values()) >= 0.8)
        rows.append(dict(name=n, manuscript=b['manuscript'], material=b['material'],
                         linked=bool(inv[n]['text_fragments']), area=area,
                         dark_ink=round(seg.get('dark_ink_px', 0) / area, 5), lines=len(seg.get('lines', [])),
                         read=len(probs), conf=conf,
                         reading=[l['text'] for l in readings[n] if l['text']]))
    out = dict(versos=len(rows), by_material={})
    for mat in ('Parchment', 'Papyrus'):
        r = [x for x in rows if x['material'] == mat]
        pos = [x for x in r if x['linked']]
        neg = [x for x in r if not x['linked']]
        out['by_material'][mat] = dict(
            linked=len(pos), unlinked=len(neg),
            auc={k: auc([x[k] for x in pos], [x[k] for x in neg]) for k in ('dark_ink', 'lines', 'read', 'conf')},
            median_conf_linked=float(np.median([x['conf'] for x in pos])) if pos else None,
            median_conf_unlinked=float(np.median([x['conf'] for x in neg])) if neg else None)
    # review queue: unlinked versos ranked by confident letters, then ink
    q = sorted([x for x in rows if not x['linked']], key=lambda x: (-x['conf'], -x['dark_ink']))
    # linked versos with nothing readable: SQE may link the piece, not the side
    silent = sorted([x for x in rows if x['linked']], key=lambda x: (x['conf'], x['dark_ink']))
    thr = np.percentile([x['conf'] for x in rows if x['linked']], 25) if any(x['linked'] for x in rows) else 0
    out['unlinked_with_conf_ge_linked_q1'] = sum(1 for x in q if x['conf'] >= max(thr, 1))
    out['linked_q1_conf'] = float(thr)
    out['queue'] = [{k: x[k] for k in ('name', 'manuscript', 'material', 'conf', 'read', 'lines', 'dark_ink', 'reading')}
                    for x in q[:20]]
    out['linked_silent'] = [{k: x[k] for k in ('name', 'manuscript', 'material', 'conf', 'read', 'dark_ink')}
                            for x in silent[:10]]
    json.dump(rows, open(f'{DV}/rank.json', 'w'), ensure_ascii=False)
    json.dump(out, open('reports/M9_verso_ink.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
