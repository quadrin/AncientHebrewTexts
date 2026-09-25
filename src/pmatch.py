"""Probabilistic matcher: place a recognised fragment (per-position letter
probabilities, several lines) in a reference corpus.

Corpus: MT books (data/ref/bible.json) plus the preserved letters of every
ETCBC scroll (data/ref/dss_lines.json), final forms folded into medial forms
(22 letters). Barrier symbols stop matches from crossing gaps: one per
reconstructed letter (so letter distances across a reconstruction are kept for
the line-spacing window), one per lacuna of unknown length, fragment break and
document end.

Line score at offset o: sum_i log((P_i[c_{o+i}] + eps) / E_q[P_i + eps]), a
log-likelihood ratio of "the fragment shows this text" against "random letters
with corpus frequencies q". Fragment score: line 1 at o, each next line's best
offset d in [W0, W1] letters later (the line width is unknown), summed.

Modes: 'ex' exact spelling; 'sk' drops ו and י (positions where the reading
puts over half its mass on ו/י, and those letters in the corpus).
"""
import json, os, re, collections
import numpy as np
from scipy.ndimage import maximum_filter1d

FIN = str.maketrans('ךםןףץ', 'כמנפצ')
LET = 'אבגדהוזחטיכלמנסעפצקרשת'
IDX = {c: i for i, c in enumerate(LET)}
BAR = len(LET)             # barrier id
EPS = 0.02


def _norm(c):
    return c.translate(FIN)


class LetterLM:
    """Interpolated letter 4-gram model over the 22 letters plus the barrier.

    table[ctx] is the predictive distribution over the 22 letters for each of
    the 23^3 three-symbol contexts (barriers included, so a context resets at
    gaps). Orders 0-3 are interpolated with fixed weights; each order uses
    add-ALPHA smoothing."""
    ALPHA = 0.1
    WEIGHTS = (0.05, 0.15, 0.3, 0.5)

    def __init__(self, ids):
        V, S = len(LET), len(LET) + 1
        x = ids.astype(np.int64)
        c0, c1, c2, c3 = x[3:], x[2:-1], x[1:-2], x[:-3]      # target and 3 previous symbols
        ok = c0 != BAR
        c0, c1, c2, c3 = c0[ok], c1[ok], c2[ok], c3[ok]

        def dist(ctx_id, n_ctx):
            cnt = np.zeros((n_ctx, V))
            np.add.at(cnt, (ctx_id, c0), 1)
            return (cnt + self.ALPHA) / (cnt.sum(1, keepdims=True) + V * self.ALPHA)
        p0 = dist(np.zeros_like(c0), 1)
        p1 = dist(c1, S)
        p2 = dist(c2 * S + c1, S * S)
        p3 = dist((c3 * S + c2) * S + c1, S ** 3)
        a, b, c = np.meshgrid(np.arange(S), np.arange(S), np.arange(S), indexing='ij')   # c3, c2, c1
        a, b, c = a.ravel(), b.ravel(), c.ravel()
        w0, w1, w2, w3 = self.WEIGHTS
        self.table = (w0 * p0[0][None, :] + w1 * p1[c] + w2 * p2[b * S + c] + w3 * p3[(a * S + b) * S + c])
        self.S = S

    def contexts(self, ids):
        S = self.S
        x = np.concatenate([[BAR, BAR, BAR], ids.astype(np.int64)])
        return (x[:-3] * S + x[1:-2]) * S + x[2:-1]


