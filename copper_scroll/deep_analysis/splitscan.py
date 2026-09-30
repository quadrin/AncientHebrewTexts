import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,math,statistics as st
exec(open(os.path.join(D,'vocab.py'),encoding="utf-8").read().split("def train(")[0])
F=json.load(open(os.path.join(D,'features.json'),encoding='utf-8')); by={f['entry']:f for f in F}
seg=[i for i in ids if by[i]['block'] in 'BC']   # 20..56 (37 entries)
def U(x,y): return sum((b>a)+0.5*(b==a) for a in x for b in y)
def depth_stat(L,R):
    x=[by[i]['dig'] for i in L if by[i]['dig'] is not None]; y=[by[i]['dig'] for i in R if by[i]['dig'] is not None]
    if len(x)<4 or len(y)<4: return None
    return U(x,y)/(len(x)*len(y))      # P(right deeper)
def ew_stat(L,R):
    def cnt(S):
        e=sum(1 for i in S if 'E' in by[i]['dirs'] and 'W' not in by[i]['dirs']); w=sum(1 for i in S if 'W' in by[i]['dirs'] and 'E' not in by[i]['dirs']); return e,w
    (e1,w1),(e2,w2)=cnt(L),cnt(R)
    if e1+w1==0 or e2+w2==0: return None
    return e1/(e1+w1)-e2/(e2+w2)       # east share left minus right
def chi(E1,E2):
    s=0
    for f in feats:
        a=sum(f in X[i] for i in E1); b=sum(f in X[i] for i in E2); tot=a+b
        if tot==0: continue
        n1,n2=len(E1),len(E2); e1=tot*n1/(n1+n2); e2=tot*n2/(n1+n2); s+=(a-e1)**2/e1+(b-e2)**2/e2
    return s
out={}
for name,fn in (('depth',depth_stat),('eastshare',ew_stat),('vocab',chi)):
    vals=[]
    for k in range(6,len(seg)-5):          # both sides >= 6 entries
        v=fn(seg[:k],seg[k:])
        if v is not None: vals.append((seg[k-1]+'|'+seg[k],round(v,3)))
    obs=[v for s,v in vals if s=='35|36'][0]
    rank=1+sum(1 for s,v in vals if v>obs)
    out[name]=dict(obs=obs,rank=rank,of=len(vals),top=sorted(vals,key=lambda t:-t[1])[:5])
    print(name,out[name])
json.dump(out,open(os.path.join(D,'splitscan.json'),'w'))
