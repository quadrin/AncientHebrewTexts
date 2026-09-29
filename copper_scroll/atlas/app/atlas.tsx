"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { BookOpen, ChevronLeft, ChevronRight, Compass, ExternalLink, Feather, FileText, Info, List, Map, MapPin, Search, ScrollText, X } from "lucide-react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import AtlasMap from "./atlas-map";
import EvidenceReview from "./atlas-evidence";
import EntryText, { textPage } from "./atlas-text";
import data from "./atlas-data.json";
import type { Entry, Place } from "./atlas-types";
import { sortCandidates, sortEntries, sortLabels, type SortOrder } from "./atlas-order";

const entries=data.entries as Entry[];
const places=data.places as Place[];
const mappedCount=places.filter(p=>p.lat!=null&&p.lon!=null).length;
const unmappedCount=places.length-mappedCount;
const placeById=Object.fromEntries(places.map(p=>[p.id,p]));
const repo=`https://github.com/quadrin/AncientHebrewTexts/blob/${data.snapshot}/copper_scroll`;
const regions:Record<string,string>={all:"All regions",jericho:"Jericho & Qumran",jerusalem:"Jerusalem",region:"Judean hills & north",unplaced:"Unplaced"};

export default function Atlas(){
  const [selectedId,setSelectedId]=useState("21");
  const [focusId,setFocusId]=useState<string|null>("kh_qumran");
  const [focusNonce,setFocusNonce]=useState(0);
  const [query,setQuery]=useState("");
  const [region,setRegion]=useState("all");
  const [registerMode,setRegisterMode]=useState("shortlist");
  const [sortOrder,setSortOrder]=useState<SortOrder>("scroll");
  const [detailTab,setDetailTab]=useState("places");
  const [candidateOrder,setCandidateOrder]=useState("confidence");
  const [mode,setMode]=useState("2d");
  const [mobileView,setMobileView]=useState("map");
  const detailRef=useRef<HTMLElement>(null);
  const evidenceTabRef=useRef<HTMLButtonElement>(null);
  const entry=entries.find(e=>e.id===selectedId)!;
  const place=focusId?placeById[focusId]:null;
  const visibleEntries=useMemo(()=>sortEntries(entries.filter(e=>{
    const text=[e.id,e.title,e.hebrew,e.description,...e.candidates.map(c=>placeById[c.placeId].name)].join(" ").toLowerCase();
    return (!query||text.includes(query.toLowerCase())) && (region==="all"||e.region===region||e.candidates.some(c=>placeById[c.placeId].region===region)) && (query||registerMode==="all"||e.featured);
  }),sortOrder,placeById),[query,region,registerMode,sortOrder]);
  const orderedCandidates=useMemo(()=>sortCandidates(entry.candidates,candidateOrder,placeById),[entry,candidateOrder]);
  const visibleIds=useMemo(()=>Array.from(new Set((query||region!=="all"?visibleEntries:entries).flatMap(e=>e.candidates.map(c=>c.placeId)))),[visibleEntries,query,region]);

  const modeRef=useRef(mode);
  useEffect(()=>{modeRef.current=mode},[mode]);
  const chooseEntry=useCallback((id:string,focus?:string,stayInView?:boolean)=>{
    const e=entries.find(x=>x.id===id);if(!e)return;
    setSelectedId(id);setFocusId(focus??e.candidates[0]?.placeId??null);setFocusNonce(n=>n+1);if(!stayInView)setMobileView("detail");
    history.replaceState(null,"",`#entry-${id}${modeRef.current==="scroll"?"/scroll":""}`);
    detailRef.current?.scrollTo({top:0});
  },[]);
  // An entry chosen in the scroll view: the register, map and field note follow, the view stays.
  function chooseFromScroll(id:string){const e=entries.find(x=>x.id===id);if(e&&!e.featured)setRegisterMode("all");chooseEntry(id,undefined,true)}
  function changeMode(next:string){setMode(next);history.replaceState(null,"",`#entry-${selectedId}${next==="scroll"?"/scroll":""}`)}
  function openScroll(){changeMode("scroll");setMobileView("map")}
  function choosePlace(id:string){
    const linked=entry.candidates.some(c=>c.placeId===id)?entry:entries.find(e=>e.candidates.some(c=>c.placeId===id&&c.status==="preferred"))??entries.find(e=>e.candidates.some(c=>c.placeId===id));
    if(linked){if(!linked.featured)setRegisterMode("all");setQuery("");setRegion("all");chooseEntry(linked.id,id);}
  }
  function focusCandidate(id:string){setFocusId(id);setFocusNonce(n=>n+1);setMobileView("map")}
  const index=entries.indexOf(entry);
  function stepEntry(delta:number){const e=entries[(index+delta+entries.length)%entries.length];if(!e.featured)setRegisterMode("all");chooseEntry(e.id)}
  useEffect(()=>{
    const hash=location.hash.match(/^#(?:entry-([\da]+))?(\/?scroll)?(\/photo)?$/);
    const id=hash?.[1];
    if(id&&entries.some(e=>e.id===id)){const e=entries.find(e=>e.id===id)!;setSelectedId(id);setFocusId(e.candidates[0]?.placeId??null);if(!e.featured)setRegisterMode("all");setFocusNonce(1);}
    if(hash?.[2])setMode("scroll");
  },[]);

  // Structured navigation uses the same entry-selection action as the visible register.
  useEffect(()=>{
    const context=(document as Document & {modelContext?:{registerTool:(tool:unknown,opts:{signal:AbortSignal})=>void|Promise<void>}}).modelContext;
    if(!context?.registerTool)return;
    const lifecycle=new AbortController();
    const tool={name:"navigate_scroll_entry",title:"Explore a Copper Scroll entry",description:"Open a numbered scroll entry, its candidate sites and evidence in the atlas.",inputSchema:{type:"object",properties:{entryId:{type:"string",enum:entries.map(e=>e.id)}},required:["entryId"],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute:async(input:unknown)=>{
      const id=(input as {entryId?:unknown})?.entryId;if(typeof id!=="string"||!entries.some(e=>e.id===id))throw new Error("Use an entry number 1–60, or 12a.");
      setRegisterMode("all");setQuery("");setRegion("all");chooseEntry(id);
      await new Promise<void>(resolve=>requestAnimationFrame(()=>requestAnimationFrame(()=>resolve())));
      const e=entries.find(e=>e.id===id)!;return {entryId:id,title:e.title,candidates:e.candidates.map(c=>({site:placeById[c.placeId].shortName,confidence:c.confidence,status:c.status}))};
    }};
    try{void Promise.resolve(context.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}
    return()=>lifecycle.abort();
  },[chooseEntry]);

  const primaryFocus=focusId===entry.candidates[0]?.placeId;
  return <main className="atlas-shell">
    <a className="skip-link" href="#entry-detail" onClick={event=>{event.preventDefault();setMobileView("detail");requestAnimationFrame(()=>detailRef.current?.focus())}}>Skip to selected entry</a>
    <div className="topbar"><span><ScrollText size={15} strokeWidth={1.4}/>3Q15 <span className="edition-label"> / A geographical concordance</span></span><span className="top-actions"><span className="edition-label">Research edition · 2026</span><Dialog><DialogTrigger asChild><button><BookOpen size={14}/>About the atlas</button></DialogTrigger><DialogContent className="method-dialog"><DialogHeader><DialogTitle>Reading the landscape</DialogTitle><DialogDescription>The Copper Scroll names places, buildings and waterworks. This atlas pairs their descriptions with the candidates retained in the current research.</DialogDescription></DialogHeader><div><h3>61 entries, 37 candidate places</h3><p>The numbering follows Puech and Lefkovits: entries 1–60, plus 12a. Descriptions are short editorial paraphrases. Hebrew labels show names or selected editorial readings, rather than a facsimile transcription.</p><h3>The text of each entry</h3><p>Each field note shows the entry’s lines of the scroll: Martin G. Abegg Jr.’s transcription from the ETCBC Dead Sea Scrolls dataset (CC BY-NC 4.0), which draws mainly on Milik’s edition, with an English translation written for this project. Select a Hebrew word or an underlined phrase to see how the editions of Milik, Lefkovits, Puech and others read it, with pages from the research files. The <strong>Scroll</strong> view, beside 2D, 3D and Ground, shows the whole scroll column by column; selecting an entry there opens its places. The same text, with the research tables, is also on the <a href={textPage} target="_blank" rel="noreferrer">text and translation page</a>.</p><h3>What the pins mean</h3><p>A solid pin marks a preferred candidate for at least one entry. A hollow pin marks an alternative. “Preferred” is a comparison among proposals; all current identifications remain medium or low confidence. No individual deposit has been identified.</p><p>Coordinates come from the repository’s curated gazetteer. Copper shading marks the selected candidate’s approximate area; sage shading shows the other candidates for the entry. Dashed outlines indicate coordinate precision, not surveyed site boundaries. Three places have no defensible coordinate and remain unpinned.</p><h3>Map, terrain & ground views</h3><p>2D shows a flat map. 3D uses elevation tiles, with adjustable vertical exaggeration. Both use modern geographical data. The shorelines and roads do not reconstruct the ancient landscape. Ground view offers four real photographs with anchored highlights and feature notes. Photographs have a limited field of view; their visible features provide comparisons, not verified scroll landmarks. A separate Google Street View link opens nearby imagery where coverage exists.</p><h3>Research and map sources</h3><p>Research snapshot: 28 September 2026, commit <a href={`https://github.com/quadrin/AncientHebrewTexts/commit/${data.snapshot}`} target="_blank" rel="noreferrer">5220e8b</a>. It includes the Siloam confidence correction and Q37 on Solomon’s Pool. The feature review adds the full Phase 5 tables from commit cecb12d and separates reading, site and exact-feature confidence for five priority entries. These are qualitative assessments, not probabilities.</p><p><a href={`${repo}/site_identification_review.md`} target="_blank" rel="noreferrer">Site identification review</a> · <a href={`${repo}/sources.md`} target="_blank" rel="noreferrer">Research bibliography</a> · <a href="https://openfreemap.org" target="_blank" rel="noreferrer">OpenFreeMap</a> / <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">OpenStreetMap</a> · <a href="https://mapterhorn.com" target="_blank" rel="noreferrer">Mapterhorn terrain</a></p></div></DialogContent></Dialog></span></div>
    <header className="masthead"><div className="seal" aria-hidden="true"><Compass size={35} strokeWidth={1}/></div><div><h1>The Copper Scroll Atlas</h1><p>Ancient names. Possible places.</p></div><div className="catalog-note"><span><strong>61</strong> scroll entries</span><span><strong>{places.length}</strong> candidate places</span></div></header>
    <div className="working-surface" data-mobile-view={mobileView}>
      <aside className="entry-register" aria-label="Ancient place register">
        <div className="register-heading"><span className="small-caps">Explore the archive</span><h2>Place register</h2><div className="search-wrap"><Search/><Input aria-label="Find an ancient name or candidate" placeholder="Search names, places, entries…" value={query} onChange={e=>setQuery(e.target.value)}/>{query&&<button className="clear-search" aria-label="Clear search" onClick={()=>setQuery("")}><X size={15}/></button>}</div><div className="filter-row"><Select value={region} onValueChange={setRegion}><SelectTrigger aria-label="Filter by region"><SelectValue/></SelectTrigger><SelectContent>{Object.entries(regions).map(([key,label])=><SelectItem key={key} value={key}>{label}</SelectItem>)}</SelectContent></Select></div><div className="register-tabs"><button aria-pressed={registerMode==="shortlist"} onClick={()=>setRegisterMode("shortlist")}>Highlights</button><button aria-pressed={registerMode==="all"} onClick={()=>setRegisterMode("all")}>All 61 entries</button></div></div>
        <div className="register-sort"><label htmlFor="register-sort">Sort by</label><Select value={sortOrder} onValueChange={value=>setSortOrder(value as SortOrder)}><SelectTrigger id="register-sort" aria-label="Sort the place register"><SelectValue/></SelectTrigger><SelectContent>{Object.entries(sortLabels).map(([key,label])=><SelectItem key={key} value={key}>{label}</SelectItem>)}</SelectContent></Select></div>
        <div className="register-count" aria-live="polite">{visibleEntries.length} {visibleEntries.length===1?"entry":"entries"}{query?" found":" in this view"}{sortOrder==="confidence"&&<span className="sort-explanation">Best candidate’s site confidence; ties in scroll order.</span>}</div>
        <nav className="entry-list" aria-label="Select a scroll entry">{visibleEntries.map(e=><button key={e.id} className={`entry-item ${e.id===selectedId?"selected":""}`} aria-current={e.id===selectedId?"true":undefined} onClick={()=>chooseEntry(e.id)}><span className="entry-number">{e.id.padStart(2,"0")}</span><span className="entry-text"><strong>{e.title}</strong><small>{e.candidates[0]?placeById[e.candidates[0].placeId].shortName:"Location unresolved"}</small></span>{sortOrder==="confidence"?<span className="register-confidence">{sortCandidates(e.candidates,"confidence",placeById)[0]?.confidence??"unplaced"}</span>:<ChevronRight className="entry-status" size={13}/>}</button>)}{visibleEntries.length===0&&<div className="empty-list">No entries match this view.<br/><button onClick={()=>{setQuery("");setRegion("all");setRegisterMode("all")}}>Show all entries</button></div>}</nav>
        <div className="register-foot"><MapPin size={15}/><span>{mappedCount} mapped anchors<br/><small>{unmappedCount} places remain unlocated</small></span></div>
      </aside>
      <AtlasMap entry={entry} places={places} entries={entries} focusId={focusId} focusNonce={focusNonce} visibleIds={visibleIds} mode={mode} onMode={changeMode} onPlace={id=>{choosePlace(id);setMobileView("map")}} onEntry={chooseFromScroll} mobileView={mobileView}/>
      <aside ref={detailRef} id="entry-detail" tabIndex={-1} className="detail-panel" aria-label="Selected entry and candidates">
        <div className="folio-header"><span className="small-caps">Entry <b>{entry.id.padStart(2,"0")}</b> / 3Q15</span><div className="folio-nav"><button aria-label="Previous scroll entry" onClick={()=>stepEntry(-1)}><ChevronLeft size={15}/></button><button aria-label="Next scroll entry" onClick={()=>stepEntry(1)}><ChevronRight size={15}/></button></div></div>
        <article className="folio" key={entry.id}><div className="overline"><span>Ancient description</span><span className="hebrew" lang="he" dir="rtl">{entry.hebrew}</span></div><h2>{entry.title}</h2><div className="line-reference">3Q15 · {entry.lines} · Entry {entry.id}</div><p className="entry-description">{entry.description}</p><span className="paraphrase-label">Editorial paraphrase</span><Tabs value={detailTab} onValueChange={setDetailTab} className="detail-tabs">
          <TabsList aria-label="Entry information"><TabsTrigger value="places"><MapPin size={14}/>Places</TabsTrigger><TabsTrigger value="text"><ScrollText size={14}/>Text</TabsTrigger><TabsTrigger ref={evidenceTabRef} value="evidence"><FileText size={14}/>Evidence</TabsTrigger></TabsList>
          <TabsContent value="text"><EntryText entryId={entry.id} onOpenScroll={openScroll}/></TabsContent>
          <TabsContent value="places">
          <div className="candidate-heading"><h3>Candidate {entry.candidates.length===1?"site":"sites"}</h3><span>{entry.candidates.length} {entry.candidates.length===1?"placement":"placements"}</span></div>
          {entry.candidates.length>1&&<div className="candidate-sort"><Select value={candidateOrder} onValueChange={setCandidateOrder}><SelectTrigger aria-label="Sort this entry’s candidates"><SelectValue/></SelectTrigger><SelectContent><SelectItem value="confidence">Confidence · highest first</SelectItem><SelectItem value="alphabetical">Candidate name · A–Z</SelectItem><SelectItem value="preferred">Preferred first</SelectItem></SelectContent></Select></div>}
          {orderedCandidates.map(c=>{const p=placeById[c.placeId];return <button className={`candidate-card ${focusId===p.id?"active":""}`} key={p.id} onClick={()=>focusCandidate(p.id)} aria-pressed={focusId===p.id}><span className="candidate-top">{p.shortName}{p.lat!==null?<MapPin size={15}/>:<Info size={15}/>}</span><span className="candidate-meta"><span className={`confidence ${c.confidence}`}>{c.confidence.charAt(0).toUpperCase()+c.confidence.slice(1)} site confidence</span><span className="status">{c.status==="preferred"?"Preferred candidate":c.status==="weak"?"Weak alternative":"Possible alternative"}</span></span></button>})}
          {!entry.candidates.length&&<p className="folio-empty">This entry has no mapped candidate.</p>}
          {place&&<div className="precision-note"><MapPin size={13}/><span>{place.lat===null?"No coordinate assigned. The source defines no defensible point.":`Approximate anchor · ${place.precision}.`}{place.note&&<> {place.note}</>}</span></div>}
          <button className="evidence-link" onClick={()=>{setDetailTab("evidence");evidenceTabRef.current?.focus()}}>Review evidence & uncertainty <ChevronRight size={16}/></button>
          </TabsContent>
          <TabsContent value="evidence">
          <EvidenceReview entryId={entry.id} placeId={focusId}/>
          <section className="evidence-section"><h3><Feather size={14}/>Why considered</h3><p>{primaryFocus||!place?entry.evidence:place.note||`The research retains ${place.shortName} as a comparison for this entry. Its position remains approximate, and the individual landmark has not been identified.`}</p></section>
          <section className="evidence-section caution"><h3><Info size={14}/>What remains uncertain</h3><p>{entry.caution}</p></section>
          <details className="source-details"><summary>Evidence & references</summary><p>{entry.sources}</p><p><strong>Period fit:</strong> {entry.period}.</p>{place&&<p><strong>Coordinate source:</strong> {place.source}.</p>}<a href={`${repo}/tables/phase5_archaeology_index.csv`} target="_blank" rel="noreferrer">Archaeology index <ExternalLink size={12}/></a><br/><a href={`${repo}/open_questions.md`} target="_blank" rel="noreferrer">Read the open questions <ExternalLink size={12}/></a><br/><a href={`${repo}/tables/phase3_site_index.csv`} target="_blank" rel="noreferrer">All candidate mappings <ExternalLink size={12}/></a></details>
          </TabsContent></Tabs>
          <div className="folio-footer">Site-level identification · Revised 28.09.2026</div>
        </article>
      </aside>
    </div>
    <nav className="mobile-nav" aria-label="Atlas views"><button aria-pressed={mobileView==="register"} onClick={()=>setMobileView("register")}><List size={17}/>Register</button><button aria-pressed={mobileView==="map"} onClick={()=>setMobileView("map")}><Map size={17}/>{mode==="scroll"?"Scroll":mode==="ground"?"Ground":"Map"}</button><button aria-pressed={mobileView==="detail"} onClick={()=>setMobileView("detail")}><FileText size={17}/>Entry {entry.id}</button></nav>
    <footer className="bottom-bar"><span>{mappedCount} mapped anchors · {unmappedCount} unplaced areas</span><span className="desktop-foot">Modern terrain · Historical proposals · Approximate locations</span><span className="bottom-links"><button type="button" onClick={openScroll}><ScrollText size={12}/>Read the scroll</button><a href={`${repo}/README.md`} target="_blank" rel="noreferrer">Research notebook <ExternalLink size={11}/></a></span></footer>
  </main>;
}
