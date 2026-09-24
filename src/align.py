"""M3: weak line labels. Align segmented line bands (M2) to transcription lines (M1).

For each clean one-to-one parchment pair:
  * transcription lines -> visible label (preserved letters only, '.' and 'u'),
    trimmed to the preserved span; a line whose span holds reconstructed
    letters or a lacuna is marked has_gap (the image has a hole there)
  * image bands -> ink width, vertical position
  * monotonic DP alignment (top to bottom) with three moves: match, skip a band
    (spurious: crack, stain, letter tips), skip a transcription line (not visible:
    edge tips). Match cost = width misfit |log(width / expected width)| plus the
    vertical-spacing misfit against the line-number difference.

Tiers written to the manifest:
  A  line counts agree and every matched line fits (the brief's rule)
  B  aligned with skips; the matched line itself fits

Outputs (local only): data/m3/lines/{name}_{k}.png line crops and
data/m3/manifest.jsonl; summary to reports/M3_summary.json.
"""
import json, math, os, re, sys, collections
import numpy as np, cv2

D2, D3 = 'data/m2', 'data/m3'
FIN = str.maketrans('ךםןףץ', 'כמנפצ')


def lnum(label):
    m = re.match(r'(\d+)', label)
    return int(m.group(1)) if m else None


def visible(line):
    """Label from preserved letters; None when nothing is preserved."""
    t, m = line['text'], line['marks']
    idx = [i for i, c in enumerate(m) if c in '.u']
    if not idx:
        return None
    a, b = idx[0], idx[-1] + 1
    seg_t, seg_m = t[a:b], m[a:b]
    has_gap = any(c in 'r#p' for c in seg_m)
    label = ''.join(c for c, k in zip(seg_t, seg_m) if k in '.u ')
    label = re.sub(' +', ' ', label).strip()
    return dict(label=label, letters=sum(1 for c in label if c != ' '),
                uncertain=sum(1 for k in seg_m if k == 'u'), has_gap=has_gap,
                num=lnum(line['line']), line=line['line'])


def align(bands, tlines, pitch, cw, skip_band=1.0, skip_line=1.2, fit=0.5):
    """DP over bands (i) and transcription lines (j). Returns list of (i, j, cost)."""
    m, n = len(bands), len(tlines)
    INF = 1e9

    def mcost(i, j):
        exp_w = cw * pitch * max(len(tlines[j]['label']), 1)
        w = max(bands[i]['x1'] - bands[i]['x0'], 1)
        return abs(math.log(w / exp_w))

    def vcost(i, j, pi, pj):
        # spacing between consecutive matched bands vs line-number difference
        if pi is None or tlines[j]['num'] is None or tlines[pj]['num'] is None:
            return 0.0
        dn = tlines[j]['num'] - tlines[pj]['num']
        dy = (bands[i]['y'] - bands[pi]['y']) / pitch
        return 1.5 * abs(dy - dn)

    # state: (i bands used, j lines used, last matched (band, line)) -> keep best per (i, j)
    best = {(0, 0): (0.0, None, [])}
    for i in range(m + 1):
        for j in range(n + 1):
            if (i, j) not in best:
                continue
            c, last, path = best[(i, j)]
            cand = []
            if i < m and j < n:
                pi, pj = last if last else (None, None)
                cc = c + mcost(i, j) + vcost(i, j, pi, pj)
                cand.append(((i + 1, j + 1), (cc, (i, j), path + [(i, j, mcost(i, j))])))
            if i < m:
                weak = bands[i]['strength'] < 0.35
                cand.append(((i + 1, j), (c + (0.4 if weak else skip_band), last, path)))
            if j < n:
                short = tlines[j]['letters'] <= 2
                cand.append(((i, j + 1), (c + (0.3 if short else skip_line), last, path)))
            for k, v in cand:
                if k not in best or v[0] < best[k][0]:
                    best[k] = v
    return best[(m, n)][2], best[(m, n)][0]


