# Phase 1 summary: master table of 3Q15

Session 1, 2026-09-27/28. The table itself is `copper_scroll_master_table.csv`: 61 rows, one per Puech entry, with 60 + 12a. See the note at the end on where that file lives.

**Conventions.** "Puech" = Puech 2006 (primary reading). "Lef." = Lefkovits 2000. Milik and Wolters readings are **secondhand**, reported by Puech or Lefkovits with page numbers, because neither book is in the repo. Line references are column:line. ‖ marks a line break in the Hebrew.

## 1. How many entries? (count verified against the editions)

There is no neutral count. The scroll has no separators, so each editor decides where a new hiding place begins.

| Editor | Entries | Source for the number |
|---|---|---|
| Milik (DJD III, 1962) | 64 (62 in his 1956–57 articles) | Lef. p. 17 n. 69; p. 426 n. 2; Puech p. 173 n. 26; **firsthand: Milik 1960, ADAJ 4–5, pp. 139–142 (items 1–64)** |
| Allegro | 61 | Lef. p. 17 n. 69 |
| Luria | 60 | same |
| Wise | 65 | same |
| Lefkovits | 60; #9, #12, #56 divisible | Lef. p. 17 n. 69 |
| **Puech** | **60, or 61 with 12 / 12a** | Puech pp. 173 n. 26, 179, 207 |

- **Puech and Lefkovits draw the same 60 boundaries.** This was checked line by line: every Puech entry has the same line range as the Lefkovits item with the same number. Puech's 12 + 12a together equal Lef. #12.
- **Milik's 64, now resolved from Milik 1960 (ADAJ 4–5, pp. 139–142, uploaded at the end of the session):** 64 = Puech's 60 + 1 (9 split at II 9) + 1 (12/12a) + 2 (56 split into three). Milik also makes each ובתכן/בתכן אצלם phrase (V 7, XI 1, XI 4, XI 11, XI 15) *open* the next item. That moves boundaries without adding items. The full mapping is in `tables/entry_concordance.csv`. The earlier, superseded reasoning follows. Before that upload, the documented places where he divides more finely were:
  - #9 into two (Lef. p. 126)
  - #56 into three (Lef. p. 399)
  - a new entry at V 7 ובתכן (Puech p. 189 n. 226)
  - probably #12 into two (Lef. p. 142 says "the scholars", without naming Milik)

  Together these seemed to give 65. The upload showed that the V 7 case moves a boundary and does not add an item.

## 2. Clearest entries

"Clear" here means **textually secure**: no lacuna, no "(?)" in Puech, and Lefkovits reads the same letters. That is not the same as **clear in meaning**.

- **Textually secure (15):** 2, 3, 6, 8, 12a, 19, 24, 27, 34, 35, 43, 45, 48, 53, 58.
- **Also specific in content** (a named or distinctive landmark plus a distance or depth, and both editions agree). These are candidates for Phase 3:
  - **24:** tomb in Naḥal ha-Kippa, "as one comes from Jericho to Sekakah", 7 cubits deep.
  - **35:** cairn at the mouth of the Kidron gorge, 3 cubits.
  - **48:** under the monument (*yad*) of Absalom, west side, 12 cubits.
  - **58:** mouth of the spring of Beth Sham.
  - **27:** the queen's "mausoleum" (משכן המלכא), west side, 12 cubits.
  - **57:** Mount Gerizim. Its text is secure except for השוח[[ה]] (Puech) against השית (Lef.).
- **Secure text, obscure meaning:** 3 (סתומ בחליא), 43 (בצחיאת גר פלע), 45 (בור גר מזקות שרוי). The letters are agreed; the sense is not.

## 3. Most damaged or most contested

Two different problems: physical loss, and disagreement where the text is preserved.

