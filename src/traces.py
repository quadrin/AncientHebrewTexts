"""Idea 3 scoping: do the letter traces support the letters the editors read?

For held-out lines (M4 test and validation manuscripts, M3 tiers A/B, never
seen in training), the editors' label is force-aligned to the line image with
CTC (Viterbi). Each label letter gets:
  own - mean posterior of the editors' letter over its aligned frames
  alt - the best other letter's mean posterior over the same frames
Letters are grouped by the editors' mark: certain ('.') or uncertain ('u',
the damaged letters, mostly at the edges of lacunae), and by position (next to
a lacuna or a line end, or inside). A letter is 'contested' when alt >= 0.5
and own < 0.2. The contested rate on certain letters estimates the
recogniser's own false-flag rate; the excess on uncertain letters is what a
trace check could add.

Usage: python3 src/traces.py MODEL
Outputs: data/traces/letters.json, reports/M9_traces.json
"""
import json, os, re, sys, collections
import numpy as np, cv2, torch
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(__file__))
from recognise import load_model, prep_line  # noqa: E402
from train import ALPHABET, C2I  # noqa: E402

FIN = str.maketrans('ךםןףץ', 'כמנפצ')


def label_marks(t, m):
    """Same label as align.visible, with the mark of every kept character."""
    idx = [i for i, c in enumerate(m) if c in '.u']
    a, b = idx[0], idx[-1] + 1
    out = []
    for i in range(a, b):
        c, k = t[i], m[i]
        if k in '.u ':
            if c == ' ' and out and out[-1][0] == ' ':
                continue
            # gap flag: a reconstructed/lacuna sign sits right next to this letter
            gap = (i > 0 and m[i - 1] in 'r#') or (i + 1 < len(m) and m[i + 1] in 'r#')
            out.append([c, k, gap])
    while out and out[0][0] == ' ':
        out.pop(0)
    while out and out[-1][0] == ' ':
        out.pop()
    if out:
        out[0][2] = out[-1][2] = True          # line ends count as edges
    return out


def viterbi(logp, y):
    """CTC forced alignment. logp: T x C (log-softmax), y: target ids.
    Returns, for each target index, the list of frames aligned to it."""
    T = logp.shape[0]
    S = 2 * len(y) + 1
    ext = [0] * S
    for i, c in enumerate(y):
        ext[2 * i + 1] = c
    NEG = -1e9
    dp = np.full((T, S), NEG)
    bp = np.zeros((T, S), int)
    dp[0, 0] = logp[0, 0]
    if S > 1:
        dp[0, 1] = logp[0, ext[1]]
    ext = np.array(ext)
    skip = np.zeros(S, bool)
    skip[2:] = (ext[2:] != 0) & (ext[2:] != ext[:-2])
    for t in range(1, T):
        a = dp[t - 1]
        b = np.full(S, NEG); b[1:] = a[:-1]
        c = np.full(S, NEG); c[2:] = np.where(skip[2:], a[:-2], NEG)
        st = np.stack([a, b, c])
        k = st.argmax(0)
        dp[t] = st[k, np.arange(S)] + logp[t, ext]
        bp[t] = np.arange(S) - k
    s = S - 1 if S == 1 or dp[T - 1, S - 1] >= dp[T - 1, S - 2] else S - 2
    if dp[T - 1, s] <= NEG / 2:
        return None
    frames = [[] for _ in y]
    for t in range(T - 1, -1, -1):
        if s % 2 == 1:
            frames[s // 2].append(t)
        s = bp[t, s]
    return frames


def main():
    model = load_model(sys.argv[1])
    split = json.load(open('reports/M4_split.json'))
    held = set(split['test']) | set(split['val'])
    pairs = {r['name']: r for r in json.load(open('data/m1/pairs.json'))}
    et = {}
    for s_, f, l, t, m in json.load(open('data/m0/etcbc_lines.json')):
        et[(s_, f, l)] = (t, m)
    man = [json.loads(l) for l in open('data/m3/manifest.jsonl')]
    recs = [r for r in man if r['tier'] in ('A', 'B') and r['manuscript'] in held]
    rows = []
    skipped = collections.Counter()
    for r in recs:
        links = pairs[r['name']]['links']
        if len(links) != 1:
            skipped['links'] += 1
            continue
        s_, f = links[0]['etcbc'][:2]
        tm = et.get((s_, f, r['line']))
        if not tm:
            skipped['no_line'] += 1
            continue
        lm = label_marks(*tm)
        if ''.join(c for c, _, _ in lm) != r['label']:
            skipped['label_mismatch'] += 1
            continue
        g = cv2.imread(f'data/m3/lines/{r["id"]}.png', 0)
        if g is None:
            skipped['no_image'] += 1
            continue
        with torch.no_grad():
            lg = model(prep_line(g))[0]
        logp = F.log_softmax(lg, -1).numpy()
        prob = np.exp(logp)
        # network order is left to right: reverse the label
        seq = [(c, k, gap) for c, k, gap in reversed(lm) if c in C2I]
        y = [C2I[c] for c, _, _ in seq]
        if len(y) * 1 > logp.shape[0]:
            skipped['too_long'] += 1
            continue
        fr = viterbi(logp, y)
        if fr is None:
            skipped['no_path'] += 1
            continue
        for (c, k, gap), ts in zip(seq, fr):
            if c == ' ':
                continue
            p = prob[ts, 1:].mean(0)
            own_i = C2I[c] - 1
            # the same letter in its other (final / non-final) form counts as own
            same = [i for i, a in enumerate(ALPHABET) if a != ' ' and a.translate(FIN) == c.translate(FIN)]
            own = float(p[same].sum())
            q = p.copy()
            q[same] = 0
            q[ALPHABET.index(' ')] = 0
            j = int(q.argmax())
            rows.append(dict(id=r['id'], manuscript=r['manuscript'], letter=c, mark=k, edge=bool(gap),
                             own=round(own, 4), alt=ALPHABET[j], alt_p=round(float(q[j]), 4)))
    os.makedirs('data/traces', exist_ok=True)
    json.dump(rows, open('data/traces/letters.json', 'w'), ensure_ascii=False)

    def stats(sel):
        own = np.array([x['own'] for x in sel])
        cont = np.array([x['alt_p'] >= 0.5 and x['own'] < 0.2 for x in sel])
        return dict(letters=len(sel), median_own=round(float(np.median(own)), 3) if len(sel) else None,
                    share_own_ge_0_5=round(float((own >= 0.5).mean()), 3) if len(sel) else None,
                    contested=int(cont.sum()), contested_rate=round(float(cont.mean()), 4) if len(sel) else None)
    out = dict(lines=len(recs), skipped=dict(skipped), letters=len(rows), groups={})
    for mark in '.u':
        for edge in (False, True):
            sel = [x for x in rows if x['mark'] == mark and x['edge'] == edge]
            out['groups'][f'{"certain" if mark == "." else "uncertain"}|{"edge" if edge else "inside"}'] = stats(sel)
    out['certain'] = stats([x for x in rows if x['mark'] == '.'])
    out['uncertain'] = stats([x for x in rows if x['mark'] == 'u'])
    cont_u = [x for x in rows if x['mark'] == 'u' and x['alt_p'] >= 0.5 and x['own'] < 0.2]
    out['uncertain_contested_pairs'] = collections.Counter(f"{x['letter']}->{x['alt']}" for x in cont_u).most_common(15)
    json.dump(out, open('reports/M9_traces.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
