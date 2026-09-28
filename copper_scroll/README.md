# Copper Scroll (3Q15): hiding places and Greek letters

Desk research from editions, texts and maps only. **Nothing here proposes or supports excavation.**

This folder is separate from the DSS letter-recogniser project described in the repo's `CLAUDE.md`.

## Phases

1. **Master table of all entries** (done, session 1; see `phase1_summary.md`)
2. **Landmark lexicon:** Bible, Mishnah, Josephus, Eusebius (done, session 2; see `phase2_summary.md`)
3. **Site candidates:** scored against written criteria and mapped at site level (done, session 2; see `phase3_summary.md`)
4. **Greek letters:** occurrences and tests of the hypotheses (done, session 2; see `phase4_summary.md`)
5. **Archaeology check** of the Phase 3 places, published reports only (done, session 2; see `phase5_summary.md`)

## Current site assessment

The [2026-09-28 site identification review](site_identification_review.md) updates Phase 5. It returns Siloam to medium overall confidence, records the full Szanton 2023 source, and distinguishes site compatibility from identification of a particular feature. The revised Phase 5 summary and index contain the current verdicts; the Phase 3 files retain their original assessment.

The [feature investigation](feature_investigation.md) adds five feature comparisons, a source-dependency audit, separate reading/site/feature judgments, and prepared specialist and non-invasive field-observation packets. The [constraint register](tables/feature_constraints.csv) records the tests that could distinguish or weaken each proposal. No exact feature or deposit has been identified.

## Files

| File | In git? | Contents |
|---|---|---|
| `sources.md` | yes | What is in the repo, what is missing, page offsets, encodings |
| `phase1_summary.md` | yes | Entry count, clearest and most damaged entries, recurring terms, sequences |
| `phase2_summary.md` | yes | Phase 2: the landmark lexicon, its main results and what it means for Phase 3 |
| `phase3_summary.md` | yes | Phase 3: method, the 23 best-supported places, contested cases, gazetteer errors, files |
| `phase4_summary.md` | yes | Phase 4: the Greek letters: readings, layout, 14 families of hypotheses, 9 tests, conclusions |
| `phase5_summary.md` | yes | Phase 5: what published reports say about each place's required landmark and its period; changed verdicts; limits |
| `site_identification_review.md` | yes | Current shortlist and the 2026-09-28 corrections to Phase 5 |
| `web/index.html` (with `web/map1-overview.webp`, `web/map3-jerusalem.webp`) | yes | The public web page: scored place identifications, the archaeology check, the Greek letters, maps 1 and 3. For GitHub Pages at `https://quadrin.github.io/AncientHebrewTexts/copper_scroll/web/` once the folder is on `main` |
| `findings_log.md` | yes | Running log, evidence vs inference, with pages |
| `open_questions.md` | yes | Running list of open questions |
| `tables/entry_concordance.csv` | yes | Puech entry ↔ Lefkovits item ↔ Milik item (from Milik 1960) ↔ line range, with boundary notes and other editors' divisions |
| `tables/landmark_lexicon_index.csv` | yes | Phase 2 index: 121 terms with category, entries, lines, confidence in the meaning, and the attestations checked for sense (counts and references for the Bible, Mishnah, Josephus and Onomasticon) |
| `tools/puech_heb.py` | yes | Decoder for Puech 2006's legacy Hebrew font (text layer → Unicode, logical order) |
| `copper_scroll_master_table.csv` | **no** | The master table (61 rows). It contains Puech's full edited text and Lefkovits's text and translation. |
| `variants_long.csv` | **no** | 2,072 reported readings, one per row (scholar, reading, gloss, reporting edition, page, verdict) |
| `puech_lines.csv` | **no** | Puech's text line by line (181 lines), with numeral values and sign notes |
| `copper_scroll_landmark_lexicon.csv` | **no** | The full Phase 2 lexicon (121 rows): each edition's meaning with page and short quotes, reading and meaning disagreements, attestations with comments, landmark type, what the term implies for locating, confidence, background knowledge (labelled), open questions |
| `milik1962_words_sites.csv` | **no** | Milik's DJD III word list (section C, 212 entries) and site list (section D, 75 entries): Hebrew, occurrences, meaning (French), English summary, parallels, identification, his hedging verbatim |
| `milik1960_commentary.csv` | **no** | Milik 1960's commentary, one row per heading (49): readings, identifications, evidence cited, his hedging verbatim. Phase 3 material |
| `tables/phase3_site_index.csv` | yes | Phase 3 index, one row per entry: status (best-supported / possible only / unknown), best-supported place and confidence, possible places, candidate counts by verdict. No edition text |
| `tables/phase3_places.csv` | yes | The 37 hand-curated places: coordinates, coordinate source, precision, kind (point or area), and the entries placed there by verdict and confidence |
| `tables/phase4_greek_letters.csv` | yes | The seven Greek-letter groups: readings in each edition, other readings, what they follow, gap, value as numerals |
| `tables/phase4_hypotheses.csv` | yes | Phase 4 hypotheses (H1–H14): proposers with pages, prediction, test, result, verdict |
| `phase4_records.csv` | **no** | All 212 Phase 4 records (readings, hypotheses, observations) with pages and short quotes |
| `tables/phase5_archaeology_index.csv` | yes | Phase 5 index (31 rows): landmark types required, whether reported at the site, period, Phase 3 and Phase 5 verdicts, main sources |
| `tables/phase5_assessments.csv`, `tables/phase5_reports.csv` | yes | The 37 Phase 5 assessments with reasons, and the 254 report records with pages, URLs and short quotes (20 words or fewer) |
| `phase3_candidates.csv` | **no** | All 292 Phase 3 candidates with the full scoring, reasons with pages, and short quotes |
| `phase3_entries.csv` | **no** | Per entry: the text's requirements, reading notes, best-supported place, why not the others, and the text's own relative description in each edition (quoted, not converted into positions) |
| `phase3_map1_overview.png`, `phase3_map2_jericho_qumran.png`, `phase3_map3_jerusalem.png` | **no** | The three Phase 3 maps, at site level. Map 2 is built on PEF Sheet XVIII (CC BY-NC-SA 3.0) |

