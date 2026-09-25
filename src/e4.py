"""E4: matcher calibration v2 (research report, section 5).

Pieces searched (full Hebrew reference, local line scores, run-4 readings):
  test    M5 held-out test pieces, own manuscript masked
  decoy   v4 decoys (m5_decoy.py rules, whole-manuscript parallel test in
          ms_parallel.py): real readings of texts with no known parallel,
          own manuscript masked
  srcx    source-excluded nulls: identified biblical pieces from training
          manuscripts, searched with every witness of their book masked (the
          MT book and all scroll copies of it): 'lost text with
          near-neighbours'
One full corpus is built once; exclusion masks every line's score before
chaining (pmatch.score_array(mask=...)). Masking only the start offsets was
wrong: a many-line chain starting in the previous document reached the
piece's own text through its later lines (4Q184 -> '4Q183').

Per search:
  S     best fragment score (nats; each position is a likelihood ratio with
        mean 1 under background letters)
  I     reading information, sum over positions of KL(P_i || q)
  L     reading lines with letters
  ln N  ln(corpus letters) + (L - 1) ln(W1 - W0 + 1)   (offsets x spacings)
  T     S - ln N
  gap   S minus the best score in another text group (MT book, or the scroll
        copies of it, or one non-biblical composition)
  islands  the top ISLANDS local maxima >= 200 letters apart, as T values

Null model (BLAST style): per bin of I, the expected number of islands per
search with T >= t, E(t), is counted on the calibration half of the decoy
manuscripts and extended beyond the 90th percentile with a fitted exponential
tail; p = 1 - exp(-E(T)). The other half of the decoys checks the calibration
(share flagged at 0.05 / 0.01 / 0.001). The same model is fitted a second
time on decoys + srcx nulls.

Measure (as M5): biblical test pieces whose top hit is in their own book (MT
book or a scroll copy of it) with p <= 0.05 / 0.01, by read-letter band.

Usage: python3 src/e4.py
Outputs: data/e4/searches.json, reports/E4.json
"""
import json, os, re, sys, random, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from inventory import nms  # noqa: E402
from prior import load_meta, BOOKMAP  # noqa: E402

DE = 'data/e4'
W = (15, 140)
ISLANDS = 30
SEP = 200
N_SRCX = 400
BANDS = [(3, 5), (6, 9), (10, 19), (20, 39), (40, 10 ** 6)]
NBINS = 5


def rd_of(lines):
    return [l['probs'] for l in lines if l['probs']]


def info(rd, q):
    tot = 0.0
    for line in rd:
        for d in line:
            for ch, p in d.items():
                i = pmatch.IDX.get(pmatch._norm(ch))
                if i is not None and p > 0:
                    tot += p * np.log(p / q[i])
    return tot


def islands(acc, k=ISLANDS, sep=SEP):
    order = np.argsort(-acc)[:5000]
    out, seen = [], []
    for o in order:
        if acc[o] <= 0:
            break
        if any(abs(o - p) < sep for p in seen):
            continue
        seen.append(o)
        out.append(int(o))
        if len(out) == k:
            break
    return out


class Groups:
    """Text groups: 'B:Gen' for Genesis (MT and scroll copies), 'C:<composition>' otherwise."""

    def __init__(self, c, comp):
        self.names = sorted(set(c.docs))
        idx = {d: i for i, d in enumerate(self.names)}
        self.doc_id = np.fromiter((idx[d] for d in c.docs), np.int32, len(c.docs))
        norm = {nms(k): v for k, v in comp.items()}
        self.group = []
        for d in self.names:
            kind, name = d.split(' ', 1)
            if kind == 'MT':
                self.group.append({'B:' + name})
            else:
                cm = comp.get(name) or norm.get(nms(name)) or norm.get(nms(name.split('-')[0])) or name
                bks = BOOKMAP.get(cm)
                self.group.append({'B:' + b for b in bks} if bks else {'C:' + cm})

    def mask(self, pred):
        """Boolean mask of corpus positions whose document satisfies pred(doc_name, groups)."""
        bad = np.array([pred(n, g) for n, g in zip(self.names, self.group)])
        return bad[self.doc_id]


