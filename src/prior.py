"""Physical prior: let scribal-hand similarity narrow the texts a fragment is
searched against, so that fewer letters are needed for a significant placement.

For a piece x:
  1. hand prior - rank identified manuscripts by the best cosine similarity of
     x's hand features to any of their pieces (pieces on x's own IAA plate are
     left out: one photo session, usually one manuscript); keep the top K
  2. candidate texts - for each candidate manuscript, what a new piece of it
     could contain: its MT book(s) if biblical, else every copy of its
     composition (ETCBC scrolls with the same Leon Levy composition name);
     plus the candidate's own transcription (catalogue-error case)
  3. restricted search of x's reading in that union, W = (1, 140) for scrolls
  4. calibration - decoys: readings of identified pieces whose own text has no
     known parallel (m5_decoy.py) and whose composition is outside the
     candidate set, of similar length, searched in the same union;
     p = rank of x's best score among the decoys'

Validation (held-out M5 manuscripts): x's own manuscript's transcription is
left out of the reference (as in M5), but its MT book stays. Measure: share of
biblical test pieces whose top hit is in their own book with p <= 0.01, by
read letters, against the full-corpus search (M5).

Usage: python3 src/prior.py validate [K]
"""
import json, os, re, sys, random, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from hand import matrix  # noqa: E402
from inventory import nms  # noqa: E402

BOOKMAP = {'Genesis': ['Gen'], 'Exodus': ['Exod'], 'Leviticus': ['Lev'], 'Numbers': ['Num'], 'Numbers?': ['Num'],
           'Deuteronomy': ['Deut'], 'Joshua': ['Josh'], 'Judges': ['Judg'], 'Samuel': ['1Sam', '2Sam'],
           'Kings': ['1Kgs', '2Kgs'], 'papKings': ['1Kgs', '2Kgs'], 'Isaiah': ['Isa'], 'Jeremiah': ['Jer'],
           'Ezekiel': ['Ezek'], 'Minor Prophets': ['Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab',
                                                   'Zeph', 'Hag', 'Zech', 'Mal'],
           'Psalms': ['Ps'], 'Psalms?': ['Ps'], 'Proverbs': ['Prov'], 'papProverbs': ['Prov'], 'Job': ['Job'],
           'Song of Songs': ['Song'], 'Ruth': ['Ruth'], 'Lamentations': ['Lam'], 'Qohelet': ['Eccl'],
           'Daniel': ['Dan'], 'papDaniel': ['Dan'], 'Ezra': ['Ezra', 'Neh'], 'Chronicles': ['1Chr', '2Chr'],
           'Genesis-Exodus': ['Gen', 'Exod'], 'Exodus-Leviticus': ['Exod', 'Lev'],
           'Leviticus-Numbers': ['Lev', 'Num']}
W = (1, 140)
N_DECOY = 100
BANDS = [(3, 5), (6, 9), (10, 19), (20, 10 ** 6)]


def load_meta():
    ll = {}
    for m in json.load(open('data/m0/ll_manuscripts.json')):
        ll[m['manuscript_number']] = m
    for k, m in json.load(open('data/m0/ll_other_manuscripts.json')).items():
        if m:
            ll[k] = m
    comp = {k: (m.get('composition_name') or k) for k, m in ll.items()}
    etcbc = collections.defaultdict(set)          # composition -> ETCBC scroll names
    scrolls = {s for s, *_ in json.load(open('data/ref/dss_lines.json'))}
    norm = {nms(s): s for s in scrolls}
    for ms, cname in comp.items():
        s = norm.get(nms(ms))
        if s:
            etcbc[cname].add(s)
    return ll, comp, etcbc


def candidate_texts(cands, comp, etcbc):
    books, scr = set(), set()
    for m in cands:
        c = comp.get(m, m)
        books |= set(BOOKMAP.get(c, []))
        scr |= etcbc.get(c, set())
    return books, scr


