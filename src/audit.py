"""Catalogue audit, forward direction: does each identified image show the text
its catalogue link says?

For every preprocessed identified image (M2: clean one-to-one parchment,
shared/image_many, papyrus) the recogniser reads all bands. The reading is
scored against three references, each with shuffled-reading controls on that
same reference:
  own  - the ETCBC fragments the image is linked to
  ms   - every fragment of the linked manuscript(s)
  full - MT + all scrolls (only for images whose own fit fails)
Scroll references are searched with line spacing W = (1, 140): ETCBC stores an
unrestored lacuna as one symbol, so consecutive lines of one fragment can sit
only a few letters apart.

Fragment-level test (manuscript reference). Controls are DECOYS: real readings
of images from other compositions (shuffled readings are too weak a control:
real words fit any Hebrew text better than shuffled letters). For each
manuscript, N_DECOY decoys are scored against every fragment; an image is
compared with the decoys of similar length (read letters within x1.5).
Each fragment's score is standardised against the decoys (z); the best
fragment's family-wise p compares its z with each decoy's maximum z over all
fragments (corrects for the number and size of fragments).
Verdicts:
  ok            the linked fragment fits (per-fragment p < 0.05)
  split_record  another fragment record fits (family-wise p <= 0.02) that shares
                a fragment number with the link (e.g. 'f6' vs 'f6+14'): a join or
                split in the data, not a misidentified piece
  other_frag    an unrelated fragment of the same manuscript fits (p_fw <= 0.02)
                while the linked one does not (z < 2)
  elsewhere     own fit fails, and the full-corpus best hit clears the M5
                per-band 1% threshold in another composition
  no_fit        >= 15 letters read, nothing fits (mispairing or bad reading)
  too_short     < MIN_READ letters read
Outputs: data/audit/readings.json, data/audit/forward.json,
reports/M9_audit_forward.json (counts) and reports/M9_audit_forward.md (flags).

Usage: python3 src/audit.py MODEL [SCROLL,SCROLL,...]
"""
import json, os, re, sys, random, collections, time
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402
from recognise import load_model, read_image  # noqa: E402
from inventory import nms  # noqa: E402

DA = 'data/audit'
MIN_READ = 6
N_SHUF = 100
N_DECOY = 600
W_SCROLL = (1, 140)
# M5 per-band 1% thresholds (run-2 model, full corpus): read letters -> score
M5_THR = [(1, 9, 17.7), (10, 19, 25.5), (20, 39, 39.7), (40, 10 ** 6, 44.9)]


def m5_thr(n):
    return next(t for lo, hi, t in M5_THR if lo <= n <= hi)


def shuffled(rd, rnd):
    out = []
    for l in rd:
        l = list(l)
        rnd.shuffle(l)
        out.append(l)
    return out


def fragment_index(c):
    """Fragment label for every corpus position (barriers take the previous one)."""
    lab, cur = [], None
    for r in c.refs:
        if r:
            cur = r.split(':')[0]          # 'scroll frag'
        lab.append(cur)
    names = sorted({x for x in lab if x})
    idx = {n: i for i, n in enumerate(names)}
    return np.array([idx.get(x, -1) for x in lab]), names


def frag_scores(c, fidx, nf, rd):
    a = c.score_array(rd, W=W_SCROLL)
    out = np.full(nf, -1e9)
    ok = fidx >= 0
    np.maximum.at(out, fidx[ok], a[ok])
    return out


def fragment_test(c, fidx, fnames, rd, rnd):
    nf = len(fnames)
    real = frag_scores(c, fidx, nf, rd)
    null = np.stack([frag_scores(c, fidx, nf, shuffled(rd, rnd)) for _ in range(N_SHUF)])
    mu, sd = null.mean(0), null.std(0) + 1e-6
    z_real, z_null = (real - mu) / sd, (null - mu) / sd
    p_frag = (1 + (null >= real).sum(0)) / (N_SHUF + 1)
    best = int(np.argmax(z_real))
    p_fw = (1 + (z_null.max(1) >= z_real[best]).sum()) / (N_SHUF + 1)
    return dict(real=real, z=z_real, p_frag=p_frag, best=best, p_fw=p_fw)


def frag_numbers(label):
    """'f6+14' -> {6, 14}; 'f9i_10' -> {9, 10}; 'f2ii' -> {2}; column labels '12a' -> {12}."""
    nums = set()
    for part in label.replace('f', '').split('+'):
        ends = [int(x) for x in re.findall(r'\d+', part)]
        if '_' in part and len(ends) == 2 and ends[1] >= ends[0] and ends[1] - ends[0] < 50:
            nums |= set(range(ends[0], ends[1] + 1))
        else:
            nums |= set(ends)
    return nums


