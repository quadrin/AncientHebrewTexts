import json, collections
FIN=str.maketrans('ךםןףץ','כמנפצ')
dl=json.load(open('dss_lines.json'))
heb=json.load(open('unid_in_etcbc.json'))
Q=sorted(set(s for x in heb for s in x[3]))
# per-scroll line records: list of (fragment,line, letters, recflags)
lines=collections.defaultdict(list)
for s,f,l,t,rm,b in dl:
    t2=t.translate(FIN); L=[];R=[]
    for i,c in enumerate(t2):
        if 'א'<=c<='ת': L.append(c); R.append(rm[i]=='r' if i<len(rm) else False)
    lines[s].append((f,l,''.join(L),R))
bib=json.load(open('bible.json')); book=collections.defaultdict(list)
for ref,s in bib:
    book[ref.split('.')[0]].append((ref,''.join(c for c in s.translate(FIN) if 'א'<=c<='ת')))
# target docs: all DSS scrolls + MT books, as continuous strings with ref maps
targets=[]
for b,vs in book.items():
    t=''.join(v for _,v in vs); refs=[r for r,v in vs for _ in v]; targets.append(('MT '+b,t,refs,None))
for s,ls in lines.items():
    t=''.join(x[2] for x in ls); refs=[f'{x[0]}:{x[1]}' for x in ls for _ in x[2]]; rec=[r for x in ls for r in x[3]]
    targets.append((s,t,refs,rec))
K=9
idx=collections.defaultdict(list)
for ti,(lab,t,refs,rec) in enumerate(targets):
    for i in range(len(t)-K+1): idx[t[i:i+K]].append((ti,i))
tlab=[x[0] for x in targets]
def family(s):  # treat sibling sigla of the same number as self
    import re; m=re.match(r'(\d+Q\d+)',s); return m.group(1) if m else s
out=[]
for q in Q:
    fam=family(q)
    for f,l,s,R in lines[q]:
        # preserved-only runs within the line
        runs=[];cur='';
        for c,r in zip(s,R):
            if r: 
                if len(cur)>=K: runs.append(cur)
                cur=''
            else: cur+=c
        if len(cur)>=K: runs.append(cur)
        for run in runs:
            seen=set()
            for i in range(len(run)-K+1):
                for ti,p in idx.get(run[i:i+K],[]):
                    if family(tlab[ti])==fam: continue
                    # extend both directions
                    t=targets[ti][1]; a,b=i,p
                    while a>0 and b>0 and run[a-1]==t[b-1]: a-=1;b-=1
                    e1,e2=i+K,p+K
                    while e1<len(run) and e2<len(t) and run[e1]==t[e2]: e1+=1;e2+=1
                    key=(ti,b,a)
                    if key in seen: continue
                    seen.add(key)
                    trec=targets[ti][3]; recfrac=(sum(trec[b:e2])/(e2-b)) if trec else 0
                    out.append(dict(q=q,frag=f,line=l,seg=run[a:e1],L=e1-a,target=tlab[ti],tref=targets[ti][2][b],trec=round(recfrac,2)))
# segment frequency across whole target set (how generic is it)
alltext='|'.join(x[1] for x in targets)
for o in out: o['n_occ']=alltext.count(o['seg'])
json.dump(out,open('overlaps.json','w'),ensure_ascii=False)
print('query scrolls',len(Q),'raw hits',len(out))
