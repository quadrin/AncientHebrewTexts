import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import math,csv,itertools,json,numpy as np
from skimage.graph import MCP_Geometric
d=np.load(os.environ.get('DEM_NPZ',os.path.join(D,'dem.npz'))); dem=d['dem']; Z=int(d['Z']); tx0=int(d['tx0']); ty0=int(d['ty0'])
def px(lat,lon):
    n=2**Z; x=(lon+180)/360*n; y=(1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n
    return int((y-ty0)*256), int((x-tx0)*256)
res=40075016.7*math.cos(math.radians(32.0))/(2**Z*256)
gy,gx=np.gradient(dem,res); slope=np.hypot(gx,gy)
speed=6*np.exp(-3.5*np.abs(slope+0.05)); speed[dem<-400]=0.05; cost=(res/1000)/speed
places={r['place_id']:r for r in csv.DictReader(open(os.path.join(D,'..','tables','phase3_places.csv'),encoding='utf-8-sig'))}
def run(stops,label):
    P=[px(float(places[s]['lat']),float(places[s]['lon'])) for s,_ in stops]; n=len(P)
    T=np.zeros((n,n)); D=np.zeros((n,n))
    for i in range(n):
        cum,_=MCP_Geometric(cost).find_costs([P[i]])
        for j in range(n):
            T[i,j]=cum[P[j]]
            a,b=places[stops[i][0]],places[stops[j][0]]
            la1,lo1,la2,lo2=map(math.radians,[float(a['lat']),float(a['lon']),float(b['lat']),float(b['lon'])])
            D[i,j]=6371*2*math.asin(math.sqrt(math.sin((la2-la1)/2)**2+math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2))
    T=(T+T.T)/2
    out={}
    for nm,M in (('walk_h',T),('km',D)):
        L=lambda o: sum(M[a,b] for a,b in zip(o,o[1:]))
        obs=L(list(range(n))); allv=[L(o) for o in itertools.permutations(range(n))]
        p=sum(v<=obs+1e-12 for v in allv)/len(allv)
        out[nm]=dict(scroll=round(obs,2),median=round(float(np.median(allv)),2),best=round(min(allv),2),p_exact=round(p,4),n_orders=len(allv))
        best=min(itertools.permutations(range(n)),key=L)
        out[nm]['best_order']=[stops[i][1] for i in best]
    print(label,[s[1] for s in stops]); print(' ',out)
    return out
R={}
R['strict']=run([('ramat_rahel','46'),('jer_kidron_mon','48'),('jer_se_corner','51'),('jer_kidron_east','52'),('jer_bethesda','55')],'Jerusalem block, strict anchors')
R['lenient']=run([('natuf','38'),('ramat_rahel','46'),('jer_kidron_mon','48'),('jer_siloam','49'),('jer_se_corner','51'),('jer_kidron_east','52'),('jer_bethesda','55')],'Jerusalem block, + Natuf 38 and Siloam 49')
R['jericho_exact']=run([('nuweimeh','1,17'),('wadi_qumran','20'),('kh_qumran','21,22'),('kuteif','24'),('doq','31'),('choziba','32'),('mar_saba','35')],'Jericho block (exact enumeration)')
json.dump(R,open(os.path.join(D,'route_jer.json'),'w'),indent=1)
