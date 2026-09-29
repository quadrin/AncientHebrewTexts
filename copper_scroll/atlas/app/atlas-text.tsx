"use client";

import { Fragment, useEffect, useMemo, useState } from "react";
import { ExternalLink, ScrollText, X } from "lucide-react";

// The entry's lines of 3Q15: Abegg's transcription (ETCBC dss 2.0.1, CC BY-NC 4.0),
// with the translation, glosses and reading notes written for the project.
// atlas-text.json is built by copper_scroll/tools/build_scroll_notes.py.

type Seg = [string, string];
export type Word = { h: Seg[]; m?: [string, string, string][]; n?: number; ns?: string; greek?: number };
export type TrSeg = string | [string, string];
export type Line = { ref: string; w: Word[]; tr: TrSeg[]; from: number; to: number };
type Reading = { who: string; reading: string; meaning: string; ref: string };
type Note = { label?: string; readings?: Reading[]; note?: string; entry: string; at: [string, number[]][]; lemma?: string[]; src?: string[] };
export type TextData = { gloss: Record<string, string>; notes: Record<string, Note>; entries: Record<string, Line[]> };
export type Selection = { line: string; word?: number; note?: string } | null;

export const textPage = "https://quadrin.github.io/AncientHebrewTexts/copper_scroll/web/";
const research = "https://github.com/quadrin/AncientHebrewTexts/blob/main/copper_scroll/";

// Loaded once, on the first field note; later notes render from the cache at once.
let loaded: TextData | null = null;
let pending: Promise<TextData> | null = null;
function loadText() {
  pending ??= import("./atlas-text.json").then(m => (loaded = ((m as { default?: unknown }).default ?? m) as TextData));
  return pending;
}

const segClass: Record<string, string> = { r: "st-r", u: "st-u", x: "st-x", d: "st-x", c: "st-c", s: "st-s", g: "st-g" };
const segWrap: Record<string, [string, string]> = { r: ["[", "]"], x: ["{", "}"], d: ["{{", "}}"], c: ["⟨", "⟩"] };
const sigla: Record<string, string> = {
  r: "Letters in square brackets are lost and restored by the editor.",
  u: "A circle above a letter marks it as damaged; the reading is not certain.",
  x: "Letters in braces are struck out by the editor as an engraver's error.",
  d: "Letters in double braces were cancelled on the scroll itself.",
  c: "Letters in angle brackets are supplied or corrected by the editor.",
  s: "A raised letter is written above the line on the scroll.",
};

export function plain(w: Word) {
  return w.h.filter(s => s[1] !== "x" && s[1] !== "d").map(s => s[0]).join("");
}
export function Segments({ w }: { w: Word }) {
  return <>{w.h.map((s, i) => {
    const k = s[1];
    if (!k) return <Fragment key={i}>{s[0]}</Fragment>;
    const wrap = segWrap[k];
    return <span key={i} className={segClass[k]}>{wrap ? wrap[0] + s[0] + wrap[1] : s[0]}</span>;
  })}</>;
}

// The text data and its note index, shared by the field note and the scroll view.
export function useScrollText() {
  const [data, setData] = useState<TextData | null>(() => loaded);
  const [failed, setFailed] = useState(false);
  useEffect(() => {
    let live = true;
    if (!loaded) loadText().then(d => { if (live) setData(d); }, () => { if (live) setFailed(true); });
    return () => { live = false; };
  }, []);
  const index = useMemo(() => {
    const byWord: Record<string, string[]> = {}, byLemma: Record<string, string[]> = {}, lineWords: Record<string, Word[]> = {};
    if (data) for (const ls of Object.values(data.entries)) for (const l of ls) lineWords[l.ref] = l.w;
    if (data) for (const [id, n] of Object.entries(data.notes)) {
      for (const [line, words] of n.at) for (const i of words) (byWord[`${line}#${i}`] ??= []).push(id);
      for (const lx of n.lemma ?? []) (byLemma[lx] ??= []).push(id);
    }
    const notesFor = (line: string, i: number) => {
      const ids = [...(byWord[`${line}#${i}`] ?? [])];
      for (const m of lineWords[line]?.[i]?.m ?? []) for (const id of byLemma[m[1]] ?? []) if (!ids.includes(id)) ids.push(id);
      return ids;
    };
    return { lineWords, notesFor };
  }, [data]);
  return { data, failed, ...index };
}

