import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
# Rebuilds dem.npz for route_jer.py. The original dem.py (an earlier bundle) is not in the repository;
# this follows the terrain described in sequence_model_followup_2026-09-30.md §1: Mapzen/AWS Terrarium
# tiles at zoom 11, 32 tiles covering 31.55-32.60 N and 35.10-35.62 E.
import io,math,urllib.request,numpy as np
from PIL import Image
Z=11; S,N,W,E=31.55,32.60,35.10,35.62
URL='https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
def tile(lat,lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return int(x),int(y)
tx0,ty0=tile(N,W); tx1,ty1=tile(S,E)
dem=np.zeros(((ty1-ty0+1)*256,(tx1-tx0+1)*256))
for ty in range(ty0,ty1+1):
    for tx in range(tx0,tx1+1):
        a=np.asarray(Image.open(io.BytesIO(urllib.request.urlopen(URL.format(z=Z,x=tx,y=ty)).read())).convert('RGB'),dtype=float)
        dem[(ty-ty0)*256:(ty-ty0+1)*256,(tx-tx0)*256:(tx-tx0+1)*256]=a[...,0]*256+a[...,1]+a[...,2]/256-32768
np.savez_compressed(os.path.join(D,'dem.npz'),dem=dem,Z=Z,tx0=tx0,ty0=ty0)
print(f'{(tx1-tx0+1)*(ty1-ty0+1)} tiles, x {tx0}-{tx1}, y {ty0}-{ty1}; elevation {dem.min():.0f} to {dem.max():.0f} m')
