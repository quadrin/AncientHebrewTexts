# DSS letter recogniser: project brief

## Goal

Build a letter recogniser for Dead Sea Scroll fragments in the Herodian/Hasmonean square script, trained on fragments whose text is already known, then use it to read the unassigned Cave 4 scraps (4Q9999) and try to place them against known texts.

The recogniser exists to feed a matcher. Its output must be per-letter probabilities (top-k per position), not a single best string, because the matcher tolerates uncertain letters and the statistics depend on honest uncertainty.

## Why this project exists

A chat session (September 2026) tried to read 23 of the richest 4Q9999 fragments by eye and match them against the Bible and the ETCBC scroll transcriptions. Nothing was identified, for two reasons:

1. Most fragments show 3–5 legible letters per line, and a string that short matches somewhere by chance.
2. Reading by eye on worn Herodian script was unreliable. One fragment (B-511092) produced a clean-looking two-line match to Psalm 82:8 from a loose reading; at near-native resolution the line read השמש and the match vanished.

Calibration from that session. Random letter strings taken from sectarian scrolls (1QS, 1QHa, 1QM, CD, 1QpHab, 11Q19, Shirot) were checked against the Bible alone:

| String length | Exact-spelling hit rate | Hit rate ignoring ו/י |
|---|---|---|
| 6 | 31% | 82% |
| 9 | 5% | 30% |
| 11–14 | 1–3% | 5–11% |

Some hits are genuine quotations, so the true accident rate is a little lower; against Bible plus all scrolls it is higher. A single line needs roughly ten certain letters before a hit means anything. The stronger evidence is two or more lines landing a plausible line-width apart in one source.

The session also validated the matcher: a blind text-only overlap check re-identified 2Q29 frag. 1 as Numbers 23:5–7 (published by Tigchelaar 2008 and assigned to 2QNum-b; the Leon Levy library still labels it "Unidentified").

## Hard constraints

- **Image rights.** Leon Levy images are © Israel Antiquities Authority, all rights reserved; single copies for private use only. Never commit images or derived crops to git, never upload them anywhere public, never build a shareable dataset from them. Keep everything under `data/` and put `data/` in `.gitignore` from the first commit.
- **Text licences.** The ETCBC `dss` dataset is CC BY-NC 4.0 (Abegg, Bowley, Cook; converted by Jacobs, Naaijer, Roorda). SQE edition texts carry per-edition copyright statements; read them before reusing text outside this project.
- **No scripts other than square script.** Exclude paleo-Hebrew, Cryptic A and Greek fragments from training and from the target set.
- Any claimed identification is a lead for a specialist, not a finding. Every candidate must ship with the image crop, the recogniser's reading with probabilities, the matched source passage and the E-value.

## Data sources (all checked as reachable on 2026-09-24)

### Leon Levy Dead Sea Scrolls Digital Library (images and metadata)

- Search API, no auth: `GET https://www.deadseascrolls.org.il/api/search?t={manuscript|image}&q={query}&p={page}` returns JSON with `length`, `totalpages`, `results`.
  - Manuscripts listed as unidentified: `t=manuscript&q='Unidentified'` (254 records).
  - All images of one manuscript: `t=image&q=manuscript_numbers:'4Q9999'`.
  - Image records carry `name` (e.g. `B-511264`), `url` (a ggpht base URL), `photo_type` (`Infrared Image`, `Full Spectrum Color Image`, `Scanned Infrared Negative`, ...), `content_type` (`Fragment` or `Plate`), `frag_num`, `plate_numbers`, `side`, `full_width`, `full_height`.
- Images are Google tile pyramids:
  - `{url}` alone returns a 512 px preview.
  - `{url}=g` returns an XML TileInfo (tile size 512, pyramid depth, empty pixels at the edges).
  - `{url}=x{X}-y{Y}-z{Z}-nt0` returns one tile. The top level Z = depth − 1 is full resolution. `prior_work/fetch.py` stitches a full image.
- Use `Infrared Image` + `Fragment` records. `Plate` images (old PAM plates) show many fragments at once and are not labelled per fragment.
- Unidentified Hebrew/Aramaic parchment pool: 34 manuscripts, 2,281 infrared images, of which 2,023 belong to 4Q9999. `prior_work/ink_rank.json` ranks 1,999 of them by letter-sized ink blobs (field 3); the top ~150 are the ones worth reading.

### Scripta Qumranica Electronica (SQE) API: text ↔ image pairing

- Base: `https://sqe-api.deadseascrolls.org.il/v1`, spec at `/swagger/v1/swagger.json`. 1,369 public editions (`GET /editions`).
- Useful endpoints: `/editions/{id}/text-fragments`, `/editions/{id}/text-fragments/{tf}/lines`, `/editions/{id}/artefacts`, `/catalogue/editions/{id}/imaged-object-text-fragment-matches`, `/catalogue/imaged-objects/{io}/text-fragments`, `/editions/{id}/script-lines`.
- `/editions/{id}/artefacts/{aid}/rois` exists, but a sample of 29 editions (including 4Q51, 4Q27, 4Q266, 1QS) returned zero ROIs. Do not count on sign-level boxes; the pairing is at fragment level, and letter positions have to be learned.

