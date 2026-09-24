"""Probabilistic matcher: place a recognised fragment (per-position letter
probabilities, several lines) in a reference corpus.

Corpus: MT books (data/ref/bible.json) plus the preserved letters of every
ETCBC scroll (data/ref/dss_lines.json), final forms folded into medial forms
(22 letters). A barrier symbol sits between lacunae, scroll lines of different
fragments, and documents, so no match crosses a gap.

Line score at offset o: sum_i log((P_i[c_{o+i}] + eps) / E_q[P_i + eps]), a
log-likelihood ratio of "the fragment shows this text" against "random letters
with corpus frequencies q". Fragment score: line 1 at o, each next line's best
offset d in [W0, W1] letters later (the line width is unknown), summed.

Modes: 'ex' exact spelling; 'sk' drops ו and י (positions where the reading
puts over half its mass on ו/י, and those letters in the corpus).
"""
import json, re, collections
import numpy as np
from scipy.ndimage import maximum_filter1d

FIN = str.maketrans('ךםןףץ', 'כמנפצ')
LET = 'אבגדהוזחטיכלמנסעפצקרשת'
IDX = {c: i for i, c in enumerate(LET)}
BAR = len(LET)             # barrier id
EPS = 0.02


def _norm(c):
    return c.translate(FIN)


class Corpus:
    def __init__(self, exclude=(), mode='ex'):
        """exclude: normalised scroll sigla to leave out (the fragment's own manuscript)."""
        self.mode = mode
        ids, refs, docs = [], [], []

        def add(label, seq):
            # seq: list of (letter or None for barrier, ref)
            for c, r in seq:
                if c is None:
                    if ids and ids[-1] != BAR:
                        ids.append(BAR); refs.append(r); docs.append(label)
                    continue
                c = _norm(c)
                if mode == 'sk' and c in 'וי':
                    continue
                ids.append(IDX[c]); refs.append(r); docs.append(label)
            ids.append(BAR); refs.append(None); docs.append(label)

        by_book = collections.defaultdict(list)
        for ref, t in json.load(open('data/ref/bible.json')):
            by_book[ref.split('.')[0]].append((ref, t))
        for b, vs in by_book.items():
            add('MT ' + b, [(c, r) for r, t in vs for c in t if c != ' '])
        by_scroll = collections.defaultdict(list)
        for s, f, l, t, m, _ in json.load(open('data/ref/dss_lines.json')):
            by_scroll[s].append((f, l, t, m))
        for s, ls in by_scroll.items():
            if re.sub(r'[\s.^]', '', s).upper() in exclude:
                continue
            seq, last_f = [], None
            for f, l, t, m in ls:
                if f != last_f:
                    seq.append((None, None))
                    last_f = f
                for c, k in zip(t, m):
                    if k in '.u' and 'א' <= c <= 'ת':
                        seq.append((c, f'{s} {f}:{l}'))
                    elif k in 'r#p':
                        seq.append((None, None))
            add('DSS ' + s, seq)
        self.ids = np.array(ids, np.int8)
        self.refs, self.docs = refs, docs
        cnt = np.bincount(self.ids[self.ids != BAR], minlength=len(LET)).astype(np.float64)
        self.q = cnt / cnt.sum()

    # -------------------------------------------------------------- scoring
    def llr_table(self, dists):
        """dists: list of {letter: p} (final forms allowed) -> (L x 23) table."""
        rows = []
        for d in dists:
            p = np.zeros(len(LET))
            for c, v in d.items():
                c = _norm(c)
                if c in IDX:
                    p[IDX[c]] += v
            if self.mode == 'sk':
                if p[IDX['ו']] + p[IDX['י']] > 0.5 * p.sum():
                    continue
                p[IDX['ו']] = p[IDX['י']] = 0
            p = p / p.sum() if p.sum() else np.full(len(LET), 1 / len(LET))
            den = float(np.dot(self.q, p + EPS))
            rows.append(np.concatenate([np.log((p + EPS) / den), [-20.0]]))
        return np.array(rows) if rows else np.zeros((0, len(LET) + 1))

    def line_scores(self, table):
        n = len(self.ids)
        L = len(table)
        if L == 0:
            return None
        s = np.zeros(n, np.float32)
        ids = self.ids.astype(np.int64)
        for i in range(L):
            col = table[i][ids]
            s[:n - i] += col[i:]
            if i:
                s[n - i:] = -1e9
        return s

    def line_scores_gapped(self, table, gap=4.0):
        """Local alignment with single-step gaps, scored at the START offset.

        A_i[j]: best score with reading position i on corpus position j.
          A_i[j] = s(i, c_j) + max(0, A_{i-1}[j-1],
                                   A_{i-1}[j-2] - gap,   # a corpus letter the reading missed
                                   A_{i-2}[j-1] - gap)   # an extra letter in the reading
        Runs right to left over the corpus so the result is indexed by the
        start position, like line_scores. Computed row by row with numpy.
        """
        L = len(table)
        if L == 0:
            return None
        ids = self.ids[::-1].astype(np.int64)         # reversed corpus
        n = len(ids)
        NEG = np.float32(-1e9)

        def shift(a, k):
            out = np.full(n, NEG, np.float32)
            out[k:] = a[:n - k]
            return out
        prev2 = np.full(n, NEG, np.float32)
        prev = np.full(n, NEG, np.float32)
        best = np.full(n, NEG, np.float32)
        # reading reversed too, so alignment order stays consistent
        for i in range(L - 1, -1, -1):
            s = table[i][ids].astype(np.float32)
            cand = np.maximum(np.float32(0), shift(prev, 1))
            cand = np.maximum(cand, shift(prev, 2) - gap)
            cand = np.maximum(cand, shift(prev2, 1) - gap)
            cur = s + cand
            best = np.maximum(best, cur)
            prev2, prev = prev, cur
        return best[::-1].copy()                      # index = start position in the corpus

    def search(self, lines, W=(15, 140), top=5, min_letters=1, gapped=False):
        """lines: list of lists of distributions (top to bottom).
        Returns best total score and the top hits [(score, doc, ref, offset)]."""
        tables = [self.llr_table(l) for l in lines]
        tables = [t for t in tables if len(t) >= min_letters]
        if not tables:
            return None
        score = self.line_scores_gapped if gapped else self.line_scores
        # chain lines top to bottom: each next line starts W0..W1 letters after
        # the previous one. Built backwards: T_k = s_k,
        # T_{k-1}[o] = s_{k-1}[o] + max(T_k[o+W0 .. o+W1]).
        # A band can be junk (a crack, letter tips at a broken edge) or a line
        # the matcher cannot place: every line contributes max(score, 0), so it
        # may be skipped while the spacing still advances one line. A reported
        # offset then lies within about one line of the matched text.
        size = W[1] - W[0] + 1
        acc = None
        for k, t in enumerate(reversed(tables)):
            s = score(t).astype(np.float64)
            s = np.maximum(s, 0.0)
            if acc is not None:
                mx = maximum_filter1d(acc, size=size, origin=-(size // 2), mode='constant', cval=-1e9)
                nxt = np.full_like(s, -1e9)
                nxt[:len(s) - W[0]] = mx[W[0]:]
                s = s + nxt
            acc = s
        order = np.argsort(-acc)[:200]
        hits, seen = [], []
        for o in order:
            if any(abs(o - p) < 50 for p in seen):
                continue
            seen.append(o)
            hits.append((float(acc[o]), self.docs[o], self.refs[o], int(o)))
            if len(hits) == top:
                break
        return hits
