"""M0: harvest SQE editions, text fragments and imaged-object matches.

Writes data/m0/sqe_editions.json, data/m0/sqe_text_fragments.json and
data/m0/sqe_matches.json. Cached; delete a file to refetch.
"""
import json, os, sys, time, urllib.request
from concurrent.futures import ThreadPoolExecutor

OUT = 'data/m0'
API = 'https://sqe-api.deadseascrolls.org.il/v1'


def get(path, tries=5):
    for k in range(tries):
        try:
            return json.load(urllib.request.urlopen(API + path, timeout=120))
        except Exception:
            if k == tries - 1:
                raise
            time.sleep(2 ** k)


def cached(path, fn):
    if os.path.exists(path):
        return json.load(open(path))
    d = fn()
    json.dump(d, open(path, 'w'), ensure_ascii=False)
    return d


def per_edition(eds, fn, workers=8):
    def one(e):
        try:
            return e['id'], fn(e['id'])
        except Exception as ex:
            print('  failed', e['id'], e['name'], ex, file=sys.stderr)
            return e['id'], None
    with ThreadPoolExecutor(workers) as ex:
        return dict(ex.map(one, eds))


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)

    def editions():
        eds = [e for grp in get('/editions')['editions'] for e in grp]
        return [dict(id=e['id'], name=e['name'], manuscriptId=e['manuscriptId'],
                     isPublic=e['isPublic'], copyright=e.get('copyright'))
                for e in eds]
    eds = cached(f'{OUT}/sqe_editions.json', editions)
    print(len(eds), 'editions', file=sys.stderr)

    tfs = cached(f'{OUT}/sqe_text_fragments.json', lambda: per_edition(
        eds, lambda i: get(f'/editions/{i}/text-fragments')['textFragments']))

    def matches():
        m = per_edition(eds, lambda i: get(
            f'/catalogue/editions/{i}/imaged-object-text-fragment-matches')['matches'])
        # drop the repeated licence text; keep one copy
        lic = next((r['license'] for v in m.values() if v for r in v), None)
        for v in m.values():
            for r in v or []:
                r.pop('license', None)
        return {'license': lic, 'matches': m}
    ms = cached(f'{OUT}/sqe_matches.json', matches)
    n_tf = sum(len(v or []) for v in tfs.values())
    n_m = sum(len(v or []) for v in ms['matches'].values())
    print(len(eds), 'editions;', n_tf, 'text fragments;', n_m, 'image matches')
