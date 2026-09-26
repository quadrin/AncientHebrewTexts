"""E4 evaluation (steps 4, 5, 7, 8) and the new M7 queue, from data/e4/searches2.json.

Calibration (step 4): WindowNull with a fitted tail (e4.py): decoys of similar
length (x1.5) plus source-excluded nulls, islands per search, exponential
tail past the 90th percentile; p = 1 - exp(-E(T)).
Decoy manuscripts are split in three folds by manuscript:
  A  fits the null for p-values
  B  negatives for the rescoring model (with srcx fold B)
  C  held out: false-positive checks (with srcx fold C)

Step 5, rescoring: logistic model on [-log10 p, gap, I, L, log read], fitted
on ownx pieces whose top hit is their own book (positives) against fold-B
decoys and srcx (negatives). Its output is turned into a p-value with the
fold-C nulls of similar length (empirical); T alone gets the same treatment,
so the two can be compared at 0.05 and 0.01 on the M5 test pieces.

Step 7, lowest level: posterior of the top book
  P_book = 1 / (1 + exp(-gap) + odds0),  odds0 = p / (1 - p) x (1 - pi) / pi
(pi = PI, the prior that a piece has a source in the reference); the piece is
assigned its book when P_book >= TAU, its chapter when also
P_chap = 1 / (1 + sum over other chapters of exp(-(T1 - Ti)) + odds0) >= TAU.
Measured: assignment rate and precision on ownx (source present), false
assignment rate on fold-C nulls (no source), and on the M5 test pieces.

Step 8, entrapment: every search also scored the Mishnah + Tosefta
(blanked where they share text with the reference; r = entrapment / reference
letters). Combined search: T_comb = max(T, T_en) - ln(1 + r); a piece passes at
level a when its p(T_comb) <= a; N_E = passing pieces whose best hit is in
the entrapment corpus, N_T = the others. FDP upper bound
N_E (1 + 1/r) / (N_T + N_E) (Wen et al. 2025).

Queue: target images (M7 pool) with p (null fitted on all decoys + srcx),
Benjamini-Hochberg q over the targets, lowest-level label, entrapment check.

env SEARCHES (default data/e4/searches2.json) and SUFFIX (appended to report
names) evaluate the forward-sum variant; sets that are missing are skipped.

Usage: python3 src/e4_eval.py
Outputs: reports/E4_eval.json, reports/E4_queue.md, data/e4/queue.json
"""
import json, os, sys, random, collections
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from e4 import WindowNull  # noqa: E402
from prior import load_meta, BOOKMAP  # noqa: E402

BANDS = [(3, 5), (6, 9), (10, 19), (20, 39), (40, 10 ** 6)]
PI = 0.5
TAU = 0.95
LEVELS = (0.05, 0.01, 0.001)


def folds(recs, k=3, seed=1):
    ms = sorted({r['manuscript'] for r in recs})
    random.Random(seed).shuffle(ms)
    f = {m: i % k for i, m in enumerate(ms)}
    return [[r for r in recs if f[r['manuscript']] == i] for i in range(k)]


def feats(r, p):
    return [-np.log10(max(p, 1e-12)), min(r['gap'], 50.0), r['I'] / 10.0, r['L'], np.log(r['read'])]


def logistic(X, y, l2=1e-2, it=500):
    X = np.asarray(X, float)
    mu, sd = X.mean(0), X.std(0) + 1e-9
    Z = np.c_[(X - mu) / sd, np.ones(len(X))]
    w = np.zeros(Z.shape[1])
    y = np.asarray(y, float)
    for _ in range(it):                       # Newton steps
        pr = 1 / (1 + np.exp(-Z @ w))
        g = Z.T @ (pr - y) + l2 * w
        H = (Z * (pr * (1 - pr))[:, None]).T @ Z + l2 * np.eye(len(w))
        step = np.linalg.solve(H, g)
        w -= step
        if np.abs(step).max() < 1e-8:
            break
    return lambda x: float((np.c_[(np.atleast_2d(np.asarray(x, float)) - mu) / sd, np.ones((1, 1))] @ w)[0])


