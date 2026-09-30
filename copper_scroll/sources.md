# Copper Scroll (3Q15): source inventory

Checked 2026-09-27 against branch `main` (commit 637a7a9, "Add files via upload").

## Summary

| Source you listed | In the repo? | Readable? | How it is used |
|---|---|---|---|
| Puech 2006, *Le Rouleau de cuivre de la grotte 3 de Qumrân (3Q15)* | Yes, 11 PDF parts, 706 pages | Yes. Born-digital text layer. The Hebrew is in a legacy font and needs decoding (see below). | Primary reading |
| Lefkovits 2000, *The Copper Scroll – 3Q15: A Reevaluation* | Yes, 11 PDF parts, 624 pages | Partly. Scanned library copy with OCR. The English OCR is usable; **the Hebrew OCR is useless**, so every Hebrew word was read from the page images. | Variant readings; secondhand Milik, Allegro, Luria and Wolters readings |
| Milik, DJD III (1962) | Not in the repo. **Uploaded in session 2** as a zip (Internet Archive scan). | Yes, as images. The French OCR can be used; the Hebrew OCR cannot, so Hebrew is read from the page images. The plates are **not** in the scan. | **Firsthand** Milik 1962: Hebrew text, French translation, reading notes, word list (section C) and site list (section D). The secondhand Milik columns stay in the table as a cross-check. |
| Milik 1960, ADAJ 4–5 (uploaded in session 1) | Not in the repo (upload only) | Yes, an image scan with no text layer; read visually | **Firsthand** Milik: his complete English translation with his 1–64 numbering, and his commentary on the place names |
| Wolters (you listed his readings as a variant column) | **No.** Wolters 1996, *The Copper Scroll: Overview, Text and Translation*, is not in the repo. | — | Taken **secondhand** from Lefkovits (who cites "Wolters 1996" throughout) and Puech. |
| TIR Iudaea-Palaestina, North sheet | **Only crops**, not the sheet | Yes (see below) | Not used in Phase 1 |
| Wolters 1994, "History and the Copper Scroll" (uploaded in session 2) | Not in the repo (upload only) | Yes. A scan with an OCR layer; the OCR has noise, and transliterations were checked on the page images | **Firsthand** Wolters: five of his own readings, a history of interpretation, and the 1988 juglet argument |
| Brooke and Davies (eds.), *Copper Scroll Studies* (preview, then the **full volume**, both uploaded in session 2) | Not in the repo (upload only) | Yes. The full volume (361 PDF pages) has an OCR text layer; the Hebrew in the OCR is often garbled. **Printed page = PDF page − 17** | All 22 chapters (see below) |
| Puech 2015, *The Copper Scroll Revisited* (STDJ 112; English translation by D. E. Orton) (uploaded in session 2) | Not in the repo (upload only) | Yes. Born digital, **Unicode Hebrew**. **Printed page = PDF page − 11** | An independent check of the decoded Puech 2006 text; Puech's own English translation; his **corrigenda to the 2006 edition** (pp. 151–152) |
| Høgenhaven 2020, *The Cave 3 Copper Scroll: A Symbolic Journey* (STDJ 132) (uploaded in session 2) | Not in the repo (upload only) | Yes. Born digital, Unicode Hebrew. **Printed page = PDF page − 11** | Structure, symbolic reading, Greek letters (pp. 149–153), language, numerals; a translation (pp. 239–244) |
| DJD III, **plates volume** (uploaded in session 2) | Not in the repo (upload only) | Yes, but heavily compressed (88 PDF pages) | 3Q15 pl. XLIII–LXXI: the two rolls, the sawing, and **a drawing and a photograph of every column** |
| "Copper_Scroll_Geographical_Resources" archive, 12 parts (uploaded in session 2) | Not in the repo (upload only) | **Complete.** All 12 parts rejoined; the SHA-256 of the whole archive matches the README, and all 15 files match `manifest.json` | See the next section |
| Elitzur 2004, *Ancient Place Names in the Holy Land: Preservation and History* (uploaded in session 2) | Not in the repo (upload only) | A photocopy scan (237 two-page spreads) with **no text layer**. I made a local OCR text with Tesseract (English only; the Hebrew and Arabic in it are garbled) | Method for judging whether a modern name preserves an ancient one; a few direct remarks (Dok, Kohlith, Beth ha-Kerem) |
| *ʿAtiqot* 41 (2002), Hebrew issue: *Surveys and Excavations of Caves in the Northern Judean Desert (CNJD) — 1993*, 6 parts (uploaded in session 2) | Not in the repo (upload only) | **Complete.** The six parts rejoined; SHA-256 matches; 25 PDF files, 295 pages, born digital, Hebrew in Unicode | The IAA cave survey from Wadi el-Makkuk to Naḥal Kidron, with maps. Main use: Phase 5 |
| DJD VII, Baillet, *Qumrân grotte 4. III (4Q482–4Q520)* (uploaded in session 2) | Not in the repo (upload only) | Yes. The complete volume (444 pages) with plates | **Almost nothing on 3Q15**: one spelling parallel (p. 222) |

## Puech 2006 (primary reading)

