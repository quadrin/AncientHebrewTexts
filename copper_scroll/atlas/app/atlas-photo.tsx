"use client";

import { useEffect, useRef, useState, type PointerEvent as ReactPointerEvent } from "react";
import { ChevronLeft, ChevronRight, Focus, Minus, Plus, RotateCcw } from "lucide-react";
import photo from "./atlas-photo-data.json";
import { plain, ReadingCard, Segments, useScrollText } from "./atlas-text";

type Box = { x: number; y: number; width: number; height: number };
type Layer = (typeof photo.views)[number];
const START: Box = { x: 230, y: 400, width: 580, height: 850 };
const clamp = (n: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, n));
// Image, hit regions and strokes share a single SVG coordinate system.
// Panning and zooming only change its viewBox; nothing is positioned in CSS pixels.
export default function PhotoReader({ onEntry, onText }: { onEntry: (id: string) => void; onText: () => void }) {
  const { data, failed, lineWords, notesFor } = useScrollText();
  const [selected, setSelected] = useState(1);
  const [view, setView] = useState<Box>(START);
  const [tracing, setTracing] = useState(true);
  const [viewId, setViewId] = useState(photo.defaultView);
  const [opacity, setOpacity] = useState(.85);
  const [original, setOriginal] = useState(false);
  const [imageState, setImageState] = useState<"loading" | "loaded" | "failed">("loading");
  const [retry, setRetry] = useState(0);
  const svg = useRef<SVGSVGElement>(null);
  const drag = useRef<{ id: number; x: number; y: number; view: Box; scale: number; moved: boolean } | null>(null);
  const moved = useRef(false);
  const pinch = useRef<{ distance: number; view: Box } | null>(null);
  const pointers = useRef(new Map<number, { x: number; y: number }>());
  const item = photo.words[selected];
  const line = Object.values(data?.entries ?? {}).flat().find(l => l.ref === item.line);
  const word = line?.w[item.word];
  const owner = Object.entries(data?.entries ?? {}).find(([, ls]) => ls.some(l => l.ref === item.line && item.word >= l.from && item.word < l.to))?.[0];
  const base = import.meta.env?.BASE_URL ?? "/";
  const layer: Layer = photo.views.find(v => v.id === viewId) ?? photo.views[0];
  function chooseView(id: string) {
    if (id === viewId) return;
    setImageState("loading");
    setViewId(id);
  }

  function bounded(b: Box): Box {
    return { ...b, x: clamp(b.x, -300, photo.width - b.width + 300), y: clamp(b.y, -300, photo.height - b.height + 300) };
  }
  function zoom(factor: number, cx?: number, cy?: number) {
    setView(b => {
      const w = clamp(b.width * factor, 150, 1400), f = w / b.width;
      const x = cx ?? b.x + b.width / 2, y = cy ?? b.y + b.height / 2;
      return bounded({ x: x - (x - b.x) * f, y: y - (y - b.y) * f, width: w, height: b.height * f });
    });
  }
  function focus(index = selected) {
    const [x, y, w, h] = photo.words[index].box;
    const rect = svg.current?.getBoundingClientRect();
    const aspect = rect ? rect.width / rect.height : .8;
    const width = Math.max(w + 100, (h + 160) * aspect);
    const height = width / aspect;
    setView(bounded({ x: x + w / 2 - width / 2, y: y + h / 2 - height / 2, width, height }));
  }
  function pick(index: number, center = false) {
    setSelected(index);
    if (center) focus(index);
  }
  function next(delta: number) { pick((selected + delta + photo.words.length) % photo.words.length, true); }
  function start(e: ReactPointerEvent<SVGSVGElement>) {
    if (e.button !== 0) return;
    e.currentTarget.setPointerCapture(e.pointerId);
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    const rect = e.currentTarget.getBoundingClientRect();
    drag.current = { id: e.pointerId, x: e.clientX, y: e.clientY, view, scale: Math.min(rect.width / view.width, rect.height / view.height), moved: false };
    moved.current = false;
    if (pointers.current.size === 2) {
      const [a, b] = [...pointers.current.values()];
      pinch.current = { distance: Math.hypot(a.x - b.x, a.y - b.y), view };
    }
  }
  function move(e: ReactPointerEvent<SVGSVGElement>) {
    if (!pointers.current.has(e.pointerId)) return;
    pointers.current.set(e.pointerId, { x: e.clientX, y: e.clientY });
    if (pointers.current.size === 2 && pinch.current) {
      const [a, b] = [...pointers.current.values()], p = pinch.current;
      const width = clamp(p.view.width * p.distance / Math.max(1, Math.hypot(a.x - b.x, a.y - b.y)), 150, 1400);
      const height = p.view.height * width / p.view.width;
      setView(bounded({ x: p.view.x + (p.view.width - width) / 2, y: p.view.y + (p.view.height - height) / 2, width, height }));
      moved.current = true; return;
    }
    const d = drag.current;
    if (!d || d.id !== e.pointerId) return;
    const dx = e.clientX - d.x, dy = e.clientY - d.y;
    if (Math.hypot(dx, dy) > 4) { d.moved = true; moved.current = true; }
    if (d.moved) setView(bounded({ ...d.view, x: d.view.x - dx / d.scale, y: d.view.y - dy / d.scale }));
  }
  function end(e: ReactPointerEvent<SVGSVGElement>) {
    const wasPinch = pointers.current.size > 1 || !!pinch.current;
    pointers.current.delete(e.pointerId);
    if (e.currentTarget.hasPointerCapture(e.pointerId)) e.currentTarget.releasePointerCapture(e.pointerId);
    // Pointer capture retargets clicks to the SVG. Hit-test in the same viewBox
    // coordinates instead of relying on the browser's click target.
    if (!moved.current && !wasPinch && e.type !== "pointercancel") {
      const matrix = e.currentTarget.getScreenCTM();
      if (matrix) {
        const point = new DOMPoint(e.clientX, e.clientY).matrixTransform(matrix.inverse());
        const i = photo.words.findIndex(({ box: [x, y, w, h] }) => point.x >= x && point.x <= x + w && point.y >= y && point.y <= y + h);
        if (i >= 0) pick(i);
      }
    }
    drag.current = null; pinch.current = null;
  }
  useEffect(() => {
    const el = svg.current;
    if (!el) return;
    function wheel(e: WheelEvent) {
      e.preventDefault();
      const matrix = el!.getScreenCTM();
      const p = matrix ? new DOMPoint(e.clientX, e.clientY).matrixTransform(matrix.inverse()) : null;
      zoom(Math.exp(clamp(e.deltaY, -150, 150) * .002), p?.x, p?.y);
    }
    el.addEventListener("wheel", wheel, { passive: false });
    return () => el.removeEventListener("wheel", wheel);
  }, []);

  return <div className="reader-reader">
    <header className="reader-head"><div><span className="small-caps">The original metal · Jordan Museum</span><h2>{photo.title}</h2></div><button className="reader-text-button" onClick={onText}>Full scroll text</button></header>
    <div className="reader-workspace">
      <section className="reader-stage" aria-label="Photograph with word tracings">
        <div className="reader-controls" aria-label="Photograph controls">
          <button onClick={() => zoom(1.3)} aria-label="Zoom out"><Minus size={17}/></button><button onClick={() => zoom(1 / 1.3)} aria-label="Zoom in"><Plus size={17}/></button><button onClick={() => setView(START)} aria-label="Reset photograph view"><RotateCcw size={16}/></button><button onClick={() => focus()} aria-label="Focus selected word"><Focus size={17}/></button>
          <span>{Math.round(START.width / view.width * 100)}%</span>
        </div>
        <div className="reader-views" role="group" aria-label="Image version">{photo.views.map(v => <button key={v.id} aria-pressed={v.id === layer.id} title={v.description} onClick={() => chooseView(v.id)}>{v.label}</button>)}</div>
        <svg ref={svg} className="reader-canvas" data-view={layer.id} viewBox={`${view.x} ${view.y} ${view.width} ${view.height}`} preserveAspectRatio="xMidYMid meet" aria-label={`Copper Scroll strip 13, ${layer.label.toLowerCase()} view. Select an outlined word; drag to pan or scroll to zoom.`} tabIndex={0}
          onPointerDown={start} onPointerMove={move} onPointerUp={end} onPointerCancel={end}
          onDoubleClick={() => zoom(.65)} onKeyDown={e => {
            if (["ArrowRight", "ArrowLeft", "+", "=", "-", "0", " "].includes(e.key)) e.preventDefault();
            if (e.key === "ArrowRight") next(-1); if (e.key === "ArrowLeft") next(1);
            if (e.key === "+" || e.key === "=") zoom(.8); if (e.key === "-") zoom(1.25); if (e.key === "0") setView(START); if (e.key === " ") setOriginal(true);
          }} onKeyUp={e => { if (e.key === " ") setOriginal(false); }} onBlur={() => setOriginal(false)}>
          <image key={`${layer.id}-${retry}`} href={`${base}${layer.image}`} x={0} y={0} width={photo.width} height={photo.height} onLoad={() => setImageState("loaded")} onError={() => setImageState("failed")}/>
          {original && layer.image !== photo.image && <image href={`${base}${photo.image}`} x={0} y={0} width={photo.width} height={photo.height}/>}
          {!original && imageState === "loaded" && photo.words.map((w, i) => <g key={w.id} className={`reader-word ${i === selected ? "selected" : ""}`} data-word-id={w.id}>
            <rect x={w.box[0]} y={w.box[1]} width={w.box[2]} height={w.box[3]} rx={9} className="reader-hit" vectorEffect="non-scaling-stroke"/>
            {i === selected && tracing && <g className="reader-trace" opacity={opacity} pointerEvents="none">{w.paths.map((d, j) => <g key={`${w.id}-${j}`}><path d={d} className="trace-shadow"/><path d={d} className="trace-line" pathLength={1}/></g>)}</g>}
          </g>)}
        </svg>
        {imageState === "loading" && <div className="reader-loading" role="status">Loading the {layer.id === "photo" ? "photograph" : `${layer.label.toLowerCase()} image`}…</div>}
        {imageState === "failed" && <div className="reader-loading" role="alert">The image could not load.<button onClick={() => { setImageState("loading"); setRetry(v => v + 1); }}>Retry</button></div>}
        <div className="reader-stage-foot"><span>Drag to pan · scroll or pinch to zoom</span><button aria-pressed={original} onPointerDown={e => { e.currentTarget.setPointerCapture(e.pointerId); setOriginal(true); }} onPointerUp={() => setOriginal(false)} onPointerCancel={() => setOriginal(false)} onLostPointerCapture={() => setOriginal(false)} onKeyDown={e => { if (e.key === " " || e.key === "Enter") setOriginal(true); }} onKeyUp={() => setOriginal(false)} onBlur={() => setOriginal(false)}>Hold for photo</button></div>
      </section>
      <aside className="reader-reading" aria-label="Selected word interpretation">
        <div className="reader-word-nav"><button onClick={() => next(-1)} aria-label="Previous mapped word"><ChevronLeft size={18}/></button><span>{item.line} · word {item.word + 1}</span><button onClick={() => next(1)} aria-label="Next mapped word"><ChevronRight size={18}/></button></div>
        {failed ? <p>The text could not load. Reload to retry.</p> : !data || !word || !line ? <p role="status">Loading the reading…</p> : <>
          <div className="reader-modern" lang="he" dir="rtl"><Segments w={word}/></div>
          <p className="reader-gloss">{word.m?.map(m => data.gloss[m[1]]).filter(Boolean).join(" · ") || plain(word)}</p>
          <p className="reader-label">The line in context</p><p className="reader-line-he" dir="rtl" lang="he">{line.w.map((w, i) => <span key={i} className={i === item.word ? "active" : ""}>{w.n ?? plain(w)} </span>)}</p>
          <p className="reader-translation">{line.tr.map(s => typeof s === "string" ? s : s[0]).join("")}</p>
          <div className="reader-options"><label><input type="checkbox" checked={tracing} onChange={e => setTracing(e.target.checked)}/>Trace strokes</label><label className="reader-opacity">Trace opacity<input type="range" min=".15" max="1" step=".05" value={opacity} onChange={e => setOpacity(+e.target.value)}/></label></div>
          <p className="reader-provisional">Provisional tracing</p><p className="reader-note">{item.note}</p>
          <details className="reader-editions"><summary>Lettering and interpretation</summary><ReadingCard data={data} line={line} sel={{ line: item.line, word: item.word }} notesFor={notesFor} lineWords={lineWords} onClose={() => {}}/></details>
          {owner && <button className="reader-entry-link" onClick={() => onEntry(owner)}>Show entry {owner} in the atlas</button>}
        </>}
      </aside>
    </div>
    <nav className="reader-word-strip" aria-label="Mapped words in reading order">{photo.words.map((w, i) => {
      const text = lineWords[w.line]?.[w.word];
      return <button key={w.id} aria-pressed={i === selected} onClick={() => pick(i, true)}><span lang="he" dir="rtl">{text ? plain(text) : "…"}</span><small>{w.line}</small></button>;
    })}</nav>
    <footer className="reader-credit"><p>8 words traced in VII 7–11, matched to Puech’s radiograph of strip 13. Each stroke follows a groove visible in this photograph; gaps remain unfilled. {layer.description}</p><p>Photograph: <a href={photo.source} target="_blank" rel="noreferrer">{photo.author}</a>, 2020 · <a href={photo.licenseUrl} target="_blank" rel="noreferrer">{photo.license}</a>. Full size, no retouching. The Grooves and Relief images and the tracings are derived from it and use the same licence.</p></footer>
  </div>;
}
