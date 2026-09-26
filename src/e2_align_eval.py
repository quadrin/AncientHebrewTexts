"""E2 step 2: measure the M2 line bands and the M3 aligners against the SQE gold
letters (sqe_rois.py, roi_register.py).

Gold letter: an SQE letter polygon mapped into the M2 crop, with its letter.
The SQE line field is NOT used: checked by eye (B-358099), the letters and
their positions are right, but SQE files letters of four physical lines under
one line name. Physical gold lines are therefore rebuilt from the boxes
(clustered by vertical centre; a new line starts when the gap exceeds half
the median box height).

Measures:
  segmentation  per physical gold line (>= 2 letters): share whose letters
                all fall in one M2 band; per band: share holding letters of
                more than one physical gold line
  line choice   per labelled band (M3 tiers A/B, width alignment; tier S,
                self-alignment) holding >= MIN_GOLD gold letters: the gold
                letters, right to left, are matched (approximate substring)
                against every ETCBC line of the band's fragment; the aligner is
                right when its label's line is the best match (ties count as
                right), and wrong when another line is strictly better
  label text    edit rate of the gold letters inside the chosen label
Output: reports/E2_align_eval.json
Usage: python3 src/e2_align_eval.py
"""
import json, os, re, sys, collections
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from align_self import semiglobal, fold  # noqa: E402

MIN_GOLD = 3


def norm_frag(name):
    """'frg. 1' -> 'f1', 'frgs. 1-2' -> 'f1_2', 'col. 6' -> '6' (fallback only)."""
    s = name.strip()
    m = re.match(r'frgs?\.\s*(.+)', s)
    if m:
        return 'f' + m.group(1).replace('-', '_').replace(' ', '')
    m = re.match(r'col\.\s*(.+)', s)
    if m:
        return m.group(1).replace(' ', '')
    return s


