import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,random,math
exec(open(os.path.join(D,'vocab.py'),encoding="utf-8").read().split("def train(")[0])
random.seed(5)
seq=ids[:]   # 61 entries in order
def chi(E1,E2):
    s=0
    for f in feats:
        a=sum(f in X[i] for i in E1); b=sum(f in X[i] for i in E2); tot=a+b
        if tot==0: continue
        n1,n2=len(E1),len(E2); e1=tot*n1/(n1+n2); e2=tot*n2/(n1+n2)
        s+=(a-e1)**2/e1+(b-e2)**2/e2
    return s
def scan(order,w):
    return [chi(order[max(0,k-w):k],order[k:k+w]) for k in range(1,len(order))]  # split before position k
res={}
for w in (6,8,10):
    obs=scan(seq,w)
    # null: shuffle entries (destroys order), record max of scan and value distribution
    null_max=[]; null_vals=[]
    for _ in range(2000):
        s=seq[:]; random.shuffle(s); v=scan(s,w); null_max.append(max(v)); null_vals.extend(v)
    null_vals.sort(); null_max.sort()
    def pt(x): # pointwise p
        import bisect; return 1-bisect.bisect_left(null_vals,x)/len(null_vals)
    peaks=sorted(range(len(obs)),key=lambda k:-obs[k])[:8]
    res[w]=[(seq[k],seq[k+1],round(obs[k],1),round(pt(obs[k]),4),round(sum(m>=obs[k] for m in null_max)/len(null_max),3)) for k in peaks]
    res[f'{w}_at_boundaries']={b:(round(obs[seq.index(b[1])-1],1),round(pt(obs[seq.index(b[1])-1]),4)) for b in [('19','20'),('35','36'),('56','57'),('15','16')]} if False else {f'{a}|{b}':(round(obs[seq.index(b)-1],1),round(pt(obs[seq.index(b)-1]),4)) for a,b in [('19','20'),('35','36'),('56','57'),('15','16')]}
for k,v in res.items(): print(k,v)
json.dump({str(k):v for k,v in res.items()},open(os.path.join(D,'changepoint.json'),'w'),ensure_ascii=False)