### Transcriptions

- ETCBC `dss` Text-Fabric, version 2.0.1: `git clone --filter=blob:none --sparse https://github.com/ETCBC/dss` then `git sparse-checkout set tf/2.0.1`. Sign-level features include `glyph`, `rec` (reconstructed), `unc` (uncertain), `scroll`, `fragment`, `line`. Train only on signs that are not `rec`.
- Hebrew Bible: `openscriptures/morphhb` (`wlc/*.xml`), for the matcher.
- Sefaria's full export is public at `storage.googleapis.com/sefaria-export/` (index in `Sefaria-Export/books.json`), if later/rabbinic parallels are needed.

### Prior work worth reading before designing anything

- Groningen "Hands that Wrote the Bible" / Enoch project: BiNet binarisation for DSS images (arXiv:1911.07930); Enoch data on Zenodo (binarised images of 30 radiocarbon-dated manuscripts; check the licence).
- Tel Aviv / SQE: "Transcription Alignment for Highly Fragmentary Historical Manuscripts: The Dead Sea Scrolls" (2020): the closest published method to milestone M3.
- Groningen HWR coursework has used Kraken and TrOCR on a DSS Hebrew character subset (arXiv:2508.10356); check whether that character set is obtainable.

## Pipeline and milestones

Do them in order. Each milestone ends with a short `reports/Mx.md` stating what worked, the numbers, and what changed in the plan.

- **M0 Inventory.** Pull the SQE edition list and the Leon Levy image metadata for every square-script Hebrew/Aramaic manuscript. Produce a table: edition ↔ manuscript number ↔ infrared fragment images ↔ ETCBC scroll/fragment ids, with counts of preserved (non-`rec`) letters per fragment.
- **M1 Pairing.** For identified fragments, pair each infrared fragment image with its transcription fragment and lines (SQE catalogue matches first; fall back to manuscript + fragment number joins). Measure how many pairs are unambiguous.
- **M2 Preprocessing.** Parchment mask (bright parchment on black; exclude the grey tissue mounting strips), binarisation, deskew, line segmentation (Kraken `blla` or projection profiles). Check on 50 hand-inspected fragments.
- **M3 Weak line labels.** Align segmented lines to transcription lines using preserved letters only. Keep a pair only when line counts agree and the image length fits the letter count; then clean iteratively by CTC loss after a first training round. Report how many letters of training data survive.
- **M4 Train.** Line-level CTC recogniser (Kraken, or a small CRNN if Kraken's output lacks usable per-character posteriors). Heavy augmentation: erosion, ink fade, holes, cropping to fragment-like shapes. Output top-k letter probabilities per position.
- **M5 The test that decides whether to continue.** Hold out whole manuscripts. Treat their fragments as unknown; run recogniser → matcher; record identification rate and false-positive rate as a function of visible letters. Include shuffled-reading controls. Stop and write up if identification is poor for fragments with 10 or more letters or if false positives exceed about 1%.
- **M6 Matcher upgrade.** Start from `prior_work/match.py`. Consume per-position probabilities. Replace the letter-independence E-value, which proved far too optimistic, with an empirical one calibrated like `prior_work/calib.py` against non-biblical text and against shuffles. Add the multi-line spacing constraint.
- **M7 Apply.** Run on 4Q9999 in `ink_rank.json` order, then on the other unidentified square-script sets (4Q584, 4Q585, 3Q14, 4Q282, 4Q363, 11Q30, …). Output a review queue: crop, reading with probabilities, best matches, E-value.

## Pitfalls already seen

- Editors' reconstructions sit inside the transcriptions. Train and match only on preserved letters.
- Qumran spelling is fuller than the Masoretic text; keep a mode that ignores ו and י.
- Most 4Q9999 images show a fragment on one or two tissue strips; the strips are textured and can pass as parchment in a naive mask.
- Common words (אשר, לשארית, החכמה, עליכם) produce dozens to hundreds of chance hits. Only multi-line or long-line matches carry weight.
- Aramaic fragments exist in the target pool; the matcher needs the Aramaic scrolls in its reference set.

## Files in `prior_work/`

- `q.py`: Leon Levy search API helper.
- `fetch.py`: tile stitcher and fragment cropper for Leon Levy images (full resolution, stays local).
- `ink.py`: ranks fragments by letter-sized ink blobs from 512 px previews. Output: `ink_rank.json`.
- `zoom.py`: contrast-enhanced crop for reading.
- `match.py`: matcher over Bible + ETCBC scrolls with uncertain-letter classes, a multi-line spacing constraint and a mode that ignores ו/י. Its analytic E-value is too optimistic; see M6.
- `calib.py`: the false-hit calibration that produced the table above.
- `overlap.py`: text-only overlap check between "unidentified" transcriptions and the rest of the corpus (the 2Q29 validation).

These scripts assume data files from the chat session (`bible.json`, `dss_lines.json`, `q9999_ir.json`, `thumbs/`) that are not included. Regenerate them in M0 rather than hunting for them.
