import csv, json
from pathlib import Path

root=Path(__file__).resolve().parent
def rows(name):
    return list(csv.DictReader((root/name).open(encoding='utf-8-sig',newline='')))

# Short factual paraphrases; these are not quotations or a new critical edition.
records='''1|Valley of Achor|עמק עכור|A ruin and a flight of steps in the Valley of Achor.
2|The monument|נפש|A monument and a course of masonry.
3|The great courtyard|חצר|A cistern, a courtyard and a colonnaded space.
4|The mound of Kohlit|כחלת|A mound, water conduit and immersion cave at Kohlit.
5|The winding stair|מסבה|A winding stair and an adjoining passage or refuge.
6|The Millo cistern|מלה|A cistern and steps at a place interpreted as the Millo or an esplanade.
7|House of Measures|בית המדה|A cave and a stone course at the House of Measures.
8|The courtyard cistern|חצר|A cistern in a courtyard, with a chamber or tower nearby.
9|The eastern gate|השער המזרחי|A cistern with a channel opposite the eastern gate.
10|The eastern wall|חומה|A cistern beneath a wall, beside a rock spur and threshold.
11|Kohlit's pool|כחלת|A corner of a pool associated with Kohlit.
12|The courtyard corner|חצר|A corner within a courtyard.
12a|The adjoining corner|פנה|Another corner, separated as entry 12a in this numbering.
13|The Millo pit|מלה|A pit at a corner or entrance of the Millo or esplanade.
14|The Millo tomb|מלה|A tomb and a slab or cover associated with the Millo.
15|Kohlit's great cistern|כחלת|A cistern and a pillar at Kohlit.
16|The entering conduit|אמת המים|A conduit and a pool approached on entering; the location needs restoration.
17|Achor's two features|עמק עכור|Two features in Achor, read as cavities, tamarisks or buildings by different editors.
18|Asla|העצלא|An earth pit in the area called Asla.
19|The Kohlit pit|כחלת|A pit associated with Kohlit.
20|Valley of Sekakah|סככא|A cairn or dam in the valley of Sekakah.
21|Sekakah|סככא|The head of a water conduit associated with Sekakah; the link and stone landmark are partly restored.
22|Solomon's reservoir|שלומו|A fissure in Sekakah east of a reservoir associated with Solomon.
23|Solomon or Shallum’s channel|שלומו|A trench or channel associated with Solomon or Shallum, directed toward a large landmark read as a boulder or mound.
24|The Kippa ravine|נחל הכפא|A tomb in the Kippa ravine, on the approach from Jericho toward Sekakah.
25|Cave of the Column|מערה|A cave entrance distinguished by a column.
26|The facing cave|מערה|A cave, its entrance and an adjacent mound or clod.
27|The queen's residence|המלכא|A dwelling or enclosure associated with a queen.
28|The high priest's ford|מגזת|A cairn at a crossing associated with the high priest.
29|The collected waters|קיבוץ|A conduit, a reservoir and a collection of water; Jericho appears in a restoration.
30|House of Haqqoz|בית הקוץ|A cave next to the cool room of a house associated with Haqqoz.
31|Doq|דוק|A corner at Doq, read as a fortress or as a drying floor.
32|Koziba|כוזבא|A water outlet and a retaining wall at Koziba.
33|Ahiyah's treasury|אחיה|A conduit, a treasury and a road; the personal name is disputed.
34|The inscribed stone|כתב חרת|A valley marked by an inscribed stone.
35|Kidron|קדרון|A cairn at the mouth of the Kidron gorge.
36|Valley of Shaveh|השוא|Fallow land and an underground chamber in Shaveh.
37|Shaveh's irrigated land|השוא|Irrigated land and a chamber or stone marker in Shaveh.
38|Netophah|הנטף|A spring associated with a dovecote or cave opening.
39|The terrace|חבלה|A terrace facing a chamber or tower.
40|Horon or the Horites|החורין|Burial chambers facing the Sea (west) or south, and a channel; the name and the direction have competing readings.
41|The damaged entry|קומעה|A very short, uncertain expression. No candidate has a defensible map location.
42|The sounding conduit|ביב|A conduit and the sound of water; one reading supplies the name Kephar Nebo.
43|Beth Tamar|בית תמר|A pit, exposed rock and a place read as Beth Tamar.
44|The fort's upper room|מצד|A fort, an upper room and a dovecote.
45|The ravine cistern|בור|A cistern and channels in a ravine.
46|Beth ha-Kerem|בית הכרם|A large reservoir at Beth ha-Kerem.
47|The spring basin|מעין|A spring, basin and chamber in a valley whose name is disputed.
48|Absalom's monument|יד אבשלום|A freestanding monument associated with Absalom.
49|Siloam?|שלוח|A water installation and a trough; the reading that names Siloam is disputed.
50|Zadok's court|צדוק|A corner of the garden or court associated with Zadok.
51|Zadok's tomb setting|צדוק|A tomb with a vestibule and pillar, associated with Zadok's surroundings.
52|The rock opposite Zadok|צדוק|A west-facing rock opposite Zadok's court or garden.
53|The gallery tomb|סבין|A tomb associated with galleries.
54|The Jericho people's tomb|ירחו|A tomb associated with people from Jericho.
55|House of the two pools|בית אשוחין|A double reservoir with a smaller basin; Bethesda depends on an editorial identification.
56|The burial chamber|בית המשכב|A burial complex with recesses, a cave, entrance stones and a platform.
57|Mount Gerizim|הר גריזין|A step and an upper pit on Mount Gerizim.
58|Beth Sham|בית שם|The mouth of a spring at a place usually compared with Beth Shean.
59|Bezek?|הבזך|A great conduit; the Bezek reading competes with other readings.
60|The final Kohlit entry|כחלת|A pit, tomb and opening associated with Kohlit; Lefkovits also reads Janoah.'''
descriptions={r.split('|')[0]:r.split('|')[1:] for r in records.splitlines()}
places={}
for r in rows('phase3_places.csv'):
    places[r['place_id']]={'id':r['place_id'],'name':r['name'],'lat':float(r['lat']) if r['lat'] else None,'lon':float(r['lon']) if r['lon'] else None,'precision':r['precision'],'kind':r['kind'],'region':r['map_group'],'note':r['note'],'source':r['coord_source']}