def validate(K):
    z = np.load('data/hand/features.npz')
    names = list(z['names'])
    X = matrix(z)
    pos = {n: i for i, n in enumerate(names)}
    inv = {x['name']: x for x in json.load(open('data/m0/inventory_images.json'))}
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    ll, comp, etcbc = load_meta()
    split = json.load(open('reports/M4_split.json'))
    test = set(split['test'])
    readings = json.load(open('data/m5/readings_run2.json'))          # held-out pieces
    audit_rd = json.load(open('data/audit/readings.json'))             # decoy pool (identified)
    # reference pool for the hand prior: identified parchment pieces with features
    ref = [n for n in names if n in pairs and pairs[n]['split'] == 'train' and pairs[n]['material'] == 'Parchment']
    ref_i = np.array([pos[n] for n in ref])
    ref_ms = np.array([inv[n]['manuscript'] for n in ref])
    ref_plate = np.array([inv[n]['plate'] for n in ref])
    full = pmatch.Corpus()
    rnd = random.Random(0)
    # decoys: images whose own text has no known parallel (m5_decoy.py)
    clean = set(json.load(open('data/m5/decoy_names.json')))
    decoy_pool = []
    for d, lines in audit_rd.items():
        if d not in clean:
            continue
        rd = [l['probs'] for l in lines if l['probs']]
        k = sum(len(l) for l in rd)
        if k >= 3:
            decoy_pool.append((d, pairs[d]['manuscript'], rd, k))
    rows = []
    t0 = time.time()
    for n, lines in readings.items():
        if n not in pos:
            continue
        x_ms = pairs[n]['manuscript']
        rd = [l['probs'] for l in lines if l['probs']]
        k = sum(len(l) for l in rd)
        if k < 3:
            continue
        # 1. hand prior
        sim = X[ref_i] @ X[pos[n]]
        sim[ref_plate == inv[n]['plate']] = -9
        best = collections.defaultdict(lambda: -9.0)
        for s, m in zip(sim, ref_ms):
            if s > best[m]:
                best[m] = s
        ranked = sorted(best, key=lambda m: -best[m])
        cands = ranked[:K]
        own_rank = ranked.index(x_ms) + 1 if x_ms in ranked else None
        # 2. candidate texts; leave x's own transcription out (as in M5)
        books, scr = candidate_texts(cands, comp, etcbc)
        scr = {s for s in scr if nms(s) != nms(x_ms)}
        c = pmatch.Corpus(mt=books or False, keep=lambda s, f: s in scr, q=full.q)
        if c.letters == 0:
            continue
        h = c.search(rd, W=W, top=3)
        # 4. decoys from compositions outside the candidate set
        cand_comps = {comp.get(m, m) for m in cands} | {comp.get(x_ms, x_ms)}
        pool = [d for d in decoy_pool if comp.get(d[1], d[1]) not in cand_comps
                and abs(np.log(d[3] / k)) <= np.log(1.5)]
        dec = rnd.sample(pool, min(N_DECOY, len(pool)))
        ds = np.array([c.search(d[2], W=W, top=1)[0][0] for d in dec])
        p = float((1 + (ds >= h[0][0]).sum()) / (len(ds) + 1))
        x_books = BOOKMAP.get(comp.get(x_ms, ''), [])
        top_book = h[0][2].split('.')[0] if h[0][1].startswith('MT') else None
        rows.append(dict(name=n, manuscript=x_ms, read=k, own_rank=own_rank, books=sorted(books),
                         corpus_letters=c.letters, biblical=bool(x_books), own_book_in_corpus=bool(set(x_books) & books),
                         top=h[0][:3], p=round(p, 4), top_in_own_book=top_book in x_books))
        if len(rows) % 20 == 0:
            print(len(rows), 'pieces', round(time.time() - t0), 's', file=sys.stderr, flush=True)
    json.dump(rows, open(f'data/hand/prior_validation_K{K}.json', 'w'), ensure_ascii=False)
    out = dict(K=K, pieces=len(rows),
               own_ms_in_topK=sum(1 for r in rows if r['own_rank'] and r['own_rank'] <= K),
               median_corpus_letters=int(np.median([r['corpus_letters'] for r in rows])), bands=[])
    for lo, hi in BANDS:
        b = [r for r in rows if r['biblical'] and lo <= r['read'] <= hi]
        out['bands'].append(dict(read=f'{lo}-{hi if hi < 10**6 else "+"}', biblical_pieces=len(b),
                                 own_book_in_corpus=sum(r['own_book_in_corpus'] for r in b),
                                 top_in_own_book=sum(r['top_in_own_book'] for r in b),
                                 p001=sum(r['p'] <= 0.01 for r in b),
                                 p001_own_book=sum(r['p'] <= 0.01 and r['top_in_own_book'] for r in b),
                                 p005=sum(r['p'] <= 0.05 for r in b),
                                 p005_own_book=sum(r['p'] <= 0.05 and r['top_in_own_book'] for r in b)))
    # false positives: non-biblical pieces (no MT parallel expected) passing p <= 0.01
    nb = [r for r in rows if not r['biblical']]
    out['non_biblical'] = dict(pieces=len(nb), p001=sum(r['p'] <= 0.01 for r in nb))
    json.dump(out, open(f'reports/M9_prior_validation_K{K}.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    if sys.argv[1] == 'validate':
        validate(int(sys.argv[2]) if len(sys.argv) > 2 else 20)
