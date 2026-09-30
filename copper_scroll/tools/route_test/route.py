"""Least-cost walking-route test of the scroll order. Needs cache/dem.npz from dem.py (public Mapzen/AWS Terrarium tiles)
and tables/phase3_places.csv. Writes registration/sequence_route_results.json. Needs numpy, scikit-image and Pillow.
Write-up: sequence_model_followup_2026-09-30.md, section 1."""
import math, csv, random, itertools, json, os, numpy as np
from skimage.graph import MCP_Geometric
HERE=os.path.dirname(os.path.abspath(__file__)); ROOT=os.path.dirname(os.path.dirname(HERE))
d=np.load(os.path.join(HERE,'cache','dem.npz')); dem=d['dem']; Z=int(d['Z']); tx0=int(d['tx0']); ty0=int(d['ty0'])
def px(lat,lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return int((y-ty0)*256), int((x-tx0)*256)
lat_c=32.0
res=40075016.7*math.cos(math.radians(lat_c))/(2**Z*256)   # metres per pixel
gy,gx=np.gradient(dem,res)
slope=np.hypot(gx,gy)
speed=6*np.exp(-3.5*np.abs(slope+0.05))   # Tobler km/h (isotropic approximation)
speed[dem<-400]=0.05  # Dead Sea surface: effectively impassable
cost=(res/1000)/speed   # hours per pixel step
places={r['place_id']:r for r in csv.DictReader(open(os.path.join(ROOT,'tables','phase3_places.csv'),encoding='utf-8-sig'))}
def pt(pid): r=places[pid]; return px(float(r['lat']),float(r['lon']))
# strict-anchor itinerary in scroll order (entries in brackets)
stops=[('nuweimeh','1,17'),('wadi_qumran','20'),('kh_qumran','21,22'),('kuteif','24'),('doq','31'),('choziba','32'),('mar_saba','35'),
       ('ramat_rahel','46'),('jer_kidron_mon','48'),('jer_se_corner','51'),('jer_kidron_east','52'),('jer_bethesda','55'),('gerizim','57'),('beth_shean','58')]
ids=[s[0] for s in stops]
P=[pt(i) for i in ids]
n=len(P); T=np.zeros((n,n)); D=np.zeros((n,n))
for i in range(n):
    m=MCP_Geometric(cost); cum,_=m.find_costs([P[i]])
    for j in range(n): T[i,j]=cum[P[j]]
    for j in range(n):
        a=places[ids[i]]; b=places[ids[j]]
        la1,lo1,la2,lo2=map(math.radians,[float(a['lat']),float(a['lon']),float(b['lat']),float(b['lon'])])
        D[i,j]=6371*2*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
T=(T+T.T)/2
def plen(order,M): return sum(M[a,b] for a,b in zip(order,order[1:]))
def test(idx,M,label,N=200000,seed=7):
    obs=plen(idx,M); rng=random.Random(seed); k=0; vals=[]
    for _ in range(N):
        o=idx[:]; rng.shuffle(o); v=plen(o,M); vals.append(v); k+= v<=obs
    # best open path by 2-opt restarts
    best=float('inf')
    for r in range(300):
        o=idx[:]; rng.shuffle(o); imp=True
        while imp:
            imp=False
            for i in range(len(o)-1):
                for j in range(i+2,len(o)+1):
                    o2=o[:i]+o[i:j][::-1]+o[j:]
                    if plen(o2,M)<plen(o,M)-1e-9: o=o2; imp=True
        best=min(best,plen(o,M))
    print(f'{label}: scroll order = {obs:.1f}; random median = {np.median(vals):.1f}; best possible ≈ {best:.1f}; p(random ≤ scroll) = {(k+1)/(N+1):.2g}; excess over best = {100*(obs/best-1):.0f}%')
    return obs, float(np.median(vals)), best, (k+1)/(N+1)
res_all={}
print('Stops:', ids)
res_all['all_walk_h']=test(list(range(n)),T,'All 14 anchored stops, walking hours')
res_all['all_km']=test(list(range(n)),D,'All 14 anchored stops, straight-line km')
jb=list(range(7))   # Jericho block + Kidron exit
res_all['jericho_walk_h']=test(jb,T,'Jericho block (1-35), walking hours')
res_all['jericho_km']=test(jb,D,'Jericho block (1-35), straight-line km')
print('\nLeg by leg (walking hours / km):')
for a,b in zip(range(n-1),range(1,n)): print(f'  {ids[a]:>16} -> {ids[b]:<16} {T[a,b]:6.1f} h  {D[a,b]:6.1f} km')
json.dump({'stops':ids,'T':T.tolist(),'D':D.tolist(),'results':res_all},open(os.path.join(ROOT,'registration','sequence_route_results.json'),'w'),indent=1)
