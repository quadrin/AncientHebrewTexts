# Copper Scroll (3Q15): hiding places and Greek letters

Identify the places and specific locations described in the Copper Scroll using editions, archaeological reports, maps, surveys and photographs. Compare named sites and individual features, then test the scroll's directions, distances and depths against candidate locations. Record the source, assumptions, confidence and positional uncertainty for each proposal.

Research workflow: [`AGENTS.md`](AGENTS.md).

This folder contains the geographical research workstream. The repository's `CLAUDE.md` also describes the DSS letter-recogniser workstream.

## Phases

1. **Master table of all entries** (done, session 1; see `phase1_summary.md`)
2. **Landmark lexicon:** Bible, Mishnah, Josephus, Eusebius (done, session 2; see `phase2_summary.md`)
3. **Site candidates:** scored against written criteria and mapped at site level (done, session 2; see `phase3_summary.md`)
4. **Greek letters:** occurrences and tests of the hypotheses (done, session 2; see `phase4_summary.md`)
5. **Archaeology check** of the Phase 3 places, published reports only (done, session 2; see `phase5_summary.md`)

## Current site assessment

The [2026-09-28 site identification review](site_identification_review.md) updates Phase 5. It returns Siloam to medium overall confidence, records the full Szanton 2023 source, and distinguishes site compatibility from identification of a particular feature. The revised Phase 5 summary and index contain the current verdicts; the Phase 3 files retain their original assessment.

The [feature investigation](feature_investigation.md) adds five feature comparisons, a source-dependency audit, separate reading/site/feature judgments, and prepared specialist and non-invasive field-observation packets. The [constraint register](tables/feature_constraints.csv) records the tests that could distinguish or weaken each proposal. No exact feature or deposit has been identified.

The [Qumran reference review](qumran_reference_review.md) locates Ilan–Amit’s aqueduct chapter and Hebrew figure index, records the registered-access barrier, and compares entries 20–24. The atlas now includes nine evidence reviews. The [Ilan–Amit plan review](ilan_amit_1989_plan_review.md) now examines the recovered Hebrew plan. The [research log](registration/qumran_online_followup.json) tracks subsequent source access; the [Humbert–Chambon review](registration/humbert_english_extracted.md) separates inlet phases and reconstructed channels. Specific feature matches and geographic registration remain open research questions.

The [plate check](plate_check.md) (29 September 2026) tests 30 disputed lines against Puech's plates:

- Siloam (49) leans to Puech's cursive waw.
- Doq (31) leans to *hmšṭḥ*.
- IX 7 leans to ים.
- Milik's Bethesda reading needs an emendation.

No site confidence changes. The recovered *ʿAtiqot* 41 names V/48 as V/49's neighbour for entry 17 ([review](entry17_cave_pair_review.md)).

The [entry 40 review](entry40_bethhoron_review.md) adds Upper Beth-Horon as a possible, low-confidence place. It also records that Milik himself preferred the Horite tombs near Beit Guvrin in 1960, and re-checks the Phase 3 name tests against Elitzur's corpus.

The [source leads of 29 September 2026](source_leads_2026-09-29.md) locate the reports missing in Phase 5 (Q32). They also record three uploads: Stacey 2007 on the Qumran aqueducts (read in full) and Zertal's *Manasseh Hill Country Survey* Vols. 2–4 (Ibziq read in Vol. 2). Stacey's phasing is recorded as a constraint for entry 21; its confidence does not change. The [Stacey 2007 review](qumran_stacey2007_review.md) gives his construction sequence in detail, with a check of his citations of the 2002 book.

