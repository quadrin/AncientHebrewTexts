"""Group small fragments: do several pieces of (presumably) one manuscript point
to the same work when none of them can alone?

compute:  for each piece (>= MIN_READ letters read), the best score in every
          reference document for the real reading and for N shuffled readings
          -> data/group/{tag}.npz
evaluate: per piece and document an empirical p-value against the pooled
          shuffled maxima of that document (pieces in the same read-letter band);
          a group's statistic per document is Fisher's sum of -log p; its best
          document is the argmax. Null groups are built from shuffled readings;
          the 1% threshold is taken per group size.

Usage:
  python3 src/group.py compute-m5 MODEL_READINGS_JSON   (held-out M5 pieces)
  python3 src/group.py compute-target [N_SHUF]          (M7 target pieces)
  python3 src/group.py validate                         (grouping test on M5 pieces)
  python3 src/group.py plates                           (4Q9999 plates)
"""
import json, os, re, sys, random, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402

DG = 'data/group'
MIN_READ = 3
BANDS = [(3, 5), (6, 9), (10, 19), (20, 10 ** 6)]


def band(n):
    return next(i for i, b in enumerate(BANDS) if b[0] <= n <= b[1])


def nms(s):
    return re.sub(r'[\s.^]', '', s).replace('_', '-').upper()


def shuffled(rd, rnd):
    out = []
    for l in rd:
        l = list(l)
        rnd.shuffle(l)
        out.append(l)
    return out


def compute(pieces, tag, n_shuf):
    """pieces: list of dict(name, manuscript, reading=[[dist...]...], exclude, targum)."""
    os.makedirs(DG, exist_ok=True)
    rnd = random.Random(0)
    corpora, docs_all = {}, None
    real, null, keep = [], [], []
    t0 = time.time()
    for k, p in enumerate(sorted(pieces, key=lambda p: (p['exclude'] or '', p['targum']))):
        key = (p['exclude'], p['targum'])
        if key not in corpora:
            corpora.clear()
            corpora[key] = pmatch.Corpus(exclude={p['exclude']} if p['exclude'] else (), mode='ex',
                                         targum=p['targum'])
        c = corpora[key]
        a = c.score_array(p['reading'])
        if a is None:
            continue
        c.doc_max(a)
        names = c.doc_names
        if docs_all is None:
            # global document list: all MT books, all scrolls, targums if any piece uses them
            full = pmatch.Corpus(mode='ex', targum=any(q['targum'] for q in pieces))
            full.doc_max(np.zeros(len(full.ids)))
            docs_all = full.doc_names
            index = {d: i for i, d in enumerate(docs_all)}

        def to_global(v):
            g = np.full(len(docs_all), -1e9, np.float32)
            g[[index[d] for d in names]] = v
            return g
        real.append(to_global(c.doc_max(a)))
        null.append(np.stack([to_global(c.doc_max(c.score_array(shuffled(p['reading'], rnd))))
                              for _ in range(n_shuf)]))
        keep.append(p)
        if k % 20 == 19:
            print(k + 1, 'pieces', round(time.time() - t0), 's', file=sys.stderr)
    np.savez_compressed(f'{DG}/{tag}.npz', real=np.stack(real), null=np.stack(null),
                        docs=np.array(docs_all))
    json.dump([dict(name=p['name'], manuscript=p['manuscript'], read=p['read'], targum=p['targum'])
               for p in keep], open(f'{DG}/{tag}.json', 'w'))


# ------------------------------------------------------------------ evaluation
def piece_pvalues(real, null, reads):
    """p[i, d] for real readings and pn[i, j, d] for shuffled ones, against the
    pooled shuffled maxima of document d among pieces in the same band."""
    P, N, D = null.shape
    b = np.array([band(r) for r in reads])
    p = np.ones((P, D), np.float32)
    pn = np.ones((P, N, D), np.float32)
    for bi in range(len(BANDS)):
        idx = np.nonzero(b == bi)[0]
        if not len(idx):
            continue
        pool = np.sort(null[idx].reshape(-1, D), axis=0)           # (M, D)
        M = pool.shape[0]
        for d in range(D):
            col = pool[:, d]
            p[idx, d] = (M - np.searchsorted(col, real[idx, d], 'left') + 1) / (M + 1)
            pn[idx, :, d] = (M - np.searchsorted(col, null[idx, :, d].ravel(), 'left').reshape(len(idx), N) + 1) / (M + 1)
    return p, pn


