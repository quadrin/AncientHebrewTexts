import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,csv,re
R=os.path.join(D,'..')+os.sep
src=open(R+'web/scroll-text.js',encoding='utf-8').read()
js=src[src.index('window.SCROLL_TEXT = ')+len('window.SCROLL_TEXT = '):].strip()
if js.endswith(';'): js=js[:-1]
ST=json.loads(js)
roman=['I','II','III','IV','V','VI','VII','VIII','IX','X','XI','XII']
heb={}   # 'I 1' -> list of word dicts
for col in ST['columns']:
    for ln in col['lines']:
        heb[f"{roman[col['c']-1]} {ln['l']}"]=ln['w']
tr=json.load(open(R+'text/translation_en.json',encoding='utf-8'))
order=list(tr)
conc=list(csv.DictReader(open(R+'tables/entry_concordance.csv',encoding='utf-8-sig')))
def lines_for(rng):
    parts=[x.strip() for x in rng.replace('–','-').split('-')]
    a=parts[0].replace(':',' '); b=parts[-1].replace(':',' ')
    return order[order.index(a):order.index(b)+1]
out=[]
for r in conc:
    e=r['entry_puech']; L=lines_for(r['col_line'])
    words=[];lemmas=[];nums=[];greek=[]
    for l in L:
        for w in heb.get(l,[]):
            if w.get('greek'): greek.append(''.join(p[0] for p in w['h'])); continue
            if 'n' in w: nums.append((w['n'],w.get('ns'))); words.append(f"<{w.get('ns',w['n'])}>"); continue
            words.append(''.join(p[0] for p in w['h']))
            for m in w.get('m',[]): lemmas.append(m[1])
    txt=' '.join(re.sub(r'\{\{([^|}]*)\|[^}]*\}\}',r'\1',tr[l]) for l in L)
    out.append(dict(entry=e,col_line=r['col_line'],lines=L,heb=' '.join(words),lemmas=lemmas,numsigns=nums,greek=greek,en=txt,note=r['division_notes']))
json.dump(out,open(os.path.join(D,'entries_full.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
for o in out:
    print(f"[{o['entry']}] {o['col_line']}  GR={o['greek']} NUM={o['numsigns']}\n  H: {o['heb']}\n  E: {o['en']}")
