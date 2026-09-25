"""Idea 5 scoping: variant readings of the biblical scrolls against the MT.

For every ETCBC biblical scroll word with a book/chapter/verse, the scroll's
verse text is aligned word by word to the Leningrad Codex verse (WLC,
data/ref/bible.json). Orthographic words are rebuilt from ETCBC word nodes
with the `after` feature (ETCBC splits prefixes). Only fully preserved scroll
words take part (no reconstructed or uncertain sign). Each aligned pair is:
  same         identical consonants (final forms folded)
  orthographic identical once ו, י and א are removed (plene / defective)
  long_form    identical once the long suffixes of Qumran scribal practice
               (-כה, -תה, -מה) are also folded
  substantive  anything else (another word, another form, a different prefix)
Unaligned scroll words (pluses) are counted apart; MT words facing a scroll
lacuna are not scored.

Per manuscript: words compared, plene-spelling rate, substantive rate.
Agreement pattern: two manuscripts that preserve the same MT word both
diverge from the MT the same way (identical after the orthographic fold) =
a shared non-MT reading. Pairs of manuscripts are ranked by shared
substantive non-MT readings, against the number of MT words they both
preserve.

No Septuagint or Samaritan text is in reach, so readings can only be typed
as MT / non-MT, and clustering rests on shared non-MT readings. Treat every
item as a lead: some 'variants' are ETCBC transcription choices or
alignment slips.

Usage: python3 src/variants.py
Outputs: data/variants/words.json, reports/M9_variants.json
"""
import json, os, re, sys, collections, itertools
import numpy as np
from tf.fabric import Fabric

TFDIR = 'data/dss/tf/2.0.1'
HEB = re.compile(r'[א-ת]')
FIN = str.maketrans('ךםןףץ', 'כמנפצ')


BOOKFIX = {'Is': 'Isa', 'Ex': 'Exod'}      # ETCBC acronyms that differ from WLC


def fold(w):
    return w.translate(FIN)


def ortho(w):
    return re.sub('[ויא]', '', fold(w))


