import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,random,itertools,math,re
from math import comb
random.seed(7)
F=json.load(open(os.path.join(D,'features.json'),encoding='utf-8'))
ids=[f['entry'] for f in F]; by={f['entry']:f for f in F}
res={}
def hyper_ge(k,K,n,N):   # P(X>=k), X~Hypergeom(N,K,n)
    return sum(comb(K,i)*comb(N-K,n-i) for i in range(k,min(K,n)+1))/comb(N,n)
def fisher_1s(a,b,c,d):  # table [[a,b],[c,d]], P(top-left >= a)
    return hyper_ge(a,a+b,a+c,a+b+c+d)
# ---------------- T1 name recurrence ----------------
def adj_same(seq):
    s=0
    for x,y in zip(seq,seq[1:]):
        if set(by[x]['names'])&set(by[y]['names']): s+=1
    return s
A=[i for i in ids if by[i]['block']=='A']
BC=[i for i in ids if by[i]['block'] in 'BC' ]   # 20-56
BCD=[i for i in ids if by[i]['block'] in 'BCD' and i!='60']  # 20-59
def perm_adj(seq,n=200000):
    obs=adj_same(seq); ge=le=0; tot=0
    s=list(seq)
    for _ in range(n):
        random.shuffle(s); v=adj_same(s); tot+=v
        ge+= v>=obs; le+= v<=obs
    return obs,tot/n,ge/n,le/n
res['T1_A']=perm_adj(A); res['T1_20_59']=perm_adj(BCD)
# same-name pairs (all pairs) and how many adjacent
def pairs(seq):
    P=0
    for i,j in itertools.combinations(range(len(seq)),2):
        if set(by[seq[i]]['names'])&set(by[seq[j]]['names']): P+=1
    return P
res['T1_pairs']=dict(A=pairs(A),B=pairs(BCD))
# ---------------- T2 orientation ----------------
def EW(block_set):
    e=w=0; el=[];wl=[]
    for i in ids:
        f=by[i]
        if f['block'] not in block_set: continue
        d=set(f['dirs'])
        if 'E' in d and 'W' not in d: e+=1; el.append(i)
        if 'W' in d and 'E' not in d: w+=1; wl.append(i)
    return e,w,el,wl
b=EW('B'); c=EW('C'); a=EW('A')
res['T2a_anchored_B_vs_C']=dict(B=b[:2],C=c[:2],Blist=b[2:],Clist=c[2:],p=fisher_1s(b[0],b[1],c[0],c[1]))
res['T2b_AB_vs_C']=dict(AB=(a[0]+b[0],a[1]+b[1]),C=c[:2],p=fisher_1s(a[0]+b[0],a[1]+b[1],c[0],c[1]))
# aspect only
def asp(block_set):
    e=w=0
    for i in ids:
        f=by[i]
        if f['block'] in block_set:
            e+= 'E' in f['aspect']; w+= 'W' in f['aspect']
    return e,w
ab=asp('AB'); cc=asp('C')
res['T2c_aspect_AB_vs_C']=dict(AB=ab,C=cc,p=fisher_1s(ab[0],ab[1],cc[0],cc[1]))
# N-frame inside A: Koḥlit/ha-Melaḥ entries vs the rest
KM=[i for i in A if set(by[i]['names'])&{'Kohlit','Melah'}]
oth=[i for i in A if i not in KM]
nK=sum('N' in by[i]['dirs'] for i in KM); nO=sum('N' in by[i]['dirs'] for i in oth)
res['T2d_Nframe_A']=dict(KM=KM,N_in_KM=nK,others=len(oth),N_in_others=nO,p=fisher_1s(nK,len(KM)-nK,nO,len(oth)-nO))
# conditional on having any direction word
KMd=[i for i in KM if by[i]['dirs']]; othd=[i for i in oth if by[i]['dirs']]
nKd=sum('N' in by[i]['dirs'] for i in KMd); nOd=sum('N' in by[i]['dirs'] for i in othd)
res['T2d_cond']=dict(KMd=KMd,othd=othd,p=fisher_1s(nKd,len(KMd)-nKd,nOd,len(othd)-nOd))
# Milik variant: entry 15 not Koḥlit
KM2=[i for i in KM if i!='15']; oth2=oth+['15']
n2=sum('N' in by[i]['dirs'] for i in KM2); o2=sum('N' in by[i]['dirs'] for i in oth2)
res['T2d_milik15']=dict(p=fisher_1s(n2,len(KM2)-n2,o2,len(oth2)-o2),counts=(n2,len(KM2),o2,len(oth2)))
# whole-scroll Koḥlit north
kn=[i for i in ids if 'Kohlit' in by[i]['names']]; Nall=sum('N' in by[i]['dirs'] for i in ids)
res['T2e_Kohlit_all']=dict(K=kn,N_total=Nall,n=len(ids),p=hyper_ge(sum('N' in by[i]['dirs'] for i in kn),Nall,len(kn),len(ids)))
# direction counts by block
cnt={}
for i in ids:
    f=by[i]; cnt.setdefault(f['block'],{'E':0,'N':0,'S':0,'W':0,'n':0}); cnt[f['block']]['n']+=1
    for d in f['dirs']: cnt[f['block']][d]+=1
res['dir_counts']=cnt
# ---------------- T3 dig depth ----------------
def mw_perm(x,y,n=200000):
    # U = #pairs y>x (+0.5 ties); permutation two-sided on |U-mean|
    def U(x,y): return sum((b>a)+0.5*(b==a) for a in x for b in y)
    obs=U(x,y); mu=len(x)*len(y)/2; allv=x+y; k=len(x); ext=0; ge=0
    for _ in range(n):
        random.shuffle(allv); u=U(allv[:k],allv[k:])
        ext+= abs(u-mu)>=abs(obs-mu)-1e-9; ge+= u>=obs-1e-9
    return obs,len(x)*len(y),ge/n,ext/n
dig={bl:[by[i]['dig'] for i in ids if by[i]['block']==bl and by[i]['dig'] is not None] for bl in 'ABCD'}
res['T3_depths']=dig
res['T3_B_vs_C']=mw_perm(dig['B'],dig['C'])
res['T3_AB_vs_C']=mw_perm(dig['A']+dig['B'],dig['C'])
import statistics as st
res['T3_summary']={bl:(len(v),round(st.mean(v),2) if v else None,st.median(v) if v else None) for bl,v in dig.items()}
# ---------------- T6 record formula ----------------
rec=[i for i in ids if by[i]['f_ktb']]; dem=[i for i in ids if by[i]['f_dema']]
both=[i for i in rec if i in dem]
res['T6_record']=dict(rec=rec,dema=dem,both=both,p_cooc=hyper_ge(len(both),len(dem),len(rec),len(ids)))
def maxwin(pos,w=6,N=61):
    return max(sum(1 for p in pos if s<=p<s+w) for s in range(N-w+1))
posrec=[ids.index(i) for i in rec]; obs=maxwin(posrec); ge=0; n=200000
for _ in range(n):
    ge+= maxwin(random.sample(range(61),len(rec)))>=obs
res['T6_scan']=dict(obs=obs,p=ge/n)
json.dump(res,open(os.path.join(D,'tests_results.json'),'w'),ensure_ascii=False,indent=1,default=str)
for k,v in res.items(): print(k,':',v)
