# Qumran tunnel photographs and upstream connection

Reviewed 28 September 2026, following the [entry 21 comparison](entry21_feature_comparison.md).

Reeder–Jol 2006 Figure 2's tunnel photograph and Magen–Peleg 2018 Figure 87 depict the **same physical mouth with high visual confidence**. Magen labels it the long tunnel's entrance; Reeder calls the pictured opening an exit without identifying a tunnel number. The captions alone cannot establish flow direction. This match strengthens the long-tunnel correspondence but leaves the exact Copper Scroll feature confidence low.

## Photograph audit

**Reeder–Jol 2006, Fig. 2, printed p. 226 → Magen–Peleg 2018, Fig. 87, printed p. 76.** Three visible configurations support the match: the irregular, notched crown of the opening beneath an overhanging block; the narrow projecting rock wall on the image's left, ending beside the opening; and the broken horizontal bedrock ledges on the right, interrupted by a near-vertical joint beside the aperture. Their arrangement agrees across the two views. Reeder's people obscure part of the threshold; Magen's photograph exposes more of the channel and cliff. This is a visual correspondence, without photogrammetric control points or a camera-pose solution.

The matched mouth belongs to Magen's long tunnel by his caption. His p. 79 describes the tunnel running from west to east and explicitly measures the first crack from its western entrance. Combining that text with Figure 87 makes the **western/upstream mouth** the working attribution. Reeder's generic “exit” could describe passage through the tunnel rather than hydraulic direction; this review does not silently amend the caption. Reeder's plan places the longer eastern tunnel at label **Tunnel 1**, so the photo-to-number assignment remains a plan-and-text inference.

**Ilan–Amit 1989, Fig. 4, printed p. 286 → Magen–Peleg 2018, Fig. 86, printed p. 76.** The captions identify the eastern opening of the eastern tunnel and the long tunnel's exit, respectively. They are compatible with the other end of the same tunnel. The available Ilan reproduction crops the upper part of the opening and presents the approach obliquely. The foreground rubble and angle prevent this review from identifying a comparably discriminating set of shared rock joints. Retain this as a **probable caption-and-route correspondence**, rather than another independently verified visual match.

**Ilan–Amit Fig. 3, printed p. 285** shows the eastern tunnel's interior and a lateral patch of light. It does not give a sufficiently complete sequence of both internal breaches to match the two openings individually to Magen's measurements. An illuminated gap in a single interior view does not supply its distance from a named entrance.

**Ilan–Amit Fig. 2, printed pp. 284–285** locates both tunnels in a panorama and labels the western tunnel as point 10 and eastern tunnel as point 11. The traced route and text support their spatial order. The panorama does not independently identify Reeder's upstream boulder.

**Masterman 1903, Fig. 2, printed p. 266** shows an open channel near its beginning. It shows neither a securely matched tunnel mouth nor a demonstrably identical view of Reeder's boulder. The dimensional correspondence in Masterman's p. 267 remains useful; the photograph supplies upstream context only. No object in it was used as an improvised scale.

The Reeder Flash-page renderings contain black image placeholders. This review inspected the separately extracted embedded bitmap `reeder2006-page-03.bitmap-16.png` for the tunnel image and `reeder2006-page-08.bitmap-18.png` for Figure 6. Figure 6 shows a collapsed channel section downstream from the tunnels, not the upstream intake. The HTML/SVG page render alone is insufficient for reviewing these photographs.

## Tracing upstream

Starting at the probable long tunnel, both plans lead west through an open channel to the short tunnel and a lower branch. Continue upstream from that split to the channel beginning in Ilan's plan and to the rock–pothole–wall collection sequence in Reeder's plan. This topology supports a **probable shared upstream collection sector**. It does not make the rock itself point 3.

Ilan's point 3 is at the outlet of a small ravine on the main wadi's northern bank (p. 284). Reeder's p. 231 follows an uphill channel segment to the boulder, a depression and pothole above it, a wall at the depression's upper end, and a plunge pool and waterfall above that wall. Reeder's earlier 2004 account (printed p. 18, Fig. 12) describes a small dam and channel collecting winter runoff farther up the canyon. This is the same research programme, not independent corroboration.