def qsp(w):
    """Also fold the long forms of Qumran scribal practice: -כה, -תה, -מה, -הא."""
    w = ortho(w)
    return re.sub('(?<=[כתמ])ה$', '', w)


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def align(sw, mw):
    """Global word alignment. sw: scroll words (text or None for lacuna),
    mw: MT words. Returns list of (i or None, j or None)."""
    n, m = len(sw), len(mw)
    D = np.zeros((n + 1, m + 1))
    B = np.zeros((n + 1, m + 1), int)
    D[1:, 0] = np.arange(1, n + 1)
    D[0, 1:] = np.arange(1, m + 1) * 0.6
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            a, b = sw[i - 1], mw[j - 1]
            if a is None:                              # lacuna: matches any MT word cheaply
                sub = 0.3
            else:
                x, y = ortho(a), ortho(b)
                sub = 0.0 if x == y else min(1.2, lev(fold(a), fold(b)) / max(len(a), len(b), 1) * 1.6)
            opts = (D[i - 1, j - 1] + sub, D[i - 1, j] + 1.0, D[i, j - 1] + 0.6)
            k = int(np.argmin(opts))
            D[i, j], B[i, j] = opts[k], k
    out, i, j = [], n, m
    while i > 0 or j > 0:
        k = B[i, j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if k == 0:
            out.append((i - 1, j - 1)); i -= 1; j -= 1
        elif k == 1:
            out.append((i - 1, None)); i -= 1
        else:
            out.append((None, j - 1)); j -= 1
    return out[::-1]


def main():
    os.makedirs('data/variants', exist_ok=True)
    api = Fabric(locations=TFDIR, silent='deep').load(
        'otype scroll book chapter verse glyph rec unc after script biblical', silent='deep')
    F, L = api.F, api.L
    bible = {k: v.replace('־', ' ').split() for k, v in json.load(open('data/ref/bible.json'))}
    # scroll verse texts: list of orthographic words (text, preserved) per (scroll, ref)
    verses = collections.defaultdict(list)
    for sc in F.otype.s('scroll'):
        scroll = F.scroll.v(sc)
        cur, ok, ref = '', True, None
        for w in L.d(sc, 'word'):
            b, c, v = F.book.v(w), F.chapter.v(w), F.verse.v(w)
            if not (b and c and v):
                cur, ok = '', True
                continue
            r = f'{BOOKFIX.get(b, b)}.{c}.{v}'
            if r != ref and cur:
                verses[(scroll, ref)].append((cur, ok))
                cur, ok = '', True
            ref = r
            for s in L.d(w, 'sign'):
                g = F.glyph.v(s) or ''
                if not HEB.search(g):
                    continue
                if F.rec.v(s) or F.unc.v(s) or F.script.v(s):
                    ok = False
                cur += ''.join(HEB.findall(g))
            aft = F.after.v(w) or ''
            if aft.strip('\u05be') != '' or '\u05be' in aft:   # word end (space, punctuation, maqaf)
                if cur:
                    verses[(scroll, ref)].append((cur, ok))
                cur, ok = '', True
        if cur and ref:
            verses[(scroll, ref)].append((cur, ok))
    print(len(verses), 'scroll verses', file=sys.stderr, flush=True)

    words = []
    miss = collections.Counter()
    for (scroll, ref), sw in verses.items():
        mw = bible.get(ref)
        if not mw:
            miss[ref.split('.')[0]] += 1           # unplaced pieces carry the scroll name as book
            continue
        # fully reconstructed words behave as lacunae
        seq = [t if ok else None for t, ok in sw]
        if not any(seq):
            continue
        for i, j in align(seq, mw):
            if i is None or seq[i] is None:
                continue
            s = seq[i]
            if j is None:
                words.append(dict(scroll=scroll, ref=ref, j=None, scroll_word=s, mt='', kind='plus'))
                continue
            m = mw[j]
            kind = ('same' if fold(s) == fold(m) else 'orthographic' if ortho(s) == ortho(m)
                    else 'long_form' if qsp(s) == qsp(m) else 'substantive')
            words.append(dict(scroll=scroll, ref=ref, j=j, scroll_word=s, mt=m, kind=kind,
                              plene=len(s) - len(m) if kind == 'orthographic' else 0))
    json.dump(words, open('data/variants/words.json', 'w'), ensure_ascii=False)

    per = collections.defaultdict(collections.Counter)
    for w in words:
        per[w['scroll']][w['kind']] += 1
        if w['kind'] == 'orthographic':
            per[w['scroll']]['fuller' if w['plene'] > 0 else 'shorter' if w['plene'] < 0 else 'other_ortho'] += 1
    prof = []
    for sc, c in per.items():
        n = c['same'] + c['orthographic'] + c['long_form'] + c['substantive']
        if n < 50:
            continue
        prof.append(dict(scroll=sc, words=n, same=round(c['same'] / n, 3),
                         fuller=round(c['fuller'] / n, 3), shorter=round(c['shorter'] / n, 3),
                         long_form=round(c['long_form'] / n, 3),
                         substantive=round(c['substantive'] / n, 3), pluses=c['plus']))
    prof.sort(key=lambda r: -r['substantive'])

    # shared non-MT readings
    at = collections.defaultdict(dict)            # (ref, j) -> scroll -> (kind, orthographic form)
    for w in words:
        if w['j'] is not None:
            at[(w['ref'], w['j'])][w['scroll']] = (w['kind'], ortho(w['scroll_word']))
    both = collections.Counter()
    shared = collections.Counter()
    examples = collections.defaultdict(list)
    for key, d in at.items():
        for a, b in itertools.combinations(sorted(d), 2):
            both[(a, b)] += 1
            ka, fa = d[a]
            kb, fb = d[b]
            if ka == kb == 'substantive' and qsp(fa) == qsp(fb):
                shared[(a, b)] += 1
                if len(examples[(a, b)]) < 4:
                    examples[(a, b)].append(f"{key[0]} w{key[1] + 1}")
    pairs = [dict(a=a, b=b, overlap=both[(a, b)], shared_substantive=k,
                  rate=round(k / both[(a, b)], 3), examples=examples[(a, b)])
             for (a, b), k in shared.items() if k >= 2]
    pairs.sort(key=lambda r: (-r['shared_substantive'], -r['rate']))

    tot = collections.Counter(w['kind'] for w in words)
    out = dict(scroll_verses=len(verses), verses_not_in_mt=sum(miss.values()), not_in_mt_by_book=dict(miss.most_common(8)), words=dict(tot),
               manuscripts_profiled=len(prof),
               substantive_rate_median=float(np.median([p['substantive'] for p in prof])) if prof else None,
               fuller_rate_median=float(np.median([p['fuller'] for p in prof])) if prof else None,
               most_divergent=prof[:15], least_divergent=sorted(prof, key=lambda r: r['substantive'])[:10],
               fullest_spelling=sorted(prof, key=lambda r: -r['fuller'])[:10],
               shared_pairs=pairs[:25], n_pairs_ge2=len(pairs))
    json.dump(out, open('reports/M9_variants.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('shared_pairs',)}, ensure_ascii=False, indent=1)[:4000])
    print(json.dumps(pairs[:12], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
