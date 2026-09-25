"""Manuscript-level parallel test, for choosing decoys (E4 step 1).

A decoy must be a real reading of a text with no known parallel. Testing only
the fragment a photo is linked to lets true parallels in (catalogue links to
the wrong fragment; reworked or quoting texts whose composition name hides
the source). Here every ETCBC scroll is tested as a whole: all its preserved
letters, skeleton form (ו and י removed, final forms folded), cut into
K-letter shingles; a shingle is 'shared' when it occurs in any other document
of the reference (MT or another scroll). Consecutive shared shingles merge
into stretches. Per scroll: the longest shared stretch (skeleton letters),
the share of shingles shared, and the documents behind the longest stretch.

Usage: python3 src/ms_parallel.py
Output: data/m5/ms_parallel.json
"""
import json, os, sys, collections
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402

K = 10
FIN = str.maketrans('ךםןףץ', 'כמנפצ')


def skel(s):
    return s.translate(FIN).replace('ו', '').replace('י', '')


def main():
    c = pmatch.Corpus(mode='sk')
    rev = {i: ch for ch, i in pmatch.IDX.items()}
    text = ''.join(rev.get(int(i), '|') for i in c.ids)
    docs = c.docs
    # shingle -> set of documents (capped)
    where = collections.defaultdict(set)
    for p in range(len(text) - K + 1):
        g = text[p:p + K]
        if '|' in g:
            continue
        s = where[g]
        if len(s) < 6:
            s.add(docs[p])
    print(len(where), 'shingles', file=sys.stderr, flush=True)
    lines = collections.defaultdict(list)
    for s_, f, l, t, m in json.load(open('data/m0/etcbc_lines.json')):
        lines[s_].append((t, m))
    out = {}
    for scroll, ls in lines.items():
        own = 'DSS ' + scroll
        runs = []
        for t, m in ls:
            cur = ''
            for ch, k in zip(t, m):
                if k in '.u' and 'א' <= ch <= 'ת':
                    cur += ch
                elif k != ' ':
                    if cur:
                        runs.append(skel(cur))
                    cur = ''
            if cur:
                runs.append(skel(cur))
        n_sh = n_shared = 0
        best, best_docs = 0, []
        for r in runs:
            flags = []
            for p in range(len(r) - K + 1):
                d = where.get(r[p:p + K], set()) - {own}
                flags.append(d)
            n_sh += len(flags)
            n_shared += sum(1 for d in flags if d)
            # merge consecutive shared shingles into stretches
            p = 0
            while p < len(flags):
                if flags[p]:
                    q = p
                    ds = set(flags[p])
                    while q + 1 < len(flags) and flags[q + 1]:
                        q += 1
                        ds |= flags[q]
                    length = q - p + K
                    if length > best:
                        best, best_docs = length, sorted(ds)[:6]
                    p = q + 1
                else:
                    p += 1
        out[scroll] = dict(shingles=n_sh, shared=n_shared, share=round(n_shared / n_sh, 4) if n_sh else 0,
                           longest=best, docs=best_docs)
    json.dump(out, open('data/m5/ms_parallel.json', 'w'), ensure_ascii=False, indent=0)
    L = np.array([v['longest'] for v in out.values() if v['shingles'] >= 20])
    print(len(out), 'scrolls; longest shared stretch percentiles (10,25,50,75,90):',
          np.percentile(L, [10, 25, 50, 75, 90]), file=sys.stderr)


if __name__ == '__main__':
    main()
