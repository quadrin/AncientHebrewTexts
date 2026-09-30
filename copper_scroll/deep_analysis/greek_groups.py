import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,itertools,math
exec(open(os.path.join(D,'vocab.py'),encoding="utf-8").read().split("def train(")[0])
F=json.load(open(os.path.join(D,'features.json'),encoding='utf-8')); by={f['entry']:f for f in F}
seq=ids[:ids.index('16')+1]          # entries 1..16 (17 entries incl. 12a)
gaps=list(range(len(seq)-1))          # gap g lies between seq[g] and seq[g+1]
cuts={seq.index(x) for x in ('1','4','6','7','9','12a','15')}   # letters close these entries
print('entries',seq); print('cut gaps after',[seq[g] for g in sorted(cuts)])
def feat(i):
    f=by[i]
    return dict(named=bool(set(f['names'])&{'Achor','Kohlit','Melah'}),N='N' in f['dirs'],dig=f['f_dig'],
                kkryn=f['f_kkryn'],talent=f['talents'] is not None,gold='זהב' in f['heb'],
                builtT=bool(X[i]&{'court','gate_wall_threshold','chamber','corner'}))
FV={i:feat(i) for i in seq}
def jacc(a,b):
    u=X[a]|X[b]; return 1-len(X[a]&X[b])/len(u) if u else 0
def diss(g):
    a,b=seq[g],seq[g+1]
    return sum(FV[a][k]!=FV[b][k] for k in FV[a])+jacc(a,b)
D=[diss(g) for g in gaps]
obs=sum(D[g] for g in cuts)/len(cuts)-sum(D[g] for g in gaps if g not in cuts)/(len(gaps)-len(cuts))
cnt=0;tot=0
for comb_ in itertools.combinations(gaps,len(cuts)):
    s=set(comb_); v=sum(D[g] for g in s)/len(s)-sum(D[g] for g in gaps if g not in s)/(len(gaps)-len(s))
    tot+=1; cnt+= v>=obs-1e-12
print('combined dissimilarity: cut-minus-noncut =',round(obs,3),' exact p =',round(cnt/tot,4),'of',tot)
# per-feature: are changes enriched at cut gaps?
from math import comb
def hyp(k,K,n,N): return sum(comb(K,i)*comb(N-K,n-i) for i in range(k,min(K,n)+1))/comb(N,n)
for k in FV[seq[0]]:
    ch=[g for g in gaps if FV[seq[g]][k]!=FV[seq[g+1]][k]]
    kc=len([g for g in ch if g in cuts])
    print(f'{k:7s} changes at {len(ch):2d} of {len(gaps)} gaps; at cuts {kc} of {len(cuts)}; P(>=)={hyp(kc,len(ch),len(cuts),len(gaps)):.3f}; P(<=)={1-hyp(kc+1,len(ch),len(cuts),len(gaps)):.3f}')
print('table:')
for i in seq: print(i,{k:int(v) for k,v in FV[i].items()},sorted(X[i]))
