"""Idea 6 scoping: can the recogniser read the documentary collections
(Murabba'at, Nahal Hever, Se'elim, Masada)?

These manuscripts are in the Leon Levy library but not in ETCBC, so M1 left
them unlinked. SQE serves sign-level transcriptions for many of them
(CC BY-SA 4.0, Kratz/Kottsieper/Steudel on the basis of the Qumran-Woerterbuch
text). Pairing is by manuscript name only, so the test uses manuscripts whose
SQE text is short enough that every photo can be compared with all of it.

Measure, per detected line band with >= 4 letters read: edits of the best
approximate-substring match of the top-1 reading in the manuscript's preserved
letters, divided by the reading length (align_self.semiglobal). The same
measure on the held-out literary test images (M5, run-2 readings, against
their own ETCBC text) is the reference. A random-text control (the reading
matched against another documentary manuscript's text of similar length,
within x1.5) shows the rate
reached by chance.

Usage: python3 src/doc_test.py MODEL
Outputs: data/doc/, reports/M9_doc_test.json
"""
import json, os, sys, random, collections
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from sqe_harvest import get, per_edition  # noqa: E402
from inventory import nms  # noqa: E402
from align_self import semiglobal, fold  # noqa: E402

DD = 'data/doc'
PREFIX = ('MUR', '5/6HEV', 'XHEV', '8HEV', '34SE', 'MAS')
MAX_TEXT = 3000          # preserved letters per manuscript (keeps the search honest)
MIN_READ = 4


def edition_text(eid):
    """Preserved letters of every line of one SQE edition."""
    path = f'{DD}/sqe_{eid}.json'
    if os.path.exists(path):
        return json.load(open(path))
    lines = []
    for tf in get(f'/editions/{eid}/text-fragments')['textFragments']:
        for ln in get(f'/editions/{eid}/text-fragments/{tf["id"]}/lines')['lines']:
            d = get(f'/editions/{eid}/lines/{ln["lineId"]}')
            s = []
            for sg in d['signs']:
                si = sg['signInterpretations'][0]
                at = {(a['attributeString'], a['attributeValueString']) for a in si['attributes']}
                if ('sign_type', 'LETTER') not in at or not si['character']:
                    continue
                if any(k == 'is_reconstructed' and v == 'TRUE' for k, v in at):
                    continue
                s.append(si['character'])
            lines.append(dict(tf=tf['name'], line=ln['lineName'], text=''.join(s)))
    json.dump(lines, open(path, 'w'), ensure_ascii=False)
    return lines


def rate(reading, text):
    a, b = fold(reading), fold(text)
    if not a or not b:
        return None
    e, _, _ = semiglobal(a, b)
    return e / len(a)


def main():
    os.makedirs(DD, exist_ok=True)
    inv = json.load(open('data/m0/inventory_images.json'))
    eds = json.load(open('data/m0/sqe_editions.json'))
    by_nms = {nms(e['name']): e for e in eds}
    imgs = collections.defaultdict(list)
    for x in inv:
        if (x['manuscript'].upper().startswith(PREFIX) and x['ms_status'] == 'square'
                and x['side'] == 'Recto' and nms(x['manuscript']) in by_nms):
            imgs[x['manuscript']].append(x)
    todo = [by_nms[nms(m)] for m in imgs]
    texts = per_edition(todo, edition_text, workers=6)
    ms_text = {}
    for m in imgs:
        t = texts.get(by_nms[nms(m)]['id']) or []
        s = ''.join(l['text'] for l in t)
        if 0 < len(s) <= MAX_TEXT:
            ms_text[m] = s
    print(len(imgs), 'documentary manuscripts with an SQE edition;', len(ms_text),
          'with 1..%d preserved letters' % MAX_TEXT, file=sys.stderr, flush=True)

    # preprocess and read
    import prep
    from recognise import load_model, read_image
    model = load_model(sys.argv[1])
    rpath = f'{DD}/readings.json'
    readings = json.load(open(rpath)) if os.path.exists(rpath) else {}
    for m in ms_text:
        for x in imgs[m]:
            n = x['name']
            if n in readings:
                continue
            if not os.path.exists(f'data/m2/seg/{n}.json'):
                try:
                    prep.process(n, x['url'])
                except Exception as e:
                    readings[n] = dict(error=str(e))
                    continue
            try:
                readings[n] = read_image(model, n)
            except Exception as e:
                readings[n] = dict(error=str(e))
        json.dump(readings, open(rpath, 'w'), ensure_ascii=False)

    rnd = random.Random(0)
    others = sorted(ms_text)
    rows = []
    for m in ms_text:
        for x in imgs[m]:
            rd = readings.get(x['name'])
            if not isinstance(rd, list):
                continue
            for l in rd:
                t = l['text'].replace(' ', '')
                if len(t) < MIN_READ:
                    continue
                near = [o for o in others if o != m and abs(np.log(len(ms_text[o]) / len(ms_text[m]))) <= np.log(1.5)]
                ctrl = rnd.choice(near or [o for o in others if o != m] or [m])
                rows.append(dict(name=x['name'], manuscript=m, read=len(t), rate=rate(t, ms_text[m]),
                                 ctrl=rate(t, ms_text[ctrl]),
                                 material=x.get('material')))
    json.dump(rows, open(f'{DD}/rows.json', 'w'), ensure_ascii=False)

    # literary reference: M5 held-out test images against their own ETCBC text
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    et = collections.defaultdict(str)
    for s_, f, l, t, mk in json.load(open('data/m0/etcbc_lines.json')):
        et[(s_, f)] += ''.join(c for c, k in zip(t, mk) if k in '.u' and c != ' ')
    lit = []
    for n, rd in json.load(open('data/m5/readings_run2.json')).items():
        own = ''.join(et[tuple(x['etcbc'][:2])] for x in pairs[n]['links'])
        for l in rd:
            t = l['text'].replace(' ', '')
            if len(t) >= MIN_READ and own:
                lit.append(rate(t, own[:MAX_TEXT]))

    def summ(v):
        v = np.array([x for x in v if x is not None])
        return dict(lines=int(len(v)), median=round(float(np.median(v)), 3) if len(v) else None,
                    share_le_0_35=round(float((v <= 0.35).mean()), 3) if len(v) else None)
    mat = collections.defaultdict(list)
    for r in rows:
        mat[r['manuscript'][:3].upper()].append(r)
    out = dict(manuscripts_with_edition=len(imgs), manuscripts_tested=len(ms_text),
               images_read=sum(isinstance(v, list) for v in readings.values()),
               documentary=summ([r['rate'] for r in rows]),
               documentary_control=summ([r['ctrl'] for r in rows]),
               literary_test_set=summ(lit),
               by_collection={k: dict(own=summ([r['rate'] for r in v]), control=summ([r['ctrl'] for r in v]))
                              for k, v in mat.items()})
    json.dump(out, open('reports/M9_doc_test.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