def main():
    model_path = sys.argv[1]
    os.makedirs(DA, exist_ok=True)
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    names = []
    for f in ('data/m2/batch_parchment.json', 'data/m2/batch_shared.json', 'data/m2/batch_papyrus.json'):
        names += [b['name'] for b in json.load(open(f)) if not b.get('error')]
    names = [n for n in dict.fromkeys(names) if pairs[n]['links'] and os.path.exists(f'data/m2/seg/{n}.json')]
    rpath = f'{DA}/readings.json'
    readings = json.load(open(rpath)) if os.path.exists(rpath) else {}
    model = load_model(model_path)
    for k, n in enumerate(names):
        if n not in readings:
            readings[n] = read_image(model, n)
        if k % 500 == 499:
            json.dump(readings, open(rpath, 'w'), ensure_ascii=False)
    json.dump(readings, open(rpath, 'w'), ensure_ascii=False)
    rd_of = {n: [l['probs'] for l in readings[n] if l['probs']] for n in names}
    nread = {n: sum(len(l) for l in rd_of[n]) for n in names}
    print(len(names), 'identified images read', file=sys.stderr, flush=True)

    comp = {}
    for m in json.load(open('data/m0/ll_manuscripts.json')):
        comp[m['manuscript_number']] = m.get('composition_name') or m['manuscript_number']
    for k, m in json.load(open('data/m0/ll_other_manuscripts.json')).items():
        if m:
            comp[k] = m.get('composition_name') or k
    full = pmatch.Corpus()
    q = full.q
    rnd = random.Random(0)
    decoy_pool = [n for n in names if nread[n] >= MIN_READ]

    by_ms = collections.defaultdict(list)
    for n in names:
        by_ms[tuple(sorted({x['etcbc'][0] for x in pairs[n]['links']}))].append(n)
    out = []
    t0 = time.time()
    only = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None   # test on a few scrolls
    items = [(sc, im) for sc, im in sorted(by_ms.items()) if only is None or set(sc) & only]
    for k, (scrolls, imgs) in enumerate(items):
        ms_names = {pairs[n]['manuscript'] for n in imgs}
        comps = {comp.get(m, m) for m in ms_names}
        c = pmatch.Corpus(mt=False, keep=lambda s, f: s in scrolls, q=q)
        fidx, fnames = fragment_index(c)
        nf = len(fnames)
        # decoys: real readings of images from other compositions
        cand = [d for d in decoy_pool if pairs[d]['manuscript'] not in ms_names
                and comp.get(pairs[d]['manuscript'], '') not in comps]
        dec = rnd.sample(cand, min(N_DECOY, len(cand)))
        dscore = np.stack([frag_scores(c, fidx, nf, rd_of[d]) for d in dec])
        dlen = np.array([nread[d] for d in dec])
        for n in imgs:
            pr = pairs[n]
            rec = dict(name=n, manuscript=pr['manuscript'], category=pr['category'], material=pr['material'],
                       links=[x['etcbc'] for x in pr['links']], read=nread[n],
                       reading=[l['text'] for l in readings[n] if l['text']])
            if nread[n] < MIN_READ:
                rec['verdict'] = 'too_short'
                out.append(rec)
                continue
            own = {f"{x['etcbc'][0]} {x['etcbc'][1]}" for x in pr['links']}
            own_i = [i for i, f in enumerate(fnames) if f in own]
            real = frag_scores(c, fidx, nf, rd_of[n])
            # decoys of similar length
            sel = np.abs(np.log(dlen / nread[n])) <= np.log(1.5)
            if sel.sum() < 20:
                sel = np.argsort(np.abs(np.log(dlen / nread[n])))[:20]
            D = dscore[sel]
            mu, sd = D.mean(0), D.std(0) + 1e-6
            z = (real - mu) / sd
            zD = (D - mu) / sd
            p_own = min(float((1 + (D[:, i] >= real[i]).sum()) / (len(D) + 1)) for i in own_i) if own_i else 1.0
            z_own = max(float(z[i]) for i in own_i) if own_i else -99.0
            b = int(np.argmax(z))
            p_fw = float((1 + (zD.max(1) >= z[b]).sum()) / (len(D) + 1))
            rec.update(p_own=round(p_own, 4), z_own=round(z_own, 2), n_frags=nf, n_decoys=int(len(D)),
                       best_frag=fnames[b], z_best=round(float(z[b]), 2), p_fw=round(p_fw, 4),
                       s_best=round(float(real[b]), 2))
            own_nums = set().union(*[frag_numbers(f.split(' ')[1]) for f in own]) if own else set()
            if p_own <= 0.05:
                rec['verdict'] = 'ok'
            elif fnames[b] not in own and p_fw <= 0.02 and z_own < 2:
                related = bool(frag_numbers(fnames[b].split(' ')[1]) & own_nums)
                rec['verdict'] = 'split_record' if related else 'other_frag'
            else:
                h = full.search(rd_of[n], top=3)
                rec['full_hits'] = [(round(a, 2), d, r) for a, d, r, _ in h] if h else []
                top_doc = h[0][1] if h else ''
                if (h and nread[n] >= 10 and h[0][0] >= m5_thr(nread[n])
                        and not (top_doc.startswith('DSS ') and top_doc[4:] in scrolls)):
                    rec['verdict'] = 'elsewhere'
                elif nread[n] >= 15:
                    rec['verdict'] = 'no_fit'
                else:
                    rec['verdict'] = 'weak'
            out.append(rec)
        if k % 20 == 19:
            print(k + 1, 'manuscripts', len(out), 'images', round(time.time() - t0), 's',
                  dict(collections.Counter(r['verdict'] for r in out)), file=sys.stderr, flush=True)
            json.dump(out, open(f'{DA}/forward.json', 'w'), ensure_ascii=False)
    json.dump(out, open(f'{DA}/forward.json', 'w'), ensure_ascii=False)
    cnt = collections.Counter(r['verdict'] for r in out)
    by_cat = collections.Counter((r['category'], r['verdict']) for r in out)
    json.dump(dict(images=len(out), verdicts=dict(cnt), by_category={f'{a}|{b}': v for (a, b), v in by_cat.items()}),
              open('reports/M9_audit_forward.json', 'w'), indent=1)
    print(dict(cnt))


if __name__ == '__main__':
    main()
