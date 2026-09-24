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

TOL = 300
BINS = [(0, 9), (10, 19), (20, 39), (40, 10 ** 6)]


def correct(m):
    if not m['hits'] or not m['truth']:
        return False
    s, d, ref, o = m['hits'][0]
    tdocs = {t[0] for t in m['truth']}
    return d in tdocs and any(abs(o - p) <= TOL for p in m['truth_pos'])


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
                       top1_correct=sum(correct(r[mode]) for r in idr))
            for fp, t in thr.items():
                row[f'id@fp{fp}'] = sum(correct(r[mode]) and r[mode]['hits'][0][0] >= t for r in idr)
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