def search(c, G, rd, mask):
    acc = c.score_array(rd, W, mask=mask)
    if acc is None:
        return None
    b = int(np.argmax(acc))
    S = float(acc[b])
    gtop = G.group[G.doc_id[b]]
    other = ~np.array([bool(g & gtop) for g in G.group])[G.doc_id]
    other &= ~mask
    s2 = float(acc[other].max()) if other.any() else 0.0
    isl = islands(acc)
    L = len([l for l in rd if l])
    lnN = np.log(c.letters) + (L - 1) * np.log(W[1] - W[0] + 1)
    return dict(S=S, lnN=float(lnN), T=S - float(lnN), gap=S - s2, groups=sorted(gtop),
                doc=c.docs[b], ref=c.refs[b], L=L, islands=[float(acc[o]) - float(lnN) for o in isl])


class Null:
    def __init__(self, recs, bins):
        self.bins = bins
        self.tab = []
        for lo, hi in zip(bins[:-1], bins[1:]):
            r = [x for x in recs if lo <= x['I'] < hi]
            t = np.sort(np.concatenate([x['islands'] for x in r])) if r else np.array([0.0])
            u = np.percentile(t, 90)
            ex = t[t > u] - u
            lam = 1.0 / max(ex.mean(), 1e-3) if len(ex) else 1.0
            self.tab.append(dict(n=len(r), t=t, u=float(u), lam=float(lam), Eu=float((t > u).sum()) / max(len(r), 1)))

    def p(self, I, T):
        k = int(np.clip(np.searchsorted(self.bins, I, side='right') - 1, 0, len(self.tab) - 1))
        b = self.tab[k]
        if T <= b['u']:
            E = float((b['t'] >= T).sum()) / max(b['n'], 1)
        else:
            E = b['Eu'] * np.exp(-b['lam'] * (T - b['u']))
        return float(1 - np.exp(-E))


class WindowNull:
    """Decoys of similar length (read letters within x1.5), own manuscript left out.
    tail=False: p = share of those decoys whose best T is >= the piece's (M5 style).
    tail=True: expected islands per search above T, counted on those decoys and
    extended past their 90th percentile with a fitted exponential; p = 1 - exp(-E)."""

    def __init__(self, recs, tail):
        self.recs, self.tail = recs, tail
        self.read = np.array([r['read'] for r in recs], float)

    def p(self, r):
        sel = [x for x, k in zip(self.recs, np.abs(np.log(self.read / r['read'])) <= np.log(1.5))
               if k and x['manuscript'] != r['manuscript']]
        if len(sel) < 20:
            sel = sorted(self.recs, key=lambda x: abs(np.log(x['read'] / r['read'])))[:20]
        if not self.tail:
            best = np.array([x['T'] for x in sel])
            return float((1 + (best >= r['T']).sum()) / (len(best) + 1))
        t = np.concatenate([x['islands'] for x in sel])
        u = np.percentile(t, 90)
        if r['T'] <= u:
            E = float((t >= r['T']).sum()) / len(sel)
        else:
            ex = t[t > u] - u
            lam = 1.0 / max(ex.mean(), 1e-3)
            E = float((t > u).sum()) / len(sel) * np.exp(-lam * (r['T'] - u))
        return float(1 - np.exp(-E))