def emp_p(value, read, null_vals, null_read, manuscript=None, null_ms=None):
    sel = np.abs(np.log(null_read / read)) <= np.log(1.5)
    if manuscript is not None:
        sel &= null_ms != manuscript
    nb = null_vals[sel]
    return float((1 + (nb >= value).sum()) / (len(nb) + 1))


def posterior_book(r, p):
    odds0 = p / max(1 - p, 1e-12) * (1 - PI) / PI
    return 1.0 / (1.0 + np.exp(-min(r['gap'], 700)) + odds0)


def posterior_chapter(r, p):
    ch = r.get('top_chapters') or []
    if not ch:
        return 0.0, None
    odds0 = p / max(1 - p, 1e-12) * (1 - PI) / PI
    t1 = ch[0][1]
    rest = sum(np.exp(-(t1 - t)) for _, t in ch[1:])
    return 1.0 / (1.0 + rest + odds0), ch[0][0]


def scroll_books(min_words=5, min_share=0.2):
    """ETCBC scroll -> biblical books it copies (the word feature `book`; pieces
    that ETCBC could not place carry the scroll name as book and are ignored)."""
    path = 'data/e4/scroll_books.json'
    if os.path.exists(path):
        return {k: set(v) for k, v in json.load(open(path)).items()}
    from tf.fabric import Fabric
    api = Fabric(locations='data/dss/tf/2.0.1', silent='deep').load('otype scroll book', silent='deep')
    F, L = api.F, api.L
    out = {}
    for sc in F.otype.s('scroll'):
        name = F.scroll.v(sc)
        c = collections.Counter(F.book.v(w) for w in L.d(sc, 'word') if F.book.v(w) and F.book.v(w) != name)
        tot = sum(c.values())
        bks = {({'Is': 'Isa', 'Ex': 'Exod'}).get(b, b) for b, n in c.items() if n >= min_words and n / tot >= min_share}
        if bks:
            out[name] = bks
    json.dump({k: sorted(v) for k, v in out.items()}, open(path, 'w'))
    return out


def canonicalise(recs, sb):
    """Search-time groups filed a scroll copy under 'C:<scroll>' when its Leon
    Levy composition did not join (e.g. 4Q12a); map those to their books and
    recompute the gap from the stored per-group scores."""
    def canon(g):
        if g.startswith('C:') and g[2:] in sb:
            return {'B:' + b for b in sb[g[2:]]}
        return {g}
    for r in recs:
        r['groups'] = sorted(set().union(*[canon(g) for g in r['groups']]))
        best = collections.defaultdict(lambda: -1e9)
        for g, t in r.get('top_groups') or []:
            for c in canon(g):
                best[c] = max(best[c], t)
        r['top_groups'] = sorted(best.items(), key=lambda x: -x[1])
        other = [t for g, t in r['top_groups'] if g not in r['groups']]
        if other:
            r['gap'] = r['T'] - max(other)