def window_lse(x, size, mx):
    """y[i] = log(sum(exp(x[i:i+size]))) (past the end: exp = 0), computed in blocks
    of `size` with the block-pair maximum as reference; clamped to
    [mx, mx + log(size)] (mx: the window maximum), which also covers
    cancellation in the cumulative sums."""
    n = len(x)
    nb = -(-n // size)
    X = np.full((nb + 1) * size, -np.inf)
    X[:n] = x
    Xr = X.reshape(nb + 1, size)
    R = np.concatenate([Xr[:-1], Xr[1:]], axis=1)             # nb x 2*size
    ref = R.max(1)
    ref = np.where(np.isfinite(ref), ref, 0.0)
    E = np.exp(R - ref[:, None])
    CS = np.concatenate([np.zeros((nb, 1)), np.cumsum(E, axis=1)], axis=1)
    with np.errstate(divide='ignore', invalid='ignore'):
        Y = ref[:, None] + np.log(CS[:, size:2 * size] - CS[:, :size])
    y = Y.reshape(-1)[:n]
    y = np.where(np.isfinite(y), y, -np.inf)
    return np.clip(y, mx, mx + np.log(size))


class Corpus:
    def __init__(self, exclude=(), mode='ex', targum=False, mt=True, keep=None, q=None, bg='unigram', lm=None,
                 local=None, entrap=False):
        """exclude: normalised scroll sigla to leave out (the fragment's own manuscript).
        targum: also search the Aramaic targums (data/ref/targum.json), for Aramaic targets.
        mt: include the Masoretic text (True), none of it (False), or a set of
        book codes ('Gen', 'Ps', ...). keep: optional callable (scroll, fragment) -> bool
        restricting the scroll fragments (a small, targeted corpus). q: letter
        frequencies to use (pass the full corpus's for small corpora).
        bg: background model for the log-likelihood ratio. 'unigram' compares a
        match with random letters of corpus frequency; 'lm' compares it with a
        letter 4-gram model of Hebrew, so that common words earn little and rare
        ones much (real readings consist of real words, which fit any Hebrew
        text better than random letters do). lm: a trained LetterLM to reuse
        (pass the full corpus's for small corpora).
        entrap: also add the entrapment corpus (data/ref/entrap.json: Mishnah and
        Tosefta with shared stretches blanked) as documents 'EN <work>'; the
        letter frequencies q stay those of the reference.
        local: score each reading line by its best contiguous stretch on each
        diagonal (misread letters at the ends of a long line then cost nothing)
        instead of the sum over the whole line."""
        self.mode = mode
        ids, refs, docs = [], [], []

        def add(label, seq):
            # seq: list of (letter, ref); letter None = barrier of unknown
            # length (collapsed), letter '' = one reconstructed letter (one
            # barrier each, so distances across reconstructions are kept)
            for c, r in seq:
                if c == '':
                    ids.append(BAR); refs.append(r); docs.append(label)
                    continue
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
        for b, vs in (by_book.items() if mt else []):
            if mt is not True and b not in mt:
                continue
            add('MT ' + b, [(c, r) for r, t in vs for c in t if c != ' '])
        if targum:
            by_work = collections.defaultdict(list)
            for ref, t in json.load(open('data/ref/targum.json')):
                by_work[ref.rsplit('.', 2)[0]].append((ref, t))
            for w, vs in by_work.items():
                add('TG ' + w, [(c, r) for r, t in vs for c in t if c != ' '])
        n_ref = None
        by_scroll = collections.defaultdict(list)
        for s, f, l, t, m, _ in json.load(open('data/ref/dss_lines.json')):
            by_scroll[s].append((f, l, t, m))
        for s, ls in by_scroll.items():
            if re.sub(r'[\s.^]', '', s).upper() in exclude:
                continue
            seq, last_f = [], None
            for f, l, t, m in ls:
                if keep is not None and not keep(s, f):
                    continue
                if f != last_f:
                    seq.append((None, None))
                    last_f = f
                for c, k in zip(t, m):
                    if k in '.u' and 'א' <= c <= 'ת':
                        seq.append((c, f'{s} {f}:{l}'))
                    elif k == 'r' and not (mode == 'sk' and _norm(c) in 'וי'):
                        seq.append(('', f'{s} {f}:{l}'))
                    elif k in '#p':
                        seq.append((None, None))
            if seq:
                add('DSS ' + s, seq)
        n_ref = len(ids)
        if entrap:
            by_work = collections.defaultdict(list)
            for ref, t in json.load(open('data/ref/entrap.json')):
                by_work[ref.rsplit('.', 2)[0]].append((ref, t))
            for w, vs in by_work.items():
                add('EN ' + w, [(None if c == '|' else c, r) for r, t in vs for c in t if c != ' '])
        self.ids = np.array(ids, np.int8)
        self.refs, self.docs = refs, docs
        ref_ids = self.ids[:n_ref]
        cnt = np.bincount(ref_ids[ref_ids != BAR], minlength=len(LET)).astype(np.float64)
        self.q = q if q is not None else cnt / cnt.sum()
        self.letters = int(cnt.sum())
        self.bg = bg
        # default from the environment so whole pipelines can switch: PMATCH_LOCAL=1
        self.local = (os.environ.get('PMATCH_LOCAL') == '1') if local is None else local
        if bg == 'lm':
            self.lm = lm if lm is not None else LetterLM(self.ids)
            self.ctx = self.lm.contexts(self.ids)

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
            if self.bg == 'lm':
                rows.append(np.concatenate([np.log(p + EPS), [-20.0], p + EPS]))
            else:
                den = float(np.dot(self.q, p + EPS))
                rows.append(np.concatenate([np.log((p + EPS) / den), [-20.0]]))
        width = len(LET) + 1 + (len(LET) if self.bg == 'lm' else 0)
        return np.array(rows) if rows else np.zeros((0, width))

    def _col(self, row, ids):
        """Score of one reading position at every corpus position (ids order)."""
        if self.bg != 'lm':
            return row[ids]
        num = row[:len(LET) + 1][ids]
        v = self.lm.table @ row[len(LET) + 1:]          # expected P(reading) per context
        ctx = self.ctx if ids is self._ids64 else self.ctx[::-1]
        col = num - np.log(v[ctx])
        col[ids == BAR] = -20.0
        return col

    def line_scores(self, table):
        n = len(self.ids)
        L = len(table)
        if L == 0:
            return None
        s = np.zeros(n, np.float32)
        ids = self._ids64 = getattr(self, '_ids64', None) if getattr(self, '_ids64', None) is not None else self.ids.astype(np.int64)
        if self.local:
            # Kadane along each diagonal: E_i[o] = max(E_{i-1}[o], 0) + col_i[o+i]
            best = np.full(n, -1e9, np.float32)
            E = np.zeros(n, np.float32)
            for i in range(min(L, n)):
                col = self._col(table[i], ids)
                v = np.full(n, -1e9, np.float32)
                v[:n - i] = col[i:]
                E = np.maximum(E, 0) + v
                best = np.maximum(best, E)
            return best
        for i in range(L):
            if i >= n:                       # line longer than a tiny corpus
                s[:] = -1e9
                break
            col = self._col(table[i], ids)
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
            s = self._col(table[i], ids).astype(np.float32)
            cand = np.maximum(np.float32(0), shift(prev, 1))
            cand = np.maximum(cand, shift(prev, 2) - gap)
            cand = np.maximum(cand, shift(prev2, 1) - gap)
            cur = s + cand
            best = np.maximum(best, cur)
            prev2, prev = prev, cur
        return best[::-1].copy()                      # index = start position in the corpus

    def search(self, lines, W=(15, 140), top=5, min_letters=1, gapped=False):
        """lines: list of lists of distributions (top to bottom).
        Returns the top hits [(score, doc, ref, offset)], best first."""
        acc = self.score_array(lines, W, min_letters, gapped)
        if acc is None:
            return None
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

    def doc_max(self, acc):
        """Best score inside each document (self.doc_names order)."""
        if not hasattr(self, 'doc_start'):
            starts = [0] + [i for i in range(1, len(self.docs)) if self.docs[i] != self.docs[i - 1]]
            self.doc_start = np.array(starts)
            self.doc_names = [self.docs[i] for i in starts]
        return np.maximum.reduceat(acc, self.doc_start)

    def score_array(self, lines, W=(15, 140), min_letters=1, gapped=False, mask=None, forward=False):
        """Fragment score at every corpus offset (line 1 start), or None.
        mask: optional boolean array over corpus positions to leave out (e.g. the
        piece's own manuscript). Every line scores 0 there, before chaining, so a
        chain that starts elsewhere cannot reach the masked text through a later
        line; start offsets inside the mask get -inf.
        forward: sum over line spacings instead of taking the best one: the next
        line contributes log(mean over the W window of exp(score)) (a uniform
        prior over spacings), so the chained score stays a likelihood ratio with
        mean 1 and the spacing multiplicity drops out of ln N."""
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
            if mask is not None:
                s[mask] = 0.0
            if acc is not None:
                # lines that would fall past the end of the reference count
                # as skipped (0), like any other unplaceable line
                mx = maximum_filter1d(acc, size=size, origin=-(size // 2), mode='constant', cval=0.0)
                if forward:
                    mx = window_lse(acc, size, mx) - np.log(size)
                nxt = np.zeros_like(s)
                if len(s) > W[0]:
                    nxt[:len(s) - W[0]] = mx[W[0]:]
                s = s + nxt
            acc = s
        if mask is not None:
            acc[mask] = -1e9
        return acc
