import json, re, urllib.request, io, os, sys
import numpy as np
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
ir={i['name']:i for i in json.load(open('q9999_ir.json'))}
def get(u,t=60):
    return urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=t).read()
def full(name):
    p=f'full/{name}.png'
    if os.path.exists(p): return p
    base=ir[name]['url'].replace('http://','https://')
    x=get(base+'=g').decode()
    lv=re.findall(r'num_tiles_x="(\d+)" num_tiles_y="(\d+)" inverse_scale="(\d+)" empty_pels_x="(\d+)" empty_pels_y="(\d+)"',x)
    tw=int(re.search(r'tile_width="(\d+)"',x).group(1)); z=len(lv)-1
    nx,ny,_,ex,ey=map(int,lv[-1])
    W,H=nx*tw-ex, ny*tw-ey
    canvas=Image.new('L',(nx*tw,ny*tw))
    def t(xy):
        a,b=xy; return a,b,Image.open(io.BytesIO(get(f'{base}=x{a}-y{b}-z{z}-nt0'))).convert('L')
    with ThreadPoolExecutor(8) as ex_: 
        for a,b,im in ex_.map(t,[(a,b) for a in range(nx) for b in range(ny)]): canvas.paste(im,(a*tw,b*tw))
    canvas=canvas.crop((0,0,W,H)); canvas.save(p); return p
def crop_view(name, out, maxw=1100, pad=40):
    g=np.array(Image.open(full(name)))
    import cv2
    b=cv2.GaussianBlur(g,(0,0),3); fg=b>40; t=np.percentile(b[fg],60)
    parch=(b>max(t*0.8,70)).astype(np.uint8)
    n,l,st,_=cv2.connectedComponentsWithStats(parch); k=1+np.argmax(st[1:,4])
    x,y,w,h=st[k,:4]; c=g[max(0,y-pad):y+h+pad, max(0,x-pad):x+w+pad]
    im=Image.fromarray(c); 
    if im.width>maxw: im=im.resize((maxw,int(im.height*maxw/im.width)),Image.LANCZOS)
    im.save(out,quality=92); return im.size, g.shape
if __name__=='__main__':
    for n in sys.argv[1:]: print(n, crop_view(n, f'view_{n}.jpg'))
