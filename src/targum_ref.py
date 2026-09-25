"""Aramaic reference text for the matcher: targums from the Sefaria export.

Downloads json/Tanakh/Targum/**/Hebrew/merged.json (Aramaic text; Sefaria files
it under "Hebrew") for every targum except Tafsir Rasag (Judeo-Arabic), keeps
consonants only, and writes
  data/ref/targum.json          [[ref, consonantal text], ...]  ref = 'Work.ch.v'
  data/ref/targum_sources.json  per work: versionTitle, versionSource, license
Local only; read the licences in targum_sources.json before any reuse.
"""
import json, os, re, urllib.request, urllib.parse

B = 'https://storage.googleapis.com/sefaria-export/'
HEB = re.compile(r'[א-ת]+')


def flatten(node, path=()):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, list):
        for i, x in enumerate(node, 1):
            yield from flatten(x, path + (i,))


if __name__ == '__main__':
    keys = [k for k in json.load(open('data/ref/targum/keys.json')) if 'Tafsir Rasag' not in k]
    out, src = [], {}
    for k in keys:
        work = k.split('/')[-3]
        path = f'data/ref/targum/{work}.json'
        if not os.path.exists(path):
            data = urllib.request.urlopen(B + urllib.parse.quote(k), timeout=120).read()
            open(path, 'wb').write(data)
        d = json.load(open(path))
        src[work] = {x: d.get(x) for x in ('versionTitle', 'versionSource', 'license', 'versions') if x in d}
        n = 0
        for p, s in flatten(d.get('text', [])):
            s = re.sub(r'<[^>]+>', ' ', s)                   # markup
            s = s.replace('\u05be', ' ')                       # maqaf
            s = re.sub(r'[\u0591-\u05c7]', '', s)             # points and accents
            t = ' '.join(HEB.findall(s))
            if t:
                out.append([f'{work}.' + '.'.join(map(str, p)), t])
                n += len(t.replace(' ', ''))
        print(f'{work}: {n} letters')
    json.dump(out, open('data/ref/targum.json', 'w'), ensure_ascii=False)
    json.dump(src, open('data/ref/targum_sources.json', 'w'), ensure_ascii=False, indent=1)
    print(len(out), 'segments,', sum(len(t.replace(' ', '')) for _, t in out), 'letters')
