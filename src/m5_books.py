"""M5, second measure: for the biblical test manuscripts, does the top hit land
in the manuscript's own book? This does not depend on a transcription parallel
of >= 10 letters, so it covers small fragments too.

Chance level for a book = its share of the letters in the MT reference (a
random placement lands there that often). Thresholds: 1% of the shuffled
controls, per band of read letters.
Usage: python3 src/m5_books.py data/m5/results_runX.json
"""
import json, sys, collections
import numpy as np

BOOKS = {'Leviticus': ['Lev'], 'Genesis': ['Gen'], 'Exodus': ['Exod'], 'Deuteronomy': ['Deut'],
         'Judges': ['Judg'], 'Kings': ['1Kgs', '2Kgs'], 'Isaiah': ['Isa'], 'Jeremiah': ['Jer'],
         'Minor Prophets': ['Hos', 'Joel', 'Amos', 'Obad', 'Jonah', 'Mic', 'Nah', 'Hab', 'Zeph', 'Hag', 'Zech', 'Mal'],
         'Psalms': ['Ps']}
RB = [(1, 9), (10, 19), (20, 39), (40, 10 ** 6)]


def main(path):
    R = json.load(open(path))
    ll = {m['manuscript_number']: m for m in json.load(open('data/m0/ll_manuscripts.json'))}
    bible = json.load(open('data/ref/bible.json'))
    size = collections.Counter()
    for ref, t in bible:
        size[ref.split('.')[0]] += len(t.replace(' ', ''))
    total = sum(size.values())
    out = {}
    for mode in ('ex', 'sk'):
        rows = []
        for lo, hi in RB:
            rs = [r for r in R if lo <= r['read_letters'] <= hi]
            null = np.array([x for r in rs for x in r[mode]['null'] if x is not None])
            t = float(np.quantile(null, 0.99)) if len(null) >= 20 else None
            bib = [r for r in rs if ll.get(r['manuscript'], {}).get('composition_name') in BOOKS]
            n = own = over = own_over = 0
            chance = []
            for r in bib:
                books = BOOKS[ll[r['manuscript']]['composition_name']]
                chance.append(sum(size[b] for b in books) / total)
                h = r[mode]['hits']
                if not h:
                    continue
                n += 1
                hit_book = h[0][2].split('.')[0] if h[0][1].startswith('MT') else None
                ok = hit_book in books
                own += ok
                if t is not None and h[0][0] >= t:
                    over += 1
                    own_over += ok
            rows.append(dict(read_letters=f'{lo}-{hi if hi < 10**6 else "+"}', images=len(bib), threshold=round(t, 1) if t else None,
                             top1_own_book=own, chance_own_book=round(float(np.mean(chance)) if chance else 0, 3),
                             over_threshold=over, over_threshold_own_book=own_over))
        out[mode] = rows
        print('== mode', mode)
        for r in rows:
            print(r)
    return out


if __name__ == '__main__':
    res = {p: main(p) for p in sys.argv[1:]}
    json.dump(res, open('reports/M5_books.json', 'w'), indent=1)
