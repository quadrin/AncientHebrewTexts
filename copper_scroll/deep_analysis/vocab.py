import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,math,random,itertools
F=json.load(open(os.path.join(D,'features.json'),encoding='utf-8'))
ids=[f['entry'] for f in F]; by={f['entry']:f for f in F}
# concept map fixed BEFORE looking at classifier output
C={'cistern':['בֹּור'],'pit':['שִׁית_9','שִׂיחַ_3','שִׁיחַ'],'pool':['בְּרֵכָה','אשׁיח','אשׁוח'],
 'conduit':['אַמָּה_2','מזקה','בִּיב','בִּיבָה','זרב','יְצִיאָה'],'court':['חָצֵר','פרסטל'],
 'gate_wall_threshold':['שַׁעַר_1','חֹומָה','סַף_2'],'corner':['פִּנָּה','מִקְצֹועַ'],'pillar_portico':['עַמּוּד','אסטאן','אכסדרן'],
 'chamber':['צְרִיחַ','מִשְׁכָּב','עֲלִיָּה','מְקֵרָה'],'building':['בַּיִת_1','בֵּית','אֹוצָר','מִשְׁכָּן','מִשְׁמָרָה','מְצָד','שֹׁובַךְ_9'],
 'tomb_monument':['קֶבֶר','נֶפֶשׁ','יָד'],'cave':['מְעָרָה_1'],'cairn_heap':['יְגָר','רגם_9'],
 'valley_wadi_gorge':['עֵמֶק','גַּיְא','נַחַל_1','צֹוק_9'],'rock_stone':['סֶלַע','אֶבֶן','שֵׁן_1','סֶדֶק','מְסַמָּא','שַׂכִּין'],
 'ruin_mound':['חרובה_1','תֵּל'],'steps':['מַעֲלָה'],'ledge_course':['רֹובֶד','נִדְבָּךְ','חַבְלָא'],'road_ford':['דֶּרֶךְ','מגזה'],
 'spring_water':['מַבּוּעַ','מַיִם'],'trench':['חָרִיץ_9'],'field_garden':['שֶׁלֶף_9','גַּנָּה','דֹּור_1']}
inv={l:k for k,v in C.items() for l in v}
def concepts(i):
    s={inv[l] for l in by[i]['lemmas'] if l in inv}
    if i in ('47','49'): s.add('pool')      # ים = basin in 47, 49 (in 40 it is the direction 'sea')
    return s
X={i:concepts(i) for i in ids}
blk={i:by[i]['block'] for i in ids}
B=[i for i in ids if blk[i]=='B']; Cc=[i for i in ids if blk[i]=='C']; A=[i for i in ids if blk[i]=='A']
feats=sorted(C)
def train(pos,neg,alpha=1.0):
    th={}
    for f in feats:
        p=(sum(f in X[i] for i in pos)+alpha)/(len(pos)+2*alpha)
        q=(sum(f in X[i] for i in neg)+alpha)/(len(neg)+2*alpha)
        th[f]=(p,q)
    return th
def llr(i,th):   # log P(x|B)/P(x|C), Bernoulli NB over all features
    s=0
    for f in feats:
        p,q=th[f]
        s+= math.log(p/q) if f in X[i] else math.log((1-p)/(1-q))
    return s
def llr_present(i,th):  # only features present (multinomial-like), robust to absence
    return sum(math.log(th[f][0]/th[f][1]) for f in X[i])
out={}
for name,fn in (('bernoulli',llr),('present_only',llr_present)):
    correct=0; det=[]
    for i in B+Cc:
        pos=[j for j in B if j!=i]; neg=[j for j in Cc if j!=i]
        th=train(pos,neg); v=fn(i,th); pred='B' if v>0 else ('C' if v<0 else '?')
        correct+= pred==blk[i]; det.append((i,blk[i],round(v,2)))
    th=train(B,Cc)
    out[name]=dict(loo_acc=f"{correct}/{len(B+Cc)}",loo=det,A={i:(round(fn(i,th),2),sorted(X[i])) for i in A},
                   D={i:round(fn(i,th),2) for i in ids if blk[i]=='D'})
# permutation check of LOO accuracy (labels shuffled)
def loo_acc(labels,fn):
    c=0
    for i in B+Cc:
        pos=[j for j in B+Cc if labels[j]=='B' and j!=i]; neg=[j for j in B+Cc if labels[j]=='C' and j!=i]
        th=train(pos,neg); v=fn(i,th); c+= ('B' if v>0 else 'C')==labels[i]
    return c
random.seed(3)
for name,fn in (('bernoulli',llr),('present_only',llr_present)):
    obs=loo_acc(blk,fn); ge=0; n=2000; L=[blk[i] for i in B+Cc]
    for _ in range(n):
        random.shuffle(L); lab=dict(zip(B+Cc,L)); ge+= loo_acc(lab,fn)>=obs
    out[name]['perm_p']=ge/n
th=train(B,Cc)
out['feature_table']={f:(sum(f in X[i] for i in A),sum(f in X[i] for i in B),sum(f in X[i] for i in Cc),round(math.log(th[f][0]/th[f][1]),2)) for f in feats}
json.dump(out,open(os.path.join(D,'vocab_results.json'),'w'),ensure_ascii=False,indent=1)
for k in ('bernoulli','present_only'):
    print(k,out[k]['loo_acc'],'perm p',out[k]['perm_p']); print(' A:',out[k]['A']); print(' D:',out[k]['D'])
print('feature: (A,B,C, logratio B/C)')
for f,v in out['feature_table'].items(): print(' ',f,v)
