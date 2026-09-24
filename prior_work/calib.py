import random, re, json
from match import docs, skel
random.seed(0)
bible=[t for lab,t,_ in docs if lab.startswith('MT')]
sect=[t for lab,t,_ in docs if lab.startswith('DSS') and lab.split()[1] in ('1QS','1QHa','1QM','CD','1QpHab','11Q19','4Q400','4Q403','4Q405')]
print('sectarian letters',sum(map(len,sect)))
BIB='|'.join(bible); BIBs='|'.join(skel(t) for t in bible)
res={}
for L in range(3,15):
    for mode in ('ex','sk'):
        hits=0; n=300
        for _ in range(n):
            t=random.choice(sect); i=random.randrange(0,len(t)-L); s=t[i:i+L]
            if mode=='sk': s=skel(s)
            if not s: continue
            if (s in (BIBs if mode=='sk' else BIB)): hits+=1
        res[(L,mode)]=hits/n
for L in range(3,15): print(L, 'exact %.2f'%res[(L,'ex')], ' skeleton %.2f'%res[(L,'sk')])
json.dump({f'{k[0]}_{k[1]}':v for k,v in res.items()},open('calib.json','w'))
