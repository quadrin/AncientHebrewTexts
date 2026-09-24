"""M0: harvest Leon Levy metadata (no images).

Writes data/m0/ll_manuscripts.json (all square-script manuscripts) and
data/m0/ll_ir_images.json (all infrared image records). Both are cached;
delete the file to refetch.
"""
import json, os, sys, time, urllib.request, urllib.parse
from concurrent.futures import ThreadPoolExecutor

OUT = 'data/m0'
API = 'https://www.deadseascrolls.org.il/api/search?'


def q(t, query, p=1, tries=5):
    u = API + urllib.parse.urlencode({'t': t, 'q': query, 'p': p})
    for k in range(tries):
        try:
            r = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
            return json.load(urllib.request.urlopen(r, timeout=60))
        except Exception as e:
            if k == tries - 1:
                raise
            time.sleep(2 ** k)


def harvest(t, query, path, workers=8):
    if os.path.exists(path):
        return json.load(open(path))
    first = q(t, query)
    pages = int(first['totalpages'])
    print(f'{t} {query}: {first["length"]} records, {pages} pages', file=sys.stderr)
    with ThreadPoolExecutor(workers) as ex:
        rest = list(ex.map(lambda p: q(t, query, p)['results'], range(2, pages + 1)))
    recs = first['results'] + [r for page in rest for r in page]
    # pages are sorted, but de-duplicate defensively
    key = 'manuscript_id' if t == 'manuscript' else 'name'
    recs = list({r[key]: r for r in recs}.values())
    if len(recs) != first['length']:
        print(f'  warning: got {len(recs)} unique of {first["length"]}', file=sys.stderr)
    json.dump(recs, open(path, 'w'), ensure_ascii=False)
    return recs


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    ms = harvest('manuscript', "script_type:'Square'", f'{OUT}/ll_manuscripts.json')
    ims = harvest('image', "photo_type:'Infrared Image'", f'{OUT}/ll_ir_images.json')
    print(len(ms), 'manuscripts;', len(ims), 'infrared images')
