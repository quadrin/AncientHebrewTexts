"""E4 step 8: entrapment corpus. Later rabbinic Hebrew that cannot be the source
of a Qumran fragment: Mishnah (Sefaria, 63 tractates) and Tosefta (Vilna
edition, Sefaria). Every stretch that shares a 10-letter skeleton shingle
(ו/י removed) with the reference (MT + ETCBC scrolls) is blanked (biblical
quotations and stock phrases), so a hit in this corpus cannot be a real
parallel. The matcher's hits in it measure the false-discovery rate.

Writes data/ref/entrap.json [[ref, text]] ('|' = blanked letter; spaces
between words) and data/ref/entrap_sources.json (licences). Local only.
Usage: python3 src/entrap_ref.py
"""
import json, os, re, sys, urllib.request, urllib.parse

sys.path.insert(0, os.path.dirname(__file__))
import pmatch  # noqa: E402

B = 'https://storage.googleapis.com/sefaria-export/'
HEB = re.compile(r'[א-ת]+')
FIN = str.maketrans('ךםןףץ', 'כמנפצ')
K = 10


def flatten(node, path=()):
    if isinstance(node, str):
        yield path, node
    elif isinstance(node, list):
        for i, x in enumerate(node, 1):
            yield from flatten(x, path + (i,))


def main():
    keys = [k for k in json.load(open('data/ref/mishnah_keys.json'))
            if k.split('/')[2].startswith('Seder')]
    keys += [k for k in json.load(open('data/ref/tosefta_keys.json'))
             if k.split('/')[2] == 'Vilna Edition' and 'Commentar' not in k]
    os.makedirs('data/ref/entrap', exist_ok=True)
    segs, src = [], {}
    for k in keys:
        work = k.split('/')[-3]
        path = f'data/ref/entrap/{work}.json'
        if not os.path.exists(path):
            open(path, 'wb').write(urllib.request.urlopen(B + urllib.parse.quote(k), timeout=120).read())
        d = json.load(open(path))
        src[work] = {x: d.get(x) for x in ('versionTitle', 'versionSource', 'license') if x in d}
        for p, s in flatten(d.get('text', [])):
            s = re.sub(r'<[^>]+>', ' ', s).replace('־', ' ')
            s = re.sub(r'[֑-ׇ]', '', s)
            t = ' '.join(HEB.findall(s))
            if t:
                segs.append([f'{work}.' + '.'.join(map(str, p)), t])
    # reference shingles (skeleton)
    c = pmatch.Corpus(mode='sk')
    rev = {i: ch for ch, i in pmatch.IDX.items()}
    text = ''.join(rev.get(int(i), '|') for i in c.ids)
    ref = {text[p:p + K] for p in range(len(text) - K + 1) if '|' not in text[p:p + K]}
    out, total, blank = [], 0, 0
    for r, t in segs:
        letters = [(i, ch.translate(FIN)) for i, ch in enumerate(t) if ch != ' ']
        sk = [(i, ch) for i, ch in letters if ch not in 'וי']
        kill = set()
        for j in range(len(sk) - K + 1):
            if ''.join(ch for _, ch in sk[j:j + K]) in ref:
                a, b = sk[j][0], sk[j + K - 1][0]
                kill.update(i for i, _ in letters if a <= i <= b)
        t2 = ''.join('|' if i in kill else ch for i, ch in enumerate(t))
        total += len(letters)
        blank += len(kill)
        out.append([r, t2])
    json.dump(out, open('data/ref/entrap.json', 'w'), ensure_ascii=False)
    json.dump(src, open('data/ref/entrap_sources.json', 'w'), ensure_ascii=False, indent=1)
    print(len(keys), 'works,', len(out), 'segments,', total, 'letters,', blank, 'blanked')


if __name__ == '__main__':
    main()
