import numpy as np, cv2, json, os
ir=json.load(open('q9999_ir.json'))
rows=[]
for i in ir:
    p=f"thumbs/{i['name']}.jpg"
    if not os.path.exists(p): continue
    g=cv2.imread(p,0)
    if g is None: continue
    sc=i['full_width']/g.shape[1]             # full-res px per thumb px
    b=cv2.GaussianBlur(g,(0,0),1)
    # parchment is the brightest material; tissue is mid-grey textured, background black
    fg=b>40
    if fg.sum()<50: rows.append((i['name'],0,0,0,0)); continue
    t=np.percentile(b[fg],60)
    parch=(b>max(t*0.8,70)).astype(np.uint8)
    parch=cv2.morphologyEx(parch,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    cnt,_=cv2.findContours(parch,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    filled=np.zeros_like(parch); cv2.drawContours(filled,cnt,-1,1,-1)
    # ink = dark pixels enclosed by parchment
    ink=((filled==1)&(b<t*0.55)).astype(np.uint8)
    n,l,st,_=cv2.connectedComponentsWithStats(ink)
    area=st[1:,4] if n>1 else np.array([])
    letters=int(((area>=6)&(area<=400)).sum())
    rows.append((i['name'],int(filled.sum()),int(ink.sum()),letters,round(sc,2)))
json.dump(rows,open('ink_rank.json','w'))
rows.sort(key=lambda r:-r[3])
print(len(rows)); 
import collections
print('letter-blob count distribution:',np.percentile([r[3] for r in rows],[25,50,75,90,95,99]))
print(rows[:15])
