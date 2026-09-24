import json, re, math, collections
FIN=str.maketrans('ךםןףץ','כמנפצ')
def norm(s): return ''.join(c for c in s.translate(FIN) if 'א'<=c<='ת')
def skel(s): return s.replace('ו','').replace('י','')
# ---- build corpus: list of (label, text, posmap)
docs=[]
bib=json.load(open('bible.json'))
book=collections.defaultdict(list)
for ref,s in bib:
    b=ref.split('.')[0]; book[b].append((ref,norm(s)))
for b,vs in book.items():
    text=''.join(v for _,v in vs); refs=[]
    for r,v in vs: refs+= [r]*len(v)
    docs.append(('MT '+b,text,refs))
dl=json.load(open('dss_lines.json'))
sc=collections.defaultdict(list)
for s,f,l,t,rm,bibl in dl:
    t2=t.translate(FIN); keep=[(c,rm[i] if i<len(rm) else '.') for i,c in enumerate(t2) if 'א'<=c<='ת']
    sc[s].append((f,l,keep))
for s,ls in sc.items():
    text=''.join(c for _,_,k in ls for c,_ in k); refs=[]
    for f,l,k in ls: refs+=[f'{s} {f}:{l}']*len(k)
    docs.append(('DSS '+s,text,refs))
N=sum(len(t) for _,t,_ in docs)
freq=collections.Counter(c for _,t,_ in docs for c in t); tot=sum(freq.values())
P={c:freq[c]/tot for c in freq}
sk=[(lab,skel(t)) for lab,t,_ in docs]; Nsk=sum(len(t) for _,t in sk)
fs=collections.Counter(c for _,t in sk for c in t); ts=sum(fs.values()); PS={c:fs[c]/ts for c in fs}
# skeleton position maps
skmap=[]
for lab,t,refs in docs:
    idx=[i for i,c in enumerate(t) if c not in 'וי']; skmap.append(idx)
def pat_to_regex(p):
    # p: letters, '?' any single letter, [..] class
    out=''; i=0
    while i<len(p):
        if p[i]=='[': j=p.index(']',i); out+=p[i:j+1]; i=j+1
        elif p[i]=='?': out+='.'; i+=1
        else: out+=p[i]; i+=1
    return out
def prob(p,PP):
    pr=1.0; i=0
    while i<len(p):
        if p[i]=='[': j=p.index(']',i); pr*=sum(PP.get(c,0) for c in p[i+1:j]); i=j+1
        elif p[i]=='?': i+=1
        else: pr*=PP.get(p[i],1e-6); i+=1
    return pr
def prep(line,mode):
    line=line.translate(FIN)
    line=re.sub(r'[^א-ת\?\[\]]','',line)
    if mode=='sk':
        line=re.sub(r'\[([^\]]*)\]',lambda m:('['+m.group(1).replace('ו','').replace('י','')+']') if m.group(1).replace('ו','').replace('י','') else '',line)
        line=re.sub(r'[וי]','',line)
    return line
def search(lines, mode='ex', W=(15,140), maxhits=20):
    """lines: fragment reading, list of strings top->bottom. Returns hits with E-values."""
    pats=[prep(l,mode) for l in lines]; pats=[p for p in pats if p]
    PP=P if mode=='ex' else PS; NN=N if mode=='ex' else Nsk
    texts=[t for _,t,_ in docs] if mode=='ex' else [t for _,t in sk]
    # hits of first pattern
    res=[]
    r0=re.compile('(?='+pat_to_regex(pats[0])+')')
    for di,t in enumerate(texts):
        for m in r0.finditer(t):
            pos=[m.start()]; ok=True; prev=m.start()
            for p in pats[1:]:
                rr=re.compile(pat_to_regex(p)); mm=rr.search(t,prev+W[0],prev+W[1]+len(p))
                if not mm: ok=False; break
                pos.append(mm.start()); prev=mm.start()
            if ok: res.append((di,pos))
    # E-value: expected random occurrences of this configuration
    E=NN*prob(pats[0],PP)
    for p in pats[1:]: E*= (W[1]-W[0])*prob(p,PP)
    out=[]
    for di,pos in res[:maxhits]:
        lab,t,refs=docs[di]
        p0=pos[0] if mode=='ex' else skmap[di][pos[0]]
        pe=(pos[-1] if mode=='ex' else skmap[di][min(pos[-1],len(skmap[di])-1)])
        out.append((lab,refs[p0],refs[min(pe,len(refs)-1)],t[max(0,p0-10):p0+40]))
    return {'mode':mode,'E':E,'nhits':len(res),'hits':out}
if __name__=='__main__':
    print('corpus letters',N,'docs',len(docs))
    # calibration: a Qumran line from 1QIsa-a style test and a short string
    for test in [['משפטיעשה'],['ומשפט','ישראל'],['כיריבל','בשרומשפט'],['שמעו','צדק']]:
        for mode in ('ex','sk'):
            r=search(test,mode); print(test,mode,'E=%.3g'%r['E'],'hits',r['nhits'],r['hits'][:2])
