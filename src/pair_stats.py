"""M1: agreement between ink on the image and letters in the transcription.

Reads data/m1/pairs.json and data/m1/ink_features.json, writes flags back into
data/m1/pairs.json (field 'ink') and adds an 'ink_check' section to
reports/M1_summary.json.
"""
import json, re, collections
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

    def assembly(label):
        # plain column numbers ('2', '6a') and joins ('f10_13', 'f3i+17') are
        # editorial assemblies of several pieces
        return bool(re.fullmatch(r'\d+[a-z]?', label) or re.search(r'[_+]', label))

    for r in rows:
        f = dict(ink[r['name']])
        f['assembly'] = any(assembly(x['etcbc'][1]) for x in r['links'])
        f['density'] = r['preserved'] / (f['parch'] / 1e6) if f['parch'] else None
        r['ink'] = f
    # letters per megapixel of parchment: calibrate on single-piece labels whose
    # ink agrees with the letter count, then allow 3x the 95th percentile
    ref = [r['ink']['density'] for r in rows if not r['ink']['assembly'] and r['preserved'] >= 10
           and r['ink']['density'] and 0.1 <= r['ink']['blobs'] / r['preserved'] <= 2]
    dmax = 3 * float(np.percentile(ref, 95))
    for r in rows:
        f = r['ink']
        if f['parch'] < 1e4 and r['preserved'] > 0:
            f['flag'] = 'no_parchment_found'
        elif f['density'] and f['density'] > dmax:
            f['flag'] = 'too_many_letters_for_area'
        elif r['preserved'] >= 20 and f['blobs'] < 0.1 * r['preserved']:
            f['flag'] = 'letters_without_ink'
        elif f['blobs'] >= 60 and r['preserved'] <= 3:
            f['flag'] = 'ink_without_letters'
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
        ok = [r for r in rs if not r['ink'].get('flag')]
        out[key] = dict(n=len(rs), spearman=round(spearman(p, b), 3),
                        spearman_unflagged=round(spearman([r['preserved'] for r in ok], [r['ink']['blobs'] for r in ok]), 3) if len(ok) > 10 else None,
                        clean=len(ok), clean_letters=sum(r['preserved'] for r in ok),
                        blobs_per_letter_median=round(float(np.median(b[p >= 10] / p[p >= 10])), 2) if (p >= 10).any() else None,
                        flags={k: v for k, v in flags.items() if k})
    summ = json.load(open('reports/M1_summary.json'))
    out['density_limit_letters_per_mpx'] = round(dmax, 1)
    out['density_ref_median'] = round(float(np.median(ref)), 1)
    summ['ink_check'] = out
    json.dump(summ, open('reports/M1_summary.json', 'w'), indent=1)
    print(json.dumps(out, indent=1))
    worst = sorted((r for r in rows if r['ink'].get('flag')), key=lambda r: -r['preserved'])
    for r in worst[:15]:
        print(r['name'], r['manuscript'], r['links'][0]['etcbc'], r['preserved'], r['ink'])
