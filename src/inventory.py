"""M0: join Leon Levy images, SQE editions/matches and ETCBC transcriptions.

Inputs (from ll_harvest.py, sqe_harvest.py, etcbc_extract.py) in data/m0/.
Outputs:
  data/m0/inventory_images.json   one record per infrared fragment image (local only)
  data/m0/ll_other_manuscripts.json  LL records for image manuscripts outside the
                                     square-script query (cached lookups)
  reports/M0_manuscripts.tsv      one row per manuscript (metadata and counts only)
  reports/M0_summary.json         headline numbers for reports/M0.md
"""
import json, os, re, sys, collections

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'prior_work'))
from q import q  # noqa: E402

D = 'data/m0'
LANGS = {'Hebrew', 'Aramaic', 'Hebrew?', 'Aramaic?'}
# SQE / ETCBC names that differ after normalisation
ALIAS = {'11QTA': '11Q19'}


def nms(s):
    """Normalise a manuscript siglum across LL, SQE and ETCBC."""
    s = re.sub(r'[\s.^]', '', s or '').replace('_', '-').upper()
    return ALIAS.get(s, s)


def ll_base(ms):
    """LL sometimes appends a plate to a siglum: '4Q254a-820' -> '4Q254a'."""
    m = re.fullmatch(r'(\d+Q\d+[a-z]*)-\d+', ms)
    return m.group(1) if m else ms


def link_type(ll_ms, sqe_ms):
    """How an SQE match's manuscript relates to the LL image's manuscript."""
    a, b = nms(ll_base(ll_ms)), nms(sqe_ms)
    if a == b:
        return 'exact'
    # LL files sub-sigla (4Q249z, 4Q418a, 4Q324d) under the parent number
    if re.fullmatch(re.escape(a) + r'[A-Z]{1,2}', b):
        return 'subsiglum'
    return None


def nfr(s):
    """SQE text-fragment name -> ETCBC fragment label ('frg. 3 i' -> 'f3i')."""
    s = re.sub(r'^frg\.\s*', 'f', s.strip())
    s = re.sub(r'^col\.\s*', '', s)
    return re.sub(r'\s', '', s)


def nplate(p):
    """LL plate '466/Vrs', '28/Rec', '12a' and SQE '466', '12a' -> comparable key."""
    return re.sub(r'/(Rec|Vrs)$', '', (p or '').strip()).lstrip('*').lower()


def load(name):
    return json.load(open(f'{D}/{name}'))


def other_manuscripts(numbers):
    path = f'{D}/ll_other_manuscripts.json'
    have = json.load(open(path)) if os.path.exists(path) else {}
    for n in sorted(set(numbers) - set(have)):
        res = q('manuscript', f"manuscript_number:'{n}'")['results']
        have[n] = next((r for r in res if r['manuscript_number'] == n), None)
    json.dump(have, open(path, 'w'), ensure_ascii=False)
    return have


