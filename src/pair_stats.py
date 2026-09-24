"""M1: agreement between ink on the image and letters in the transcription.

Reads data/m1/pairs.json and data/m1/ink_features.json, writes flags back into
data/m1/pairs.json (field 'ink') and adds an 'ink_check' section to
reports/M1_summary.json.
"""
import json, collections
import numpy as np

D1 = 'data/m1'


def spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra, rb)[0, 1])


if __name__ == '__main__':
    pairs = json.load(open(f'{D1}/pairs.json'))
    ink = json.load(open(f'{D1}/ink_features.json'))
    rows = [r for r in pairs if r['name'] in ink and 'error' not in ink[r['name']]]
    for r in rows:
        f = ink[r['name']]
        r['ink'] = f
        # letters written on this piece: preserved (+ uncertain) letters
        if r['preserved'] >= 20 and f['blobs'] < 0.1 * r['preserved']:
            r['ink']['flag'] = 'letters_without_ink'
        elif f['blobs'] >= 60 and r['preserved'] <= 3:
            r['ink']['flag'] = 'ink_without_letters'
    json.dump(pairs, open(f'{D1}/pairs.json', 'w'), ensure_ascii=False)

    out = {}
    for key, sel in [('all', lambda r: True),
                     ('recto', lambda r: r['side'] == 'Recto'),
                     ('recto_parchment', lambda r: r['side'] == 'Recto' and r['material'] == 'Parchment'),
                     ('recto_papyrus', lambda r: r['side'] == 'Recto' and r['material'] == 'Papyrus'),
                     ('catalogue_exact', lambda r: r['links'][0]['source'] == 'catalogue' and r['links'][0]['link'] == 'exact'),
                     ('artefact', lambda r: r['links'][0]['source'] == 'artefact'),
                     ('subsiglum', lambda r: r['links'][0]['link'] == 'subsiglum'),
                     ('verso', lambda r: r['side'] == 'Verso')]:
        rs = [r for r in rows if sel(r)]
        if len(rs) < 10:
            continue
        p = np.array([r['preserved'] for r in rs])
        b = np.array([r['ink']['blobs'] for r in rs])
        flags = collections.Counter(r['ink'].get('flag') for r in rs)
        out[key] = dict(n=len(rs), spearman=round(spearman(p, b), 3),
                        blobs_per_letter_median=round(float(np.median(b[p >= 10] / p[p >= 10])), 2) if (p >= 10).any() else None,
                        letters_without_ink=flags['letters_without_ink'],
                        ink_without_letters=flags['ink_without_letters'])
    summ = json.load(open('reports/M1_summary.json'))
    summ['ink_check'] = out
    json.dump(summ, open('reports/M1_summary.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))
    worst = sorted((r for r in rows if r['ink'].get('flag')), key=lambda r: -r['preserved'])
    for r in worst[:15]:
        print(r['name'], r['manuscript'], r['links'][0]['etcbc'], r['preserved'], r['ink'])
