"""M2 batch: preprocess the clean one-to-one pairs and compare line counts.

Usage: python3 src/prep_batch.py [parchment|papyrus|all]
Writes data/m2/{raw,crop,ink,seg}/ and data/m2/batch_{set}.json, and prints
line-count agreement against the transcription.
"""
import json, os, re, sys, collections
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(__file__))
import prep  # noqa: E402

D2 = 'data/m2'


def lnum(label):
    m = re.match(r'(\d+)', label)
    return int(m.group(1)) if m else None


def expected_lines(lines):
    """Transcription lines that show preserved letters, and their physical span."""
    vis = [l for l in lines if any(c in '.u' for c in l['marks'])]
    nums = [lnum(l['line']) for l in vis if lnum(l['line']) is not None]
    span = (max(nums) - min(nums) + 1) if nums else len(vis)
    return len(vis), span


def work(job):
    name, url = job
    seg = f'{D2}/seg/{name}.json'
    if os.path.exists(seg):
        return json.load(open(seg))
    try:
        return prep.process(name, url)
    except Exception as e:
        return dict(name=name, error=f'{type(e).__name__}: {e}')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'parchment'
    pairs = json.load(open('data/m1/pairs.json'))
    urls = {x['name']: x['url'] for x in json.load(open('data/m0/inventory_images.json'))}
    sel = [r for r in pairs if r['split'] == 'train' and r['category'] == 'one_to_one'
           and r['side'] == 'Recto' and 'ink' in r and not r['ink'].get('flag')
           and (which == 'all' or r['material'].lower() == which)]
    print(len(sel), 'images', file=sys.stderr)
    with Pool(4) as pool:
        res = {}
        for k, r in enumerate(pool.imap_unordered(work, [(r['name'], urls[r['name']]) for r in sel], 4)):
            res[r['name']] = r
            if k % 250 == 249:
                print(k + 1, file=sys.stderr)
    out = []
    for r in sel:
        s = res[r['name']]
        lines = list(r['lines'].values())[0]
        n_vis, span = expected_lines(lines)
        out.append(dict(name=r['name'], manuscript=r['manuscript'], preserved=r['preserved'],
                        period=r['period'], expected=n_vis, span=span,
                        detected=len(s.get('lines', [])) if 'error' not in s else None,
                        pitch=s.get('pitch'), angle=s.get('angle'), error=s.get('error')))
    json.dump(out, open(f'{D2}/batch_{which}.json', 'w'))
    ok = [o for o in out if o['detected'] is not None]
    c = collections.Counter()
    for o in ok:
        d = o['detected'] - o['expected']
        c['exact'] += d == 0
        c['within1'] += abs(d) <= 1
        c['exact_span'] += o['detected'] == o['span']
        c['within1_span'] += abs(o['detected'] - o['span']) <= 1
        c['more'] += d > 1
        c['fewer'] += d < -1
    print(json.dumps(dict(images=len(out), processed=len(ok), errors=len(out) - len(ok),
                          **{k: round(v / max(len(ok), 1), 3) for k, v in c.items()}), indent=1))
