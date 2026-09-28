"use client";

import { BookOpen, ExternalLink } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import evidence from "./atlas-evidence.json";

export default function EvidenceReview({ entryId, placeId }: { entryId: string; placeId: string | null }) {
  const review = evidence.entries.find(e => e.entryId === entryId && e.placeId === placeId);
  if (!review) return <p className="unreviewed-note">Reading and exact-feature confidence have not yet been assessed separately for this candidate.</p>;
  const axes = [{ name: "Reading", value: review.reading, note: review.readingNote }, { name: "Site", value: review.site, note: review.siteNote }, { name: "Exact feature", value: review.feature, note: review.featureNote }];
  return <section className="feature-review" aria-label="Confidence and feature investigation">
    <span className="small-caps">Evidence review · 28 September</span>
    <div className="confidence-axes">{axes.map(axis => <div key={axis.name}><span>{axis.name}</span><strong>{axis.value}</strong></div>)}</div>
    <p>{review.finding}</p>
    <Dialog>
      <DialogTrigger asChild><button className="review-open"><BookOpen size={16}/>Compare features & evidence</button></DialogTrigger>
      <DialogContent className="feature-dialog">
        <DialogHeader><span className="small-caps">Investigation / entry {entryId}</span><DialogTitle>{review.title}</DialogTitle><DialogDescription>What supports the proposal, what could weaken it, and what to check next.</DialogDescription></DialogHeader>
        <div className="review-axes">{axes.map(axis => <section key={axis.name}><h3>{axis.name}<span>{axis.value}</span></h3><p>{axis.note}</p></section>)}</div>
        <p className="review-method">{evidence.method}</p>
        <h3 className="review-heading">Feature comparisons</h3>
        <div className="feature-comparisons">{review.features.map((feature,i) => <article key={feature.id}><span className="feature-number">{String(i+1).padStart(2,"0")}</span><h4>{feature.name}</h4><dl><dt>Why compare it</dt><dd>{feature.support}</dd><dt>Limit</dt><dd>{feature.limit}</dd><dt>Discriminating check</dt><dd>{feature.test}</dd></dl></article>)}</div>
        <section className="review-next"><h3>Next evidence needed</h3><p>{review.next}</p><p>Independent specialist review and field verification remain pending. Map shading still represents the locality’s coordinate uncertainty.</p></section>
        <section className="review-sources"><h3>Sources and dependencies</h3><p>{review.dependency}</p><ul>{review.sources.map(id => {const source=evidence.sources[id as keyof typeof evidence.sources];return <li key={id}><a href={source.url} target="_blank" rel="noreferrer">{source.label}<ExternalLink size={13}/></a><p>{source.access}</p></li>;})}</ul><a href="https://github.com/quadrin/AncientHebrewTexts/blob/main/copper_scroll/feature_investigation.md" target="_blank" rel="noreferrer">Full dossier and review packets<ExternalLink size={13}/></a></section>
      </DialogContent>
    </Dialog>
  </section>;
}