export default function EntryText({ entryId, onOpenScroll }: { entryId: string; onOpenScroll?: () => void }) {
  const { data, failed, lineWords, notesFor } = useScrollText();
  const [sel, setSel] = useState<Selection>(null);
  // The folio is keyed by entry, so a new entry mounts a fresh component and selection.

  if (failed) return null;
  const lines = data?.entries[entryId];
  if (!data || !lines) return <section className="scroll-text" aria-busy="true"><div className="st-head"><span className="small-caps">The text</span></div><p className="st-loading">Loading the lines of the scroll…</p></section>;
  const marked = new Set<string>();
  if (sel?.note) for (const [line, words] of data.notes[sel.note]?.at ?? []) for (const i of words) marked.add(`${line}#${i}`);
  if (sel?.word !== undefined) marked.add(`${sel.line}#${sel.word}`);
  const first = lines[0].ref, last = lines[lines.length - 1].ref;
  const span = first === last ? first : first.split(" ")[0] === last.split(" ")[0] ? `${first}–${last.split(" ")[1]}` : `${first}–${last}`;

  return <section className="scroll-text" aria-label={`The text of entry ${entryId}`}>
    <div className="st-head"><span className="small-caps">The text · {span}</span>{onOpenScroll ? <button type="button" onClick={onOpenScroll}><ScrollText size={13}/>Open the scroll</button> : <a href={`${textPage}#entry-${entryId}`} target="_blank" rel="noreferrer">Full text <ExternalLink size={12}/></a>}</div>
    <ol className="st-lines">{lines.map(l => {
      const lineNo = l.ref.split(" ")[1];
      return <li key={l.ref} className={sel?.line === l.ref ? "st-line active" : "st-line"}>
        <span className="st-no" aria-label={`Line ${l.ref}`}>{lineNo}</span>
        <p className="st-he" lang="he" dir="rtl">{l.w.map((w, i) => {
          const inside = i >= l.from && i < l.to;
          const key = `${l.ref}#${i}`;
          const cls = ["st-w", w.n != null ? "st-num" : "", w.greek ? "st-greek" : "", notesFor(l.ref, i).length ? "has-note" : "", marked.has(key) ? "on" : "", inside ? "" : "outside"].filter(Boolean).join(" ");
          return <Fragment key={i}>{i > 0 && " "}<button type="button" className={cls} aria-label={w.n != null ? `numeral ${w.n}` : plain(w)} title={inside ? undefined : "Part of the neighbouring entry"} onClick={() => setSel(sel?.line === l.ref && sel.word === i ? null : { line: l.ref, word: i })}>{w.n != null ? <>{w.n}{w.h.length > 0 && <> <Segments w={w}/></>}</> : <Segments w={w}/>}</button></Fragment>;
        })}</p>
        <p className="st-en">{l.tr.map((s, i) => typeof s === "string" ? <Fragment key={i}>{s}</Fragment> : <button key={i} type="button" className={sel?.note === s[1] ? "st-nt on" : "st-nt"} onClick={() => setSel(sel?.note === s[1] ? null : { line: l.ref, note: s[1] })}>{s[0]}</button>)}</p>
        {sel?.line === l.ref && <ReadingCard data={data} line={l} sel={sel} notesFor={notesFor} lineWords={lineWords} onClose={() => setSel(null)}/>}
      </li>;
    })}</ol>
    <p className="st-credit">Hebrew: M. G. Abegg Jr.’s transcription, ETCBC Dead Sea Scrolls dataset, <a href="https://creativecommons.org/licenses/by-nc/4.0/" target="_blank" rel="noreferrer">CC BY-NC 4.0</a>. Translation and notes written for this project. Select a word or an underlined phrase for the editions’ readings.</p>
  </section>;
}

export function ReadingCard({ data, line, sel, notesFor, lineWords, onClose }: { data: TextData; line: Pick<Line, "ref" | "w">; sel: NonNullable<Selection>; notesFor: (line: string, i: number) => string[]; lineWords: Record<string, Word[]>; onClose: () => void }) {
  const w = sel.word !== undefined ? line.w[sel.word] : null;
  const ids = sel.note ? [sel.note] : w ? notesFor(line.ref, sel.word!) : [];
  const kinds = w ? Array.from(new Set(w.h.map(s => s[1]).filter(k => sigla[k]))) : [];
  return <div className="st-card" role="region" aria-label="Word and readings" aria-live="polite">
    <button type="button" className="st-close" aria-label="Close" onClick={onClose}><X size={14}/></button>
    {w && (w.n != null
      ? <><div className="st-card-word st-card-num">{w.n}</div><p>A numeral written with signs. In this transcription: {w.ns?.split("+").join(" + ")} (a stroke is 1; the other signs are 10, 20 and 100).</p></>
      : <><div className="st-card-word" lang={w.greek ? "grc" : "he"} dir={w.greek ? "ltr" : "rtl"}><Segments w={w}/></div>
        {kinds.map(k => <p key={k} className="st-small">{sigla[k]}</p>)}
        {w.greek ? <p>Greek letters engraved at the end of an entry. Seven such groups stand in columns I–IV; their meaning is unknown.</p>
          : w.m && <dl className="st-parts">{w.m.map((m, i) => <Fragment key={i}><dt lang="he" dir="rtl">{m[0]}</dt><dd><span lang="he" dir="rtl">{m[1].replace(/_\d+$/, "").trim()}</span> {data.gloss[m[1]] ?? ""}</dd></Fragment>)}</dl>}
      </>)}
    {ids.map(id => {
      const n = data.notes[id]; if (!n) return null;
      const shown = n.at.map(([ln, words]) => words.map(i => { const x = lineWords[ln]?.[i]; return x ? (x.n != null ? String(x.n) : plain(x)) : ""; }).join(" ")).join(" … ");
      return <section key={id} className="st-note">
        <h4>{n.label ?? id}</h4>
        <ul className="st-readings">
          {shown && <li className="shown"><span className="who">Text shown <em>Abegg</em></span><span className="rd" lang="he" dir="rtl">{shown}</span></li>}
          {(n.readings ?? []).map((r, i) => <li key={i}><span className="who">{r.who}{r.ref && <em> {r.ref}</em>}</span>{r.reading && <span className="rd" lang="he" dir="rtl">{r.reading}</span>}{r.meaning && <span className="mn">{r.meaning}</span>}</li>)}
        </ul>
        {n.note && <p>{n.note}</p>}
        {n.src && n.src.length > 0 && <p className="st-small">Research files: {n.src.map((f, i) => <Fragment key={f}>{i > 0 && ", "}<a href={research + f} target="_blank" rel="noreferrer">{f.split("/").pop()}</a></Fragment>)}</p>}
      </section>;
    })}
    {w && !ids.length && !w.greek && <p className="st-small">The editions are not reported to differ on this word.</p>}
  </div>;
}
