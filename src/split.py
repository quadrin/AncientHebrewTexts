"""M4/M5: split manuscripts into train / val / test (held out for M5).

Test manuscripts must have a parallel text outside themselves, so that M5 can
ask the matcher to identify them with their own transcription removed:
  * biblical manuscripts (parallel: the Masoretic text)
  * one copy of each composition that survives in several manuscripts
Everything is split by whole manuscript. Output: reports/M4_split.json.
"""
import json, random, collections, csv

SEED = 20260924

if __name__ == '__main__':
    man = [json.loads(l) for l in open('data/m3/manifest.jsonl')]
    use = [r for r in man if r['tier']]
    letters = collections.Counter()
    for r in use:
        letters[r['manuscript']] += r['letters']
    ll = {m['manuscript_number']: m for m in json.load(open('data/m0/ll_manuscripts.json'))}
    rows = {r['manuscript']: r for r in csv.DictReader(open('reports/M0_manuscripts.tsv'), delimiter='\t')}

    def comp(ms):
        return (ll.get(ms, {}).get('composition_name') or '').strip()

    ctype = {ms: rows[ms]['composition_type'] for ms in letters}
    rnd = random.Random(SEED)
    # enough text to be worth testing, but not the biggest training sources
    mid = [ms for ms in letters if 60 <= letters[ms] <= 800]

    bib = sorted(ms for ms in mid if ctype[ms] == 'Scripture')
    test = set(rnd.sample(bib, 15))

    by_comp = collections.defaultdict(list)
    for ms in letters:
        if ctype[ms] != 'Scripture' and comp(ms):
            by_comp[comp(ms)].append(ms)
    multi = sorted(c for c, v in by_comp.items() if len(v) >= 2)
    rnd.shuffle(multi)
    picked = []
    for c in multi:
        cands = sorted(ms for ms in by_comp[c] if ms in mid and ms not in test)
        if cands:
            ms = rnd.choice(cands)
            test.add(ms)
            picked.append((c, ms, sorted(by_comp[c])))
        if len(picked) == 10:
            break

    rest = sorted(ms for ms in letters if ms not in test)
    val = set(rnd.sample(rest, round(0.08 * len(rest))))
    train = [ms for ms in rest if ms not in val]
    out = dict(seed=SEED,
               test=sorted(test), val=sorted(val), train=sorted(train),
               test_multi_copy=[dict(composition=c, held_out=ms, copies=v) for c, ms, v in picked],
               letters=dict(test=sum(letters[m] for m in test), val=sum(letters[m] for m in val),
                            train=sum(letters[m] for m in train)))
    json.dump(out, open('reports/M4_split.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: (len(v) if isinstance(v, list) else v) for k, v in out.items()}, ensure_ascii=False))
    for p in picked:
        print(p[0], '->', p[1], 'of', p[2])
