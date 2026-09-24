"""M5 analysis: identification and false-positive rates from data/m5/results.json.

A fragment is identifiable when its own transcription has a >= 10-letter
parallel outside its manuscript (m5_eval.truth). Its top hit is correct when it
lies in a truth document within TOL letters of a truth position.
Score thresholds come from the shuffled-reading controls: at threshold t the
false-positive rate is the share of controls whose best score is >= t.
Writes reports/M5_summary.json and prints tables.
"""
import json, sys, collections
import numpy as np

BINS = [(0, 9), (10, 19), (20, 39), (40, 10 ** 6)]


# synoptic passages: a hit in either copy is the same text
PARALLEL = [('Ps.18', '2Sam.22'), ('Isa.36', '2Kgs.18'), ('Isa.37', '2Kgs.19'), ('Isa.38', '2Kgs.20'),
            ('Ps.14', 'Ps.53'), ('Ps.105', '1Chr.16'), ('Ps.96', '1Chr.16'), ('Jer.52', '2Kgs.25')]


def same_place(a, b):
    """Two corpus references point at the same passage."""
    if a is None or b is None:
        return False
    if '.' in a and '.' in b and ' ' not in a and ' ' not in b:          # MT: Book.ch.v
        (ba, ca, va), (bb, cb, vb) = a.split('.')[:3], b.split('.')[:3]
        if f'{ba}.{ca}' != f'{bb}.{cb}':
            pair = {f'{ba}.{ca}', f'{bb}.{cb}'}
            return any(pair == set(p) for p in PARALLEL)
        return abs(int(va) - int(vb)) <= 3
    sa, fa = a.split(' ')[0], a.split(' ')[1].split(':')[0] if ' ' in a else ''
    sb, fb = b.split(' ')[0], b.split(' ')[1].split(':')[0] if ' ' in b else ''
    return sa == sb and fa == fb


def correct(r, mode):
    m = r[mode]
    if not m['hits']:
        return False
    ref = m['hits'][0][2]
    truths = [t[1] for md in ('ex', 'sk') for t in r[md]['truth']]
    return any(same_place(ref, t) for t in truths)


def main(path='data/m5/results.json', out='reports/M5_summary.json'):
    R = json.load(open(path))
    summ = {}
    for mode in ('ex', 'sk'):
        null = np.array([x for r in R for x in r[mode]['null'] if x is not None])
        ident = [r for r in R if r['ex']['truth'] or r['sk']['truth']]
        thr = {}
        for fp in (0.05, 0.01, 0.001):
            thr[fp] = float(np.quantile(null, 1 - fp)) if len(null) else None
        rows = []
        for lo, hi in BINS:
            rs = [r for r in R if lo <= r['preserved'] <= hi]
            idr = [r for r in rs if r['ex']['truth'] or r['sk']['truth']]
            row = dict(letters=f'{lo}-{hi if hi < 10**6 else "+"}', images=len(rs), identifiable=len(idr),
                       top1_correct=sum(correct(r, mode) for r in idr))
            for fp, t in thr.items():
                row[f'id@fp{fp}'] = sum(correct(r, mode) and r[mode]['hits'][0][0] >= t for r in idr)
                # real fragments with no parallel whose best score still clears the bar
                nid = [r for r in rs if r not in idr and r[mode]['hits']]
                row[f'noparallel_over@fp{fp}'] = sum(r[mode]['hits'][0][0] >= t for r in nid)
            rows.append(row)
        tot = {k: sum(r[k] for r in rows) for k in rows[0] if k != 'letters'}
        tot['letters'] = 'all'
        rows.append(tot)
        summ[mode] = dict(thresholds={str(k): round(v, 2) for k, v in thr.items()},
                          n_controls=int(len(null)), rows=rows)
        print(f'== mode {mode}: {len(null)} controls, thresholds',
              {k: round(v, 1) for k, v in thr.items()})
        cols = list(rows[0])
        print('\t'.join(cols))
        for r in rows:
            print('\t'.join(str(r[c]) for c in cols))
    # read quality on the test set
    summ['read'] = dict(images=len(R), read_letters=sum(r['read_letters'] for r in R),
                        transcription_letters=sum(r['preserved'] for r in R))
    json.dump(summ, open(out, 'w'), indent=1)


if __name__ == '__main__':
    main(*sys.argv[1:])
