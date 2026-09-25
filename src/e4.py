"""E4 search pass: matcher calibration v2 (research report, section 5).

Pieces searched (full Hebrew reference, local line scores, run-4 readings):
  test    M5 held-out test pieces, own manuscript masked
  decoy   v4 decoys (m5_decoy.py rules, whole-manuscript parallel test in
          ms_parallel.py): real readings of texts with no known parallel,
          own manuscript masked
  srcx    source-excluded nulls: identified biblical pieces from training
          manuscripts, every witness of their book masked (the MT book and all
          scroll copies of it): 'lost text with near-neighbours'
  ownx    other identified biblical training pieces, only their own manuscript
          masked: the true source is present (positives for rescoring)
  target  the M7 target images (unidentified sets), nothing masked
The corpus also holds the entrapment documents (entrap_ref.py: Mishnah and
Tosefta, shared stretches blanked). They are scored, but kept apart from the
reference statistic: S and T use reference positions only, T_en is the best
entrapment score on the same scale. Exclusion masks every line's score
before chaining (pmatch.score_array(mask=...)); masking only start offsets
let a many-line chain reach the piece's own text (4Q184 -> '4Q183').

Per search:
  S     best fragment score in the reference (nats)
  I     reading information, sum over positions of KL(P_i || q)
  L     reading lines with letters
  ln N  ln(reference letters) + (L - 1) ln(W1 - W0 + 1)   (offsets x spacings)
  T     S - ln N
  gap   S minus the best score in another text group (MT book with its
        scroll copies, or one non-biblical composition)
  top_groups, top_chapters   best T per text group / MT chapter (LCA)
  islands  T of the top ISLANDS local maxima >= 200 letters apart
  T_en, en_doc   best entrapment hit

Step 6 variant: env FORWARD=1 sums over line spacings (pmatch forward=True);
ln N then drops the (L - 1) ln(W1 - W0 + 1) term. env KINDS=test,decoy,srcx
limits the sets. Output then goes to data/e4/searches2_fwd.json.

Usage: python3 src/e4.py        (then src/e4_eval.py)
Output: data/e4/searches2.json
"""
import json, os, re, sys, random, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from inventory import nms  # noqa: E402
from prior import load_meta, BOOKMAP  # noqa: E402

DE = 'data/e4'
FORWARD = os.environ.get('FORWARD') == '1'
KINDS = set(os.environ.get('KINDS', 'test,decoy,srcx,ownx,target').split(','))
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
            elif kind == 'EN':
                self.group.append({'E:' + name})
            else:
                cm = comp.get(name) or norm.get(nms(name)) or norm.get(nms(name.split('-')[0])) or name
                bks = BOOKMAP.get(cm)
                self.group.append({'B:' + b for b in bks} if bks else {'C:' + cm})

        starts = [0] + [i for i in range(1, len(c.docs)) if c.docs[i] != c.docs[i - 1]]
        self.doc_start = np.array(starts)
        self.start_doc = [idx[c.docs[i]] for i in starts]
        # MT chapter of every position ('' elsewhere)
        self.chap = [r.rsplit('.', 1)[0] if (d.startswith('MT ') and r) else '' for d, r in zip(c.docs, c.refs)]

    def mask(self, pred):
        """Boolean mask of corpus positions whose document satisfies pred(doc_name, groups)."""
        bad = np.array([pred(n, g) for n, g in zip(self.names, self.group)])
        return bad[self.doc_id]


