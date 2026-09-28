import type { Candidate, Entry, Place } from "./atlas-types";

export type SortOrder = "scroll" | "confidence" | "ancient" | "candidate" | "region";
export const sortLabels: Record<SortOrder, string> = {
  scroll: "Scroll order", confidence: "Confidence · highest first", ancient: "Ancient name · A–Z", candidate: "Candidate name · A–Z", region: "Region · A–Z",
};
const confidenceRank: Record<string, number> = { high: 3, medium: 2, low: 1, unknown: 0 };
const statusRank: Record<string, number> = { preferred: 2, possible: 1, weak: 0 };
const regionNames: Record<string,string> = {jericho:"Jericho & Qumran",jerusalem:"Jerusalem",region:"Judean hills & north",unplaced:"Unplaced"};
const compare = (a: string, b: string) => a.localeCompare(b, "en", { numeric: true, sensitivity: "base" });
export function sortEntries(entries: Entry[], order: SortOrder, places: Record<string, Place>) {
  const score = (entry: Entry) => Math.max(0, ...entry.candidates.map(c => confidenceRank[c.confidence] ?? 0));
  return [...entries].sort((a, b) => {
    let result = 0;
    if (order === "confidence") result = score(b) - score(a);
    if (order === "ancient") result = compare(a.title, b.title);
    if (order === "candidate") result = compare(a.candidates[0] ? places[a.candidates[0].placeId].shortName : "\uffff", b.candidates[0] ? places[b.candidates[0].placeId].shortName : "\uffff");
    if (order === "region") result = compare(regionNames[a.region]??a.region, regionNames[b.region]??b.region);
    return result || compare(a.id, b.id);
  });
}
export function sortCandidates(candidates: Candidate[], order: string, places: Record<string, Place>) {
  return [...candidates].sort((a, b) => {
    if (order === "alphabetical") return compare(places[a.placeId].shortName, places[b.placeId].shortName);
    if (order === "confidence") return (confidenceRank[b.confidence] ?? 0) - (confidenceRank[a.confidence] ?? 0) || (statusRank[b.status] ?? 0) - (statusRank[a.status] ?? 0);
    return (statusRank[b.status] ?? 0) - (statusRank[a.status] ?? 0);
  });
}
