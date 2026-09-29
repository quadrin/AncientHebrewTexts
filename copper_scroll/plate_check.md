# Plate check: disputed readings against Puech's photographs and radiographs

29 September 2026. This addresses Q11 and the [independent reading packet](feature_investigation.md#independent-reading-packet--ready-not-yet-reviewed). It compares the lines where the editions disagree with the column plates in Puech 2006, vol. II.

**Result.** Of the 30 lines checked, the plates support or lean to one of the competing readings on 9 and cannot decide 11. The other 10 were not located securely, not analysed, or not in dispute between the editions. A verification pass against the same plates corrected several first-draft statements; they are worded below as corrected. Three results bear on site identifications:

- **Entry 49 (Siloam), X 15.** The letter after של is a single curved stroke with no head bar. That is the form Puech describes as a cursive *waw* (2006 p. 200). Earlier project files said Puech "reads the engraved ר as ו"; that misstates his argument. The Siloam reading still needs the particle that Puech supplies, and it still needs a period trough.
- **Entry 31 (Doq), VII 11.** The landmark word ends in two letters after המש, the second of them ח. This leans to Puech's *hmšṭḥ* ("drying place") and away from המשמרה ("guard post"). The plates do not decide it.
- **Entry 40, IX 7.** The direction word shows a short vertical and a closed final mem. In the space before them, by the saw cut, neither the copy nor the radiograph shows a clear stroke, though the zone is cracked and washed out. This leans to ים ("the Sea, west": Milik, Lefkovits) and away from Puech's דרום.

No site confidence changes on the plates alone. The reading axis changes for entries 7, 12a, 31, 32, 39, 40, 49, 52, 55 and 60; see [the table](tables/plate_check.csv).

## What was checked

**Images.** Puech 2006, vol. II (the local PDF parts 9–11):

| Series | Plates | What it shows | Use here |
|---|---|---|---|
| Radiographs of the original segments | CCCXXXIII–CCCLVI (two per column) | engraving depth through the metal; several strips per plate, often overlapping | primary for stroke presence |
| Colour photograph of the galvanoplastic copy | CCCLIX–CCCLXXXI (odd numbers) | surface relief of the electrotype copy made during the EDF conservation | primary for letter shapes |
| Puech's facsimile drawing | CCCLX–CCCLXXXII (even numbers) | an editorial drawing | used only after the blind pass, to locate letters |
| Second photograph of the copy | CCXCVI–CCCVII | — | excluded: after registration it correlates 0.94–0.96 with the first series, so it is the same photograph |

The copy photographs are about 1,400 × 1,800 px per column; the radiographs about 400–800 px per strip. These are printed reproductions, not the metal or the original negatives. The DJD III plates (Milik's drawings and the 1950s photographs) are not in the repository; they were not re-examined.

**Lines.** 30 lines, one or more per disputed reading in `text/readings.json` where the dispute concerns letters, signs or spacing rather than meaning. They cover Q8, Q9, Q12, Q14, Q15, Q26, Q27, Q35 and Q41, plus the restored words in entries 16 and 21.

**Blind protocol.** [`tools/plate_extract.py`](tools/plate_extract.py) extracts the plates; [`tools/plate_check_items.py`](tools/plate_check_items.py) cuts each line from the copy and both radiograph plates and labels it with a random code (P01–P30). Two independent readers (separate model sessions, R1 and R2, each split into two halves) had only the crops and [the instructions](registration/plate_check/INSTRUCTIONS.md). They saw no line numbers, editions or site proposals.

- **Stage 1:** each reader transcribed every line letter by letter with a grade.
- **Stage 2:** only after saving Stage 1, each reader answered one targeted question per line ([questions](registration/plate_check/QUESTIONS.md)). A question names the competing letter shapes but not which edition or site they belong to.
- **Reconciliation:** I compared their answers with the editions and made my own non-blind check against the same plates and Puech's commentary.

Outputs, code key and crop coordinates are in [`registration/plate_check/`](registration/plate_check/). No image or crop is committed.

**Limits.**

- The readers recognised the object as the Copper Scroll. They report that they did not use remembered readings, but that cannot be verified.
- Their letter-level readings of whole lines are poor. Most letters are graded "possible", and word division was rarely visible. The protocol is useful for specific shape questions, not as a new transcription. The DSS workstream's warning about reading worn script by eye applies here (repository `CLAUDE.md`).
- Several crops cut the line at the wrong height, because the copy and the radiograph strips are offset or the line slopes. Where a reader examined the wrong stroke, that answer is not counted (noted below).
- The script distinguishes some letters poorly. Puech notes a cursive reš that looks like waw (2006 p. 196) and ḥet and he drawn alike (p. 200). A shape that fits one letter does not exclude the other.
- This is a check of published images. It is not a new reading of the manuscript and does not replace a specialist's inspection of the metal, the copy or the original radiographs.

## Results that bear on sites

### X 15, entry 49: Siloam (Q35)

**Plates.** On the copy (pl. CCCLXXVII) and the first radiograph (pl. CCCLI), the letter after the ש-ל group is a single curved stroke of full letter height. It has no horizontal head and is spaced like a letter within a word. The ר in עסר (X 6, same plate) has a short head bar. Next comes one roof over three legs (ח with a following yod or waw, in Puech's šlwḥ w-), then a ל.

**Readers.** R2 described the stroke independently as "a single curved vertical from the top line to the baseline … no horizontal roof or head bar", though it did not recognise the ש before the ל. R1 took the roofed group for a ש and answered about the next ל (a location error), so its answer is not counted.

**Editions.** Puech 2006 p. 200 reads the sequence as *šlwḥ* "with the first waw cursive … preferable to reš for rḥyl". He then supplies a genitive [[של]], lost by haplography: "the source of the waters [[of]] Siloam and under". He does not correct an engraved reš. He calls "of Jehu" (Lefkovits) "far from compelling, though materially possible".

**Verdict: leans to ו (Puech, Milik), not decisive.** The plates show no reš head. Because the script has a waw-like cursive reš, the shape cannot exclude ר.

**Effect.** The Siloam reading depends on the supplied particle and on the competing word division, not on emending a letter. The earlier wording in `phase5_summary.md`, `site_identification_review.md` and `readings.json` is corrected here. Site confidence stays **medium**: the particular trough is still unestablished (F6.5).

### VII 11, entry 31: Doq landmark word (Q24)

**Plates.** On the copy (pl. CCCLXXI) the word begins ה-מ-ש. Two letter-spaces follow:

- an arch-topped letter whose lower half is damaged (מ or ט);
- a roofed letter whose two legs both reach the roof (ח; a ה would show a gap at the left leg).

A vertical crack runs between them. Both exposures of the first radiograph plate (CCCXLV) show the same arch and roof. No third letter is confirmed: faint uprights appear on the copy against the crack and just left of the ח, but not on the radiograph.

**Readers.** Both independently:

- the last letter is ח ("probable");
- a separate ו or other letter in the crack is not confirmed (R1 noted a short vertical against the crack, not seen on the radiograph);
- the arch letter is undecided between מ and ט.

**Editions.** המשמרה (Milik, Lefkovits, Eshel) needs three letters after ש: מ-ר-ה. Puech's המשט<ו>ח needs two, with a waw inserted by the engraver; he calls ṭet and ḥet "indisputable" (2015 p. 67).

**Verdict: leans to Puech's *hmšṭḥ*, not decisive.** A narrow ר could hide in the crack, and ḥet and he are drawn alike in this hand.

**Effect.** The "guard post / fortress" reading loses its textual advantage. The Hasmonean summit fortress remains the site-level candidate on the name Doq. The feature test in [dok_achor_feature_tests.md](dok_achor_feature_tests.md) should now lead with the drying-place reading, and it still must not use the archaeology to choose the word.

### IX 7, entry 40: west or south (Q14)

**Plates.**

- **Copy (pl. CCCLXXV).** The direction word stands on the far side of a saw cut. It shows two signs: a short vertical, shorter than the letter beside it, and a closed pentagonal final mem. About two letter-widths of corroded surface separate them from the cut.
- **First radiograph (pl. CCCXLIX).** It shows the same two signs. Towards the strip edge there are faint marks, a crack and a washed-out band, but no clear stroke.

**Readers.** Both: two letters, a ו/י and a ם. In the gap R1 found "only indistinct traces" and left a four-letter word undecided; R2 saw one low curved stroke, which it assigned to the line below.

**Editions.** Puech 2006 p. 196 reads דרום: "traces of dalet, reš followed by waw/yod and certain mem". His facsimile (pl. CCCLXXVI) draws the ד and ר as dashed traces in exactly this gap. Milik and Lefkovits read ים; Milik's drawing shows two signs (see `readings.json`).

**Verdict: leans to ים, not decisive.** Puech's dalet and reš are not clearly visible in these reproductions. He worked from better images, and the metal by the saw cut is damaged.

**Effect.** Milik's Upper Beth-Horon placement keeps its textual basis. Puech's statement that "the certain reading drwm removes the main support for Ḥoron" is not borne out by these plates, though they do not refute it.

### XI 12, entry 55: Bethesda (Q26)

**Plates.** The copy (pl. CCCLXXIX) shows the word after בית clearly. In order:

1. a Γ-shaped letter (ה without a visible left leg, or א);
2. א;
3. ש;
4. a letter with a head bar and a right vertical (ו or ד);
5. a two-legged roofed letter with no foot;
6. י;
7. a long final stroke.

The same line ends באשוח.

**Readers.** Both: the fifth letter is ח rather than ת (graded "possible"). R2 read the fourth letter as ד; R1 could not decide between ו and ד. Neither confirmed the final ן: R1 had "ן?", R2 "-חיו or run on".

**Verdict: leans to ח, not ת.** If it is ח, Milik's "Bet Eshdatain = Bethesda" needs at least one emendation, ח to ת, and possibly two. Puech's and Lefkovits's "house of the (two) reservoirs" fits the letters. The ending is unclear.

**Effect.** The twin-pool description stands. The name reading is weaker than before. Bethesda stays **medium**, on the double pool alone, with the Sisters of Sion twin pool as a rival (unchanged).

### XII 10, entry 60: Janoah (Q12)

**Plates.** On the copy (pl. CCCLXXXI), after בשית:

- a word that begins with ש and a box letter (ב or כ);
- then a letter like נ;
- then a letter at a fold in the copy (ה or ח);
- then a clear בצפון;
- no צ between the ש-group and בצפון.

**Readers.** Both saw a ב/כ-type letter followed by a נ-like letter, with no yod between them. At the fold R2 allows a possible י/ו, and R1 hatching that "could be a cancelled letter".

**Verdict: leans against Milik's "Smooth Rock" (שבצח) and against a yod between ב and נ.** The sequence fits Puech's שכנה or שבנה ("situated") best. Lefkovits's שבינח ("in Janoah") needs a yod between ב and נ, which neither reader saw, and a ח that the fold cannot confirm. Not decisive.

**Effect.** A second place name beside Koḥlit is not supported by the plates. Q12 stays open, narrowed.

## Results on sums, Greek letters and restorations

| Line | Question | What the plates show | Verdict |
|---|---|---|---|
| IX 6 (39), Q8 | ½, 1–2 or 24? | After ככ: one numeral sign, three unit strokes, then a distinct sign with a curled head and a long descender, like ף. Both readers and my check agree on the last three. Puech's facsimile draws the first sign as a double '3' (20); both readers describe a single hook (10). | **Supports** a special final sign (Puech, Milik: ½). It is not a unit stroke, which Allegro's 24 and Lefkovits's 1–2 options would need. The value ½ comes from the editors' sign table. Whether the first sign is 20 or 10 (23½ or 13½) is unresolved on these images. |
| VII 16 (32) | 80 or 60? | Radiograph pl. CCCXLVI, two of its three exposures: ככ followed by **four** arch-shaped numeral signs, the first larger and peaked (also so drawn in Puech's facsimile). Both readers counted four; R2 could not fully exclude a fifth. The copy is too damaged. | **Supports four signs.** That gives Puech's 80, against Milik and Lefkovits's 60, only if all four are 20-signs. |
| XI 7 (52), Q9 | cancelled letters or a sum? | At the line end, a box letter and a ק-like letter (R1: finely incised, lighter than the punched letters). No ככ, no unit strokes (both readers, graded "possible"). | **Leans to Puech** ({בק}, no sum) against Lefkovits's ככ + numeral. |
| II 4 (7), Q27 | ΘΕ or ΞΕ? | A closed ring with a central bar (both readers, copy only). The second sign is three-barred and closed on one side for R2; R1 could not identify it. | **Supports Θ, not Ξ.** The ΞΕ = 65 coincidence falls away. |
| III 7 (12a), Q27 | ΤΡ or ΤΡΙ? | Τ, a small Ρ-loop, then a vertical stroke longer than a letter, directly after it. A blank of about five letter-widths separates it from the two 20-signs. R1 saw it independently; Puech's facsimile also draws it. | **A third stroke is present.** Whether it is an Ι (Allegro, the Baker drawing, Lefkovits's option) is not established. Puech rejects a third letter. A unit stroke would make 41, which no edition reads. |
| IV 2 (15), Q27 | first Greek letter; cancelled Ι | The Greek group lies on a separate, corroded fragment. Neither reader found any Greek letter. | **Cannot decide.** |
| X 6, X 13 (46, 48), Q15 | cubits or feet? | The unit word begins with a gimel-shaped, Λ-with-foot letter, as in the drawings. At X 13 no ר-shaped letter precedes it. At X 6 the preceding stroke can end the previous word. | **Cannot decide the unit.** The engraved form is confirmed: Lefkovits's printed אמות normalises it. Puech explains it as a cursive alef "close to gamma" (2006 p. 199). Milik's extra ר (רגמות) is not seen at X 13. |
| X 16 (49) | השקת or השקות | No letter between ק and ת (both readers). | Engraved **השקת**, as all editions read; not a dispute between the editions. The web text's השקות comes from the ETCBC dataset. |
| X 16 (49) | the sum, 17 | The copy shows a tens sign and three clear unit strokes, then corroded surface. Radiograph pl. CCCLI shows the same tens sign followed by at least five evenly spaced grooves, and possibly a sixth. | **Compatible with 17.** The first draft's doubt (Q43) came from the copy alone and is withdrawn. |
| V 1–3 (21) | restored link, "stone", depth | The line breaks into a smooth, filled lacuna on the copy and in all radiograph strips. No traces. | These are **pure restorations**. The Qumran constraints stay restoration-dependent (unchanged). |
| IV 3–4 (16) | 14, 40 or 41 cubits | A lacuna with no traces after ארבע. | **Cannot decide.** |
| V 8–9 (23), Q41 | Solomon or Shallum | V 9 begins with a ו written close against עד. Word spacing in this hand is irregular. | **Cannot decide.** It fits either שלומ\|ו עד or שלום \| ועד. |
| VII 14 (32) | Koziba or Buz | The readers split: R1 leans to כ, R2 to ב. Both were unsure the crop showed the right row of the sloping line. | **Not resolved.** |
| VII 15 (32) | הטור or Eshel's הסור | R1 leans to ט over ס (possible); R2 could not follow the line past a seam in the copy. | **Not resolved.** |
| IV 6 (17) | kynyn / bynyn / btyn | Word boundaries not located. | **Not resolved.** |
| XI 13 (55) | the smallest basin (לימומית) | Neither reader found a ימ…ית sequence; a crease crosses the word. | **Not resolved.** |
| V 6 (22) | אשיח שלומו | Included for context; the editions agree on the letters. | **No change.** |
| VIII 9, VIII 13, X 11 | 4/7; 66/67; 10/20 cups | The sums were not located securely in the crops. | **Not resolved; re-crop.** |
| XII 6 (58) | final letter of בית שם | Possibly a closed box (R1); R2 could not locate the word. | The final mem is not in dispute between the editions; **no change**. |

## What this changes

- **Reading axis.** The feature register now records the plate evidence for entries 49, 31, 55, 17 and 40. See [feature_constraints.csv](tables/feature_constraints.csv).
- **Site confidence.** It stays where it was:
  - Siloam (49) and Doq (31) remain medium and conditional;
  - Bethesda (55) remains medium, on the twin pool;
  - Upper Beth-Horon (40) remains a candidate, as before.
- **Corrections.** The characterisation of Puech's Siloam reading is corrected in `phase5_summary.md`, `site_identification_review.md` and `text/readings.json`.

## Next

1. **Re-crop** VIII 9, VIII 13, X 11 and VII 14 with the line fixed on Puech's facsimile, not by height. Then repeat the blind questions on those four lines with two fresh readers.
2. **Specialist review of the leaning results.** Send the unlabelled crops and questions for X 15, VII 11, IX 7 and XII 10 to a human specialist, with the DJD III pl. XLIII.3 pre-cutting photograph for X 15–16. These results lean one way but are not decisive.
3. **Obtain DJD III pls. XLVIII–LXXI at full resolution,** or the IAA 3Q15 images, for an independent image source. Every result here comes from one publication's reproductions.
