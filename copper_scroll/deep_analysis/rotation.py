import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json
exec(open(os.path.join(D,'vocab.py'),encoding="utf-8").read().split("def train(")[0])
F=json.load(open(os.path.join(D,'features.json'),encoding='utf-8')); by={f['entry']:f for f in F}
sizes=[('A',20),('B',16),('C',21),('D',4)]
def chi(E1,E2):
    s=0
    for f in feats:
        a=sum(f in X[i] for i in E1); b=sum(f in X[i] for i in E2); tot=a+b
        if tot==0: continue
        n1,n2=len(E1),len(E2); e1=tot*n1/(n1+n2); e2=tot*n2/(n1+n2); s+=(a-e1)**2/e1+(b-e2)**2/e2
    return s
def U(x,y): return sum((b>a)+0.5*(b==a) for a in x for b in y)
def parts(order):
    out={}; k=0
    for nm,n in sizes: out[nm]=order[k:k+n]; k+=n
    return out
def stats(order):
    P=parts(order)
    v=chi(P['A'],P['B'])+chi(P['A'],P['C'])+chi(P['B'],P['C'])
    x=[by[i]['dig'] for i in P['B'] if by[i]['dig'] is not None]; y=[by[i]['dig'] for i in P['C'] if by[i]['dig'] is not None]
    dep=U(x,y)/(len(x)*len(y)) if x and y else None
    def ew(S):
        e=sum(1 for i in S if 'E' in by[i]['dirs'] and 'W' not in by[i]['dirs']); w=sum(1 for i in S if 'W' in by[i]['dirs'] and 'E' not in by[i]['dirs']); return e,w
    (e1,w1),(e2,w2)=ew(P['A']+P['B']),ew(P['C'])
    eshare=(e1/(e1+w1) if e1+w1 else 0)-(e2/(e2+w2) if e2+w2 else 0)
    return v,dep,eshare
obs=stats(ids); rot=[stats(ids[r:]+ids[:r]) for r in range(1,61)]
for j,nm in enumerate(('vocab chi (A,B,C)','depth P(C>B)','east share (A+B) - C')):
    vals=[s[j] for s in rot if s[j] is not None]
    print(f'{nm}: observed {obs[j]:.3f}; rank {1+sum(v>obs[j] for v in vals)} of {len(vals)+1} (rotations)')
