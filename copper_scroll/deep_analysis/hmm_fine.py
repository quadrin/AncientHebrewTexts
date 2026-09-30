import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import numpy as np, json
S=['JO','QB','DS']; K=3
seq=[str(i) for i in range(1,13)]+['12a']+[str(i) for i in range(13,36)]   # entries 1..35
def fb(anch,s):
    T=np.full((K,K),(1-s)/(K-1)); np.fill_diagonal(T,s)
    n=len(seq); E=np.ones((n,K))
    for i,e in enumerate(seq):
        if e in anch: E[i]=0; E[i,S.index(anch[e])]=1
    a=np.zeros((n,K)); c=np.zeros(n); a[0]=E[0]/K; c[0]=a[0].sum(); a[0]/=c[0]
    for i in range(1,n): a[i]=E[i]*(a[i-1]@T); c[i]=a[i].sum(); a[i]/=c[i]
    b=np.ones((n,K))
    for i in range(n-2,-1,-1): b[i]=T@(E[i+1]*b[i+1]); b[i]/=c[i+1]
    post=a*b; post/=post.sum(1,keepdims=True)
    return np.log(c).sum(), post
base={'20':'QB','21':'QB','22':'QB','31':'JO','32':'JO','35':'DS'}
variants={'Achor=Nuweimeh':{**base,'1':'JO','17':'JO'},'Achor=Buqeia':{**base,'1':'QB','17':'QB'}}
extra={'+28 ford (JO)':{'28':'JO'},'+18 Asla (QB)':{'18':'QB'}}
grid=np.linspace(0.5,0.995,100)
out={}
for vn,anch in variants.items():
    for en,ex in [('none',{})]+list(extra.items())+[('both',{**extra['+28 ford (JO)'],**extra['+18 Asla (QB)']})]:
        A={**anch,**ex}
        ll=[fb(A,s)[0] for s in grid]; sb=grid[int(np.argmax(ll))]
        row={}
        for s in (sb,0.8,0.9):
            L,post=fb(A,s)
            row[f's={s:.3f}']=dict(loglik=round(L,3),**{e:{S[k]:round(float(post[seq.index(e),k]),2) for k in range(K)} for e in ('4','6','11','13','14','15','16','18','19')})
        out[f'{vn} | {en}']=dict(s_hat=round(float(sb),3),maxll=round(max(ll),3),detail=row)
for k,v in out.items():
    d=v['detail'][[x for x in v['detail']][0]]
    print(k,'s_hat',v['s_hat'],'maxLL',v['maxll'],' P(same sub-district as Achor) for 4/11/15/19:',
          {e:d[e] for e in ('4','15','19')})
json.dump(out,open(os.path.join(D,'hmm_fine.json'),'w'),indent=1)
# likelihood ratio between Achor placements at common s values
for s in (0.8,0.9,0.95):
    l1=fb(variants['Achor=Nuweimeh'],s)[0]; l2=fb(variants['Achor=Buqeia'],s)[0]
    print(f's={s}: logLik Nuweimeh {l1:.2f}, Buqeia {l2:.2f}, LR(Buqeia:Nuweimeh) = {np.exp(l2-l1):.2f}')