TRUNC = -np.log(0.05)


def group_stat(logp, truncated=False):
    """logp: (k, D) of -log p -> (best doc index, statistic).
    truncated: only pieces with p < 0.05 for a document count towards it
    (robust for large, mixed groups such as whole plates)."""
    s = np.maximum(logp - TRUNC, 0).sum(0) if truncated else logp.sum(0)
    d = int(np.argmax(s))
    return d, float(s[d])


def null_threshold(nlp, k, rnd, q=0.99, draws=2000):
    """Null groups of size k from shuffled readings of random pieces."""
    P, N, D = nlp.shape
    vals = []
    for _ in range(draws):
        ii = rnd.sample(range(P), k) if k <= P else [rnd.randrange(P) for _ in range(k)]
        g = np.stack([nlp[i, rnd.randrange(N)] for i in ii])
        vals.append(group_stat(g)[1])
    return float(np.quantile(vals, q)), vals


def mixed_null(lp, owner, k, rnd, draws=2000):
    """Decoy groups: k real pieces from k different manuscripts. They contain
    real words but share no source, which is what a same-manuscript group must
    beat. Returns the statistics and best-document indices."""
    by = collections.defaultdict(list)
    for i, o in enumerate(owner):
        by[o].append(i)
    keys = list(by)
    vals, docs = [], []
    if len(keys) < k:
        return vals, docs
    for _ in range(draws):
        ii = [rnd.choice(by[m]) for m in rnd.sample(keys, k)]
        d, st = group_stat(lp[ii])
        vals.append(st)
        docs.append(d)
    return vals, docs


def load(tag):
    z = np.load(f'{DG}/{tag}.npz')
    meta = json.load(open(f'{DG}/{tag}.json'))
    return z['real'], z['null'], list(z['docs']), meta


BOOKS = {'Leviticus': ['Lev'], 'Genesis': ['Gen'], 'Exodus': ['Exod'], 'Deuteronomy': ['Deut'],
         'Judges': ['Judg'], 'Kings': ['1Kgs', '2Kgs'], 'Isaiah': ['Isa'], 'Jeremiah': ['Jer'],
         'Minor Prophets': ['Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal'],
         'Psalms': ['Ps']}


def validate():
    real, null, docs, meta = load('m5')
    reads = [m['read'] for m in meta]
    p, pn = piece_pvalues(real, null, reads)
    lp = -np.log(p)
    ll = {m['manuscript_number']: m for m in json.load(open('data/m0/ll_manuscripts.json'))}
    rnd = random.Random(1)
    small = [i for i, m in enumerate(meta) if m['read'] <= 19]
    owner_small = [meta[i]['manuscript'] for i in small]
    lp_small = lp[small]
    by_ms = collections.defaultdict(list)
    for j, i in enumerate(small):
        if ll.get(meta[i]['manuscript'], {}).get('composition_name') in BOOKS:
            by_ms[meta[i]['manuscript']].append(j)
    out = []
    for k in (1, 2, 3, 5, 8):
        vals, ddocs = mixed_null(lp_small, owner_small, k, rnd)
        if not vals:
            continue
        thr = float(np.quantile(vals, 0.99))
        thr5 = float(np.quantile(vals, 0.95))
        n = own = over = over_own = over5 = over5_own = 0
        decoy_own = []
        for ms, idx in by_ms.items():
            if len(idx) < k:
                continue
            books = {'MT ' + b for b in BOOKS[ll[ms]['composition_name']]}
            # how often a decoy group lands on this manuscript's book: chance level
            decoy_own.append(np.mean([docs[d] in books for d in ddocs]))
            for _ in range(20):
                g = rnd.sample(idx, k)
                d, st = group_stat(lp_small[g])
                hit = docs[d] in books
                n += 1; own += hit
                if st >= thr:
                    over += 1; over_own += hit
                if st >= thr5:
                    over5 += 1; over5_own += hit
        row = dict(group_size=k, groups=n, best_doc_own_book=own, chance_own_book=round(float(np.mean(decoy_own)) * n, 1) if decoy_own else None,
                   over_5pct=over5, over_5pct_own_book=over5_own, over_1pct=over, over_1pct_own_book=over_own,
                   threshold_1pct=round(thr, 2))
        out.append(row)
        print(row)
    json.dump(dict(null='decoy groups of real pieces from different manuscripts', pieces_small=len(small),
                   biblical_manuscripts=len(by_ms), rows=out),
              open('reports/M8_group_validation.json', 'w'), indent=1)


