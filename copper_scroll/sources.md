# Copper Scroll (3Q15): source inventory

Checked 2026-09-27 against branch `main` (commit 637a7a9, "Add files via upload").

## Summary

| Source you listed | In the repo? | Readable? | How it is used |
|---|---|---|---|
| Puech 2006, *Le Rouleau de cuivre de la grotte 3 de Qumrân (3Q15)* | Yes, 11 PDF parts, 706 pages | Yes. Born-digital text layer. The Hebrew is in a legacy font and needs decoding (see below). | Primary reading |
| Lefkovits 2000, *The Copper Scroll – 3Q15: A Reevaluation* | Yes, 11 PDF parts, 624 pages | Partly. Scanned library copy with OCR. The English OCR is usable; **the Hebrew OCR is useless**, so every Hebrew word was read from the page images. | Variant readings; secondhand Milik, Allegro, Luria and Wolters readings |
| Milik, DJD III (1962) | **No.** No file matches Milik, DJD or *Les 'petites grottes'*. | — | Milik's Hebrew readings are taken **secondhand** from Puech's commentary and Lefkovits's commentary, and are labelled so in every row. |
| Milik 1960, ADAJ 4–5 (uploaded in session 1) | Not in the repo (upload only) | Yes, an image scan with no text layer; read visually | **Firsthand** Milik: his complete English translation with his 1–64 numbering, and his commentary on the place names |
| Wolters (you listed his readings as a variant column) | **No.** Wolters 1996, *The Copper Scroll: Overview, Text and Translation*, is not in the repo. | — | Taken **secondhand** from Lefkovits (who cites "Wolters 1996" throughout) and Puech. |
| TIR Iudaea-Palaestina, North sheet | **Only crops**, not the sheet | Yes (see below) | Not used in Phase 1 |

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
- Encoding: the Hebrew is set in "SuperHebrew" (plus "HebraicaII" for some final forms), stored in visual left-to-right order. Numeral signs are partly font glyphs (unit stroke "|" in Symbol; the 20-sign as a "3" glyph) and partly **vector drawings** (the 10-sign, the 100-sign). They do not survive text extraction. `tools/puech_heb.py` decodes the text layer. **Every one of the 181 lines was then checked by eye** against page renders, and all numerals were set by hand from the images and from Puech's own totals (p. 173 nn. 27–34). The line table (`puech_lines.csv`) reproduces Puech's edited text, so it is kept out of this public repository (see "Where the table lives" in `phase1_summary.md`).
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
- Caveat: this is Milik in 1960. Where DJD III (1962) differs, it is unknown until DJD III is available. The numbering agrees with the "64" that Lefkovits reports for DJD III (Lef. p. 426 n. 2).

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

## Copyright note

The repository `quadrin/AncientHebrewTexts` is **public** on GitHub, and `main` contains the complete Puech (Brill 2006) and Lefkovits (Brill 2000) books, plus map crops without an established reuse licence (see the README on `main`). Files in this `copper_scroll/` folder quote the editions only as research data: line-by-line readings with page citations, short glosses, and English translations written for this project. They do not copy the editors' translations.
