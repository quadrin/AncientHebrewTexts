import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,random,math,itertools
exec(open(os.path.join(D,'vocab.py'),encoding="utf-8").read().split("def train(")[0])
random.seed(11)
def stat(lab,g1,g2):
    # chi-square statistic on concept-presence counts, groups g1 vs g2 (entries labelled)
    E1=[i for i in lab if lab[i]==g1]; E2=[i for i in lab if lab[i]==g2]
    s=0
    for f in feats:
        a=sum(f in X[i] for i in E1); b=sum(f in X[i] for i in E2)
        n1,n2=len(E1),len(E2); tot=a+b
        if tot==0: continue
        e1=tot*n1/(n1+n2); e2=tot*n2/(n1+n2)
        s+=(a-e1)**2/e1+(b-e2)**2/e2
    return s
out={}
for g1,g2 in (('A','B'),('A','C'),('B','C')):
    lab={i:blk[i] for i in ids if blk[i] in (g1,g2)}
    obs=stat(lab,g1,g2); keys=list(lab); vals=[lab[k] for k in keys]; ge=0; n=20000
    for _ in range(n):
        random.shuffle(vals); ge+= stat(dict(zip(keys,vals)),g1,g2)>=obs-1e-9
    out[f'{g1}_vs_{g2}']=(round(obs,2),ge/n)
print(out)
json.dump(out,open(os.path.join(D,'vocab_blocks.json'),'w'))
