"""Reference corpus for the matcher (M5/M6), in the formats prior_work/match.py reads.

  data/ref/bible.json      [[ref, consonantal text], ...] from openscriptures/morphhb
                           (WLC; ketiv as written, qere notes dropped)
  data/ref/dss_lines.json  [[scroll, fragment, line, text, marks, None], ...] from
                           data/m0/etcbc_lines.json (marks: '.', 'u', 'r', 'p', ' ', '#')
"""
import glob, json, os, re
import xml.etree.ElementTree as ET

NS = {'o': 'http://www.bibletechnologies.net/2003/OSIS/namespace'}
HEB = re.compile(r'[א-ת]')


def verse_text(v):
    words = []
    for w in v.iter():
        tag = w.tag.split('}')[-1]
        if tag == 'w':
            words.append(''.join(HEB.findall(''.join(w.itertext()))))
    return ' '.join(x for x in words if x)


if __name__ == '__main__':
    out = []
    for f in sorted(glob.glob('data/ref/morphhb/wlc/*.xml')):
        root = ET.parse(f).getroot()
        # drop notes (qere readings, editorial notes) before reading words
        for parent in root.iter():
            for ch in list(parent):
                if ch.tag.split('}')[-1] == 'note':
                    parent.remove(ch)
        for v in root.iter('{%s}verse' % NS['o']):
            t = verse_text(v)
            if t:
                out.append([v.get('osisID'), t])
    json.dump(out, open('data/ref/bible.json', 'w'), ensure_ascii=False)
    lines = json.load(open('data/m0/etcbc_lines.json'))
    json.dump([[s, f, l, t, m, None] for s, f, l, t, m in lines],
              open('data/ref/dss_lines.json', 'w'), ensure_ascii=False)
    print(len(out), 'verses,', sum(len(t.replace(' ', '')) for _, t in out), 'letters;',
          len(lines), 'scroll lines')
    print(out[0], out[-1][0])