def search(c, G, rd, mask, en):
    """mask: own text (left out everywhere); en: entrapment positions (scored,
    but kept apart from the reference statistic)."""
    acc = c.score_array(rd, W, mask=mask, forward=FORWARD)
    if acc is None:
        return None
    ref_acc = np.where(en, -1e9, acc)
    b = int(np.argmax(ref_acc))
    S = float(ref_acc[b])
    L = len([l for l in rd if l])
    lnN = float(np.log(c.letters) + (0 if FORWARD else (L - 1) * np.log(W[1] - W[0] + 1)))
    gtop = G.group[G.doc_id[b]]
    # best score per text group
    dmax = np.maximum.reduceat(acc, G.doc_start)
    gbest = collections.defaultdict(lambda: -1e9)
    for di, v in zip(G.start_doc, dmax):
        for g in G.group[di]:
            gbest[g] = max(gbest[g], float(v))
    ref_groups = sorted(((g, v) for g, v in gbest.items() if not g.startswith('E:') and v > -1e8),
                        key=lambda x: -x[1])
    s2 = next((v for g, v in ref_groups if g not in gtop), 0.0)
    en_best = max(((g, v) for g, v in gbest.items() if g.startswith('E:')), key=lambda x: x[1], default=(None, -1e9))
    # best MT chapters (among the top offsets)
    chaps = []
    for o in np.argsort(-ref_acc)[:3000]:
        ch = G.chap[o]
        if ch and ch not in (x[0] for x in chaps):
            chaps.append((ch, float(ref_acc[o]) - lnN))
            if len(chaps) == 10:
                break
    isl = islands(ref_acc)
    return dict(S=S, lnN=lnN, T=S - lnN, gap=S - s2, groups=sorted(gtop), doc=c.docs[b], ref=c.refs[b], L=L,
                islands=[float(ref_acc[o]) - lnN for o in isl],
                top_groups=[(g, round(v - lnN, 3)) for g, v in ref_groups[:12]], top_chapters=chaps,
                T_en=float(en_best[1]) - lnN, en_doc=en_best[0])


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
    c = pmatch.Corpus(local=True, entrap=True)
    G = Groups(c, comp)
    en = G.mask(lambda n, g: n.startswith('EN '))
    print(c.letters, 'reference letters;', int(en.sum()), 'entrapment positions;', len(G.names), 'documents',
          file=sys.stderr, flush=True)
    path = f'{DE}/searches2_fwd.json' if FORWARD else f'{DE}/searches2.json'
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
    # identified biblical pieces from training manuscripts, read with run 4:
    #   srcx - every witness of the book masked (null with near-neighbours)
    #   ownx - only the own manuscript masked (true source present: rescoring positives)
    rnd = random.Random(0)
    audit_rd = json.load(open('data/audit/readings.json'))
    bib = [n for n in audit_rd if pairs[n]['manuscript'] not in held
           and comp.get(pairs[n]['manuscript'], '') in BOOKMAP
           and sum(len(l['probs']) for l in audit_rd[n] if l['probs']) >= 3]
    pick = rnd.sample(bib, min(2 * N_SRCX, len(bib)))
    bpath = f'{DE}/readings_run4_bib.json'
    brd = json.load(open(bpath)) if os.path.exists(bpath) else {}
    todo = [n for n in pick if n not in brd]
    if todo:
        from recognise import load_model, read_image
        model = load_model('data/m4/run4_h96/best.pt')
        for n in todo:
            brd[n] = read_image(model, n)
        json.dump(brd, open(bpath, 'w'), ensure_ascii=False)
    for n in pick[:N_SRCX]:
        jobs.append(('srcx', n, brd[n]))
    for n in pick[N_SRCX:]:
        jobs.append(('ownx', n, brd[n]))
    for n, lines in json.load(open('data/m7/readings_run4.json')).items():
        jobs.append(('target', n, lines))
    t0 = time.time()
    for k, (kind, n, lines) in enumerate(jobs):
        key = f'{kind}|{n}'
        if key in res or kind not in KINDS:
            continue
        rd = rd_of(lines)
        nread = sum(len(l) for l in rd)
        if nread < 3:
            continue
        ms = pairs[n]['manuscript']
        scrolls = {x['etcbc'][0] for x in pairs[n]['links']}
        m = own_mask(ms, scrolls) if kind != 'target' else np.zeros(len(c.docs), bool)
        if kind == 'srcx':
            books = {'B:' + b for b in BOOKMAP[comp[ms]]}
            m |= G.mask(lambda nm, g: bool(g & books))
        r = search(c, G, rd, m, en)
        if r is None:
            continue
        r.update(kind=kind, name=n, manuscript=ms, read=nread, I=info(rd, c.q))
        res[key] = r
        if k % 200 == 199:
            json.dump(res, open(path, 'w'))
            print(k + 1, '/', len(jobs), round(time.time() - t0), 's', file=sys.stderr, flush=True)
    json.dump(res, open(path, 'w'))

    print(len(res), 'searches', file=sys.stderr)


if __name__ == '__main__':
    main()
