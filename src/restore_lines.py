"""Idea 3, first check: are editors' reconstructed line lengths consistent
within a column?

For every ETCBC line whose full extent is known (no unrestored lacuna '#',
at least one preserved and one reconstructed letter), the line length is the
count of letters plus word spaces (preserved + reconstructed). Within a
fragment/column with >= 5 such lines, each line gets a robust z-score against
the column median (MAD scaled). Lines with |z| >= 3.5 are listed as outliers:
a restored line much longer or shorter than its neighbours is either a
genuinely irregular line (vacat, indentation, a line ending a section) or a
doubtful restoration.

Output: data/restore/line_lengths.json and reports/M9_restore_lines.json
"""
import json, os, collections
import numpy as np

if __name__ == '__main__':
    os.makedirs('data/restore', exist_ok=True)
    lines = json.load(open('data/m0/etcbc_lines.json'))
    by_frag = collections.defaultdict(list)
    for s, f, l, t, m in lines:
        if '#' in m or 'p' in m:
            continue
        if not any(k in '.u' for k in m) or 'r' not in m:
            continue
        rec = sum(1 for k in m if k == 'r')
        by_frag[(s, f)].append(dict(scroll=s, frag=f, line=l, length=len(t), reconstructed=rec,
                                    share_rec=round(rec / max(1, sum(1 for k in m if k != ' ')), 2), text=t, marks=m))
    out, cols = [], 0
    for key, ls in by_frag.items():
        if len(ls) < 5:
            continue
        cols += 1
        L = np.array([x['length'] for x in ls], float)
        med = np.median(L)
        mad = np.median(np.abs(L - med)) * 1.4826 + 1.0
        for x in ls:
            x['z'] = round(float((x['length'] - med) / mad), 2)
            x['column_median'] = float(med)
            out.append(x)
    flagged = sorted([x for x in out if abs(x['z']) >= 3.5], key=lambda x: -abs(x['z']))
    json.dump(out, open('data/restore/line_lengths.json', 'w'), ensure_ascii=False)
    z = np.array([x['z'] for x in out])
    summ = dict(columns=cols, lines=len(out), flagged=len(flagged),
                share_abs_z_ge_2=round(float(np.mean(np.abs(z) >= 2)), 3),
                flagged_mostly_reconstructed=sum(1 for x in flagged if x['share_rec'] >= 0.7),
                top=[{k: x[k] for k in ('scroll', 'frag', 'line', 'length', 'column_median', 'z', 'share_rec', 'text')}
                     for x in flagged[:25]])
    json.dump(summ, open('reports/M9_restore_lines.json', 'w'), ensure_ascii=False, indent=1)
    print({k: v for k, v in summ.items() if k != 'top'})
    for x in flagged[:12]:
        print(x['scroll'], x['frag'], x['line'], 'len', x['length'], 'median', x['column_median'], 'z', x['z'], 'rec', x['share_rec'], '|', x['text'][:80])