The resulting working hypothesis is that Reeder surveyed the small-ravine collection works feeding the vicinity of Ilan point 3. His surviving wall would then belong to that upstream collection sequence. Ilan point 4 remains the separate, hypothesized impounding dam across the main-wadi basin; Ilan explicitly reports no surviving remains. Neither hydraulic function nor the word “dam” establishes that these are the same structure.

## Two-anchor plan test

The [reproducible calculation](registration/check_upstream_similarity.py) fits an orientation-preserving similarity between manually picked tunnel centres. Its [inputs and output](registration/upstream_similarity.json) retain both image frames. This is an exploratory comparison of printed plans, with no geographic registration.

The Ilan centres were picked at approximately (355, 1238) for point 10 and (419, 1265) for point 11 in the 1190-pixel-wide page image. The corresponding Reeder picks are (186, 675) and (239, 698) in his 1380 × 1044 figure. Tunnel centres are approximate drawing locations, not surveyed stations. The cropped Ilan tunnel symbols were inspected to distinguish the dashed short tunnel from its adjoining channel; the interactive redrawing has been corrected accordingly.

The baseline transform places Ilan point 3, sampled at (253, 1200), near **(102, 643)** in Reeder's image, beside the depicted pothole/boulder sector. The boulder is separately sampled near (74, 650). The implied separation is about 8 m on Reeder's printed scale. This is a derived distance between drawing positions, not a ground measurement or an established intake-to-rock distance.

The transform's scale is approximately 0.832 destination pixels per source pixel; the two printed scale bars suggest approximately 0.961. That roughly 13% discrepancy indicates that picking, drawing generalization or plan differences matter. Two fitted anchors necessarily match exactly and supply no validation residual. A branch-junction comparison falls within about 8 Reeder pixels (roughly 2 m on the printed scale), but the junction's exact correspondence and branch history are themselves uncertain; it is not independent survey control.

As a sensitivity check, 20,000 trials independently perturb the four anchor picks and intake pick by up to 4 pixels in each axis. This is an analyst-chosen perturbation, not a measured error distribution. With seed 21, the projected intake ranges over approximately x = 68–129 and y = 607–670 in the Reeder frame; drawing-implied distances to the fixed rock pick range from roughly 1–17 m. These sampled extrema are not confidence intervals or exhaustive bounds, and omit original survey distortion and uncertainty in the rock pick. They demonstrate that the two-anchor fit cannot distinguish a unique intake position within the collection sector.

## Effect on the candidates

Candidate A, Ilan point 3, retains first priority as the head of the whole conduit. Candidate B, Reeder's boulder, retains second priority as a particular physical comparison for the restored stone. Their membership in the same upstream collection sector becomes more plausible, while their exact relation remains unresolved. Candidate D gains a more explicit mouth attribution through the Reeder–Magen photo match; it remains downstream and therefore a weaker conduit-head candidate.

The named reservoir and the two internal fissures in entry 22 remain unestablished. This review supplies no individual photo match for either fissure. The specific positions reported by Magen—first crack from the western entrance, second farther along—remain the appropriate textual anchors for a future photographed passage through the tunnel.

The next discriminating digital evidence is a photograph or sequence showing **the boulder, pothole and wall together**, plus the small ravine's connection to the main channel. For the tunnel correspondence, seek a sequence starting at the now-matched western mouth and showing both internal openings. Additional generic tunnel-mouth photographs would add less information than those missing transitions.

Sources inspected: Ilan–Amit 1989 pp. 283–286, supplied scans; Magen–Peleg 2018 pp. 76–79, supplied chapter; Reeder–Jol 2006 pp. 226, 229–231, publisher's recovered text and embedded images; Reeder et al. 2004 p. 18 and Fig. 12, existing local PDF/text; Masterman 1903 pp. 266–267, public digitization. The cited images have not been republished in this report.