def crop_line(g, band, pitch, pad_x=12):
    top = max(0, int(band['y'] - 0.75 * pitch))
    bot = min(g.shape[0], int(band['y'] + 0.45 * pitch))
    x0 = max(0, band['x0'] - pad_x)
    x1 = min(g.shape[1], band['x1'] + pad_x)
    return g[top:bot, x0:x1]


def main():
    os.makedirs(f'{D3}/lines', exist_ok=True)
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    batch = json.load(open(f'{D2}/batch_parchment.json'))
    segs = {}
    for b in batch:
        p = f'{D2}/seg/{b["name"]}.json'
        if os.path.exists(p):
            segs[b['name']] = json.load(open(p))

    # ---- calibrate character width per pitch on exact-count single-band lines
    ratios = []
    for name, s in segs.items():
        tl = [v for v in map(visible, list(pairs[name]['lines'].values())[0]) if v]
        if not s.get('pitch') or len(tl) != len(s['lines']) or not tl:
            continue
        for bnd, t in zip(s['lines'], tl):
            if t['letters'] >= 4 and not t['has_gap']:
                ratios.append((bnd['x1'] - bnd['x0']) / s['pitch'] / len(t['label']))
    cw = float(np.median(ratios))
    print('char width / pitch: median %.3f (IQR %.3f-%.3f, n=%d)' % (
        cw, np.percentile(ratios, 25), np.percentile(ratios, 75), len(ratios)), file=sys.stderr)

    man = open(f'{D3}/manifest.jsonl', 'w')
    stats = collections.Counter()
    letters = collections.Counter()
    for name, s in segs.items():
        pr = pairs[name]
        tl = [v for v in map(visible, list(pr['lines'].values())[0]) if v]
        stats['fragments'] += 1
        letters['fragments'] += sum(t['letters'] for t in tl)
        if not s['lines'] or not tl:
            stats['no_bands_or_text'] += 1
            continue
        pitch = s.get('pitch')
        if not pitch and len(s['lines']) > 1:
            pitch = float(np.median(np.diff([b['y'] for b in s['lines']])))
        if not pitch:
            # single band, no pitch: take the band height as pitch
            pitch = max(s['lines'][0]['bottom'] - s['lines'][0]['top'], 40)
        path, cost = align(s['lines'], tl, pitch, cw)
        counts_agree = len(s['lines']) == len(tl)
        g = cv2.imread(f'{D2}/crop/{name}.png', 0)
        for i, j, mc in path:
            t, b = tl[j], s['lines'][i]
            fits = mc < 0.5
            tier = 'A' if counts_agree and fits and all(p[2] < 0.5 for p in path) and len(path) == len(tl) else \
                   ('B' if fits else None)
            key = f'{name}_{i}'
            rec = dict(id=key, name=name, manuscript=pr['manuscript'], period=pr['period'],
                       band=i, line=t['line'], label=t['label'], letters=t['letters'],
                       uncertain=t['uncertain'], has_gap=t['has_gap'], width_misfit=round(mc, 3),
                       tier=tier, pitch=round(float(pitch), 1), ink_contrast=s.get('ink_contrast'))
            if tier:
                cv2.imwrite(f'{D3}/lines/{key}.png', crop_line(g, b, pitch))
                stats[f'lines_{tier}'] += 1
                letters[f'tier_{tier}'] += t['letters']
                if not t['has_gap']:
                    letters[f'tier_{tier}_nogap'] += t['letters']
            else:
                stats['lines_misfit'] += 1
            man.write(json.dumps(rec, ensure_ascii=False) + '\n')
        stats['fragments_counts_agree'] += counts_agree
    man.close()
    out = dict(char_width_per_pitch=round(cw, 3), fragments=dict(stats), letters=dict(letters))
    json.dump(out, open('reports/M3_summary.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