def main():
    ll_ms = {m['manuscript_number']: m for m in load('ll_manuscripts.json')}
    ims = load('ll_ir_images.json')
    eds = load('sqe_editions.json')
    tfs = load('sqe_text_fragments.json')
    sqm = load('sqe_matches.json')['matches']
    ef = load('etcbc_fragments.json')

    # ---- manuscripts: square-script list plus any image manuscript missing from it
    extra = other_manuscripts({i['manuscript_numbers'][0] for i in ims} - set(ll_ms))
    allms = dict(ll_ms)
    allms.update({k: v for k, v in extra.items() if v})

    def ms_status(m):
        if m is None:
            return 'no LL record'
        st = m.get('script_type') or ''
        if st and st != 'Square':
            return f'excluded: {st} script'
        if m.get('script_language') not in LANGS:
            return f"excluded: language '{m.get('script_language')}'"
        return 'square' if st == 'Square' else 'script type blank'

    # ---- ETCBC by normalised scroll, fragment
    et = {(nms(f['scroll']), f['fragment']): f for f in ef}
    et_scroll = collections.defaultdict(list)
    for f in ef:
        et_scroll[nms(f['scroll'])].append(f)

    # ---- SQE: edition names, text fragment names, matches by (plate, frag, side)
    ed_name = {e['id']: e['name'] for e in eds}
    tf_name = {t['id']: t['name'] for v in tfs.values() if v for t in v}
    sqe_by_ms = collections.defaultdict(list)
    for e in eds:
        sqe_by_ms[nms(e['name'])].append(e['id'])
    by_io = collections.defaultdict(list)
    for eid, v in sqm.items():
        for r in v or []:
            if r['institution'] != 'IAA':
                continue
            key = (nplate(r['catalogueNumber1']), r['catalogueNumber2'], r['catalogSide'].lower())
            by_io[key].append(r)

    # ---- per image
    out = []
    for i in ims:
        ms = i['manuscript_numbers'][0]
        m = allms.get(ms)
        key = (nplate(i['plate_numbers'][0]), i['frag_num'], (i['side'] or '').lower())
        cands = by_io.get(key, [])
        # SQE plate numbering drops LL's '*', so the manuscript must agree too
        star = i['plate_numbers'][0].startswith('*')
        same = [(r, link_type(ms, r['manuscriptName'])) for r in cands]
        same = [(r, t) for r, t in same if t == 'exact' or (t and not star)]
        if not same and not star:
            # opisthographs: LL and SQE sometimes disagree on which side is recto
            flip = {'recto': 'verso', 'verso': 'recto'}.get(key[2])
            same = [(r, 'side_swapped') for r in by_io.get((key[0], key[1], flip), [])
                    if link_type(ms, r['manuscriptName']) == 'exact']
        rejected = [r for r, _ in same if r['confirmed'] is False]
        good = [(r, t) for r, t in same if r['confirmed'] is not False]
        tfr = []
        for r, link in good:
            tname = tf_name.get(r['textFragmentId'], r['name'])
            ek = (nms(r['manuscriptName']), nfr(tname))
            f = et.get(ek)
            tfr.append(dict(edition=r['editionId'], edition_name=ed_name.get(r['editionId']),
                            text_fragment=r['textFragmentId'], tf_name=tname,
                            confirmed=r['confirmed'], link=link,
                            etcbc=[f['scroll'], f['fragment']] if f else None,
                            preserved=f['preserved'] if f else None,
                            certain=f['certain'] if f else None,
                            lines=f['lines'] if f else None))
        # a text fragment can be listed twice (several editions); de-duplicate
        tfr = list({(t['edition'], t['text_fragment']): t for t in tfr}.values())
        out.append(dict(name=i['name'], manuscript=ms, ms_status=ms_status(m),
                        plate=i['plate_numbers'][0], frag=i['frag_num'], side=i['side'],
                        w=i['full_width'], h=i['full_height'], url=i['url'],
                        sqe_other_ms=len(cands) - sum(t != 'side_swapped' for _, t in same), sqe_rejected=len(rejected),
                        text_fragments=tfr))
    json.dump(out, open(f'{D}/inventory_images.json', 'w'), ensure_ascii=False)

    # ---- per manuscript table
    per = collections.defaultdict(list)
    for r in out:
        per[r['manuscript']].append(r)
    rows = []
    for ms in sorted(set(allms) | set(per), key=lambda s: (nms(s))):
        m = allms.get(ms) or {}
        imgs = per.get(ms, [])
        recto = [r for r in imgs if r['side'] == 'Recto']
        linked = [r for r in imgs if r['text_fragments']]
        et_linked = [r for r in imgs if any(t['etcbc'] for t in r['text_fragments'])]
        one_one = [r for r in et_linked if len(r['text_fragments']) == 1]
        exact = [r for r in et_linked if all(t['link'] == 'exact' for t in r['text_fragments'])]
        efs = et_scroll.get(nms(ll_base(ms)), [])
        tf_seen = {tuple(t['etcbc']) for r in imgs for t in r['text_fragments'] if t['etcbc']}
        rows.append(dict(
            manuscript=ms, status=ms_status(m or None),
            language=m.get('script_language', ''), material=m.get('material', ''),
            period=m.get('period', ''), site=m.get('site', ''),
            composition_type=m.get('composition_type', ''),
            ir_images=len(imgs), ir_recto=len(recto),
            ir_with_sqe_match=len(linked), ir_with_etcbc_fragment=len(et_linked),
            ir_single_text_fragment=len(one_one), ir_exact_link=len(exact),
            sqe_editions=','.join(map(str, sqe_by_ms.get(nms(ll_base(ms)), []))),
            etcbc_scroll=efs[0]['scroll'] if efs else '',
            etcbc_fragments=len(efs),
            etcbc_preserved=sum(f['preserved'] for f in efs),
            etcbc_certain=sum(f['certain'] for f in efs),
            etcbc_fragments_imaged=len(tf_seen),
            etcbc_preserved_imaged=sum(et[(nms(a), b)]['preserved'] for a, b in tf_seen),
            etcbc_scrolls_via_images=','.join(sorted({a for a, _ in tf_seen})),
        ))
    os.makedirs('reports', exist_ok=True)
    cols = list(rows[0])
    with open('reports/M0_manuscripts.tsv', 'w') as fh:
        fh.write('\t'.join(cols) + '\n')
        for r in rows:
            fh.write('\t'.join(str(r[c]) for c in cols) + '\n')

    # ---- summary
    def agg(rs):
        keys = [k for k in rs[0] if isinstance(rs[0][k], int)] if rs else []
        return dict(manuscripts=len(rs), **{k: sum(r[k] for r in rs) for k in keys})
    by_status = collections.defaultdict(list)
    for r in rows:
        by_status[r['status']].append(r)
    usable = [r for r in rows if r['status'] in ('square', 'script type blank')]
    train = [r for r in usable if r['composition_type'] != 'Unidentified Text'
             and not re.match(r'\d+Q9999$', r['manuscript'])]
    summ = dict(by_status={k: agg(v) for k, v in sorted(by_status.items())},
                usable=agg(usable), usable_identified=agg(train),
                usable_identified_parchment=agg([r for r in train if r['material'] == 'Parchment']),
                sqe_editions=len(eds), etcbc_scrolls=len(et_scroll),
                etcbc_scrolls_without_images=sorted(
                    set(et_scroll) - {nms(a) for r in out for t in r['text_fragments']
                                      if t['etcbc'] for a in t['etcbc'][:1]}),
                links=dict(collections.Counter(t['link'] for r in out for t in r['text_fragments'])))
    json.dump(summ, open('reports/M0_summary.json', 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k != 'etcbc_scrolls_without_images'},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
