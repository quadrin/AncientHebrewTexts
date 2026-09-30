"""Download the public Mapzen/AWS Terrarium elevation tiles (zoom 11) for the route test and stitch them into
cache/dem.npz. The cache folder is not committed."""
import math, io, os, urllib.request, numpy as np
from PIL import Image
CACHE=os.path.join(os.path.dirname(os.path.abspath(__file__)),'cache')
Z=11
def tile_xy(lat,lon,z):
    n=2**z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n; return x,y
lat0,lat1,lon0,lon1=31.55,32.60,35.10,35.62
x0,y0=tile_xy(lat1,lon0,Z); x1,y1=tile_xy(lat0,lon1,Z)
tx=range(int(x0),int(x1)+1); ty=range(int(y0),int(y1)+1)
os.makedirs(os.path.join(CACHE,'tiles'),exist_ok=True)
rows=[]
for y in ty:
    row=[]
    for x in tx:
        fn=os.path.join(CACHE,'tiles',f'{Z}_{x}_{y}.png')
        if not os.path.exists(fn):
            urllib.request.urlretrieve(f'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{Z}/{x}/{y}.png',fn)
        a=np.asarray(Image.open(fn).convert('RGB')).astype(float)
        row.append(a[:,:,0]*256+a[:,:,1]+a[:,:,2]/256-32768)
    rows.append(np.hstack(row))
dem=np.vstack(rows)
np.savez(os.path.join(CACHE,'dem.npz'),dem=dem,Z=Z,tx0=tx[0],ty0=ty[0])
print(dem.shape, dem.min(), dem.max(), len(tx)*len(ty),'tiles')