- Files: `Le Rouleau de Cuivre de la Grotte 3 de Qumrân (3q15) (2 - Daniel Brizemeure, Noël Lacoudre, Emile Puech-1.pdf` … `-11.pdf`. These are the two volumes of STDJ 55 (Brill / EBAF 2006) split into 70-page parts; part 11 has 6 pages. The PDF says it is a multi-volume eBook.
- **Page mapping in the Puech volume I section: printed page = global PDF page − 26.** "Global" counts pages through parts 1–11 in order.
- Puech's revised edition is "Livre second", vol. I pp. 169–223:
  - Introduction: pp. 171–178
  - Text, translation and commentary, by column: pp. 179–206
  - **Text with French and English translation: pp. 207–216.** This is the text used for the master table.
  - Index: pp. 217–220 (Hebrew concordance p. 217ff; numerals and Greek letters p. 219)
  - Bibliography: p. 223
- Plates (photographs, radiographs, facsimile, galvanoplasty): vol. II, pl. CCCXXXIII–CCCLXXXIII.
- Encoding: the Hebrew is set in "SuperHebrew" (plus "HebraicaII" for some final forms), stored in visual left-to-right order. Numeral signs are partly font glyphs (unit stroke "|" in Symbol; the 20-sign as a "3" glyph) and partly **vector drawings** (the 10-sign, the 100-sign). They do not survive text extraction. `tools/puech_heb.py` decodes the text layer. **Every one of the 181 lines was then checked by eye** against page renders, and all numerals were set by hand from the images and from Puech's own totals (p. 173 nn. 27–34). The line table (`puech_lines.csv`) contains Puech's edited text and was delivered separately in the original session (see "Where the table lives" in `phase1_summary.md`). This records its delivery status; follow [Text and publication](AGENTS.md#text-and-publication) when preparing new outputs.
- **Internal inconsistencies in Puech's own book:** his English translation (pp. 208–216) disagrees with his Hebrew and French in several places. See the findings log. The master table follows his Hebrew and French.

## Lefkovits 2000

- Files: `The Copper Scroll - 3Q15_ A Reevaluation _ A New Reading, - Lefkovits, Judah-1.pdf` … `-11.pdf` (STDJ 25). The copy is from the Claremont School of Theology library; there are library stamps on the front pages.
- **Printed page = global PDF page − 24.** Parts 1–10 have 60 pages each, part 11 has 24.
- Items 1–60: pp. 29–442. Discussion: p. 443ff. Appendix A (ככ vs ככרין): p. 471. Appendix B (numerals): p. 489. Appendix C (Greek letters): pp. 498–504. Appendix D: p. 505.
- Lefkovits p. 17 n. 69: "Milik divides the text into 64 items, Allegro into 61, Lurie into 60, and Wise into 65 … This author divides the Copper Scroll into 60 items, three of which (#9, #12, #56) can be further subdivided into two or three sub-items."
- His commentary quotes the Hebrew readings and translations of Allegro, Milik, Lurie (Luria), Pixner, Wolters (1996), García Martínez, Vermes, Wise, Beyer and Wacholder, phrase by phrase. It is the richest source in the repo for the Milik and Wolters variants.

## Milik 1960 (uploaded in session 1)

- J. T. Milik, "The Copper Document from Cave III of Qumran: Translation and Commentary", *Annual of the Department of Antiquities of Jordan* 4–5 (1960), pp. 137–155. File: `ADAJ_1960_4_5-137-155.pdf` (19 pages, a scan from the DoA Publication Archive, no text layer). **PDF page n = printed page 136 + n.**
- Contents:
  - Introduction, pp. 137–138. Milik says the DJD III edition "is now ready and it will be in press when this article appears". He gives the translation "of the entire document" by permission of the Clarendon Press.
  - Translation, items 1–64, pp. 139–142. Italics mark uncertain translation; `< >` marks an omission; `°°` marks letters not deciphered.
  - Commentary on the place names, by column and line, pp. 143–155.
- What it provides: **Milik's own item numbering, and his translation of every item**, which settles open question Q4. It does *not* give his Hebrew transcription. His readings appear in the commentary only in Latin transliteration, without diacritics (p. 138 N.B.).
- Caveat: this is Milik in 1960. DJD III (1962) is now available (next section). Its numbering is the same, item for item, but some wording differs; the differences are listed in the findings log.

## Milik, DJD III (1962) (uploaded in session 2)

- M. Baillet, J. T. Milik, R. de Vaux, *Les 'Petites Grottes' de Qumrân* (DJD III; Oxford 1962). Milik's chapter: "Le rouleau de cuivre provenant de la grotte 3Q (3Q15)", pp. 199–302. The file is an Internet Archive scan (344 PDF pages) with an OCR layer. **PDF page = printed page + 20.**
- Sections used:

  | Section | Printed pages | Use |
  |---|---|---|
  | Note liminaire, with the full French translation of items 1–64 | 211–215 | Milik's 1962 translation and numbering |
  | A. Script and numerals | 215 ff. | Numeral signs (Phase 4 context) |
  | C. *Mots et objets* (word list, 122 numbered entries) | 236–259 | Phase 2 meanings |
  | D. *Sites et monuments* (site list) | 259–274 | Phase 2 and Phase 3 identifications |
  | F. *Transcription et traduction annotées* | 284–299 | Firsthand Hebrew text, line by line |
  | Addenda | 299–302 | Later corrections |

- **Missing from the scan:** the plates (DJD III pl. XLIII–LXXI, BK: plate range from memory, check). Milik's drawings can therefore not be checked here.
- Milik marks a doubtful letter with a dot above (probable) or a small circle above (possible). The transcripts use U+05C4 and U+05AF for these.
- The item numbering is the same as in Milik 1960 (1–64), item for item. The wording of some translations changed between 1960 and 1962 (see the findings log, F2.x).

## Uploaded in session 2 (after Phase 2)

### Wolters 1994

- A. Wolters, "History and the Copper Scroll", in *Methods of Investigation of the Dead Sea Scrolls and the Khirbet Qumran Site* (Annals of the New York Academy of Sciences 722; 1994), pp. 285–298. It includes the discussion after the paper, pp. 295–298.
- It gives some of Wolters's **own readings**, made from the copper segments in Amman in June 1991 (p. 292):
  - III 9 *lbwšy*
  - VIII 3 *wspry wʾlt ks[p]*
  - XI 9 *thwrty*
  - XII 1–2 *kwzyn* (p. 294)

  These are now in the master table as `readings_wolters1994_firsthand`. His full edition, with "more than seventy places" where he differs from Milik, is not in the repo (Q2).
- It has nothing on the Greek letters.

### *Copper Scroll Studies* (first upload: a preview)

- **Superseded:** the full volume was uploaded later (see *Copper Scroll Studies* (full volume) below). The table below records only what the preview lacked.

- G. J. Brooke and P. R. Davies (eds.), *Copper Scroll Studies* (JSPSup 40; Sheffield 2002; T&T Clark paperback 2004). The file is a publisher's preview of 37 PDF pages: pp. i–xvi, the Introduction (pp. 1–9), and pp. 12–20 of chapter 1 (the conservation report).
- **Not in the preview:**

  | Ch. | Author and title | Pages | Needed for |
  |---|---|---|---|
  | 5 | Puech, "Some Results of a New Examination" | 58–91 | Readings |
  | 6 | Eshel, "Aqueducts in the Copper Scroll" (maps of the Cypros and Doq aqueducts) | 92–107 | Phase 3 |
  | 7 | Elwolde, linguistic affiliation | 108–121 | Phase 2 |
  | 12 | Schiffman, architectural vocabulary | 180–197 | Phase 2 |
  | 14 | Fidler, "Inclusio and Symbolic Geography" (cited by Puech p. 179 n. 76) | 210–225 | Phase 3 |
  | 20 | Lika Tov, palaeography | 288–290 | Phase 4 |
  | 22 | Wolters, "Palaeography and Literary Structure as Guides to Reading the Copper Scroll" | 311–333 | **Probably the main source for Phase 4** (BK: Wolters links the Greek letters to the structure of the list; check) |

### Puech 2015, *The Copper Scroll Revisited*

- É. Puech, *The Copper Scroll Revisited* (STDJ 112; Leiden: Brill 2015), English translation by D. E. Orton. Foreword dated 22 March 2015. It is "the English translation of my updated edition" (the 2006 French edition), with typographical errors corrected and recent studies added (p. vii).
- Its Hebrew text is **Unicode**. I compared it with the Puech 2006 text decoded from the legacy font. **172 of 181 lines agree letter for letter.** Of the other 9 lines, 7 differ only because of PDF layout (right-to-left order, numeral signs). Two are real changes:
  - I 12: Puech 2015 restores ה in the lacuna.
  - VIII 3: Puech 2015 drops the alternative ר (it reads תבקע).
- This is an independent check of the decoding tool.
- **Corrigenda to the French edition 2006** (pp. 151–152):
  - One correction changes the Hebrew: VII 6 [ואר]בע, where the 2006 print omits the opening bracket. It is now applied in the table.
  - Others correct the 2006 English translation at entries 15, 18, 27, 32 and 37, and the entry numbers on 2006 p. 211. These are the errors listed in Q10.
- Puech's 2015 English translation is now a column of the master table (`translation_puech2015_en`).

### *Copper Scroll Studies* (full volume)

- The chapter list is given above; all chapters are present. The chapters most useful for later phases:
  - Wolters ch. 22 (pp. 311–333): palaeography, literary structure and **the Greek letters** (Phase 4).
  - Lika Tov ch. 20 (pp. 288–290): palaeography (Phase 4).
  - Eshel ch. 6 (pp. 92–107): aqueducts, with maps (Phase 3).
  - Fidler ch. 14 (pp. 210–225): Achor and Gerizim as an inclusio (Phase 3).
  - Bar-Ilan ch. 13 (pp. 198–209): order of hiding (Phase 3).
- The language chapters (7–12) and Puech ch. 5 are being read for a Phase 2 addendum.

### Høgenhaven 2020, *The Cave 3 Copper Scroll: A Symbolic Journey*

- J. Høgenhaven, *The Cave 3 Copper Scroll: A Symbolic Journey* (STDJ 132; Leiden: Brill 2020).
- Chapter 2 reads the list as a route through four "main sections" (Achor–Koḥlit; Secacah; the Kidron and Jerusalem; Gerizim–Beth-Shan–Bezek, then back to Koḥlit).
- Chapter 4 covers the object: palaeography, **the Greek letters (§4, pp. 149–153)**, language, numerals, abbreviations, and the arguments for and against the treasure being real.
- Chapter 5 covers the traditional contexts (Massekhet Kelim, the Lindian Chronicle, and others).
- Main use: Phases 3 and 4. Its ch. 3–4 sections on landscape, installations and language are being read for the Phase 2 addendum.

### DJD III, plates volume

- The Internet Archive scan "Texte. Planches" (88 PDF pages): pl. I–XLII show the small caves and their manuscripts; **pl. XLIII–LXXI are 3Q15**:
  - XLIII: the two rolls before opening;
  - XLIV: the sawing;
  - XLV–XLVII: montages of the segments;
  - then, for each column, a drawing (facsimile) and a photograph of the segments.
- The images are strongly compressed. The drawings can be read at about 150 dpi; the photographs are poor.
- The drawings are an editor's copy, not the metal. They can show what Milik's team saw, which is the evidence Lefkovits calls "Milik's drawing". They cannot settle a reading by themselves.

### DJD VII (Baillet 1982)

- An Internet Archive scan with an OCR text layer (444 pages, plates included).
- A search of the whole OCR layer finds **one** reference to 3Q15: in the commentary on 4Q511 (*Cantiques du Sage*, p. 222), Baillet cites 3Q15 V 1 for the spelling רוש for ראש.
- The volume has no treatment of the Copper Scroll, its sites or its Greek letters. (Question to you: was a different volume meant? For example, DJD II (Murabbaʿat), whose Mur 42–43 Milik uses for Kaphar Baricha and ha-Baruk (DJD III p. 269), or a copy of DJD III that includes the plates?) *Later in session 2 you uploaded the DJD III plates volume (below).*

### "Copper_Scroll_Geographical_Resources" archive (12 parts)

- Rejoined from your 12 uploads. The checksums of the whole archive and of each file match.
- Contents, as checked:

  | File | What it is | Checked | Licence (as stated in the archive's README) |
  |---|---|---|---|
  | `PEF_Sheet_XVIII_full_resolution.jpg` / `.jp2` | Survey of Western Palestine, Sheet XVIII (surveyed under Conder and Kitchener; the sheet is dated May 1878), 11,108 × 9,050 px, from the David Rumsey Map Collection | **Small labels are legible.** Examples: Wady Nueiameh, Kh. el Mefjir, Jebel Kuruntul and Tahunet el Hawa, Tell es Sultan, Tell el Kôs, Eriha, Wady el Kelt with its aqueducts, el Bukeia, Kh. Mird, Kh. Kumrân, Wady Kumran, ʿAin Feshkha, Râs Feshkhah | CC BY-NC-SA 3.0 (David Rumsey). **Not committed** |
  | `PEF_Judaea_Memoirs_Vol_III.pdf` + OCR | *SWP Memoirs* III, Judaea (1883), 510 PDF pages, sheets XVII–XXVI | Text layer on most pages | Public domain (1883) |
  | `PEF_Palmer_Name_Lists_1881.pdf` + OCR | E. H. Palmer, *Arabic and English Name Lists* (1881), 452 PDF pages, keyed to the PEF sheets | Text layer on most pages | Public domain (1881) |
  | `Jastrow_Dictionary_Vol_1.pdf`, `_Vol_2.pdf` | Jastrow, *Dictionary* (714 + 1,066 PDF pages) | Text layer on almost all pages | Public domain |
  | `eusebius_onomasticon_01/02/03*.htm` | Wolf's Onomasticon translation, introduction and notes | Byte-identical to the copies already used in Phase 2 | tertullian.org |
  | `Copper_Scroll_Studies_PUBLISHER_PREVIEW.pdf` | The same 37-page preview uploaded earlier | Duplicate | — |
  | `README.md`, `START_HERE.html`, `manifest.json` | The archive's own notes and access routes | Read | — |

- The archive's README lists sources that it could **not** download:
  - Elitzur, *Ancient Place Names in the Holy Land*;
  - the IAA *ʿAtiqot* 41 cave-survey reports (HTTP 403);
  - the Hebrew University database of churches and monasteries;
  - the Comprehensive Aramaic Lexicon.

  These are still missing. Eshel's chapter, which the README also lists as missing, is in the full *Copper Scroll Studies* uploaded earlier.

  **Correction 2026-09-29:** both were in fact uploaded at the end of session 2 and are described below (Elitzur: F2.21–F2.22; *ʿAtiqot* 41: F2.23); this list reflects the archive's own README. The 2026-09-28 reviews that reported *ʿAtiqot* 41 as inaccessible (HTTP 403) overlooked that upload. The user re-supplied both on 2026-09-29. *ʿAtiqot* 41 has now been read in detail for entry 17 ([extraction](registration/atiqot41_region_v_extracted.md)).
- Main use: Phase 3. Sheet XVIII covers the Jericho plain, Wadi Qelt, the Buqeia, Hyrcania (Kh. Mird) and the NW Dead Sea shore to Râs Feshkhah. This is the area missing from the TIR crops (Q3). It is a 19th-century survey, not TIR: names are the Arabic names of 1870s, and ancient identifications must come from other sources.

### Elitzur 2004 (uploaded in session 2)

- Y. Elitzur, *Ancient Place Names in the Holy Land: Preservation and History* (Jerusalem: Magnes; Winona Lake: Eisenbrauns 2004). The scan is a photocopy without a text layer. **I made a local OCR text** (Tesseract, English); page numbers in it come from the running heads.
- **Method** (pp. 8–14). He warns that "scholars are sometimes able to justify almost any historical theory on the basis of place names" (p. 9). An identification is **"almost positive"** only if (p. 12–13):
  - (i) the terrain and distances in the historical sources point to a well-defined location; and
  - (ii) an Arabic name matches the historical name in all or almost all letters, at or reasonably near that location.

  Remarks (p. 13): an inexact location can be accepted if the name is rare; a badly preserved name can be accepted if the sources fix the place. Pottery supports but does not prove. Inscriptions are the best proof. Names can "wander" a short distance.
- **Direct remarks on Copper Scroll places:**
  - Dok (1 Macc 16:15, Δωκ) is "known to the Arabs as dūk or dyūk ('chickens')", a popular etymology, and "the two forms have remained in living use" (p. 139 n. 2, the note to entry 27, ʿId el-Miyye = Adullam; *corrected 2026-09-29* from "entry 28, Hadid"; index "Dok … 139, 288, 351, 358").
  - "Kohlith" is cited among names with the suffix -it, a type that became frequent in the Second Temple period (pp. 230, 334). This is a remark on the name's form, not on its location.
  - Beth ha-Kerem is identified following Aharoni, with Genesis Apocryphon 22:14 and "the Copper Scroll 10,5" added to the sources (p. 185 n. 2, in entry 46, Bethlehem; checked 2026-09-29).
  - The steep cliffs of the Quruntul range "as they descend to Wadi Nweiʿmeh" (in the discussion of Benjamin's border).
- Entry 17, Ragaba / רגב, is the village of Rageb in Transjordan. It has nothing to do with the scroll's word הרגב.
- **Corpus list (pp. 15–18), checked 2026-09-29.** His 177 "positive or almost positive" identifications include Beth-Horon = [bēt ʿūr] (no. 51), Bezek = [bzīq] (no. 62) and Beth-shean = [bēsān] (no. 63), all on p. 16. The book's index does not cover this list. Siloam, Dok, Achor, Secacah and Kozeba are not in the corpus. See [entry40_bethhoron_review.md](entry40_bethhoron_review.md#elitzur-2004-the-name-test-re-checked).

### *ʿAtiqot* 41 (2002), Hebrew issue (uploaded in session 2)

- *ʿAtiqot* 41, part 1 (Hebrew): the reports of the 1993 IAA cave survey (CNJD), Regions I–XV, from Wadi el-Makkuk and Jebel Abu Saraj, along Jebel Quruntul, to the fault escarpment above Ḥorbat Qumran, south of Qumran, and from Naḥal Kidron to Naḥal Deragot. It includes an index and a map of the 1993 survey. The English issue (part 2) was not uploaded.
- A search of all 25 files finds **no discussion of the Copper Scroll**. The only hit is a bibliography entry, Luria 1964, in the Preface.
- One cave has a name that echoes the scroll: **Cave IV/11, "Cave of the Pillar"** (N. Feig), in the Jebel Abu Saraj cliff. It is named for a 2.5 m pillar (natural below, rock-cut above) at the SW end of its hall. The report does not link it to the scroll's "Cave of the Column" (VI 1). (Inference, low weight: the shared name is a modern descriptive label and is not evidence of identity. Logged only for the Phase 5 check.)

## Phase 2 reference corpora (downloaded in session 2; local only, not committed)

| Corpus | Source | Licence / note | Use |
|---|---|---|---|
| Hebrew Bible (WLC) with Strong's lemmas | `openscriptures/morphhb` (OSIS XML) | CC BY 4.0 (morphology); WLC text public domain | Biblical attestations |
| Mishnah (Hebrew) | Sefaria export (`storage.googleapis.com/sefaria-export`), "merged" version | Per-text licence on Sefaria; mostly public domain or CC | Mishnaic attestations |
| Josephus, AJ, BJ, Vita, CAp (Greek and English) | PerseusDL `canonical-greekLit` (tlg0526) | CC BY-SA | Place names in Josephus. **The English is Whiston's numbering and the Greek is Niese's**, so section numbers can differ |
| Eusebius, *Onomasticon* | Wolf 1971 English translation (tertullian.org); Klostermann, GCS 11.1 (1904), Greek and Jerome's Latin (Internet Archive, OCR text) | Wolf: free online; Klostermann: public domain | Place names; Klostermann page.line references |
| BDB (Augmented Strong) and Jastrow | Sefaria words API | Sefaria terms | Dictionary meanings |

## Phase 3 place data and map layers (session 2; local only, not committed except the curated table)

| Source | Use | Licence and notes |
|---|---|---|
| Pleiades CSV dumps (places, names, locations) | Ancient-place coordinates; a 573-place regional extract | CC BY. Errors found: see F3.6 |
| Wikidata, regional extract by SPARQL box query (18,417 items) | Coordinates of modern-named sites and monuments | CC0. Some items are wrong or merged: see F3.6 |
| OpenStreetMap via Nominatim | The outline of the Old City walls (relation 5862586), for orientation on map 3; a check of some Jerusalem points | © OpenStreetMap contributors, ODbL. The Nominatim "Haram" polygon (relation 3875817) is only the inner Dome of the Rock platform and was not used. Overpass was not reachable |
| AWS Terrain Tiles (terrarium; Mapzen; SRTM and other sources) | Relief shading; the Dead Sea shoreline (SRTM, c. 2000, about −415 m) | Open data, with attribution |
| Natural Earth 10 m | The Jordan river line | Public domain |
| PEF Survey Sheet XVIII | The base of map 2; label positions for places not in the gazetteers (ʿAin Duk, Wady Nueiameh, Tell el-Kos, Wady Ekteif, Jofet el Asla, Kh. es-Sumrah) | CC BY-NC-SA 3.0 (David Rumsey Map Collection). Affine georeference with 4 control points, residuals 15–106 m (F3.7) |

The hand-curated result is `tables/phase3_places.csv`. Each of its 37 rows names its coordinate source.

## Phase 4 sources (session 2)

- **Editions.**
  - Puech 2006 (pp. 174–175, 180–187, 219) and Puech 2015 (pp. 12–13, 28–50; facsimiles pp. 120–126).
  - Lefkovits 2000 (Appendix C, pp. 498–504; item commentaries). The Greek was read from the page images, because the text layer garbles it.
  - Milik 1960 (pp. 139–144) and DJD III (pp. 216, 221, 284–288, 300; plates XLVIII–LIV from the plates volume).
  - Wolters 1994 has nothing on the Greek letters.
- **Studies.** *Copper Scroll Studies*, all chapters; the relevant ones are Puech, Lefkovits, Bar-Ilan, Fidler, Goranson, Muchowski, Thiering, Lika Tov, Wise and Wolters. Also Høgenhaven 2020, pp. 28, 38, 50–62, 147–165, 185, 235.
- **Josephus, Greek (Perseus, Niese; local, from Phase 2).** Used for the name base-rate test and for BJ 2.520, 5.474 and 6.387.
- **Reported only at second hand** (see Q31): Ullendorff 1961; Pixner 1983; Stegemann 1993/1998; Weitzman; Richey 2012; Beyer 1994; Lehmann 1964; Lurie 1964; Zissu 2001; Bedman 2000; McCarter. Feather is mentioned only in passing (Fidler CSS p. 210 n. 1).

## Phase 5 sources (session 2)

- **Local.**
  - *ʿAtiqot* 41 (1993 IAA cave survey, Hebrew): regions V, VII, IX (Jebel Quruntul), X–XIII (by Qumran), XIV (Kidron), and the preface.
  - Eshel, CSS ch. 6.
  - SWP *Memoirs* II and III.
  - The editions' archaeological notes: Milik DJD D; Puech 2015; Lefkovits; Høgenhaven.
- **Online, open access (URLs in `tables/phase5_reports.csv`).**
  - *Hadashot Arkheologiyot* (hadashot.iaa.org.il), volumes 132–137.
  - *ʿAtiqot* 113 (Szanton **2023**, full text accessed in the 2026-09-28 review) and *ʿAtiqot* 119 (Aharonovich et al. 2025, abstract).
  - The IAA publications portal for *ʿAtiqot* 41.
  - The Tel Aviv University Ramat Raḥel reports (2006–07; the INJ 17 hoard paper).
  - Avni & Greenhut 1996 (abstract).
  - Sala 2014 (author's copy).
  - Zias 2023 (*ANE Today*).
  - Warren and Wilson, *The Recovery of Jerusalem* (1871; Internet Archive).
- **Blocked or unavailable:** see Q32.

## Sources checked for the 2026-09-28 site review

- Nahshon Szanton, “Ritual Purification and Bathing: The Location and Function of Siloam Pool and Solomon’s Pool in Second Temple Period Jerusalem,” *ʿAtiqot* **113 (2023), 29–44**. [Full article](https://jamestabor.com/wp-content/uploads/2024/01/Szanton-Antiquot-2023-Siloam-and-Solomons-Pools.pdf). The hosting path's 2024 date is not the publication year. The IAA portal's "Recommended Citation" also gives 2024 (the article went online there in November 2024), but the printed header reads "ʿAtiqot 113, 2023"; this project cites 2023. See pp. 35–42 for the two-pool discussion. Primary research article, read in full; earlier Phase 5 records had only the abstract.
- Tel Aviv–Heidelberg Ramat Raḥel expedition, [2006–2007 preliminary results](https://www.tau.ac.il/~rmtrachl/joint_project_results.html), Area C1 (corresponding to the Phase 5 report citation, pp. 15–18). Primary excavation report; the relevant pool, reuse and burial sequence was checked directly.
- Judah K. Lefkovits, *The Copper Scroll: 3Q15: A Reevaluation: A New Reading, Translation, and Commentary* (2000), entry 49, pp. 352–354. Read directly in the repository scan for the translation and competing readings.
- The review used the public summaries and indices at commit `05a233b178d27112dcceebe97d5e5e25657ddd49`. It did not have the then-uncommitted `phase5_assessments.csv` or `phase5_reports.csv` (both committed later, as `tables/phase5_assessments.csv` and `tables/phase5_reports.csv`); their 254 source records were not independently re-audited.

## TIR (Tabula Imperii Romani, Iudaea–Palaestina, 1994)

`README.md` on `main` documents the search: no full North sheet was found in public digital form. What is in the repo:

| File | Size (px) | What it shows |
|---|---|---|
| `north_samaria_jerusalem.jpeg` | 3508 × 2544 | North sheet crop: Neapolis/Gerizim south to Jerusalem–Jericho. **Legible.** Shows "Achor Vallis" NW of Jericho (near Noorath / Wadi Makukh), Dok, Chozeba, Hierico, Beth ha-Kerem, Gerizim. **Stops short of Qumran, the Buqeia and the Dead Sea shore south of Jericho.** |
| `north_caesarea_samaria.jpeg` | 3508 × 2544 | North sheet crop: Caesarea and Samaria |
| `north_galilee_ptolemais.jpeg` | 2544 × 3508 | North sheet crop: Galilee and Ptolemais |
| `north_carmel_caesarea_patrich_annotated.jpeg` | 1887 × 2943 | TIR-based map with Patrich's boundary overlay (not an unaltered sheet) |
| `overview_jerusalem_caesarea.jpeg` | 723 × 648 | Overview map excerpt, low resolution |
| `overview_jerusalem_gaza.jpeg` | 760 × 1160 | Overview map excerpt, low resolution |
| `roads_map_credited_to_TIR_Findlater.jpeg` | 1611 × 2300 | Roman roads map credited to TIR (Findlater 2004 thesis) |
| `Roman_Imperial_Roads*.zip` | — | Road shapefiles (Kraków GIS project); source field names TIR TIFFs that are not included |

For Phase 3 the most relevant gap is the **Qumran–Buqeia–Hyrcania–Dead Sea shore area**, which none of the crops covers. That area holds many candidate sites (Secacah, Achor-in-the-Buqeia, Kidron outlet).

## Uploaded dossier: "Extracted site data — Jerusalem, Jericho & the Dead Sea" (added 2026-09-27)

A 5-page PDF you uploaded in session 1: `TIR_Copper_Scroll_Research_Summary.pdf`. It is not in the repo. It is a **secondary, web-derived** compilation, and its own heading says it paraphrases scholarly and institutional web pages dated 27 Sept 2026. Its sources are Encyclopaedia Judaica entries hosted on Encyclopedia.com, the Hebrew University's *Virtual Qumran*, the Heidelberg/Trier biblical place-name database, the Barrington Atlas Map 70 directory, the LacusCurtius Strabo, and Bible Gateway.

- Contents: site notes on Jericho (with Old Palestine Grid coordinates), Jerusalem/Aelia, Doq, Kypros, Wadi Qilt, Hyrcania and the Wadi Secaca tunnels, the Kidron, Mar Saba, Khirbet Qumran, Cave 3, Ein Feshkha and the Buqeia, Ein Gedi, and Achor.
- It also gives TIR page citations recovered secondhand: Kidron 102; Kypros/Threx? 106, 249; Doq 112–113; Ein Gedi 121; Jericho 143–144; Jerusalem 145–146; Hyrcania 149.
- **Use:** Phases 3 and 5 (site candidates, archaeology). It contains no readings or translations of 3Q15 and adds nothing to the Phase 1 table.
- Cross-check done in Phase 1: its Jericho entry cites 3Q15 "V 13 and XI 9". Both lines have ירחו in Puech's preserved text (V 13 מירחו, entry 24; XI 9 ירחו, entry 54). A third mention, VII 4 "[של ירחו(?)]", is only a restoration by Puech.
- Caveat: it states that no readable TIR map of Jerusalem–Jericho–Dead Sea was obtained. The repo crop `north_samaria_jerusalem.jpeg` does cover Jerusalem–Jericho legibly. What is missing is the Qumran/Dead Sea shore part.
- Its claims are secondhand and have not been checked against the underlying publications. Treat them as leads until checked.

## Source leads and uploads, 2026-09-29

See [source_leads_2026-09-29.md](source_leads_2026-09-29.md) for the full notes.

- **Uploaded (not in the repository):**
  - Stacey, "Some Archaeological Observations on the Aqueducts of Qumran," *DSD* 14.2 (2007), pp. 222–243. Read in full.
  - Zertal, *Manasseh Hill Country Survey* Vol. 2 (Brill 2008), 9 parts. Ibziq sites 42–44 (pp. 191–198), site 23 (pp. 151–153) and the name history (pp. 104–107) read, with page images checked.
  - Zertal & Mirkam, Vol. 3, 7 parts, and Zertal & Bar, Vol. 4 (2019), 8 parts. Searched; Ibziq is in neither.
- **Located, not yet read:**
  - Patrich, "The Aqueducts of Hyrcania": Yad Ben-Zvi 1989, pp. 243–260 (Hebrew; the Ilan–Amit volume) and JRA Suppl. 46 (2002), pp. 336–352.
  - Feldman 1974 (Hebrew); Garbrecht & Peleg, *BA* 57 (1994) 161–170.
  - Magen, "Gerizim, Mount," NEAEHL Supplement (2008), pp. 1742–1748, free on the BAS Library. Its staircases and cistern are summarised in the notes.
  - *HA* 40 (1971) p. 22 on the Ibziq excavation (IAA portal; 403 from the cloud sandbox). *Read later the same day*; see the next section.
- **Print only or for sale:** Hirschfeld 1985 and Patrich 1994 survey maps; JRA Suppl. 46 (by email from J. & L. Humphrey).

## Sources checked 2026-09-29 (second batch)

These add to the [source leads and uploads](#source-leads-and-uploads-2026-09-29) above.

- **Zertal, Vol. 2 (2008).** Besides the Ibziq pages, Kh. Salhab (pp. 151–153) and the name history (pp. 104–107), the roads (pp. 25–28) were read. The pagination matches the Wikipedia citation "Zertal 2007, vol. 2, pp. 191–197". Review: [entry59_bezek_review.md](entry59_bezek_review.md).
- **Stacey 2007.** Review: [qumran_stacey2007_review.md](qumran_stacey2007_review.md).
- ***HA* 40 (1971), p. 22 (Kh. Ibziq excavation, L-52/1971).** **Read.** The item page returns 403, but the PDF opens at <https://publications.iaa.org.il/cgi/viewcontent.cgi?article=1016&context=ha_hebrew_series> (45 pp.). It reports a kokhim tomb of the 1st–2nd centuries CE (F9.9). See [entry59_bezek_review.md](entry59_bezek_review.md).
- **Magen, "Gerizim, Mount," NEAEHL Supplement (2008), pp. 1742–1748.**
  - An automated summary of the BAS Library page reports the Hellenistic staircases and the courtyard cistern listed in the source leads.
  - A direct browser check shows only the History section without a login. That section dates the destruction of the temple and city to about 110 BCE by the coins (F9.11). The rest is paywalled, and the dates of use have not been checked (see Q47). *Read in full later the same day from a PDF extract; see the second run below.*
- **Browser checks, 29 September 2026.**
  - *Christians and Christianity* IV (JSP 16) covers sites in the Hebron hills and southern Judea. It has no chapter on Mar Saba, Castellion, Choziba or Chariton. Vol. II (JSP 14) is a site corpus, pp. 165–364, not yet searched.
  - Boaz Zissu, "Kings, Hermits and Refugees in the Judean Desert in the Late Second Temple Period and During the Bar Kokhba Revolt," in *New Studies in the Archaeology of the Judean Desert* (IAA 2023), pp. 185–216, is open access on JSTOR. Read in the second run (below).
  - Garbrecht and Peleg 1994 is on JSTOR, "read online" with a free account. Read in the second run (below).
  - *The Aqueducts of Israel* on Google Books (ID GWhoAAAAMAAJ) is snippet-only; see F9.10 and F10.8.
  - WorldCat holdings could not be checked (a human-verification page).

## Source extractions, 2026-09-29 (second run)

See [source_extractions_2026-09-29.md](source_extractions_2026-09-29.md). Each extraction file in `registration/` gives its citation, access route and reading mode on its first line.

- **Uploaded by the user (not in the repository):**
  - Magen, "Gerizim, Mount," NEAEHL 5 (2008), pp. 1742–1748: an 11-page PDF extract (printed pp. 1742–1752). Text layer; the site plan (p. 1743) was checked on the page image. ISBN 978-965-221-068-5.
  - Garbrecht & Peleg, *BA* 57.3 (1994), pp. 161–170: the JSTOR PDF (stable URL 3210411), 11 pages. Printed page = PDF page + 159. The table on p. 169 was transcribed from the page image.
- **Open access, read in full:**
  - Magen, Bijovsky & Tzionit, *Mount Gerizim Excavations* III: *The Coins* (JSP 19, IAA 2021), JSTOR `j.ctv2bwvt5v`, CC BY-NC 4.0. In Section One, printed page = PDF page − 1.
  - Zissu, "Kings, Hermits and Refugees…," in *New Studies in the Archaeology of the Judean Desert* (IAA 2023), pp. 185–215, JSTOR `jj.10329820.11`, CC BY-NC 4.0. Printed page = PDF page + 181.
  - SWP *Memoirs* II (1882), Internet Archive `surveyofwesternp02conduoft`: Bezek p. 231, Kh. Ibzik p. 237, Kh. es Selhab p. 240.
  - Guérin, *Samarie* I (1874), Internet Archive `descriptionsam01gu`: Kharbet Salhab p. 355.
  - *Hadashot Arkheologiyot* 40 (Oct. 1971), IAA publications portal: Kh. Ibziq p. 22 (PDF p. 23).
  - Gaß, "Besek," *WiBiLex* (2011), Augsburg OPUS 94703.
- **Search-only or snippets:**
  - *The Aqueducts of Israel* (JRA Suppl. 46, 2002): HathiTrust `mdp.39015051834664`, page-level word hits (HathiTrust seq = printed page + 4); Google Books `GWhoAAAAMAAJ` snippet images. Used for Ilan & Amit pp. 380–386 and Patrich pp. 336–352.
  - Jeremias, *Heiligengräber in Jesu Umwelt* (1958), Internet Archive `heiligengraberin0000joac` (lending copy): search-inside paragraphs. Leaf = printed page + 2.
  - DJD III (1962), Internet Archive `lespetitesgrotte0000unse` (lending copy): search-inside paragraphs. Leaf = printed page + 20.
- **Blocked:**
  - Patrich 1989 (Hebrew) on Kotar: kotar.cet.ac.il returned a server error; en.kotar.co.il shows guests only a paywalled p. 243.
  - The BAS Library needs a login; the NEAEHL entry was supplied instead as a PDF.
  - The old *Hadashot* site search (hadashot.iaa.org.il) returns nothing even for a control query during its move to the IAA portal.
- **Not found online:** *Mount Gerizim Excavations* II (JSP 8); JRA Suppl. 46 on Internet Archive.

## Text provenance and reuse

Use the available editions as research sources. Keep ancient wording, an editor's restoration, a modern translation and the project's own interpretation distinguishable, with page and line citations. Existing files and historical delivery notes do not establish a blanket permission or prohibition for new publication. Follow [Text and publication](AGENTS.md#text-and-publication); a replacement-transcription search is not a prerequisite for the research.

For the distinction between preexisting material and new contributions in an edition, see [17 U.S.C. § 103(b)](https://www.copyright.gov/title17/92chap1.html#103). For the PEF map, see the [CC BY-NC-SA 3.0 terms](https://creativecommons.org/licenses/by-nc-sa/3.0/).


## Plates used for the 2026-09-29 plate check

Puech 2006, vol. II, in the local PDF parts 9–11:

- **Radiographs of the original segments:** pls. CCCXXXIII–CCCLVI (part 10, PDF pages 23–46), two per column.
- **Colour photograph of the galvanoplastic copy:** pls. CCCLIX–CCCLXXXI, odd numbers (part 10 pp. 51–69; part 11 pp. 1–3).
- **Puech's facsimile drawings:** the even numbers CCCLX–CCCLXXXII.
- **A second copy photograph:** pls. CCXCVI–CCCVII (part 9 pp. 50–61). It proved to be the same image.

The plate captions were checked by `tools/plate_extract.py` before extraction. See [plate_check.md](plate_check.md).
