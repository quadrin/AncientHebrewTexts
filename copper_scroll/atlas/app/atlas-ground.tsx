"use client";

import { useEffect, useRef, useState } from "react";
import { Camera, ExternalLink, Eye, EyeOff, Minus, Move, Plus, RotateCcw } from "lucide-react";
import sceneData from "./atlas-scenes.json";
import type { Entry, Place } from "./atlas-types";

type Highlight = {id:string;label:string;points:string;x:number;y:number;note:string;entryIds:string[]};
type Scene = {placeId:string;src:string;sourceUrl:string;title:string;author:string;license:string;licenseUrl:string;width:number;height:number;alt:string;caption:string;highlights:Highlight[]};
const scenes=sceneData as Scene[];
type Props={place:Place|null;entry:Entry;places:Place[];onPlace:(id:string)=>void};
const clamp=(n:number,low:number,high:number)=>Math.min(high,Math.max(low,n));

export default function GroundView({place,entry,places,onPlace}:Props){
  const scene=scenes.find(s=>s.placeId===place?.id);
  const viewport=useRef<HTMLDivElement>(null);
  const [size,setSize]=useState({width:600,height:350});
  const [zoom,setZoom]=useState(1);
  const [offset,setOffset]=useState({x:0,y:0});
  const [showHighlights,setShowHighlights]=useState(true);
  const [active,setActive]=useState(scene?.highlights[0]?.id??"");
  const [imageState,setImageState]=useState("loading");
  const drag=useRef<{x:number;y:number;originX:number;originY:number}|null>(null);
  const feature=scene?.highlights.find(h=>h.id===active);
  const ratio=scene?scene.width/scene.height:1;
  const baseWidth=Math.max(size.width,size.height*ratio);
  const imageWidth=baseWidth*zoom,imageHeight=imageWidth/ratio;
  const maxX=Math.max(0,(imageWidth-size.width)/2),maxY=Math.max(0,(imageHeight-size.height)/2);
  const panX=clamp(offset.x,-maxX,maxX),panY=clamp(offset.y,-maxY,maxY);
  const minimumZoom=Math.min(1,size.width/baseWidth,size.height/(baseWidth/ratio));
  const streetUrl=place?.lat!=null&&place.lon!=null?`https://www.google.com/maps/@?api=1&map_action=pano&viewpoint=${place.lat}%2C${place.lon}`:null;

  useEffect(()=>{
    const element=viewport.current;if(!element)return;
    const observer=new ResizeObserver(([r])=>setSize({width:r.contentRect.width,height:r.contentRect.height}));
    observer.observe(element);return()=>observer.disconnect();
  },[scene]);
  function changeZoom(value:number){setZoom(clamp(value,minimumZoom,4));setOffset({x:panX,y:panY})}
  function reset(){setZoom(1);setOffset({x:0,y:0})}
  function selectFeature(h:Highlight){
    setActive(h.id);setShowHighlights(true);
    setOffset({x:clamp((50-h.x)/100*imageWidth,-maxX,maxX),y:clamp((50-h.y)/100*imageHeight,-maxY,maxY)});
  }
  return <div className="ground-view">
    <header className="ground-heading"><span className="small-caps">At ground level</span><h2>{place?.shortName??"Location unresolved"}</h2><p>{scene?"Pan & zoom a real photograph. Select a highlight to read the landscape.":"This candidate has no annotated photograph in the atlas yet."}</p></header>
    {scene?<>
      <div ref={viewport} className="photo-viewport" tabIndex={0} role="region" aria-label={`${scene.title}. Drag to pan; arrow keys to move; plus or minus to zoom.`}
        onPointerDown={event=>{if((event.target as Element).closest("button,[role=button]"))return;event.currentTarget.setPointerCapture(event.pointerId);drag.current={x:event.clientX,y:event.clientY,originX:panX,originY:panY};event.currentTarget.classList.add("dragging")}}
        onPointerMove={event=>{if(!drag.current)return;setOffset({x:clamp(drag.current.originX+event.clientX-drag.current.x,-maxX,maxX),y:clamp(drag.current.originY+event.clientY-drag.current.y,-maxY,maxY)})}}
        onPointerUp={event=>{drag.current=null;event.currentTarget.classList.remove("dragging")}}
        onPointerCancel={event=>{drag.current=null;event.currentTarget.classList.remove("dragging")}}
        onKeyDown={event=>{const moves:Record<string,[number,number]>={ArrowLeft:[60,0],ArrowRight:[-60,0],ArrowUp:[0,60],ArrowDown:[0,-60]};if(moves[event.key]){event.preventDefault();setOffset({x:clamp(panX+moves[event.key][0],-maxX,maxX),y:clamp(panY+moves[event.key][1],-maxY,maxY)})}else if(event.key==="+"||event.key==="="){event.preventDefault();changeZoom(zoom*1.25)}else if(event.key==="-"){event.preventDefault();changeZoom(zoom/1.25)}}}
        onWheel={event=>{changeZoom(zoom*(event.deltaY<0?1.08:.92))}}>
        <div className="photo-sheet" style={{width:imageWidth,height:imageHeight,left:(size.width-imageWidth)/2+panX,top:(size.height-imageHeight)/2+panY}}>
          <img src={scene.src} alt={scene.alt} draggable={false} onLoad={()=>setImageState("ready")} onError={()=>setImageState("error")}/>
          {showHighlights&&imageState==="ready"&&<><svg className="photo-regions" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">{scene.highlights.map(h=><polygon key={h.id} points={h.points} className={active===h.id?"active":""} vectorEffect="non-scaling-stroke"/>)}</svg>{scene.highlights.map((h,index)=><button className={`photo-hotspot ${active===h.id?"active":""}`} key={h.id} style={{left:`${h.x}%`,top:`${h.y}%`}} onClick={()=>selectFeature(h)} aria-label={h.label} aria-pressed={active===h.id}><span>{index+1}</span><strong>{h.label}</strong></button>)}</>}
        </div>
        <div className="photo-view-label"><Camera size={13}/>Photographic view · limited field of view</div>
        <div className="photo-controls"><button aria-label={showHighlights?"Hide photographic highlights":"Show photographic highlights"} aria-pressed={showHighlights} onClick={()=>setShowHighlights(v=>!v)}>{showHighlights?<Eye size={17}/>:<EyeOff size={17}/>}</button><button aria-label="Zoom out photograph" onClick={()=>changeZoom(zoom/1.25)} disabled={zoom<=minimumZoom+.001}><Minus size={17}/></button><button aria-label="Zoom in photograph" onClick={()=>changeZoom(zoom*1.25)} disabled={zoom>=4}><Plus size={17}/></button><button aria-label="Reset photograph view" onClick={reset}><RotateCcw size={15}/></button></div>
        {imageState==="loading"&&<div className="photo-status" role="status">Opening the field photograph…</div>}
        {imageState==="error"&&<div className="photo-status" role="status">The photograph could not load.<a href={scene.sourceUrl} target="_blank" rel="noreferrer">View it at the source <ExternalLink size={12}/></a></div>}
        <div className="photo-drag-hint"><Move size={13}/>Drag to look around · scroll to zoom</div>
      </div>
      <div className="ground-notes">
        <div className="scroll-comparison"><span className="small-caps">Entry {entry.id} · {entry.title}</span><p>{entry.description}</p></div>
        <div className="feature-tabs" aria-label="Photograph highlights">{scene.highlights.map((h,index)=><button key={h.id} aria-pressed={active===h.id} onClick={()=>selectFeature(h)}><span>{index+1}</span>{h.label}</button>)}</div>
        {feature&&<div className="feature-reading" aria-live="polite"><span className="small-caps">{feature.entryIds.includes(entry.id)?`Compare with entry ${entry.id}`:"Visible landscape context"}</span><p>{feature.note}</p></div>}
        <p className="scene-caption">{scene.caption}</p>
        <div className="photo-credit">Photo: <a href={scene.sourceUrl} target="_blank" rel="noreferrer">{scene.author}</a> · <a href={scene.licenseUrl} target="_blank" rel="noreferrer">{scene.license}</a>. Atlas overlays added; framing changes as you pan.</div>
      </div>
    </>:<div className="ground-empty"><Camera size={34} strokeWidth={1}/><h3>Explore another viewpoint</h3><p>{place?.lat==null?"This proposal has no defensible coordinate for a Street View search.":"Try nearby Google Street View imagery, or open one of the photographed candidates below. Coverage may be absent or some distance from the site."}</p><div className="scene-shortcuts">{scenes.map(s=><button key={s.placeId} onClick={()=>onPlace(s.placeId)}><Camera size={14}/>{places.find(p=>p.id===s.placeId)?.shortName}</button>)}</div></div>}
    {streetUrl&&<div className="street-view-link"><a href={streetUrl} target="_blank" rel="noreferrer">Open nearby Google Street View <ExternalLink size={13}/></a><span>Opens separately; imagery coverage varies. Atlas highlights stay in this view.</span></div>}
  </div>;
}