The [entry 59 review](entry59_bezek_review.md) reads Zertal's survey and *HA* 40. Neither Kh. Ibziq site has a reported conduit. On Zertal's survey alone, Kh. Ibziq was first lowered from medium to low. A 1971 excavation (*HA* 40 p. 22) then showed a kokhim tomb of the 1st–2nd centuries CE there, so Kh. Ibziq stays medium. Kh. Salhab (Zertal's biblical Bezeq) is added to the atlas as a low alternative. The Phase 5 index and summary carry the result. [sources.md](sources.md#sources-checked-2026-09-29-second-batch) records where the remaining reports can be found.

The [source extractions of 29 September 2026](source_extractions_2026-09-29.md) (second run) read Magen's NEAEHL entry on Gerizim, Garbrecht & Peleg 1994 on the desert fortresses, Zissu 2023, *HA* 40 on Ibziq, and Jeremias and DJD III for entry 40. The Hyrcania chapter (Patrich 2002) and Ilan & Amit 2002 p. 385 were read only in snippets or as word searches. Gerizim's steps and cistern are Hellenistic and stood as ruins after about 110 BCE (Q47 answered). No site confidence changes; the extraction files are in `registration/`. A third run of the same prompts is kept in `registration/extractions_run3/` and compared there: it adds a Hasmonean garrison on Gerizim into the 70s BCE and the dates of Hyrcania's two aqueducts, with no confidence changes.

The [deeper analysis of 30 September 2026](deeper_analysis_2026-09-30.md) tests the order of the entries from the text alone, with code in [`deep_analysis/`](deep_analysis/README.md). From entry 20 on, entries that name the same place stand together; in entries 1–19 they do not. In 1–19, "north" occurs only in the Koḥlit and ha-Melaḥ entries, and every Koḥlit entry in the scroll says "north". The phrase כתבן אצלם always follows "vessels of offering", which favours Puech's and Lefkovits's division at Q5. The report takes these results as support for H8 (entries 1–19 come from a separate list) and for ha-Melaḥ as a named place in the Jericho district, not the Temple Esplanade. The Greek-letter gaps mark no change. The analysis identifies no site and changes no site confidence.

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
| `web/index.html` (with `web/map1-overview.webp`, `web/map3-jerusalem.webp`) | yes | The public web page: the text of the scroll with a translation and clickable readings, scored place identifications, the archaeology check, the Greek letters, maps 1 and 3. For GitHub Pages at `https://quadrin.github.io/AncientHebrewTexts/copper_scroll/web/` once the folder is on `main` |
| `web/scroll-reader.js` | yes | The scroll reader on the web page: the column strip, the facing Hebrew and English lines, and the readings panel |
| `web/scroll-text.js` | yes | The Hebrew text of 3Q15: Abegg's transcription and morphology from the ETCBC `dss` dataset 2.0.1, **CC BY-NC 4.0**. Built by `tools/build_scroll_text.py`, which lists the changes made for display |
| `web/scroll-notes.js` | yes | The translation, glosses, reading notes and entry data, built by `tools/build_scroll_notes.py` from `text/` and the tables |
| `text/translation_en.json` | yes | An English translation, one line per scroll line, written for this project from the Abegg text. `{{phrase\|note-id}}` links a phrase to a note |
| `text/glossary_en.json` | yes | A short English meaning for each of the 247 lemmas in the Abegg text |
| `text/readings.json` | yes | Notes on words the editions read or explain differently: each edition's reading and meaning, with pages, from the research files in this folder |
| `tools/build_scroll_text.py`, `tools/build_scroll_notes.py` | yes | Build the two data files above. The first needs a local copy of ETCBC `dss` (instructions in the file) |
| `plate_check.md`, `tables/plate_check.csv` | yes | Disputed readings checked against Puech 2006 vol. II copy photographs and radiographs, with a blind two-reader protocol (`registration/plate_check/`) |
| `tools/plate_extract.py`, `tools/plate_check_items.py` | yes | Extract the column plates and cut the blind line crops (output stays outside git) |
| `tools/photo_trace.py`, `registration/photo_tracing_strip13.json` | yes | The atlas photograph of strip 13: the Grooves and Relief images, and the letter-by-letter tracing of VII 7–11, with letters identified on Puech's radiograph pl. CCCXLVI (plate images stay outside git). See [the photographic reader note](atlas/research/photographic_reader.md) |
| `entry40_bethhoron_review.md`, `registration/entry40_elitzur_extracted.md` | yes | Entry 40 (IX 7–9): Beth-Horon, the Horites and Naṭuf; Elitzur's name test re-checked |
| `source_leads_2026-09-29.md` | yes | Access leads for the Phase 5 gaps (Hyrcania, Gerizim, Ibziq, Herodium, Mar Saba, Ilan–Amit 2002); notes on Stacey 2007 and Zertal's Manasseh survey Vols. 2–4 |
| `entry59_bezek_review.md` | yes | Entry 59 (XII 8–9): Kh. Ibziq and Kh. Salhab in Zertal's Manasseh survey, Vols. 2–4 |
| `qumran_stacey2007_review.md` | yes | Stacey 2007 on the phases of the Qumran aqueduct; effect on entries 20–22 |
| `source_extractions_2026-09-29.md`, `registration/*_extracted.md` | yes | The second run of 29 September 2026: Gerizim (Magen), Hyrcania (Patrich 2002, snippets), Garbrecht & Peleg 1994, Zissu 2023, Salhab/Ibziq, Ilan & Amit p. 385, entry 40 (Jeremias, DJD III) and the outreach status |
| `registration/extractions_run3/` | yes | The third run of the same eight prompts (29 September 2026), kept beside the second run's files; compared in `source_extractions_2026-09-29.md` (F11.1–F11.9). Email addresses removed from the outreach file |
| `deeper_analysis_2026-09-30.md`, `deep_analysis/` | yes | The deeper analysis of 30 September 2026 and its code and outputs: tests of the entry order (name runs, directions, dig depths, vocabulary blocks, change points, Greek-letter gaps, walking routes, a sub-district sequence model). The two earlier reports of that series are not in the repository. `entries_full.json` and `features.json` are made again by the scripts and are not in git; `route_jer.py` needs a terrain grid (`dem.npz`) that is not in the repository. See [its README](deep_analysis/README.md) |
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
| `tables/phase5_assessments.csv`, `tables/phase5_reports.csv` | yes | The 37 Phase 5 assessments with reasons, and the 261 report records with pages, URLs and short quotes (20 words or fewer) |
| `phase3_candidates.csv` | **no** | All 292 Phase 3 candidates with the full scoring, reasons with pages, and short quotes |
| `phase3_entries.csv` | **no** | Per entry: the text's requirements, reading notes, best-supported place, why not the others, and the text's own relative description in each edition (edition quotations; spatial models record their assumptions separately) |
| `phase3_map1_overview.png`, `phase3_map2_jericho_qumran.png`, `phase3_map3_jerusalem.png` | **no** | The three Phase 3 maps, at site level. Map 2 is built on PEF Sheet XVIII (CC BY-NC-SA 3.0) |

The **In git?** column records the delivery status reported by the original research sessions. It is not a blanket publication rule. Some omitted tables mix ancient Hebrew with modern edited readings, translations or commentary; assess the particular material being reproduced. Use the existing editions for research and cite them when preparing original project text. There is no prerequisite to find an openly licensed replacement transcription. See [Text and publication](AGENTS.md#text-and-publication).

The PEF base map's CC BY-NC-SA licence permits public sharing subject to its attribution, noncommercial and share-alike terms; public hosting alone is not a reason to exclude it. See the [licence terms](https://creativecommons.org/licenses/by-nc-sa/3.0/).

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
