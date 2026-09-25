"""M5 with decoy calibration, for two background models.

Shuffled readings are too weak a control (real readings consist of real words
and beat shuffled letters everywhere). Decoys here are real readings with no
true parallel: images of non-biblical compositions that survive in a single
manuscript, searched with their own manuscript left out. A held-out test piece
(own manuscript left out, as in M5) gets p = share of length-matched decoys
(read letters within x1.5) whose best score is at least its own.

Compares bg='unigram' (M5/M6 scorer) with bg='lm' (letter 4-gram background).
Measure: biblical test pieces whose top hit is in their own book, at decoy
p <= 0.01 and 0.05, by read letters; false-positive check on held-out decoys
(half of the decoys calibrate the other half).

Usage: python3 src/m5_decoy.py
Output: data/m5/decoy_scores.json, reports/M9_m5_decoy.json
"""
import json, os, re, sys, random, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from inventory import nms  # noqa: E402
from prior import BOOKMAP, load_meta  # noqa: E402

BANDS = [(3, 5), (6, 9), (10, 19), (20, 39), (40, 10 ** 6)]
N_DECOY_MS = 150


def main():
    ll, comp, etcbc = load_meta()
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    split = json.load(open('reports/M4_split.json'))
    held = set(split['test']) | set(split['val'])
    ncopies = collections.Counter(comp.values())
    audit_rd = json.load(open(os.environ.get('DECOYS', 'data/audit/readings.json')))
    # decoys: single-copy, non-biblical compositions, not held out
    by_ms = collections.defaultdict(list)
    for n, lines in audit_rd.items():
        ms = pairs[n]['manuscript']
        m = ll.get(ms, {})
        if ms in held or m.get('composition_type') in ('Scripture', 'Scripture?') or ncopies[comp.get(ms, ms)] != 1:
            continue
        rd = [l['probs'] for l in lines if l['probs']]
        k = sum(len(l) for l in rd)
        if k >= 3:
            by_ms[ms].append((n, rd, k))
    rnd = random.Random(0)
    dms = rnd.sample(sorted(by_ms), min(N_DECOY_MS, len(by_ms)))
    test_rd = json.load(open('data/m5/readings_run2.json'))
    tests = []
    for n, lines in test_rd.items():
        rd = [l['probs'] for l in lines if l['probs']]
        k = sum(len(l) for l in rd)
        if k >= 3:
            tests.append((n, pairs[n]['manuscript'], rd, k))
    path = 'data/m5/decoy_scores.json'
    res = json.load(open(path)) if os.path.exists(path) else {}
    base_lm = pmatch.Corpus(bg='lm').lm
    t0 = time.time()
    for bg in ('unigram', 'lm'):
        if bg in res:
            continue
        dec, tst = [], []
        todo = [(ms, [(n, rd, k) for n, rd, k in by_ms[ms][:4]], 'decoy') for ms in dms]
        by_t = collections.defaultdict(list)
        for n, ms, rd, k in tests:
            by_t[ms].append((n, rd, k))
        todo += [(ms, v, 'test') for ms, v in by_t.items()]
        for ms, items, kind in todo:
            c = pmatch.Corpus(exclude={nms(ms)}, bg=bg, lm=base_lm if bg == 'lm' else None)
            for n, rd, k in items:
                h = c.search(rd, top=1)
                rec = dict(name=n, manuscript=ms, read=k, score=h[0][0], ref=h[0][2], doc=h[0][1])
                (dec if kind == 'decoy' else tst).append(rec)
        res[bg] = dict(decoys=dec, tests=tst)
        json.dump(res, open(path, 'w'), ensure_ascii=False)
        print(bg, len(dec), 'decoys', len(tst), 'tests', round(time.time() - t0), 's', file=sys.stderr, flush=True)

    out = {}
    for bg in ('unigram', 'lm'):
        dec, tst = res[bg]['decoys'], res[bg]['tests']
        dl = np.array([d['read'] for d in dec]); ds = np.array([d['score'] for d in dec])

        def pval(score, k, mask=None):
            sel = np.abs(np.log(dl / k)) <= np.log(1.5)
            if mask is not None:
                sel &= mask
            nb = ds[sel]
            return float((1 + (nb >= score).sum()) / (len(nb) + 1)), int(sel.sum())
        rows = []
        for lo, hi in BANDS:
            b = [t for t in tst if lo <= t['read'] <= hi and comp.get(t['manuscript'], '') in BOOKMAP]
            r = dict(read=f'{lo}-{hi if hi < 10**6 else "+"}', biblical=len(b))
            for a in (0.01, 0.05):
                own = over = 0
                for t in b:
                    p, _ = pval(t['score'], t['read'])
                    ok = t['doc'].startswith('MT ') and t['ref'].split('.')[0] in BOOKMAP[comp[t['manuscript']]]
                    if p <= a:
                        over += 1
                        own += ok
                r[f'p<={a}'] = over
                r[f'p<={a}_own_book'] = own
            r['top1_own_book'] = sum(t['doc'].startswith('MT ') and t['ref'].split('.')[0] in BOOKMAP[comp[t['manuscript']]] for t in b)
            rows.append(r)
        # false positives: calibrate on half of the decoy manuscripts, test on the other half
        dms_list = sorted({d['manuscript'] for d in dec})
        half = set(dms_list[::2])
        mask_cal = np.array([d['manuscript'] in half for d in dec])
        fp = [pval(d['score'], d['read'], mask_cal)[0] for d in dec if d['manuscript'] not in half]
        out[bg] = dict(rows=rows, decoys=len(dec), fp_rate_at_0_01=round(float(np.mean(np.array(fp) <= 0.01)), 4),
                       fp_rate_at_0_05=round(float(np.mean(np.array(fp) <= 0.05)), 4), fp_n=len(fp))
        print(bg, json.dumps(out[bg], indent=1))
    json.dump(out, open('reports/M9_m5_decoy.json', 'w'), indent=1)


if __name__ == '__main__':
    main()
