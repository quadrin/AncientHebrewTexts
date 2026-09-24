"""M0: extract line-level transcriptions from ETCBC dss (Text-Fabric 2.0.1).

Writes data/m0/etcbc_lines.json: one record per line
  [scroll, fragment, line, text, marks]
where text holds consonants, word separators (' ', taken from the word
feature `after`, so prefixes such as ו ה ל stay joined as written) and '#'
for a lacuna the editor left unreconstructed. marks has one character per
text character:
  '.' preserved, 'u' preserved but uncertain (unc >= 1), 'r' reconstructed,
  'p' paleo-Hebrew script, ' ' separator, '#' lacuna.
Final forms are kept as written.

Also writes data/m0/etcbc_fragments.json with per-fragment counts.
"""
import json, os, collections
from tf.fabric import Fabric

OUT = 'data/m0'
TFDIR = 'data/dss/tf/2.0.1'


def mark(s, F):
    if F.script.v(s):
        return 'p'
    if F.rec.v(s):
        return 'r'
    if F.unc.v(s):
        return 'u'
    return '.'


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    api = Fabric(locations=TFDIR, silent='deep').load(
        'otype scroll fragment line glyph rec unc lang script type after', silent='deep')
    F, L = api.F, api.L
    lines, frags = [], []
    for sc in F.otype.s('scroll'):
        scroll = F.scroll.v(sc)
        for fr in L.d(sc, 'fragment'):
            frag = F.fragment.v(fr)
            c = collections.Counter()
            nlines = 0
            for ln in L.d(fr, 'line'):
                text, marks = [], []
                for w in L.d(ln, 'word'):
                    for s in L.d(w, 'sign'):
                        if F.type.v(s) == 'missing':
                            if not text or text[-1] != '#':
                                text.append('#')
                                marks.append('#')
                            continue
                        if F.type.v(s) != 'cons':
                            continue
                        m = mark(s, F)
                        text.append(F.glyph.v(s))
                        marks.append(m)
                        c[m] += 1
                        if F.lang.v(s) == 'a':
                            c['aramaic'] += 1
                    if F.after.v(w) == ' ' and text and text[-1] != ' ':
                        text.append(' ')
                        marks.append(' ')
                t, m = ''.join(text).strip(), ''.join(marks).strip()
                if t.replace('#', '').strip():
                    nlines += 1
                    lines.append([scroll, frag, F.line.v(ln), t, m])
            frags.append(dict(scroll=scroll, fragment=frag, lines=nlines,
                              preserved=c['.'] + c['u'], certain=c['.'],
                              uncertain=c['u'], reconstructed=c['r'],
                              paleo=c['p'], aramaic=c['aramaic']))
    json.dump(lines, open(f'{OUT}/etcbc_lines.json', 'w'), ensure_ascii=False)
    json.dump(frags, open(f'{OUT}/etcbc_fragments.json', 'w'), ensure_ascii=False)
    tot = collections.Counter()
    for f in frags:
        tot.update({k: v for k, v in f.items() if isinstance(v, int)})
    print(len(lines), 'lines;', len(frags), 'fragments;', dict(tot))
