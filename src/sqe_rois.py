"""E2 step 1a: harvest the public SQE sign ROIs (letter polygons on IAA images).

/editions/{id}/artefacts/{aid}/rois returns nothing; the ROIs are in
/editions/{id}/script-lines (every placed sign with its polygon). The
polygons are in the frame of the artefact's image (SQE master images,
7216 x 5412 at 1,215 ppi). Only ROIs on artefacts of the edition that sit on
an IAA imaged object are kept (the Cairo Damascus Document and 4Q54's
virtual line strips are dropped).

Local data only (image coordinates of IAA photos; no images are fetched here).
Usage: python3 src/sqe_rois.py
Output: data/sqe_rois/rois.json, data/sqe_rois/summary.json
"""
import json, os, re, sys, collections
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(__file__))
from sqe_harvest import get  # noqa: E402

OUT = 'data/sqe_rois'


def poly(wkt):
    nums = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?', wkt)]
    pts = list(zip(nums[0::2], nums[1::2]))
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return pts, [min(xs), min(ys), max(xs), max(ys)]


def one(e):
    path = f'{OUT}/sl/{e["id"]}.json'
    if os.path.exists(path):
        return e, json.load(open(path))
    sl = get(f'/editions/{e["id"]}/script-lines')
    rows = []
    if 'interpretationRoiId' in json.dumps(sl):
        arts = {str(a['id']): a for a in get(f'/editions/{e["id"]}/artefacts')['artefacts']}
        for tf in sl['textFragments']:
            for ln in tf['lines']:
                for ar in ln['artefacts']:
                    for ch in ar['characters']:
                        # script-lines gives attributes as one string, e.g. 'sign_type_LETTER'
                        attrs = {a.get('attributeValueString') or '' for a in ch.get('attributes') or []}
                        for r in ch.get('rois') or []:
                            a = arts.get(str(r['artefactId']))
                            if not a or not a.get('imagedObjectId'):
                                continue
                            pts, bb = poly(r['shape'])
                            rows.append(dict(edition=e['name'], edition_id=e['id'], text_fragment=tf['textFragmentName'],
                                             line=ln['lineName'], sign=ch['signInterpretationId'],
                                             char=ch.get('character') or '',
                                             letter='sign_type_LETTER' in attrs,
                                             reconstructed='is_reconstructed_TRUE' in attrs,
                                             readability=next((v[len('readability_'):] for v in attrs
                                                               if v.startswith('readability_')), None),
                                             attrs=sorted(attrs),
                                             imaged_object=a['imagedObjectId'], side=a['side'], image_id=a.get('imageId'),
                                             artefact=a['id'], artefact_name=a.get('name'),
                                             rotation=r.get('stanceRotation'), bbox=bb, n_pts=len(pts),
                                             shape=r['shape']))
    os.makedirs(f'{OUT}/sl', exist_ok=True)
    json.dump(rows, open(path, 'w'), ensure_ascii=False)
    return e, rows


def main():
    os.makedirs(OUT, exist_ok=True)
    eds = json.load(open('data/m0/sqe_editions.json'))
    rows = []
    with ThreadPoolExecutor(6) as ex:
        for k, (e, r) in enumerate(ex.map(one, eds)):
            rows += r
            if k % 200 == 199:
                print(k + 1, 'editions', len(rows), 'ROIs', file=sys.stderr, flush=True)
    json.dump(rows, open(f'{OUT}/rois.json', 'w'), ensure_ascii=False)
    letters = {r['sign'] for r in rows if r['letter']}
    by_ed = collections.Counter(r['edition'] for r in rows if r['letter'])
    summ = dict(rois=len(rows), letters=len(letters), editions=len(by_ed),
                imaged_objects=len({r['imaged_object'] for r in rows}),
                lines=len({(r['edition'], r['text_fragment'], r['line']) for r in rows}),
                reconstructed=sum(r['reconstructed'] for r in rows),
                top_editions=by_ed.most_common(15))
    json.dump(summ, open(f'{OUT}/summary.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(summ, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
