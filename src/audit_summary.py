"""Summarise the forward catalogue audit (data/audit/forward.json).

Two corrections to the verdicts of audit.py:
  * Long readings have few length-matched decoys, so the family-wise p of the
    fragment test cannot go below about 0.02 and strong cases fall through to
    'no_fit' / 'weak' / 'elsewhere'. When the full-corpus top hit lies in the
    image's own manuscript but in a fragment that is not linked, the image is
    re-labelled 'other_frag' (or 'split_record' when the fragment numbers
    overlap), with the full-corpus score as evidence.
  * 'elsewhere' hits are calibrated against decoys (m5_decoy.py, local line
    scores, full corpus): p = share of length-matched decoys (x1.5) scoring
    at least as high; E = p x images that reached the full-corpus search.

Usage: python3 src/audit_summary.py
Outputs: data/audit/forward_flags.json, reports/M9_audit_forward.md
"""
import json, os, sys, collections
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from audit import frag_numbers  # noqa: E402

DECOYS = 'data/m5/decoy_scores_v2_local.json'


def hit_frag(ref):
    """'4Q58 3:18' -> ('4Q58', '3')."""
    if not ref or ':' not in ref:
        return None, None
    sc, rest = ref.split(' ', 1)
    return sc, rest.split(':')[0]


def main():
    f = json.load(open('data/audit/forward.json'))
    dec = json.load(open(DECOYS))['unigram']['decoys']
    dl = np.array([d['read'] for d in dec])
    ds = np.array([d['score'] for d in dec])
    searched = [r for r in f if 'full_hits' in r]
    for r in f:
        r['verdict2'] = r['verdict']
        h = r.get('full_hits')
        if not h:
            continue
        score, doc, ref = h[0]
        own_sc = {l[0] for l in r['links']}
        sc, fr = hit_frag(ref)
        if doc.startswith('DSS ') and sc in own_sc:
            own = {l[1] for l in r['links'] if l[0] == sc}
            if fr not in own:
                on = set().union(*[frag_numbers(x) for x in own]) if own else set()
                r['verdict2'] = 'split_record' if frag_numbers(fr) & on else 'other_frag'
                r['evidence'] = f'full-corpus top hit {ref} ({score})'
            continue
        sel = np.abs(np.log(dl / r['read'])) <= np.log(1.5)
        nb = ds[sel]
        r['p_decoy'] = float((1 + (nb >= score).sum()) / (len(nb) + 1))
        r['n_decoy'] = int(sel.sum())
        r['E'] = r['p_decoy'] * len(searched)
        if r['verdict'] == 'elsewhere':
            r['verdict2'] = 'elsewhere' if r['E'] < 1 else 'weak_elsewhere'
    json.dump(f, open('data/audit/forward_flags.json', 'w'), ensure_ascii=False)

    c1 = collections.Counter(r['verdict'] for r in f)
    c2 = collections.Counter(r['verdict2'] for r in f)
    tested = [r for r in f if r['verdict'] != 'too_short']
    L = ['# Forward catalogue audit: flags', '',
         f'{len(f)} identified images read; {len(tested)} with >= 6 letters were tested. '
         f'{len(searched)} reached the full-corpus search. Decoys for the "elsewhere" test: '
         f'{len(dec)} readings (m5_decoy.py, local line scores).', '',
         '| Verdict | audit.py | after re-labelling |', '|---|---|---|']
    for v in ('ok', 'split_record', 'other_frag', 'elsewhere', 'weak_elsewhere', 'no_fit', 'weak', 'too_short'):
        L.append(f'| {v} | {c1.get(v, 0)} | {c2.get(v, 0)} |')
    L += ['', 'Crops stay local (IAA rights). Every row is a lead to check, not a finding.', '']

    def row(r):
        return (f"| {r['name']} | {r['manuscript']} | {r['category']} | "
                f"{', '.join(' '.join(l[:2]) for l in r['links'][:3])} | {r['read']} | "
                f"{r.get('evidence') or (r.get('best_frag', '') + ' z=' + str(r.get('z_best')) + ' p_fw=' + str(r.get('p_fw')))} | "
                f"{' / '.join(r['reading'][:3])} |")
    hdr = ['| Image | Manuscript | Category | Linked to | Letters read | Evidence | Reading (first lines) |',
           '|---|---|---|---|---|---|---|']
    oth = [r for r in f if r['verdict2'] == 'other_frag']
    oth.sort(key=lambda r: -(r['full_hits'][0][0] if r.get('full_hits') else r.get('z_best', 0)))
    L += ['## Another fragment of the same manuscript fits better', '',
          'Sorted by full-corpus score, then by z. Strong rows (a long reading that lands in an unlinked '
          'fragment of its own manuscript) point to a catalogue link to the wrong fragment or column, or '
          'to a photo that shows more than the linked fragment.', ''] + hdr + [row(r) for r in oth[:40]]
    sp = [r for r in f if r['verdict2'] == 'split_record']
    L += ['', '## Split or joined fragment records', '',
          'The best fragment shares a number with the link (e.g. f4i vs f4ii, or f6 vs f6+14): '
          'a column or join difference in the data, not a misidentified piece.', ''] + hdr + [row(r) for r in sp[:25]]
    el = sorted([r for r in f if r['verdict2'] in ('elsewhere', 'weak_elsewhere')], key=lambda r: r['E'])
    L += ['', '## Best fit in another composition', '',
          '| Image | Manuscript | Linked to | Letters read | Top hit | Score | Decoy p | E |', '|---|---|---|---|---|---|---|---|']
    for r in el[:25]:
        h = r['full_hits'][0]
        L.append(f"| {r['name']} | {r['manuscript']} | {', '.join(' '.join(l[:2]) for l in r['links'][:2])} | "
                 f"{r['read']} | {h[1]} {h[2]} | {h[0]} | {r['p_decoy']:.4f} | {r['E']:.2f} |")
    open('reports/M9_audit_forward.md', 'w').write('\n'.join(L) + '\n')
    rep = json.load(open('reports/M9_audit_forward.json'))
    rep['verdicts_relabelled'] = dict(c2)
    rep['elsewhere_E_below_1'] = sum(1 for r in el if r['E'] < 1)
    json.dump(rep, open('reports/M9_audit_forward.json', 'w'), indent=1)
    print(dict(c1)); print(dict(c2)); print('elsewhere E<1:', rep['elsewhere_E_below_1'])


if __name__ == '__main__':
    main()
