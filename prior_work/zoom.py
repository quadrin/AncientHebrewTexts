import sys, numpy as np, cv2
from PIL import Image, ImageDraw
from fetch import full
def tight(n, maxw=1400):
    g=np.array(Image.open(full(n))); b=cv2.GaussianBlur(g,(0,0),3); fg=b>40; t=np.percentile(b[fg],60)
    parch=(b>max(t*0.8,70)).astype(np.uint8); k,l,st,_=cv2.connectedComponentsWithStats(parch); i=1+np.argmax(st[1:,4])
    x,y,w,h=st[i,:4]; c=g[max(0,y-20):y+h+20,max(0,x-20):x+w+20]
    # local contrast
    c=cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8)).apply(c)
    im=Image.fromarray(c); s=min(1.0,maxw/im.width); return im.resize((int(im.width*s),int(im.height*s)),Image.LANCZOS)
if __name__=='__main__':
    out=sys.argv[1]; names=sys.argv[2:]; ims=[tight(n) for n in names]
    W=max(i.width for i in ims); H=sum(i.height+22 for i in ims)
    S=Image.new('L',(W,H),30); d=ImageDraw.Draw(S); y=0
    for n,i in zip(names,ims): d.text((4,y+4),n,fill=255); S.paste(i,(0,y+22)); y+=i.height+22
    S.save(out,quality=92); print(S.size)