**(a) Lacunae that remove place, direction or quantity** (Puech's own restorations):

| Entry | What is lost or restored |
|---|---|
| 12 | Name of the court: בחצ[ר ש(ל) ]דיאט(?) against Lef. בח[צר נב]ט |
| 15 | "[north(?) of Ko]ḥlit" is restored; the sum is 14 plus a lacuna |
| 16 | The landmark ל[בר]כא(?) is restored; the distance is 14 (Puech ארבע[ ע]סרה) or 40 (Lef. ארבע[ין]) |
| 21 | Direction "[west of(?)]", the "[great stone]" and the depth "[three]" are all restored |
| 28 | Direction lost; the figure is 22 + [40 or 60] (Puech), Lef. reads no figure |
| 29 | "[collection of the waters]" and "[of Jericho(?)]" are restored. **Jericho is not preserved in this entry.** |
| 33 | "[con]duit" restored; the last phrase is uncertain |
| 44 | "dist[rict]" restored |
| 56 | "ca[vity]" and "sil[ver … talents]" restored |

In entry 25 the missing letters are single first letters ([ב], [ה], [א]) and change nothing.

**(b) Preserved or partly preserved text that the editions read differently.** Lef. vs Puech; 22 entries are flagged "subst." in the table.

| Entry | Puech | Lefkovits | What changes |
|---|---|---|---|
| 1 | אריח | אחת | Distance: 40 vs 41 cubits |
| 9 | 15 cubits | 19 cubits | Distance |
| 10, 30, 38 | בדין "bars" | כדין "pitchers" | The silver deposit |
| 12 | "court of the … Tribunal(?)" | "Court of Nebaṭ" | Place name (partly in a lacuna) |
| 14 | "3 cubits under the slab(?)", 14 | "below the corpse", 13 + lacuna | Landmark and quantity |
| 16 | 14 cubits | 40 cubits | Distance (partly restored) |
| 28 | [20+20(+20?)]+22 | No figure read | Quantity |
| 31 | המשטוח "drying floor" | המשמרה "guard post" | Landmark |
| 32 | Kozeba, 80 | Buz(ba), 60 | Place name and quantity; the drawings differ |
| 37 | ברוי "irrigated land" | בדין | Landmark |
| 40 | "facing south" | "facing the sea (west)" | Direction |
| 41 | "in the hole: much silver of offering" | "in Qovaʿ: silver of consecrated matter" | Whole line |
| 44 | Maṣad-na, "dist[rict]" | "Fort of Nobah" | Place name |
| 47 | "valley of Job(?), chamber by its spring" | "Pure Valley, its western side" | Landmark and direction; also 20 vs 10 cups |
| 49 | "outlet of the waters of Siloam" | "pool of the water closet of Jehu" | Place name |
| 50 | "court of Zadok", with gold | "[inner court]", no gold | Landmark and treasure |
| 52 | No sum | A sum of 10 (or 11, or 1) karsh | Quantity |
| 54 | "the common people … of Jericho" | "the sons of Obed the Jerichoite" | Whose tomb |
| 56 | "entrance from the west" | "entrance from the city" | Direction |
| 60 | "which is north of Koḥlit" | "in Janoah, north of Koḥlit" | Place name |

**Numerals.** The editions differ at six places: III 13, IV 2, VII 2, VII 16, VIII 13 and XI 7. Lefkovits reports that the three drawings (Baker, Milik, Allegro) themselves disagree at VII 16, VIII 9, VIII 13 and X 11.

## 4. Recurring landmark terms

Counts are of Puech entries, from his text. *Italics* = attested in that entry only through Puech's restoration.

| Term | Entries |
|---|---|
| בור cistern | 3, 6, 8, 9, 10, 15, 45 |
| קבר tomb | 14, 24, 51, 53, 54, 60 |
| צריח underground chamber | 8, 36, 37, 39, 40, 47 |
| פתח opening (and ביאה entrance: 10, 13, 56) | 3, 4, 25, 26, 47, 60 |
| שית pit | 13, 18, 19, 43, 60 |
| מערה cave | 7, 25, 26, 30, *56* |
| **כחלת Koḥlit** | 4, 11, *15*, 19, 60 |
| פנה corner | 12, 12a, 13, 31, 51 |
| חצר / גנת court | 3, 8, 12 (partly), 50, 52 |
| אמא conduit | 4, 16, 29, *33* |
| אשוח reservoir | 22, 29, 46, 55 |
| **סככא Sekakah** | 20, 21, 22, 24 |
| יגר cairn | 20, 28, 35 |
| ירחו Jericho | 24, *29*, 54 |
| צדוק Zadok | 50, 51, 52 |
| גי valley | 20, 34, 47 |
| מעלות steps | 1, 6, 57 |
| עמוד pillar | 15, 25, 51 |
| **עמק עכור Valley of Achor** | 1, 17 |

Each of the following occurs twice: dovecote (38, 44), boulder (23, 26), gorge (35, 43), pipe (42, 59), Shaveh (36, 37), threshold (10, 56), wadi (24, 45), pool (11, 16), black stone (47, 56).

The **formula** is stable. A locus (usually ב- + noun) is followed by a specifier, then a direction or distance, then **חפור/חפר "dug/buried" + depth in cubits (22 entries)**, then the contents. In entry 38, חפורות means "holes" and gives no depth. Entry 5 gives a *height* above the floor, and entry 14 gives a distance "under" a slab.

## 5. Entries that seem to share a location or form a sequence

This section is inference from the text alone. Confidence: **high** = the entries share an explicit name or phrase; **medium** = adjacency plus a shared feature; **low** = editorial interpretation.

- **Same place, stated in the text (high):**
  - 12 and 12a: the two corners of one court.
  - 9: a cistern and its conduit.
  - 56: two or three deposits at one entrance.
  - 50: four corners of one court.
- **Koḥlit group (high for the name, open for the site):** 4, 11, 15, 19, 60. Entries 19 and 60 are both "north of Koḥlit" and could be one area. Entry 60 holds the duplicate document, so the list ends where it keeps its key.
- **Sekakah run (high):** 20 → 21 → 22 → 23 → 24 are consecutive. Entries 22 and 23 are also linked by "Solomon": his basin (22) and his trench (23). Entry 24 fixes the route: "coming from Jericho to Sekakah". Entries 25–27 continue without a place name and may belong to the same area (medium).
- **Zadok group (high):** 50 → 51 → 52, with the court, tomb and "opposite the court of Zadok". Entry 53, the tomb under the colonnades, follows (medium).
- **Pairs sharing a name (high):**
  - 36–37 (Shaveh)
  - 13–14 (both שבמלה/שבמלח)
  - 1 and 17 (Valley of Achor), which are 15 entries apart
- **Pairs sharing a feature (medium):**
  - 23 and 26 (הרגב "the boulder")
  - 38 and 44 (dovecotes)
  - 47 and 56 ("black stone")
- **Possible Temple-precinct cluster (low; Milik's and Puech's interpretation, not in the text):** 3, 8, 9, 10, 12/12a. These mention a court, a peristyle, an East Gate and a wall; Jerusalem is never named. Lefkovits also links 9 and 10 (Lef. item 10).
- **Outliers at the end (high for the names):** 57 Gerizim, 58 Beth Sham, 59 Bezek, far from the rest. Then 60 returns to Koḥlit.
- **Greek letters (high):** all seven groups (ΚΕΝ, ΧΑΓ, ΗΝ, ΘΕ, ΔΙ, ΤΡ, {Ι}ΣΚ) are in entries 1–15 (entries 1, 4, 6, 7, 9, 12a, 15) in columns I–IV, always at the end of an entry. Puech (p. 175) asks whether entries 1–15 formed a separately supervised list.

## 6. Data quality

- **Puech's Hebrew** was decoded from a legacy font. All 181 lines were checked against page images, and all 33 numeral groups against his own totals.
- **Lefkovits's Hebrew** was read from page images by eight parallel extraction passes, because his Hebrew OCR is unusable. His consonantal text agrees with Puech's on **108 of 181 lines**, after allowing for notation such as engraved-vs-corrected forms and numeral signs. The other **73** lines were reviewed by hand. Three were notation artefacts (I 6, X 13, XI 12); **70 lines differ in reading or restoration**. A separate numeral comparison found six lines where the figures differ.
- **Internal errors found in both books** are listed in the findings log. Neither book is error-free, and the table follows each author's Hebrew over his translation.
- **Not done in Phase 1:** place identification, lexicon, and analysis of the Greek letters (Phases 2–5).
- **Session 2 update: Milik's DJD III text read firsthand.** DJD III was uploaded after Phase 1. Milik's own Hebrew text and French translation are now columns in the master table (`hebrew_milik1962`, `translation_milik1962_fr`, `variants_milik1962_firsthand`).
  - Against Puech there are 84 hand-checked differences in 49 entries; 52 of them, in 39 entries, are substantive.
  - Milik's figures differ from Puech's at III 13, VII 16 and VIII 9, the same three figures as in Milik 1960.
  - The secondhand Milik column now labels Milik's pre-DJD (1956–57) readings, his drawings and the alternatives he mentions.

  See findings F2.3–F2.5.

## Where the table lives

The original session reported that `copper_scroll_master_table.csv`, `variants_long.csv` (2,072 reported readings, one per row) and `puech_lines.csv` were delivered directly and **not pushed**. Those tables contain complete edited readings and, in the master table, modern translations alongside project writing. `entry_concordance.csv`, which holds numbers and notes, was committed. This is a historical delivery record, not a claim that the session files remain available or a blanket restriction arising from the repository being public. Follow [Text and publication](AGENTS.md#text-and-publication) for new outputs; continue using the existing editions for research.
