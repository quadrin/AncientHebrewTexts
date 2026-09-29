"use client";

import { Fragment, useEffect, useMemo, useRef, useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import PhotoReader from "./atlas-photo";
import type { Entry, Place } from "./atlas-types";
import { plain, ReadingCard, Segments, useScrollText, type Selection, type TrSeg, type Word } from "./atlas-text";

// The whole scroll, column by column, in the map panel. The text runs right to
// left, from column I on the right; each entry heading opens that entry's places.

const ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"];
type Row = { ref: string; no: number; w: Word[]; tr: TrSeg[]; owner: string[] };
type Props = { entry: Entry; entries: Entry[]; places: Record<string, Place>; onEntry: (id: string) => void };
type Head = { id: string; continued: boolean; midLine: boolean };

// Where each entry begins in a column: at a line start, in mid-line, or carried
// over from the previous column.
function entryHeads(rows: Row[], carried: string | undefined) {
  const heads: Record<string, Head[]> = {};
  let before = carried;
  rows.forEach((r, ri) => {
    heads[r.ref] = [];
    r.owner.forEach((id, i) => {
      const prev = i === 0 ? before : r.owner[i - 1];
      if (id && id !== prev) heads[r.ref].push({ id, continued: false, midLine: i > 0 });
      else if (id && ri === 0 && i === 0) heads[r.ref].push({ id, continued: true, midLine: false });
    });
    before = r.owner[r.owner.length - 1];
  });
  return heads;
}

export default function ScrollView({ entry, entries, places, onEntry }: Props) {
  const { data, failed, lineWords, notesFor } = useScrollText();
  const [photograph, setPhotograph] = useState(() => typeof window !== "undefined" && window.location.hash.endsWith("/photo"));
  function showPhotograph(show: boolean) {
    setPhotograph(show);
    history.replaceState(null, "", `#entry-${entry.id}/scroll${show ? "/photo" : ""}`);
  }
  // A column chosen on the strip holds until another entry is selected.
  const [chosen, setChosen] = useState<{ entry: string; col: number } | null>(null);
  const [sel, setSel] = useState<Selection>(null);
  const body = useRef<HTMLDivElement>(null);
  const fromScroll = useRef(false);

  const columns = useMemo(() => {
    if (!data) return null;
    const rows: Record<string, Row> = {};
    for (const [id, lines] of Object.entries(data.entries)) for (const l of lines) {
      const row = rows[l.ref] ??= { ref: l.ref, no: +l.ref.split(" ")[1], w: l.w, tr: l.tr, owner: [] };
      for (let i = l.from; i < l.to; i++) row.owner[i] = id;
    }
    return ROMAN.map(r => Object.values(rows).filter(x => x.ref.split(" ")[0] === r).sort((a, b) => a.no - b.no));
  }, [data]);

  const entryCol = data?.entries[entry.id]?.[0] ? ROMAN.indexOf(data.entries[entry.id][0].ref.split(" ")[0]) : 0;
  const col = chosen && chosen.entry === entry.id ? chosen.col : entryCol;

  // Bring the selected entry into view when it changes, here or in the register.
  // Only the text pane scrolls; the atlas frame around it stays put.
  useEffect(() => {
    const pane = body.current;
    const target = pane?.querySelector<HTMLElement>(`[data-starts="${entry.id}"]`);
    const local = fromScroll.current;
    fromScroll.current = false;
    if (!pane || !target) return;
    const top = target.offsetTop - 6;
    if (local && top >= pane.scrollTop && top + target.offsetHeight <= pane.scrollTop + pane.clientHeight) return;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    pane.scrollTo({ top, behavior: reduced ? "auto" : "smooth" });
  }, [entry.id, col, columns]);

  if (photograph) return <PhotoReader onEntry={id => { onEntry(id); history.replaceState(null, "", `#entry-${id}/scroll/photo`); }} onText={() => { setChosen({ entry: entry.id, col: 6 }); showPhotograph(false); }}/>;

  if (failed) return <div className="scroll-view"><p className="scroll-status">The text of the scroll could not load. Reload the page to try again.</p></div>;
  if (!data || !columns) return <div className="scroll-view"><p className="scroll-status" role="status">Unrolling the scroll…</p></div>;

  const rows = columns[col];
  const byId = Object.fromEntries(entries.map(e => [e.id, e]));
  const inColumn = Array.from(new Set(rows.flatMap(r => r.owner.filter(Boolean))));
  const marked = new Set<string>();
  if (sel?.note) for (const [line, words] of data.notes[sel.note]?.at ?? []) for (const i of words) marked.add(`${line}#${i}`);
  if (sel?.word !== undefined) marked.add(`${sel.line}#${sel.word}`);

  function pick(id: string) { fromScroll.current = true; onEntry(id); }
  function heading(id: string, continued: boolean, midLine: boolean) {
    const e = byId[id]; if (!e) return null;
    const best = e.candidates[0] ? places[e.candidates[0].placeId] : null;
    return <button type="button" key={`h-${id}`} data-starts={continued ? undefined : id} className={`scroll-entry ${id === entry.id ? "selected" : ""}`} aria-current={id === entry.id ? "true" : undefined} onClick={() => pick(id)}>
      <span className="entry-number">{id.padStart(2, "0")}</span>
      <span className="entry-text"><strong>{e.title}</strong><small>{continued ? `Continued from ${e.lines.split("-")[0]}` : midLine ? "Begins in the middle of this line" : best ? best.shortName : "Location unresolved"}</small></span>
      <span className={`register-confidence ${e.candidates[0]?.confidence ?? "unplaced"}`}>{e.candidates[0]?.confidence ?? "unplaced"}</span>
    </button>;
  }

  const lastRow = col > 0 ? columns[col - 1][columns[col - 1].length - 1] : undefined;
  const heads = entryHeads(rows, lastRow ? lastRow.owner[lastRow.owner.length - 1] : undefined);
  return <div className="scroll-view">
    <header className="scroll-heading">
      <span className="small-caps">The scroll · 3Q15 · read from right to left</span>
      <h2>Column {ROMAN[col]}</h2><button className="photo-text-button" onClick={() => showPhotograph(true)}>Read the photograph</button>
      <p>Lines 1–{rows.length} · entries {inColumn[0]}–{inColumn[inColumn.length - 1]}. Select a Hebrew word or an underlined phrase for the editions’ readings, and an entry to open its places.</p>
    </header>
    <nav className="scroll-strip" aria-label="Columns of the scroll, right to left">{columns.map((c, i) => <Fragment key={i}>
      {(i === 4 || i === 8) && <span className="scroll-seam" aria-hidden="true"/>}
      <button type="button" className="scroll-tablet" aria-current={i === col ? "true" : undefined} aria-label={`Column ${ROMAN[i]}`} onClick={() => { setChosen({ entry: entry.id, col: i }); setSel(null); body.current?.scrollTo({ top: 0 }); }}>
        <span className="cn">{ROMAN[i]}</span>
        <span className="mini" aria-hidden="true">{c.map(r => <span key={r.ref}>{r.w.map(w => w.n != null ? "·" : plain(w)).join(" ")}</span>)}</span>
      </button>
    </Fragment>)}</nav>
    <div className="scroll-body" ref={body}>
      {rows.map(r => {
        const selected = r.owner.includes(entry.id);
        return <Fragment key={r.ref}>
          {heads[r.ref].map(h => heading(h.id, h.continued, h.midLine))}
          <div className={`scroll-row ${selected ? "in-entry" : ""} ${sel?.line === r.ref ? "active" : ""}`}>
            <p className="scroll-en">{r.tr.map((s, i) => typeof s === "string" ? <Fragment key={i}>{s}</Fragment> : <button key={i} type="button" className={sel?.note === s[1] ? "st-nt on" : "st-nt"} onClick={() => setSel(sel?.note === s[1] ? null : { line: r.ref, note: s[1] })}>{s[0]}</button>)}</p>
            <span className="scroll-no" aria-label={`Line ${r.ref}`}>{r.no}</span>
            <p className="scroll-he" lang="he" dir="rtl">{r.w.map((w, i) => {
              const key = `${r.ref}#${i}`;
              const cls = ["st-w", w.n != null ? "st-num" : "", w.greek ? "st-greek" : "", notesFor(r.ref, i).length ? "has-note" : "", marked.has(key) ? "on" : ""].filter(Boolean).join(" ");
              const mid = i > 0 && r.owner[i] !== r.owner[i - 1];
              return <Fragment key={i}>{i > 0 && " "}{mid && <span className="scroll-mid" title={`Entry ${r.owner[i]} begins here`}>{r.owner[i]}</span>}<button type="button" className={cls} aria-label={w.n != null ? `numeral ${w.n}` : plain(w)} onClick={() => setSel(sel?.line === r.ref && sel.word === i ? null : { line: r.ref, word: i })}>{w.n != null ? <>{w.n}{w.h.length > 0 && <> <Segments w={w}/></>}</> : <Segments w={w}/>}</button></Fragment>;
            })}</p>
            {sel?.line === r.ref && <ReadingCard data={data} line={r} sel={sel} notesFor={notesFor} lineWords={lineWords} onClose={() => setSel(null)}/>}
          </div>
        </Fragment>;
      })}
    </div>
    <footer className="scroll-foot">
      <button type="button" disabled={col === 0} onClick={() => { setChosen({ entry: entry.id, col: col - 1 }); setSel(null); body.current?.scrollTo({ top: 0 }); }}><ChevronLeft size={14}/>{col > 0 ? `Column ${ROMAN[col - 1]}` : "Column I"}</button>
      <span>Hebrew: M. G. Abegg Jr.’s transcription (ETCBC, <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noreferrer">CC BY-NC 4.0</a>). Translation and notes: this project.</span>
      <button type="button" disabled={col === ROMAN.length - 1} onClick={() => { setChosen({ entry: entry.id, col: col + 1 }); setSel(null); body.current?.scrollTo({ top: 0 }); }}>{col < ROMAN.length - 1 ? `Column ${ROMAN[col + 1]}` : "Column XII"}<ChevronRight size={14}/></button>
    </footer>
  </div>;
}
