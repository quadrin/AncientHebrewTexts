"""Catalogue audit, reverse direction: which published fragments with no linked
image appear among the unidentified photographs?

Reference: only ETCBC fragments of the target cave that no image links to
(>= 5 preserved letters, not paleo-Hebrew), plus the PAM-plate collections for
Cave 4. Line spacing W = (1, 140) (see audit.py). About 105k letters for Cave
4, against 1.9M for the full corpus, so far fewer chance hits per search.
Controls: decoys = readings of identified images (their text is known and not
in this reference), grouped by read-letter band; p = share of decoys in the
band whose best score is at least the target's; E = p x targets searched.
Kinds: missing_link (the photo is filed under the same manuscript as the
matched transcription, which simply has no image link), no_image_scroll (the
matched manuscript has no linked image at all: the 4Q12a situation),
unlinked_fragment (another manuscript's fragment without an image link).

Usage: python3 src/audit_reverse.py [READINGS_JSON]   (default data/m7/readings_run2.json)
Outputs: data/audit/reverse.json, reports/M9_audit_reverse.json
"""
import json, os, re, sys, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from inventory import nms  # noqa: E402

DA = 'data/audit'
W = (1, 140)
MIN_READ = 4
BANDS = [(4, 5), (6, 7), (8, 9), (10, 14), (15, 19), (20, 10 ** 6)]


def band(n):
    return next((b for b in BANDS if b[0] <= n <= b[1]), None)


def cave(s):
    m = re.match(r'(\d+)Q', s)
    return m.group(1) + 'Q' if m else ('4Q' if s.upper().startswith('PAM') else None)


def main():
    rpath = sys.argv[1] if len(sys.argv) > 1 else 'data/m7/readings_run2.json'
    pairs = json.load(open('data/m1/pairs.json'))
    linked = {(x['etcbc'][0], x['etcbc'][1]) for r in pairs for x in r['links']}
    has_img = collections.Counter(s for s, f in linked)
    ef = json.load(open('data/m0/etcbc_fragments.json'))
    cand = {(f['scroll'], f['fragment']) for f in ef
            if (f['scroll'], f['fragment']) not in linked and f['preserved'] >= 5
            and f['paleo'] <= f['preserved'] / 2}
    batch = {b['name']: b for b in json.load(open('data/m2/batch_target.json'))}
    targets = json.load(open(rpath))
    decoys = json.load(open(os.environ.get('DECOYS', f'{DA}/readings.json')))
    full = pmatch.Corpus()
    out, summary = [], {}
    by_cave = collections.defaultdict(list)
    for n, lines in targets.items():
        ms = batch[n]['manuscript']
        cv = cave(ms)
        rd = [l['probs'] for l in lines if l['probs']]
        k = sum(len(l) for l in rd)
        if cv and k >= MIN_READ:
            by_cave[cv].append((n, ms, rd, k, [l['text'] for l in lines if l['text']]))
    t0 = time.time()
    for cv, items in by_cave.items():
        keep = {(s, f) for s, f in cand if cave(s) == cv}
        c = pmatch.Corpus(mt=False, keep=lambda s, f: (s, f) in keep, q=full.q)
        # decoy null: each decoy's best score and read length; a target is
        # compared with decoys of similar length (within x1.5)
        dl, dsc = [], []
        for d, lines in decoys.items():
            rd = [l['probs'] for l in lines if l['probs']]
            k = sum(len(l) for l in rd)
            if k >= MIN_READ:
                h = c.search(rd, W=W, top=1)
                if h:
                    dl.append(k)
                    dsc.append(h[0][0])
        dl, dsc = np.array(dl), np.array(dsc)
        print(cv, len(keep), 'fragments,', c.letters, 'letters;', len(items), 'targets;', len(dl), 'decoys',
              round(time.time() - t0), 's', file=sys.stderr, flush=True)
        for n, ms, rd, k, txt in items:
            h = c.search(rd, W=W, top=3)
            if not h:
                continue
            sel = np.abs(np.log(dl / k)) <= np.log(1.5)
            nb = dsc[sel]
            p = float((np.sum(nb >= h[0][0]) + 1) / (len(nb) + 1))
            scroll = h[0][1][4:]
            kind = ('missing_link' if nms(scroll) == nms(ms) else
                    'no_image_scroll' if has_img[scroll] == 0 else 'unlinked_fragment')
            out.append(dict(name=n, manuscript=ms, cave=cv, read=k, reading=txt, p=p, n_decoys=int(sel.sum()),
                            hits=[(round(a, 2), d, r) for a, d, r, _ in h], kind=kind,
                            scroll_has_no_image=has_img[scroll] == 0))
        summary[cv] = dict(fragments=len(keep), letters=c.letters, targets=len(items), decoys=int(len(dl)))
    for r in out:
        r['E'] = r['p'] * len(out)
    out.sort(key=lambda r: r['p'])
    json.dump(out, open(f'{DA}/reverse.json', 'w'), ensure_ascii=False)
    summary['E_below_1'] = sum(r['E'] < 1 for r in out)
    summary['top'] = [dict(name=r['name'], manuscript=r['manuscript'], read=r['read'], E=round(r['E'], 3),
                           kind=r['kind'], hit=r['hits'][0], reading=r['reading']) for r in out[:20]]
    json.dump(summary, open('reports/M9_audit_reverse.json', 'w'), ensure_ascii=False, indent=1)
    for r in out[:15]:
        print(r['name'], r['manuscript'], r['read'], 'p=%.4f E=%.2f' % (r['p'], r['E']), r['kind'], r['hits'][:2], r['reading'])


if __name__ == '__main__':
    main()
