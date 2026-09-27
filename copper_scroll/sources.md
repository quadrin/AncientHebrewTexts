# Copper Scroll (3Q15): source inventory

Checked 2026-09-27 against branch `main` (commit 637a7a9, "Add files via upload").

## Summary

| Source you listed | In the repo? | Readable? | How it is used |
|---|---|---|---|
| Puech 2006, *Le Rouleau de cuivre de la grotte 3 de Qumrân (3Q15)* | Yes, 11 PDF parts, 706 pages | Yes. Born-digital text layer. The Hebrew is in a legacy font and needs decoding (see below). | Primary reading |
| Lefkovits 2000, *The Copper Scroll – 3Q15: A Reevaluation* | Yes, 11 PDF parts, 624 pages | Partly. Scanned library copy with OCR. The English OCR is usable; **the Hebrew OCR is useless**, so every Hebrew word was read from the page images. | Variant readings; secondhand Milik, Allegro, Luria and Wolters readings |
| Milik, DJD III (1962) | **No.** No file matches Milik, DJD or *Les 'petites grottes'*. | — | Milik's readings are taken **secondhand** from Puech's commentary and Lefkovits's commentary, and are labelled so in every row. |
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
- Encoding: the Hebrew is set in "SuperHebrew" (plus "HebraicaII" for some final forms), stored in visual left-to-right order. Numeral signs are partly font glyphs (unit stroke "|" in Symbol; the 20-sign as a "3" glyph) and partly **vector drawings** (the 10-sign, the 100-sign). They do not survive text extraction. `tools/puech_heb.py` decodes the text layer. **Every one of the 181 lines was then checked by eye** against page renders, and all numerals were set by hand from the images and from Puech's own totals (p. 173 nn. 27–34). See `data/puech_lines.csv`.
- **Internal inconsistencies in Puech's own book:** his English translation (pp. 208–216) disagrees with his Hebrew and French in several places. See the findings log. The master table follows his Hebrew and French.

## Lefkovits 2000

- Files: `The Copper Scroll - 3Q15_ A Reevaluation _ A New Reading, - Lefkovits, Judah-1.pdf` … `-11.pdf` (STDJ 25). The copy is from the Claremont School of Theology library; there are library stamps on the front pages.
- **Printed page = global PDF page − 24.** Parts 1–10 have 60 pages each, part 11 has 24.
- Items 1–60: pp. 29–442. Discussion: p. 443ff. Appendix A (ככ vs ככרין): p. 471. Appendix B (numerals): p. 489. Appendix C (Greek letters): pp. 498–504. Appendix D: p. 505.
- Lefkovits p. 17 n. 69: "Milik divides the text into 64 items, Allegro into 61, Lurie into 60, and Wise into 65 … This author divides the Copper Scroll into 60 items, three of which (#9, #12, #56) can be further subdivided into two or three sub-items."
- His commentary quotes the Hebrew readings and translations of Allegro, Milik, Lurie (Luria), Pixner, Wolters (1996), García Martínez, Vermes, Wise, Beyer and Wacholder, phrase by phrase. It is the richest source in the repo for the Milik and Wolters variants.

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

## Copyright note

The repository `quadrin/AncientHebrewTexts` is **public** on GitHub, and `main` contains the complete Puech (Brill 2006) and Lefkovits (Brill 2000) books, plus map crops without an established reuse licence (see the README on `main`). Files in this `copper_scroll/` folder quote the editions only as research data: line-by-line readings with page citations, short glosses, and English translations written for this project. They do not copy the editors' translations.