def main():
    os.makedirs(DE, exist_ok=True)
    ll, comp, etcbc = load_meta()
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    c = pmatch.Corpus(local=True)
    G = Groups(c, comp)
    print(c.letters, 'letters;', len(G.names), 'documents', file=sys.stderr, flush=True)
    path = f'{DE}/searches.json'
    res = json.load(open(path)) if os.path.exists(path) else {}

    def own_mask(ms, scrolls=()):
        keys = {nms(ms), nms(ms.split('-')[0])} | {nms(s) for s in scrolls}
        return G.mask(lambda n, g: n.startswith('DSS ') and nms(n[4:]) in keys)

    jobs = []
    for n, lines in json.load(open('data/m5/readings_run4.json')).items():
        jobs.append(('test', n, lines))
    split = json.load(open('reports/M4_split.json'))
    held = set(split['test']) | set(split['val'])
    for n, lines in json.load(open('data/audit/readings_run4_decoyv4.json')).items():
        jobs.append(('decoy', n, lines))
    # source-excluded nulls: identified biblical pieces from training manuscripts
    rnd = random.Random(0)
    audit_rd = json.load(open('data/audit/readings.json'))
    bib = [n for n in audit_rd if pairs[n]['manuscript'] not in held
           and comp.get(pairs[n]['manuscript'], '') in BOOKMAP
           and sum(len(l['probs']) for l in audit_rd[n] if l['probs']) >= 3]
    for n in rnd.sample(bib, min(N_SRCX, len(bib))):
        jobs.append(('srcx', n, audit_rd[n]))
    t0 = time.time()
    for k, (kind, n, lines) in enumerate(jobs):
        key = f'{kind}|{n}'
        if key in res:
            continue
        rd = rd_of(lines)
        nread = sum(len(l) for l in rd)
        if nread < 3:
            continue
        ms = pairs[n]['manuscript']
        scrolls = {x['etcbc'][0] for x in pairs[n]['links']}
        m = own_mask(ms, scrolls)
        if kind == 'srcx':
            books = {'B:' + b for b in BOOKMAP[comp[ms]]}
            m |= G.mask(lambda nm, g: bool(g & books))
        r = search(c, G, rd, m)
        if r is None:
            continue
        r.update(kind=kind, name=n, manuscript=ms, read=nread, I=info(rd, c.q))
        res[key] = r
        if k % 100 == 99:
            json.dump(res, open(path, 'w'))
            print(k + 1, '/', len(jobs), round(time.time() - t0), 's', file=sys.stderr, flush=True)
    json.dump(res, open(path, 'w'))

    recs = list(res.values())
    dec = [r for r in recs if r['kind'] == 'decoy']
    srcx = [r for r in recs if r['kind'] == 'srcx']
    tst = [r for r in recs if r['kind'] == 'test']
    dms = sorted({r['manuscript'] for r in dec})
    rnd = random.Random(1)
    rnd.shuffle(dms)
    half = set(dms[: len(dms) // 2])
    cal = [r for r in dec if r['manuscript'] in half]
    chk = [r for r in dec if r['manuscript'] not in half]
    bins = list(np.quantile([r['I'] for r in dec], np.linspace(0, 1, NBINS + 1)))
    bins[0], bins[-1] = -1e9, 1e9
    out = dict(pieces=dict(test=len(tst), decoy=len(dec), srcx=len(srcx)), models={})
    models = [('bins_I|decoy_half', lambda f: Null(f, bins), cal),
              ('bins_I|decoy_half+srcx', lambda f: Null(f, bins), cal + srcx),
              ('window_max|decoy_half', lambda f: WindowNull(f, False), cal),
              ('window_tail|decoy_half', lambda f: WindowNull(f, True), cal),
              ('window_tail|decoy_half+srcx', lambda f: WindowNull(f, True), cal + srcx)]
    for name, make, fit in models:
        null = make(fit)
        pv = (lambda r: null.p(r['I'], r['T'])) if isinstance(null, Null) else null.p
        pc = np.array([pv(r) for r in chk])
        ps = np.array([pv(r) for r in srcx]) if 'srcx' not in name else None
        rows = []
        own_books = lambda r: {'B:' + x for x in BOOKMAP[comp[r['manuscript']]]}
        for lo, hi in BANDS:
            b = [r for r in tst if lo <= r['read'] <= hi and comp.get(r['manuscript'], '') in BOOKMAP]
            row = dict(read=f'{lo}-{hi if hi < 10**6 else "+"}', biblical=len(b),
                       top1_own_book=sum(bool(set(r['groups']) & own_books(r)) for r in b))
            for a in (0.05, 0.01, 0.001):
                sel = [r for r in b if pv(r) <= a]
                row[f'p<={a}'] = len(sel)
                row[f'p<={a}_own_book'] = sum(bool(set(r['groups']) & own_books(r)) for r in sel)
            rows.append(row)
        b10 = [r for r in tst if r['read'] >= 10 and comp.get(r['manuscript'], '') in BOOKMAP]
        pooled = {str(a): sum(1 for r in b10 if pv(r) <= a and set(r['groups']) & own_books(r)) for a in (0.05, 0.01, 0.001)}
        out['models'][name] = dict(
            rows=rows, pooled_10plus_own_book=pooled, pooled_10plus_n=len(b10),
            heldout_decoys=len(chk),
            heldout_decoy_rate={str(a): round(float((pc <= a).mean()), 4) for a in (0.05, 0.01, 0.001)},
            srcx_rate=({str(a): round(float((ps <= a).mean()), 4) for a in (0.05, 0.01, 0.001)}
                       if ps is not None else None))
        print(name, pooled, out['models'][name]['heldout_decoy_rate'], out['models'][name]['srcx_rate'], flush=True)
    json.dump(out, open('reports/E4.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
