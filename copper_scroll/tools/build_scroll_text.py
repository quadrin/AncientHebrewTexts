"""Build web/scroll-text.js: the text of 3Q15 for the scroll reader on the web page.

Source: the ETCBC `dss` Text-Fabric dataset, version 2.0.1 (transcriptions and
morphology by Martin G. Abegg Jr., with James E. Bowley and Edward M. Cook;
converted by Jarod Jacobs, Martijn Naaijer and Dirk Roorda). Licence: CC BY-NC 4.0.
This is the only complete 3Q15 text the repository may publish: the Puech,
Lefkovits and Milik texts are kept out of it (see README.md).

Get the data first:
    git clone --filter=blob:none --sparse https://github.com/ETCBC/dss
    git -C dss sparse-checkout set tf/2.0.1
    python copper_scroll/tools/build_scroll_text.py path/to/dss/tf/2.0.1

Changes made to the source, as the licence asks us to state them:
- ETCBC words are joined into the words as written (a prefix such as ב or ה is
  joined to the next word; spaces follow the `after` feature).
- Abegg's sentence-break sign (׃) is an editorial mark, not a mark on the
  scroll, and is left out.
- Numeral signs are given as values (A, å, B, ∫ = 1; C = 10; D = 20; F = 100,
  following Abegg's QUMRAN read-me, item 7), with the signs kept in the order
  the dataset stores them.
- Text-critical marks are turned into classes for display; the source keeps
  them as bracket characters.
"""
import json, sys, os, unicodedata
from tf.fabric import Fabric

TF = sys.argv[1] if len(sys.argv) > 1 else 'dss/tf/2.0.1'
OUT = os.path.join(os.path.dirname(__file__), '..', 'web', 'scroll-text.js')

NUM = {'א֜': 1, 'אׄ': 1, 'אׅ': 1, 'אֽ': 1, 'י֜': 10, 'ך֜': 20, 'ק֜': 100}
FINAL = {'כ': 'ך', 'מ': 'ם', 'נ': 'ן', 'פ': 'ף', 'צ': 'ץ'}


def sign_class(s, F):
    """One letter code per display class. Order matters: a removed letter that is
    also uncertain shows as removed."""
    if F.rem.v(s):
        return 'x' if F.rem.v(s) == 1 else 'd'   # removed by a modern / an ancient editor
    if F.cor.v(s) == 3:
        return 's'                              # written above the line by the scribe
    if F.cor.v(s):
        return 'c'                              # supplied or corrected by the modern editor
    if F.rec.v(s):
        return 'r'                              # restored in a lacuna
    if F.unc.v(s):
        return 'u'                              # damaged, uncertain letter
    return ''


def numeral_value(glyphs):
    """Abegg writes 100 as a unit before the hundred sign; 3Q15 has one such group."""
    if 'ק֜' in glyphs:
        i = glyphs.index('ק֜')
        before = sum(NUM[g] for g in glyphs[:i]) or 1
        return before * 100 + sum(NUM[g] for g in glyphs[i + 1:])
    return sum(NUM[g] for g in glyphs)


def main():
    api = Fabric(locations=TF, silent='deep').load(
        'otype scroll fragment line glyph full lex sp type after rec unc cor rem lang', silent='deep')
    F, L = api.F, api.L
    scroll = next(s for s in F.otype.s('scroll') if F.scroll.v(s) == '3Q15')
    columns = []
    lexemes = {}
    for fr in L.d(scroll, 'fragment'):
        col = int(F.fragment.v(fr))
        lines = []
        for ln in L.d(fr, 'line'):
            words, cur = [], None

            def flush():
                nonlocal cur
                if cur and (cur['h'] or cur.get('n') is not None):
                    # merge runs of the same class
                    segs = []
                    for ch, k in cur['h']:
                        if segs and segs[-1][1] == k:
                            segs[-1][0] += ch
                        else:
                            segs.append([ch, k])
                    cur['h'] = segs
                    if not cur['m']:
                        del cur['m']
                    words.append(cur)
                cur = None

            for w in L.d(ln, 'word'):
                wtype = F.type.v(w)
                if wtype == 'punct':
                    flush()
                    continue
                if cur is None:
                    cur = {'h': [], 'm': []}
                signs = [s for s in L.d(w, 'sign')]
                if wtype == 'numr':
                    glyphs = [F.glyph.v(s) for s in signs if F.type.v(s) == 'numr']
                    cur['n'] = numeral_value(glyphs)
                    cur['ns'] = '+'.join(str(NUM[g]) for g in glyphs)
                    # a letter written after the numeral inside the same word (IX 6)
                    for s in signs:
                        if F.type.v(s) == 'cons':
                            cur['h'].append([F.glyph.v(s), sign_class(s, F)])
                    if F.after.v(w):
                        flush()
                    continue
                surface = ''
                for s in signs:
                    t = F.type.v(s)
                    if t in ('cons', 'foreign'):
                        g = F.glyph.v(s)
                        cur['h'].append([g, 'g' if t == 'foreign' else sign_class(s, F)])
                        surface += g
                    elif t == 'unc':
                        cur['h'].append(['◦', ''])         # an illegible letter: the circle is the mark
                    elif t == 'missing':
                        cur['h'].append(['…', 'r'])        # a lacuna of unknown length
                if F.lang.v(w) == 'g':
                    cur['greek'] = 1
                lex = F.lex.v(w)
                lex = unicodedata.normalize('NFC', lex) if lex else lex   # one order for the vowel points
                sp = F.sp.v(w)
                if lex and lex not in ('None',) and F.lang.v(w) != 'g':
                    cur['m'].append([surface, lex, sp or ''])
                    lexemes.setdefault(lex, {'sp': sp or '', 'n': 0})
                    lexemes[lex]['n'] += 1
                if F.after.v(w):
                    flush()
            flush()
            # a final letter in the middle of a word shows where the transcription
            # breaks a word across two lines; nothing to do, kept as written
            lines.append({'l': int(F.line.v(ln)), 'w': words})
        columns.append({'c': col, 'lines': lines})

    data = {
        'source': 'ETCBC dss 2.0.1, scroll 3Q15 (Abegg, Bowley and Cook; CC BY-NC 4.0)',
        'columns': columns,
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write('/* The text of 3Q15 from the ETCBC Dead Sea Scrolls dataset (Text-Fabric 2.0.1).\n'
                '   Transcription and morphology: Martin G. Abegg Jr., James E. Bowley and Edward M. Cook.\n'
                '   Conversion: Jarod Jacobs, Martijn Naaijer and Dirk Roorda. Licence: CC BY-NC 4.0,\n'
                '   https://creativecommons.org/licenses/by-nc/4.0/ . Changed for display by\n'
                '   copper_scroll/tools/build_scroll_text.py, which lists the changes. */\n')
        f.write('window.SCROLL_TEXT = ')
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
        f.write(';\n')
    if os.environ.get('LEXEMES_OUT'):   # the lemma list, for writing glosses
        with open(os.environ['LEXEMES_OUT'], 'w', encoding='utf-8') as f:
            json.dump(lexemes, f, ensure_ascii=False, indent=0, sort_keys=True)
    n_lines = sum(len(c['lines']) for c in columns)
    n_words = sum(len(l['w']) for c in columns for l in c['lines'])
    print(f'{len(columns)} columns, {n_lines} lines, {n_words} words, {len(lexemes)} lexemes -> {OUT}')


if __name__ == '__main__':
    main()
