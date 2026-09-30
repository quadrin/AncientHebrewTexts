import os
D=os.path.dirname(os.path.abspath(__file__))   # this folder; copper_scroll/ is its parent
import json,re,csv
E=json.load(open(os.path.join(D,'entries_full.json'),encoding='utf-8'))
ent={e['entry']:e for e in E}
# --- fix mid-line split at I 6 (Puech p.179: entry 3 starts inside I 6)
ent['2']['heb']='בנפש בנדבך השלשי עשתות זהב <1+100>'
ent['3']['heb']='בבור הגדול שבחצר הפרסטלין בור בקרקעו סתום בחליא נגד הפתח העליון ככרין תשע מאת'
ent['2']['en']='In the funerary monument, in the third course of stones: ingots of gold, 100.'
L2=ent['2']['lemmas']; ent['2']['lemmas']=L2[:L2.index('בֹּור')]   # I 6 'בבור הגדול שבחצר' belongs to entry 3
ent['3']['en']='In the great cistern that is in the court of the peristyle, in its floor, sealed with sand(?), opposite the upper opening: nine hundred talents.'
order=[e['entry'] for e in E]
# --- block by position (fixed before these tests by the anchor model R1)
def block(x):
    n=int(re.match(r'\d+',x).group())
    if n<=19: return 'A'      # first sub-list (Greek-letter part 1-15 + 16-19)
    if n<=35: return 'B'      # Jericho/desert block (anchored 20-35)
    if n<=56: return 'C'      # Jerusalem & hinterland block (anchored 36-56)
    return 'D'                # north + final Koḥlit
# --- proper place names (hand list; Hebrew forms in the Abegg text)
NAMES={'1':['Achor'],'4':['Kohlit'],'6':['Melah'],'11':['Kohlit'],'13':['Melah'],'14':['Melah'],'15':['Kohlit'],
 '17':['Achor'],'18':['Asla'],'19':['Kohlit'],'20':['Secacah'],'21':['Secacah'],'22':['Secacah','Solomon'],'23':['Solomon'],
 '24':['Kippa','Jericho','Secacah'],'29':['Qi?'],'30':['Haqqos'],'31':['Doq'],'32':['Kozeba'],'33':['BethOsar','Ahor'],'35':['Kidron'],
 '36':['Shaveh'],'37':['Shaveh'],'38':['Natof'],'40':['Horon'],'41':['Qomah'],'43':['BethTamar','Pele'],'44':['Nab'],
 '46':['BethKerem'],'47':['Zered'],'48':['Absalom'],'49':['Rahil'],'51':['Zadok'],'52':['Zadok'],'55':['BethAshuhin'],
 '57':['Gerizim'],'58':['BethSham'],'60':['Kohlit']}
# personal names that are not places: Manos (5), Mattiyah (8), the Queen (27), the High Priest (28)
# --- directions from the Hebrew (consonantal regex), then checked by eye below
def dirs(h):
    d=set()
    if re.search('מזרח',h): d.add('E')
    if re.search('צפו?[נן]',h): d.add('N')
    if re.search('(?<!ק)דרו',h): d.add('S')
    if re.search('מערב',h) or re.search('הצופא ים',h): d.add('W')
    return d
# aspect-type mentions ("facing X", "going in toward X", "entrance/opening from/to X") hand-coded
ASPECT={'1':['E'],'25':['E'],'26':['E'],'36':['W','N'],'39':['E'],'40':['W'],'52':['W'],'56':['W'],'60':['N']}
# --- dig depths (cubits) where the text says dig (חפור/חפר) + number; hand-checked against Hebrew
DIG={'11':4,'12':9,'12a':16,'14':3,'17':3,'20':1,'21':3,'23':3,'24':7,'25':3,'26':9,'27':12,'28':9,'30':6,'31':7,'32':3,
     '34':17,'35':3,'36':24,'37':11,'38':7,'39':8.5,'40':16,'42':7,'46':10,'48':12}
# --- talents (sum of stated talent amounts; None if no talent amount). hand-coded from Hebrew/English
TAL={'1':17,'3':900,'5':40,'6':41,'8':70,'9':10,'11':22,'12a':40,'14':13,'15':14,'16':55,'18':200,'19':70,'20':12,'21':7,
     '23':23,'24':32,'25':42,'26':21,'27':27,'28':22,'29':400,'31':22,'32':82,'34':17,'35':7,'36':65,'37':70,'39':23.5,
     '40':22,'42':9,'44':9,'45':11,'46':62,'47':300,'48':80,'49':17,'53':41,'56':107,'57':61,'58':600,'59':71.33}
rows=[]
for x in order:
    e=ent[x]; h=e['heb']
    f=dict(entry=x,block=block(x),col_line=e['col_line'],names=NAMES.get(x,[]),dirs=sorted(dirs(h)),aspect=ASPECT.get(x,[]),
      dig=DIG.get(x),talents=TAL.get(x),
      f_dig=bool(re.search(r'\bחפו?ר',h)), f_kkryn=bool(re.search('ככרין',h)), f_kk=bool(re.search(r'(^|\s)ככ(\s|$)',h)),
      f_bbw=bool(re.search('בביאתך|בבואך',h)), f_dema=bool(re.search('דמע',h)), f_ktb=bool(re.search('כתבן',h)),
      f_herem=bool(re.search('חר[םמ]',h)), greek=e['greek'], heb=h, en=e['en'], lemmas=e['lemmas'])
    rows.append(f)
json.dump(rows,open(os.path.join(D,'features.json'),'w',encoding='utf-8'),ensure_ascii=False,indent=0)
for f in rows:
    print(f"{f['entry']:>3} {f['block']} dirs={','.join(f['dirs']):6} asp={','.join(f['aspect']):4} dig={str(f['dig']):4} tal={str(f['talents']):6} "
          f"{'D' if f['f_dig'] else '.'}{'K' if f['f_kkryn'] else '.'}{'k' if f['f_kk'] else '.'}{'B' if f['f_bbw'] else '.'}{'M' if f['f_dema'] else '.'}{'R' if f['f_ktb'] else '.'}{'H' if f['f_herem'] else '.'} "
          f"{'/'.join(f['names'])}")