def plates():
    """4Q9999 plates hold ~38 pieces each, surely from many manuscripts. Ask
    whether several pieces on one plate point to the same document: truncated
    Fisher statistic, against random sets of the same size from all pieces."""
    real, null, docs, meta = load('target')
    reads = [m['read'] for m in meta]
    p, _ = piece_pvalues(real, null, reads)
    lp = -np.log(p)
    inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
    groups = collections.defaultdict(list)
    for i, m in enumerate(meta):
        groups[inv[m['name']]['plate']].append(i)
    rnd = random.Random(2)
    rows = []
    for plate, idx in groups.items():
        k = len(idx)
        vals = [group_stat(lp[rnd.sample(range(len(meta)), k)], truncated=True)[1] for _ in range(1000)]
        d, st = group_stat(lp[idx], truncated=True)
        pval = (1 + sum(v >= st for v in vals)) / (len(vals) + 1)
        contrib = sorted(((round(float(lp[i, d]), 2), meta[i]['name'], meta[i]['read']) for i in idx
                          if lp[i, d] > TRUNC), reverse=True)
        rows.append(dict(plate=plate, pieces=k, best_doc=docs[d], stat=round(st, 2),
                         decoy_median=round(float(np.median(vals)), 2), p=round(pval, 4),
                         pieces_pointing=contrib))
    rows.sort(key=lambda r: r['p'])
    for r in rows:
        r['E'] = round(r['p'] * len(rows), 3)
    json.dump(rows, open(f'{DG}/plates.json', 'w'), ensure_ascii=False, indent=1)
    for r in rows[:12]:
        print({k: v for k, v in r.items() if k != 'pieces_pointing'}, r['pieces_pointing'][:4])


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'compute-m5':
        rd = json.load(open(sys.argv[2]))
        test = set(json.load(open('reports/M4_split.json'))['test'])
        pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
        pieces = []
        for name, lines in rd.items():
            reading = [l['probs'] for l in lines if l['probs']]
            n = sum(len(l) for l in reading)
            if n >= MIN_READ and pairs[name]['manuscript'] in test:
                pieces.append(dict(name=name, manuscript=pairs[name]['manuscript'], reading=reading, read=n,
                                   exclude=nms(pairs[name]['manuscript']), targum=False))
        print(len(pieces), 'pieces', file=sys.stderr)
        compute(pieces, 'm5', 20)
    elif cmd == 'compute-target':
        n_shuf = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        rd = json.load(open('data/m7/readings.json'))
        batch = {b['name']: b for b in json.load(open('data/m2/batch_target.json'))}
        pieces = []
        for name, lines in rd.items():
            reading = [l['probs'] for l in lines if l['probs']]
            n = sum(len(l) for l in reading)
            if n >= MIN_READ and batch[name]['manuscript'] == '4Q9999':
                pieces.append(dict(name=name, manuscript='4Q9999', reading=reading, read=n, exclude=None, targum=False))
        print(len(pieces), 'pieces', file=sys.stderr)
        compute(pieces, 'target', n_shuf)
    elif cmd == 'validate':
        validate()
    elif cmd == 'plates':
        plates()