def main():
    reg = [r for r in json.load(open('data/sqe_rois/registered.json')) if r['letter'] and r['band'] is not None]
    rep = json.load(open('reports/E2_registration.json'))
    good = {p['name'] for p in rep['pieces'] if 'error' not in p and abs(p['scale'] - 1) < 0.05 and p['inliers'] >= 30}
    reg = [r for r in reg if r['name'] in good]
    # one record per (image, sign)
    seen, gold = set(), []
    for r in reg:
        if (r['name'], r['sign']) not in seen:
            seen.add((r['name'], r['sign']))
            gold.append(r)
    inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
    tfmap = collections.defaultdict(dict)
    for n, x in inv.items():
        for t in x.get('text_fragments') or []:
            if t.get('etcbc'):
                tfmap[n][t['tf_name']] = t['etcbc'][1]
    unmapped = 0
    for g in gold:
        f = tfmap[g['name']].get(g['text_fragment'])
        if f is None:
            unmapped += 1
            f = norm_frag(g['text_fragment'])
        g['frag'] = f
        g['key'] = (f, g['line'])
    split = json.load(open('reports/M4_split.json'))
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}

    def sp(n):
        ms = pairs[n]['manuscript']
        return 'test' if ms in split['test'] else 'val' if ms in split['val'] else 'train' if ms in split['train'] else 'outside'

    # ---- physical gold lines
    by_img = collections.defaultdict(list)
    for g in gold:
        by_img[g['name']].append(g)
    for n, gs in by_img.items():
        h = np.median([g['crop_bbox'][3] - g['crop_bbox'][1] for g in gs])
        gs.sort(key=lambda g: (g['crop_bbox'][1] + g['crop_bbox'][3]) / 2)
        k, prev = 0, None
        for g in gs:
            cy = (g['crop_bbox'][1] + g['crop_bbox'][3]) / 2
            if prev is not None and cy - prev > 0.5 * h:
                k += 1
            g['pline'] = k
            prev = cy
    by_line = collections.defaultdict(list)
    by_band = collections.defaultdict(list)
    for g in gold:
        by_line[(g['name'], g['pline'])].append(g)
        by_band[(g['name'], g['band'])].append(g)
    lines_multi = [v for v in by_line.values() if len(v) >= 2]
    one_band = sum(1 for v in lines_multi if len({g['band'] for g in v}) == 1)
    bands_multi = [v for v in by_band.values() if len(v) >= 2]
    merged = sum(1 for v in bands_multi if len({g['pline'] for g in v}) > 1)
    seg = dict(gold_lines=len(lines_multi), in_one_band=one_band,
               share_in_one_band=round(one_band / max(len(lines_multi), 1), 3),
               bands_with_gold=len(bands_multi), bands_with_two_or_more_lines=merged,
               share_merged=round(merged / max(len(bands_multi), 1), 3))

    # ---- ETCBC lines per fragment (preserved letters)
    et = collections.defaultdict(dict)
    for s_, f, l, t, m in json.load(open('data/m0/etcbc_lines.json')):
        v = ''.join(c for c, k in zip(t, m) if k in '.u' and 'א' <= c <= 'ת')
        if v:
            et[(s_, f)][l] = fold(v)

    man = []
    for f, kind in (('data/m3/manifest.jsonl', 'width'), ('data/m3/manifest_self.jsonl', 'self')):
        for l in open(f):
            r = json.loads(l)
            if not r.get('tier'):
                continue
            if kind == 'width':
                links = pairs[r['name']]['links']
                if len(links) != 1:
                    continue
                r['frag'] = tuple(links[0]['etcbc'][:2])
                r['lname'] = r['line']
            else:
                sc, fr, ln = r['line'].split('|')
                r['frag'], r['lname'] = (sc, fr), ln
            r['kind'] = kind
            man.append(r)
    out = dict(gold_letters=len(gold), gold_images=len(by_img), segmentation=seg, aligners={})
    misses = []
    for kind in ('width', 'self'):
        rows = collections.defaultdict(collections.Counter)
        errs = collections.defaultdict(list)
        for r in (x for x in man if x['kind'] == kind):
            gs = by_band.get((r['name'], r['band']), [])
            if len(gs) < MIN_GOLD or r['frag'] not in et:
                continue
            gs = sorted(gs, key=lambda g: -(g['crop_bbox'][0] + g['crop_bbox'][2]))     # right to left
            a = fold(''.join(g['char'] for g in gs))
            rates = {ln: semiglobal(a, b)[0] / len(a) for ln, b in et[r['frag']].items()}
            if r['lname'] not in rates:
                continue
            own = rates[r['lname']]
            best = min(rates.values())
            c = rows[sp(r['name'])]
            c['bands'] += 1
            if own <= best:
                c['right_line'] += 1
            else:
                c['other_line_better'] += 1
                misses.append(dict(kind=kind, name=r['name'], manuscript=r['manuscript'], band=r['band'], tier=r['tier'],
                                   label_line=r['lname'], best_line=min(rates, key=rates.get),
                                   rate_label=round(own, 2), rate_best=round(best, 2)))
            errs[sp(r['name'])].append(own)
        res = {}
        for s_, c in list(rows.items()) + [('all', sum(rows.values(), collections.Counter()))]:
            e = errs[s_] if s_ != 'all' else [x for v in errs.values() for x in v]
            res[s_] = dict(c, share_right_line=round(c['right_line'] / max(c['bands'], 1), 3),
                           median_gold_edit_rate_in_label=round(float(np.median(e)), 3) if e else None)
        out['aligners'][kind] = res
    out['misses'] = misses
    # sensitivity of the merged-band share to the line-clustering threshold
    sens = {}
    for thr in (0.5, 0.7, 0.9):
        merged = tot = 0
        for n, gs in by_img.items():
            h = np.median([g['crop_bbox'][3] - g['crop_bbox'][1] for g in gs])
            k, prev, pl = 0, None, {}
            for g in sorted(gs, key=lambda g: (g['crop_bbox'][1] + g['crop_bbox'][3]) / 2):
                cy = (g['crop_bbox'][1] + g['crop_bbox'][3]) / 2
                if prev is not None and cy - prev > thr * h:
                    k += 1
                pl[g['sign']] = k
                prev = cy
            bands = collections.defaultdict(set)
            cnt = collections.Counter(g['band'] for g in gs)
            for g in gs:
                bands[g['band']].add(pl[g['sign']])
            for b, v in bands.items():
                if cnt[b] >= 2:
                    tot += 1
                    merged += len(v) > 1
        sens[str(thr)] = f'{merged}/{tot}'
    out['segmentation']['merged_bands_by_gap_threshold'] = sens
    json.dump(out, open('reports/E2_align_eval.json', 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != 'misses'}, indent=1))
    print(len(misses), 'misses:', collections.Counter((m['kind'], m['name']) for m in misses))


if __name__ == '__main__':
    main()