The files marked **no** reproduce or quote copyrighted edition text, or are built on a base map with a non-commercial share-alike licence. This GitHub repository is public, so they are delivered to you directly rather than committed.

## Master table columns

- `entry_puech`: Puech's entry number (1–60, plus 12a). Puech and Lefkovits use the same boundaries, so the numbers coincide.
- `item_lefkovits`: Lefkovits's item number.
- `item_milik`: Milik's item number(s), from Milik 1960 (ADAJ 4–5, pp. 139–142). "(only the closing ובתכן/בתכן phrase)" marks where Milik's item begins with the last words of the Puech entry.
- `col_line`: scroll column:line range.
- `hebrew_puech`: Puech's text (pp. 208–216) with his sigla:
  - `[ ]` lacuna/restoration
  - `[[ ]]` letter supplied by the editor
  - `< >` letter inserted by the engraver (also used here for letters written above or below the line)
  - `{ }` letter cancelled by the engraver
  - `x(y)` engraved x is an error for y
  - `a/b` alternative readings
  - `(?)` uncertain
  - ‖ line break
  - Numerals appear as `‹value›`.
- `variants_lefkovits`: hand-checked differences between Lefkovits's text and Puech's. "subst." marks a difference in place, direction, distance/depth or quantity.
- `variants_milik1962_firsthand`: hand-checked differences between Milik's own text in DJD III (1962, pp. 284–299) and Puech's. Each difference is marked "subst." (a different word, sense or figure), "orth." (spelling only) or "restor." (only in a lacuna or restoration).
- `readings_wolters1994_firsthand`: the few readings Wolters gives in his 1994 article, from his own examination of the metal, with page (F2.10).
- `variants_milik_secondhand`, `variants_wolters_secondhand`: readings that differ from Puech, as reported by Lefkovits `[Lef. p.]` (Hebrew script) or Puech `[Puech p. n.]` (transliteration). The two reporters sometimes disagree about what Milik or Wolters read.
- `translation_puech2015_en`: Puech's own English translation, from *The Copper Scroll Revisited* (2015, pp. 121–144). It already includes his corrigenda to the 2006 edition. Line numbers glued to figures in the PDF were separated by script and checked against his numerals.
- `translation_en`: an English rendering written for this project. It follows Puech's reading and his French interpretation, and is not Puech's English translation, which contains errors (see the findings log).
- `landmark_terms`, `direction_distance_depth`, `treasure`: structured from Puech's text. In the treasure column, "ככ" is kept as written. Puech and Lefkovits read it as k(esef) k(arsh), 1 karsh = 10 shekels; Milik and Allegro read "talents".
- `numerals_puech`: the value of each numeral group in Puech's reading.
- `greek_letters`: Puech's reading, and Lefkovits's where it differs.
- `damage_uncertainty_notes`: lines with lacunae, "(?)", engraver's corrections, and insertions or editorial additions, plus notes on letters above or below the line.
- `division_notes`: how other editors divide or number the entry, with source pages.
- `hebrew_lefkovits`, `translation_lefkovits`: Lefkovits's text and translation, read from the scanned images.
- `hebrew_milik1962`: Milik's Hebrew text from DJD III, line by line, as printed. It keeps his item numbers `(n)` and his brackets. ׄ (a dot above) marks a probable letter and ֯ (a circle above) a possible letter; `^…^` marks letters written above the line and `_…_` letters written below it. A line shared by two entries is given in full in both.
- `translation_milik1962_fr`: Milik's French translation from DJD III (pp. 285–298), by his item number, with page.
- `readings_milik1960_firsthand`: Milik's readings (Latin transliteration, no diacritics) as he states them in his 1960 commentary, pp. 143–155, with page.
- `translation_milik1960`: Milik's own English translation (ADAJ 1960, pp. 139–142), with his italics (*…*) marking uncertain renderings. His Hebrew readings are not given there.
- `pages_puech`, `pages_lefkovits`: printed pages of the text and commentary.
- `n_*`: counts used for the clarity ranking. `n_milik1962_differences` and `n_milik1962_substantive` count the DJD III differences.

## Method in brief

- **Puech:** the Hebrew was decoded from the PDF text layer, then all 181 lines were checked visually and all 33 numeral groups checked against his own totals (p. 173).
- **Lefkovits:** his Hebrew OCR is unusable, so every Hebrew word, including every reading he quotes from other scholars, was read from page images in eight parallel passes. The automatic Puech–Lefkovits comparison was then reviewed line by line.
- **Puech's commentary:** pp. 179–206 were extracted phrase by phrase: variant readings, his verdict on each, his notes on letter shapes and damage, and place claims (kept for Phase 3).