def main():
    ll, comp, etcbc = load_meta()
    res = json.load(open(os.environ.get('SEARCHES', 'data/e4/searches2.json')))
    suf = os.environ.get('SUFFIX', '')
    recs = list(res.values())
    canonicalise(recs, scroll_books())
    by = collections.defaultdict(list)
    for r in recs:
        by[r['kind']].append(r)
    dec, srcx, ownx, tst, tgt = by['decoy'], by['srcx'], by['ownx'], by['test'], by['target']
    dA, dB, dC = folds(dec)
    sA, sB, sC = folds(srcx)
    null = WindowNull(dA + sA, True)
    pv = {id(r): null.p(r) for r in recs if r['kind'] != 'target'}
    own_books = lambda r: {'B:' + x for x in BOOKMAP.get(comp.get(r['manuscript'], ''), [])}
    is_bib = lambda r: bool(own_books(r))
    correct = lambda r: bool(set(r['groups']) & own_books(r))
    out = dict(pieces={k: len(v) for k, v in by.items()})

    # ---- step 4: held-out calibration and M5 counts
    chk = dC + sC
    out['heldout_fp'] = {str(a): round(float(np.mean([pv[id(r)] <= a for r in chk])), 4) for a in LEVELS}
    out['heldout_fp_decoys_only'] = {str(a): round(float(np.mean([pv[id(r)] <= a for r in dC])), 4) for a in LEVELS}
    rows = []
    for lo, hi in BANDS:
        b = [r for r in tst if lo <= r['read'] <= hi and is_bib(r)]
        row = dict(read=f'{lo}-{hi if hi < 10**6 else "+"}', biblical=len(b), top1_own_book=sum(map(correct, b)))
        for a in LEVELS:
            row[f'p<={a}_own'] = sum(1 for r in b if pv[id(r)] <= a and correct(r))
            row[f'p<={a}_all'] = sum(1 for r in b if pv[id(r)] <= a)
        rows.append(row)
    out['m5_rows'] = rows
    b10 = [r for r in tst if r['read'] >= 10 and is_bib(r)]
    out['m5_pooled_10plus'] = dict(n=len(b10), **{str(a): sum(1 for r in b10 if pv[id(r)] <= a and correct(r))
                                                   for a in LEVELS})

    # ---- step 5: rescoring (skipped when the ownx set is missing)
    pos = [r for r in ownx if correct(r)]
    nullC = dC + sC
    if pos:
        neg = dB + sB
        X = [feats(r, pv[id(r)]) for r in pos + neg]
        y = [1] * len(pos) + [0] * len(neg)
        f = logistic(X, y)
        nv_R = np.array([f(feats(r, pv[id(r)])) for r in nullC])
        nv_T = np.array([r['T'] for r in nullC])
        nread = np.array([r['read'] for r in nullC], float)
        nms_ = np.array([r['manuscript'] for r in nullC])
        resc = {}
        for name, val, nv in (('T_only', lambda r: r['T'], nv_T),
                              ('rescored', lambda r: f(feats(r, pv[id(r)])), nv_R)):
            resc[name] = {str(a): sum(1 for r in b10 if correct(r) and
                                      emp_p(val(r), r['read'], nv, nread, r['manuscript'], nms_) <= a)
                          for a in (0.05, 0.01)}
        out['rescoring'] = dict(positives=len(pos), negatives=len(neg), fold_C_nulls=len(nullC),
                                m5_pooled_10plus_empirical=resc,
                                note='empirical p on fold-C nulls (floor ~1/n per length window); '
                                     'compare the two rows, not with the tail p')

    # ---- step 7: lowest-level assignment
    def lca(r, p):
        pb = posterior_book(r, p)
        if pb < TAU:
            return 'none', pb, None
        pc, ch = posterior_chapter(r, p)
        if ch and pc >= TAU and any(ch.startswith(g[2:] + '.') for g in r['groups']):
            return 'chapter', pb, ch
        return 'book', pb, None
    lc = {}
    for name, S in (('ownx', ownx), ('nulls_C', nullC), ('test', tst)):
        c = collections.Counter()
        for r in S:
            lvl, pb, ch = lca(r, pv[id(r)])
            if lvl == 'none':
                c['none'] += 1
                continue
            ok = correct(r) if is_bib(r) else False
            c[f'{lvl}_{"right" if ok else "wrong"}'] += 1
        lc[name] = dict(c)
    t1019 = [r for r in tst if 10 <= r['read'] <= 19 and is_bib(r)]
    lc['test_10_19_book_or_better'] = sum(1 for r in t1019 if lca(r, pv[id(r)])[0] != 'none')
    lc['test_10_19_n'] = len(t1019)
    out['lca'] = dict(pi=PI, tau=TAU, **lc)

    # ---- step 8: entrapment
    r_ratio = 1900923 / 1845669
    ent = {}
    for name, S in (('test', tst), ('nulls_C', nullC), ('ownx', ownx)):
        e = {}
        for a in LEVELS:
            NT = NE = 0
            for r in S:
                tc = max(r['T'], r['T_en']) - np.log(1 + r_ratio)
                p = null.p(dict(r, T=tc))
                if p <= a:
                    if r['T_en'] > r['T']:
                        NE += 1
                    else:
                        NT += 1
            e[str(a)] = dict(N_T=NT, N_E=NE, FDP_upper=round(NE * (1 + 1 / r_ratio) / max(NT + NE, 1), 4))
        ent[name] = e
    out['entrapment'] = dict(r=round(r_ratio, 3), **ent)

    if not tgt:
        json.dump(out, open(f'reports/E4_eval{suf}.json', 'w'), ensure_ascii=False, indent=1)
        print(json.dumps(out, indent=1))
        return
    # ---- queue
    nullall = WindowNull(dec + srcx, True)
    q = []
    for r in tgt:
        p = nullall.p(r)
        q.append((p, r))
    q.sort(key=lambda x: x[0])
    m = len(q)
    qs, prev = [], 1.0
    for i in range(m - 1, -1, -1):
        prev = min(prev, q[i][0] * m / (i + 1))
        qs.append(prev)
    qs = qs[::-1]
    rd = json.load(open('data/m7/readings_run4.json'))
    batch = {b['name']: b for b in json.load(open('data/m2/batch_target.json'))}
    rows_q = []
    for (p, r), qq in zip(q, qs):
        lvl, pb, ch = lca(r, p)
        tc = max(r['T'], r['T_en']) - np.log(1 + r_ratio)
        rows_q.append(dict(name=r['name'], manuscript=batch.get(r['name'], {}).get('manuscript', r['manuscript']),
                           read=r['read'], lines=r['L'], T=round(r['T'], 2), p=p, q=qq, gap=round(r['gap'], 2),
                           hit=f"{r['doc']} {r['ref']}", level=lvl, P_book=round(pb, 3), chapter=ch,
                           entrap_wins=bool(r['T_en'] > r['T']), T_en=round(r['T_en'], 2), en_doc=r['en_doc'],
                           p_combined=nullall.p(dict(r, T=tc)),
                           reading=[l['text'] for l in rd.get(r['name'], []) if l['text']]))
    json.dump(rows_q, open('data/e4/queue.json', 'w'), ensure_ascii=False)
    lead = next((i + 1 for i, x in enumerate(rows_q) if x['name'] == 'B-359582'), None)
    out['queue'] = dict(targets=m, q_le_0_05=sum(1 for x in rows_q if x['q'] <= 0.05),
                        q_le_0_2=sum(1 for x in rows_q if x['q'] <= 0.2),
                        p_le_0_001=sum(1 for x in rows_q if x['p'] <= 0.001),
                        lead_B359582_rank=lead,
                        lead=next((x for x in rows_q if x['name'] == 'B-359582'), None))
    json.dump(out, open(f'reports/E4_eval{suf}.json', 'w'), ensure_ascii=False, indent=1)
    L = ['# E4 review queue (M7 targets, run-4 readings, E4 calibration)', '',
         f'{m} target images searched. Null: decoys (v4) + source-excluded nulls, length window x1.5, fitted tail. '
         'q = Benjamini-Hochberg over all targets. Level: lowest node with posterior >= 0.95 (book or chapter). '
         '"Entrapment wins" = the Mishnah/Tosefta decoy corpus scored higher than the reference: treat as chance.', '',
         'Every row is a lead for a specialist, not an identification. Crops stay local (IAA rights).', '',
         '| # | Image | Set | Letters | Lines | Best hit | T | p | q | Gap | Level | Entrapment wins | Reading |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, x in enumerate(rows_q[:40], 1):
        lvl = x['level'] + (f" ({x['chapter']})" if x['chapter'] else '')
        L.append(f"| {i} | {x['name']} | {x['manuscript']} | {x['read']} | {x['lines']} | {x['hit']} | {x['T']} | "
                 f"{x['p']:.2g} | {x['q']:.2g} | {x['gap']} | {lvl} | {'yes' if x['entrap_wins'] else ''} | "
                 f"{' / '.join(x['reading'][:3])} |")
    open('reports/E4_queue.md', 'w').write('\n'.join(L) + '\n')
    print(json.dumps({k: v for k, v in out.items() if k != 'queue'}, indent=1))
    print(json.dumps({k: v for k, v in out['queue'].items() if k != 'lead'}, indent=1), out['queue']['lead'])


if __name__ == '__main__':
    main()
