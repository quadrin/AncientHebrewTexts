"""Build web/scroll-notes.js: the translation, glosses, readings and entry data for
the scroll reader on the web page.

Inputs, all written for this project:
- text/translation_en.json   one English line per scroll line; {{words|note-id}} marks
                             a phrase that opens a note
- text/glossary_en.json      a short English meaning for every lemma in the ETCBC text
- text/readings.json         notes: how the editions read and interpret a word or phrase
Inputs from the research tables:
- tables/entry_concordance.csv, tables/phase3_site_index.csv, atlas/app/atlas-data.json

Run build_scroll_text.py first; this script checks every note against its output.
    python copper_scroll/tools/build_scroll_notes.py
"""
import csv, json, os, re, sys, unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ROMAN = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII']
NFC = lambda s: unicodedata.normalize('NFC', s)


def load_js(path, var):
    s = open(path, encoding='utf-8').read()
    return json.loads(s[s.index(var + ' = ') + len(var) + 3:].rstrip().rstrip(';'))


def parse_ref(ref):
    """'I:6' or 'I 6' -> ('I', 6)."""
    col, line = re.split(r'[: ]', ref.strip())
    return col, int(line)


def main():
    text = load_js(os.path.join(ROOT, 'web', 'scroll-text.js'), 'window.SCROLL_TEXT')
    lines = {}
    for c in text['columns']:
        for l in c['lines']:
            lines[f"{ROMAN[c['c'] - 1]} {l['l']}"] = l['w']
    order = list(lines)
    errors = []

    # translation, with {{phrase|note}} links
    tr_src = json.load(open(os.path.join(ROOT, 'text', 'translation_en.json'), encoding='utf-8'))
    tr = {}
    links = set()
    for key in order:
        if key not in tr_src:
            errors.append(f'no translation for {key}')
            continue
        segs = []
        for part in re.split(r'(\{\{[^}]+\}\})', tr_src[key]):
            m = re.fullmatch(r'\{\{([^|]+)\|([^}]+)\}\}', part)
            if m:
                segs.append([m.group(1), m.group(2)])
                links.add(m.group(2))
            elif part:
                segs.append(part)
        tr[key] = segs
    for key in tr_src:
        if key not in lines:
            errors.append(f'translation for a line the text does not have: {key}')

    # glosses, keyed as the text keys its lemmas
    gloss = {NFC(k): v for k, v in json.load(open(os.path.join(ROOT, 'text', 'glossary_en.json'), encoding='utf-8')).items()}
    used = set()
    for ws in lines.values():
        for w in ws:
            for m in w.get('m', []):
                m[1] = NFC(m[1])
                used.add(m[1])
    for lx in sorted(used - set(gloss)):
        errors.append(f'no gloss for lemma {lx}')
    gloss = {k: v for k, v in gloss.items() if k in used}

    # readings: check each note's line and word indices
    notes_src = json.load(open(os.path.join(ROOT, 'text', 'readings.json'), encoding='utf-8'))
    notes = {}
    for n in notes_src:
        nid = n['id']
        if nid in notes:
            errors.append(f'duplicate note id {nid}')
        spots = []
        for spot in [{'line': n.get('line'), 'words': n.get('words', [])}] + n.get('also', []):
            if not spot.get('line'):
                continue
            if spot['line'] not in lines:
                errors.append(f'{nid}: no line {spot["line"]}')
                continue
            for i in spot['words']:
                if not 0 <= i < len(lines[spot['line']]):
                    errors.append(f'{nid}: no word {i} on {spot["line"]}')
            spots.append([spot['line'], spot['words']])
        out = {k: n[k] for k in ('label', 'readings', 'note') if n.get(k)}
        out['entry'] = n.get('entry', '')
        out['at'] = spots
        if n.get('lemma'):
            out['lemma'] = [NFC(x) for x in n['lemma']]
        if n.get('sources'):
            out['src'] = n['sources']
        notes[nid] = out
    for nid in sorted(links - set(notes)):
        errors.append(f'translation links to a missing note {nid}')

    # entries: line ranges from the concordance, places from Phase 3, words from the atlas
    site = {r['entry']: r for r in csv.DictReader(open(os.path.join(ROOT, 'tables', 'phase3_site_index.csv'), encoding='utf-8-sig'))}
    places = {r['place_id']: r['name'] for r in csv.DictReader(open(os.path.join(ROOT, 'tables', 'phase3_places.csv'), encoding='utf-8-sig'))}
    atlas = {e['id']: e for e in json.load(open(os.path.join(ROOT, 'atlas', 'app', 'atlas-data.json'), encoding='utf-8'))['entries']}
    entries = []
    for r in csv.DictReader(open(os.path.join(ROOT, 'tables', 'entry_concordance.csv'), encoding='utf-8-sig')):
        e = r['entry_puech']
        a, b = r['col_line'].split('–') if '–' in r['col_line'] else (r['col_line'], r['col_line'])
        start, end = '%s %d' % parse_ref(a), '%s %d' % parse_ref(b)
        s = site.get(e, {})
        at = atlas.get(e, {})
        entries.append({
            'id': e, 'start': start, 'end': end,
            'lef': r['item_lefkovits'], 'milik': r['item_milik'],
            'title': at.get('title', ''), 'desc': at.get('description', ''),
            'evidence': at.get('evidence', ''), 'caution': at.get('caution', ''),
            'status': s.get('status', ''), 'conf': s.get('best_confidence', ''),
            'place': s.get('best_place', ''),
            'possible': [places[p] for p in (s.get('possible_place_ids') or '').split('; ') if p in places],
            'n': s.get('n_candidates', ''),
        })
    # entry 3 is the one entry that starts inside a line (Puech p. 179): after the
    # sentence that ends entry 2 on I 6
    for e in entries:
        if e['id'] == '3':
            e['startWord'] = next(i for i, w in enumerate(lines['I 6']) if w.get('n') is not None) + 1
    for e in entries:
        for k in ('start', 'end'):
            if e[k] not in lines:
                errors.append(f'entry {e["id"]}: no line {e[k]}')

    if errors:
        print('\n'.join(errors))
        sys.exit(1)

    data = {'tr': tr, 'gloss': gloss, 'notes': notes, 'entries': entries}
    out = os.path.join(ROOT, 'web', 'scroll-notes.js')
    with open(out, 'w', encoding='utf-8') as f:
        f.write('/* Translation, glosses and reading notes for the Copper Scroll reader.\n'
                '   Written for this project; built from copper_scroll/text/ by\n'
                '   copper_scroll/tools/build_scroll_notes.py. Readings cite the editions by page. */\n')
        f.write('window.SCROLL_NOTES = ')
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
    print(f'{len(tr)} lines, {len(gloss)} glosses, {len(notes)} notes, {len(entries)} entries -> {out}')


if __name__ == '__main__':
    main()