short_names={'kh_qumran':'Khirbet Qumran','wadi_qumran':'Wadi Qumran','doq':'Jebel Qarantal / Doq','choziba':'Choziba · Wadi Qelt','jer_siloam':'Silwan pool & tunnel outlet','jer_bethesda':'Bethesda · St Anne’s','ramat_rahel':'Ramat Rahel','gerizim':'Mount Gerizim','beth_shean':'Beth Shean / Scythopolis','nuweimeh':'Wadi Nuweimeh','ain_duk':'Ain Duk springs','tell_es_sultan':'Tell es-Sultan','jericho_area':'Jericho oasis','jericho_palaces':'Jericho royal palaces','hyrcania':'Hyrcania / Khirbet el-Mird','mar_saba':'Kidron gorge · Mar Saba','natuf':'Ain en-Natuf · Khareitun','ibziq':'Khirbet Ibziq','buqeia':'Buqeia plateau','jer_east_gate':'Eastern gate & wall','jer_kidron_mon':'Kidron monuments','jer_kidron_east':'Silwan necropolis','jer_temple':'Temple enclosure','jer_se_corner':'Southeastern Temple slope','jer_south_wall':'Southern Temple wall','jer_baqa':'Baqa plain','jer_shaveh':'Shaveh / King’s Valley','jer_bir_ayyub':'Bir Ayyub / En-Rogel','jer_tyropoeon':'Tyropoeon valley','jer_tombs_kings':'Tombs of the Kings','jer_gethsemane':'Gethsemane','tell_el_ful':'Tell el-Ful','asla':'Asla area','kuteif':'Wadi Kuteif','jordan_ford':'Lower Jordan crossing','tekoa_herodium':'Tekoa–Herodium sector','tell_el_qos':'Tell el-Qos'}
for k,p in places.items(): p['shortName']=short_names[k]
# Revisions after Phase 3 (the Phase 3 tables keep their original assessment).
# 29 September 2026: entry40_bethhoron_review.md adds Beth-Horon as a possible place for entry 40.
places['beth_horon']={'id':'beth_horon','name':'Upper Beth-Horon (Beit ʿUr el-Foqa)','lat':31.88530,'lon':35.11341,'precision':'~300 m','kind':'point','region':'region','note':'Village anchor from the IAA Benjamin survey (sites 28/143). Lower Beth-Horon (Beit ʿUr et-Taḥta) is equally compatible and has the only tomb with pottery of the period. Not a feature location.','source':'IAA survey, Ramallah–Benjamin map 83/1, sites 28 and 143','shortName':'Upper Beth-Horon · Beit Ur'}
revised_candidates={'40':[{'placeId':'beth_horon','status':'possible','confidence':'low'}]}
# 29 September 2026: source_leads_2026-09-29.md (Zertal 2008, Manasseh Hill Country Survey Vol. 2) lowers
# Kh. Ibziq for entry 59 from medium to low: no conduit, weak 1st-century presence, name attested there only
# from the Byzantine period. Kh. Salhab (Zertal site 23) is recorded as an alternative bearer of the name; it is not mapped.
revised_confidence={'59':'low'}
revised_candidate_confidence={('59','ibziq'):'low'}
# The Phase 5 index now carries the same change and lists Zertal among the main sources, so no source is added here.
places['ibziq']['note']='Upper Kh. Ibziq, Zertal site 44 (Old Israel Grid 1878/1971). Lower Kh. Ibziq, site 42, lies 1 km north-east. Zertal reports cisterns, burial caves and a Roman road, but no conduit. Not a feature location.'
places['jer_siloam']['note']='The inherited coordinate anchors the wider Siloam complex (~300 m). It does not select a particular pool or trough.'
places['mar_saba']['note']='Mar Saba is one proposed stretch of the Kidron gorge. The escarpment exit remains another possibility.'
specific={
'1':('Late-antique geographical tradition points north of Jericho. Wadi Nuweimeh accommodates both the northwestern springs and northeastern lower valley.','The Iron Age Achor tradition points toward the Buqeia. No reported ruin-and-steps combination decides between them.'),
'4':('Tell es-Sultan supplies a mound and a nearby cemetery. The repository retains it as one possible Kohlit candidate.','Kohlit remains unidentified. The public index maps only a subset of the proposals discussed in the full research.'),
'20':('A cairn and a dam imply different features. Puech prefers a cairn; the dam proposal must be checked independently.','The proposed Qumran dam is reconstructed. Neither it nor a particular cairn has been established as this entry’s landmark.'),
'21':('Qumran’s water system supplies a plausible conduit-head setting. Ilan–Amit’s 1989 plan puts the visible intake beside a reconstructed dam. Stacey (2007) dates the main aqueduct after the 31 BCE earthquake and makes the dam and the cliff tunnel a later stage.','The link to Sekakah and the stone noun are partly restored. Northern approach and northern side must be tested separately. Under Stacey’s phasing, the earlier channel began where the aqueduct leaves the cliff, so the head of a construction stage is an alternative to the dam intake; the phasing is a hypothesis. The pin marks the settlement.'),
'22':('Qumran’s reservoirs provide a setting to test against the fissure east of the named reservoir.','Neither the ancient reservoir name nor the specific eastern fissure has been established. Jerusalem’s similarly named pool does not relocate this entry.'),
'23':('Puech allows Shallum as an alternative to Solomon and a large boulder as the landmark. The channel’s connection to entry 22’s reservoir is conditional.','No origin or endpoint is identified for the stated distance. Entry order alone does not establish a continuous route.'),
'24':('The wording permits a regional approach test from Jericho toward Sekakah. Wadi Kuteif remains a published proposal.','The recorded rock-cut chamber is undated and does not identify the required tomb. A route from entry 23 to entry 24 is not specified.'),
'31':('A Hasmonean fortress occupied the summit. The name Doq survives nearby at Ain Duk.','Editors disagree over “guard post” and “drying place.” The 2026 plate check leans to the drying place, so the fortress is not the landmark by default. The surviving name does not distinguish the summit from the spring; Q24 remains open.'),
'40':('Under the reading “facing the Sea” (west), which the 2026 plate check favours, Beth-Horon keeps Milik’s textual basis; its name survives at Beit ʿUr, and rock-cut tombs are reported at both villages. Naṭuf rests on the order of the entries.','Milik himself later judged the Horite tombs near Beit Guvrin slightly more likely. Puech reads “south”. No chamber facing west, channel or 16-cubit depth is reported anywhere.'),
'32':('Choziba preserves a related name, and the Wadi Qelt waterworks fit the outlet-and-wall description in the relevant period.','The individual outlet and retaining wall remain unidentified. The pin represents a stretch of the valley.'),
'35':('The Kidron gorge supplies the named landscape; Mar Saba and Hyrcania feature in published proposals.','“Mouth of the gorge” could also describe the escarpment exit. No cairn fixes the location; Hyrcania’s link depends on restorations.'),
'38':('The spring name and the Khareitun setting support a candidate in this district.','The required dovecote or cave feature has not been demonstrated at this spring.'),
'46':('Ramat Rahel has an earlier pool-and-channel enclosure and later settlement.','The known enclosure lay under fill containing pottery as late as the second century BCE. The current verdict is low; the required period reservoir remains unverified.'),
'48':('The standing Kidron monument has first-century architectural features.','Its earliest surviving labels name Zacharias. A first-century association with Absalom remains unestablished.'),
'49':('The tunnel outlet and surrounding pools supply a compatible water-installation setting. Szanton distinguishes the smaller Silwan pool from Birkat el-Hamra.','Siloam depends on a supplied word; the 2026 plate check shows the disputed letter as a waw-shaped stroke, which leans to Puech without deciding it. Lefkovits reads no Siloam name. The trough remains unverified; overall confidence stays medium and conditional.'),
'55':('The Bethesda complex supplies double pools and a smaller basin in the relevant period.','The text may describe two pools without naming Bethesda; the 2026 plate check shows what looks like a ḥet where Milik’s Bethesda needs a taw. The nearby Strouthion twin pool prevents a unique match on that feature alone.'),
'57':('The mountain name provides the geographical anchor.','The checked steps and cisterns date later. Missing excavation reports prevent a comprehensive judgment about earlier features.'),
'58':('Perennial springs and period water installations fit the regional setting at Beth Shean.','The scroll’s final mem differs from the usual nun in Beth Shean. No evidence selects the particular spring.'),
'59':('Zertal identifies Eusebius’s two villages called Bezek, 17 miles from Neapolis, with the two Ibziq sites. Upper Ibziq has 45 cisterns and a Roman road; Lower Ibziq has about 70 burial caves.','Zertal’s survey reports no conduit at either site. Upper Ibziq has only two Early Roman sherds, and Lower Ibziq starts in the Byzantine period. Zertal places Biblical Bezek at Kh. Salhab, which has Early Roman pottery; it is not mapped here. The name also depends on the disputed reading.'),
}
audit=rows('phase5_archaeology_index.csv')
entries=[]
for r in rows('phase3_site_index.csv'):
    eid=r['entry']; title,hebrew,description=descriptions[eid]
    ids=list(dict.fromkeys(([r['best_place_id']] if r['best_place_id'] else [])+[x.strip() for x in r['possible_place_ids'].split(';') if x.strip()]))
    ar=[a for a in audit if a['entry']==eid]
    primary=next((a for a in ar if a['phase3_verdict']=='best-supported'),ar[0] if ar else None)
    confidence=primary['phase5_confidence'] if primary else r['best_confidence'] or ('unknown' if not ids else 'low')
    confidence=revised_confidence.get(eid,confidence)
    candidates=[]
    for pid in ids:
        preferred=pid==r['best_place_id']
        conf=confidence if preferred else 'medium' if (eid,pid) in [('17','buqeia'),('18','asla'),('30','jericho_area'),('59','ibziq')] else 'low'
        conf=revised_candidate_confidence.get((eid,pid),conf)
        status='preferred' if preferred else 'weak' if pid=='tell_el_qos' else 'possible'
        candidates.append({'placeId':pid,'status':status,'confidence':conf})
    evidence=primary['landmark_reported_at_site'].capitalize()+'.' if primary else 'The public site index retains these candidates for comparison. It supplies no uniquely identified landmark for this entry.'
    caution='The placement remains at site or district level. The scroll’s individual feature has not been identified.'
    if eid in specific: evidence,caution=specific[eid]
    if eid=='41': evidence='The public index leaves this entry unmapped.';caution='The reading and geographical setting remain unresolved.'
    candidates+=revised_candidates.get(eid,[])
    entries.append({'id':eid,'title':title,'hebrew':hebrew,'description':description,'lines':r['col_line'],'status':r['status'],'confidence':confidence,'region':places[ids[0]]['region'] if ids else 'unplaced','candidates':candidates,'evidence':evidence,'caution':caution,'landmark':primary['landmark_types_required'] if primary else '', 'period':primary['period'] if primary else 'Not established in the public archaeology index','sources':primary['main_sources'] if primary else 'Phase 3 site index; Phase 2 landmark lexicon','featured':eid in ['21','31','32','49']})
for entry in entries:
    if entry['id'] in ['20','21','22','23','24']:
        entry['sources'] += '; Puech 2006 pp. 187–189; Qumran reference review (28 September 2026)'
    if entry['id']=='21':
        entry['sources'] += '; Lefkovits 2000 pp. 185–189; Stacey 2009, The Dam; Stacey 2007, DSD 14 pp. 222–243'
out={'snapshot':'e3b51ce6523e947fe217a630d64fa16486fc3c7c','reviewDate':'29 September 2026','entries':entries,'places':list(places.values())}
assert len(entries)==61 and len(places)==38
assert all(c['placeId'] in places for e in entries for c in e['candidates'])
(root.parent/'app/atlas-data.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(f'Built {len(entries)} entries and {len(places)} places; {sum(p["lat"] is not None for p in places.values())} mapped anchors.')
