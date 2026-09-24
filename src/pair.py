"""M1: pair infrared fragment images with transcription fragments and lines.

Input: data/m0/* (run inventory.py first) and data/m0/sqe_artefacts.json
(fetched by this script if missing).
Output:
  data/m1/pairs.json   one record per usable image, with category and, where
                       the pairing is usable, the ETCBC lines (local only)
  reports/M1_summary.json
"""
import json, os, re, sys, collections

sys.path.insert(0, os.path.dirname(__file__))
from inventory import nms, nplate, nfr, link_type, ll_base  # noqa: E402
from sqe_harvest import get, per_edition, cached  # noqa: E402

D0, D1 = 'data/m0', 'data/m1'
# Named unidentified sets that M7 will read. Keep them out of training even
# where ETCBC has a transcription, so M7 readings are not contaminated.
TARGET_SETS = {'4Q584', '4Q585', '3Q14', '4Q282', '11Q30'}


def is_target(ms, comp):
    return (comp == 'Unidentified Text' or re.fullmatch(r'\d+Q9999', ms)
            or nms(ll_base(ms)) in {nms(t) for t in TARGET_SETS})


def artefact_index(eds):
    def fn(i):
        a = get(f'/editions/{i}/artefacts')['artefacts']
        return [dict(id=x['id'], io=x['imagedObjectId'], side=x['side'], name=x['name'],
                     imageId=x['imageId'], has_mask=bool(x.get('mask'))) for x in a]
    art = cached(f'{D0}/sqe_artefacts.json', lambda: per_edition(eds, fn))
    ed_name = {e['id']: e['name'] for e in eds}
    by = collections.defaultdict(list)
    for eid, v in art.items():
        for a in v or []:
            m = re.fullmatch(r'IAA-(.+)-(\d+)', a['io'] or '')
            # only artefacts carrying an edition fragment name; many carry IAA labels
            if m and re.match(r'(Frg|Col)\. ', a['name']):
                by[(nplate(m.group(1)), m.group(2), a['side'])].append((ed_name[int(eid)], a))
    return by


def main():
    os.makedirs(D1, exist_ok=True)
    inv = json.load(open(f'{D0}/inventory_images.json'))
    eds = json.load(open(f'{D0}/sqe_editions.json'))
    ms_meta = {}
    for m in json.load(open(f'{D0}/ll_manuscripts.json')):
        ms_meta[m['manuscript_number']] = m
    for k, m in json.load(open(f'{D0}/ll_other_manuscripts.json')).items():
        if m:
            ms_meta[k] = m
    et_frag = {(nms(f['scroll']), f['fragment']): f for f in json.load(open(f'{D0}/etcbc_fragments.json'))}
    et_lines = collections.defaultdict(list)
    for s, f, l, t, m in json.load(open(f'{D0}/etcbc_lines.json')):
        et_lines[(nms(s), f)].append(dict(line=l, text=t, marks=m))
    arts = artefact_index(eds)

    recs = []
    for r in inv:
        if r['ms_status'] not in ('square', 'script type blank'):
            continue
        meta = ms_meta.get(r['manuscript'], {})
        links = [dict(etcbc=t['etcbc'], link=t['link'], confirmed=t['confirmed'],
                      source='catalogue') for t in r['text_fragments'] if t['etcbc']]
        if not r['text_fragments']:
            key = (nplate(r['plate']), r['frag'], (r['side'] or '').lower())
            for ed, a in arts.get(key, []):
                if link_type(r['manuscript'], ed) != 'exact':
                    continue
                fr = nfr(a['name'].replace('Frg.', 'frg.').replace('Col.', 'col.'))
                f = et_frag.get((nms(ed), fr))
                if f:
                    links.append(dict(etcbc=[f['scroll'], f['fragment']], link='exact',
                                      confirmed=None, source='artefact'))
        links = list({tuple(x['etcbc']): x for x in links}.values())
        recs.append(dict(name=r['name'], manuscript=r['manuscript'], side=r['side'],
                         plate=r['plate'], frag=r['frag'], w=r['w'], h=r['h'],
                         material=meta.get('material', ''), period=meta.get('period', ''),
                         language=meta.get('script_language', ''),
                         split='target' if is_target(r['manuscript'], meta.get('composition_type')) else 'train',
                         links=links))

    # how many physical pieces (IAA plate/fragment, same side) carry each text
    # fragment; the same piece photographed twice does not make a pair ambiguous
    def piece(r):
        return (nplate(r['plate']), r['frag'], r['side'])
    on_pieces = collections.defaultdict(set)
    photos = collections.Counter(piece(r) for r in recs)
    for r in recs:
        for x in r['links']:
            on_pieces[(tuple(x['etcbc']), r['side'])].add(piece(r))

    def colbase(label):
        m = re.fullmatch(r'(f?\d+[a-z]?)(i{1,3}|iv|v|vi{0,3})', label)
        return m.group(1) if m else None

    for r in recs:
        ks = [tuple(x['etcbc']) for x in r['links']]
        pres = sum(et_frag[(nms(a), b)]['preserved'] for a, b in ks)
        shared = any(len(on_pieces[(k, r['side'])]) > 1 for k in ks)
        # a verso image whose text fragment also sits on a recto: the blank back
        back = r['side'] == 'Verso' and ks and all(on_pieces[(k, 'Recto')] for k in ks)
        if not ks:
            cat = 'unlinked'
        elif back:
            cat = 'verso_back'
        elif shared:
            cat = 'shared'  # a text fragment spread over several images (joins)
        elif len(ks) == 1:
            cat = 'one_to_one'
        elif len({colbase(b) for _, b in ks}) == 1 and colbase(ks[0][1]):
            cat = 'multi_column'  # one piece carrying columns i, ii, ...
        else:
            cat = 'image_many'
        if ks and cat != 'unlinked' and pres == 0:
            cat = 'no_text'
        r['category'] = cat
        r['preserved'] = pres
        r['photos_of_piece'] = photos[piece(r)]
        if cat in ('one_to_one', 'multi_column'):
            r['lines'] = {f'{a}|{b}': et_lines[(nms(a), b)] for a, b in ks}
    json.dump(recs, open(f'{D1}/pairs.json', 'w'), ensure_ascii=False)

    summ = {}
    for split in ('train', 'target'):
        rs = [r for r in recs if r['split'] == split]
        by = collections.defaultdict(list)
        for r in rs:
            by[(r['category'], r['side'])].append(r)
        summ[split] = {f'{c}|{s}': dict(images=len(v), preserved=sum(x['preserved'] for x in v))
                       for (c, s), v in sorted(by.items())}
    tr = [r for r in recs if r['split'] == 'train']
    summ['train_link_mix'] = dict(collections.Counter(
        f"{x['source']}/{x['link']}"
        for r in tr if r['category'] == 'one_to_one' for x in r['links']))
    json.dump(summ, open('reports/M1_summary.json', 'w'), indent=1)
    print(json.dumps(summ, indent=1))


if __name__ == '__main__':
    main()
