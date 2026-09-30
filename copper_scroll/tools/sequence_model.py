"""Sequence (hidden Markov) model of the Copper Scroll's regional order.
Input registration/sequence_model_entries.json is built from text/translation_en.json,
tables/entry_concordance.csv and tables/phase3_site_index.csv (one object per Puech entry, in scroll order).
Output: registration/sequence_model_results.json. Needs numpy. Run from any directory:
  python tools/sequence_model.py
Write-up: sequence_model_and_new_leads_2026-09-30.md.
States: O = Jericho / Qumran / lower Jordan; D = Judean desert interior; J = Jerusalem; N = north.
Anchors: entries whose toponym is placed by a source outside the scroll. Everything else is inferred from order only.
"""
import json, random, math, itertools, os
import numpy as np
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E_ = json.load(open(os.path.join(ROOT, 'registration', 'sequence_model_entries.json'), encoding='utf-8'))
order = [e['entry'] for e in E_]
R = ['O','D','J','N']   # O = Jericho/Qumran/lower Jordan; D = Judean desert interior; J = Jerusalem; N = north
# strict anchors: a toponym in the text whose region is fixed by a source outside the scroll
strict = {'1':'O','17':'O','20':'O','21':'O','22':'O','24':'O','31':'O','32':'O',
          '35':'D','36':'J','37':'J','46':'J','48':'J','51':'J','52':'J','55':'J','57':'N','58':'N'}
def variant(**kw):
    a = dict(strict); a.update({k:v for k,v in kw.items()})
    return {k:v for k,v in a.items() if v}
def fb(anchors, s):
    n=len(order); K=len(R)
    T=np.full((K,K),(1-s)/(K-1)); np.fill_diagonal(T,s)
    Em=np.ones((n,K))
    for i,e in enumerate(order):
        if e in anchors: Em[i]=0; Em[i,R.index(anchors[e])]=1
    a=np.zeros((n,K)); c=np.zeros(n)
    a[0]=Em[0]/K; c[0]=a[0].sum(); a[0]/=c[0]
    for i in range(1,n):
        a[i]=(a[i-1]@T)*Em[i]; c[i]=a[i].sum(); a[i]/=c[i]
    b=np.ones((n,K))
    for i in range(n-2,-1,-1):
        b[i]=T@(Em[i+1]*b[i+1]); b[i]/=b[i].sum()
    p=a*b; p/=p.sum(1,keepdims=True)
    return p, np.log(c).sum()
def fit(anchors):
    grid=np.linspace(0.5,0.995,100)
    ll=[fb(anchors,s)[1] for s in grid]
    return grid[int(np.argmax(ll))]
def changes(seq): return sum(1 for x,y in zip(seq,seq[1:]) if x!=y)
def perm_test(anchors, n=200000, seed=1):
    seq=[anchors[e] for e in order if e in anchors]
    obs=changes(seq); rng=random.Random(seed); k=0
    for _ in range(n):
        s=seq[:]; rng.shuffle(s)
        if changes(s)<=obs: k+=1
    return obs, len(seq), (k+1)/(n+1)
def report(name, anchors):
    s=fit(anchors); p,_=fb(anchors,s)
    obs,m,pv=perm_test(anchors)
    print(f'\n=== {name}: {m} anchors, {obs} region changes; permutation p={pv:.2g}; fitted stay-prob s={s:.3f}')
    # leave-one-out
    hits=0; loo=[]
    for e in anchors:
        a2={k:v for k,v in anchors.items() if k!=e}
        p2,_=fb(a2,fit(a2)); i=order.index(e); pr=p2[i]
        pred=R[int(np.argmax(pr))]; hits+= pred==anchors[e]
        loo.append((e,anchors[e],pred,round(float(pr[R.index(anchors[e])]),2)))
    print(f'leave-one-out: {hits}/{len(anchors)} anchors recovered from order alone')
    print('  misses:', [x for x in loo if x[1]!=x[2]])
    rows=[]
    for i,e in enumerate(order):
        if e in anchors: continue
        rows.append((e, {r:round(float(p[i][j]),2) for j,r in enumerate(R)}))
    return rows
out={}
out['strict']=report('STRICT anchors', strict)
for e,d in out['strict']: print(f'  {e:>4}: '+'  '.join(f'{r}={d[r]:.2f}' for r in R))
out['buqeia']=report('Achor=Buqeia & Secacah=Buqeia (D)', variant(**{'1':'D','17':'D','20':'D','21':'D','22':'D'}))
out['lenient']=report('LENIENT (+Siloam 49 J, +East Gate 9,10 J, +Aḥor 33 O)', variant(**{'49':'J','9':'J','10':'J','33':'O'}))
for e,d in out['lenient']:
    if e in ('2','3','4','5','6','7','8','11','12','12a','13','14','15','16','18','19'): print(f'  {e:>4}: '+'  '.join(f'{r}={d[r]:.2f}' for r in R))
json.dump(out,open(os.path.join(ROOT,'registration','sequence_model_results.json'),'w'),indent=1)
