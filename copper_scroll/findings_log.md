# Findings log

A running record, newest session first. Each entry says whether it is **evidence** (what a
source says, with page) or **inference** (with reason and confidence). "BK" marks background
knowledge that does not come from the files in this repo.

---

## Session 1 — 2026-09-27 (Phase 1: master table)

### Sources

- F1.1 (evidence) The repo holds Puech 2006 (complete, 706 pp.) and Lefkovits 2000 (complete, 624 pp.). **Milik's DJD III edition and Wolters 1996 are not in the repo.** Milik and Wolters readings in the table are therefore secondhand, via Puech's commentary (pp. 179–206) and Lefkovits's commentary (pp. 29–442), and each one is labelled with the reporting source and page. See `sources.md`.
- F1.2 (evidence) The TIR material consists of crops only. `north_samaria_jerusalem.jpeg` is legible and shows "Achor Vallis" NW of Jericho. **No crop covers Qumran, the Buqeia or the Dead Sea shore.**
- F1.3 (evidence) Puech's Hebrew text is in a legacy font, and the numerals are partly vector drawings. It was decoded by script (`tools/puech_heb.py`), and all 181 lines were then checked against page images. Numeral values were checked against Puech's own totals (p. 173 nn. 27–34). All 33 numeral groups agree.

### Entry count

- F1.4 (evidence) There is no single agreed count of entries:
  - Milik (editio princeps): 64
  - Allegro: 61
  - Luria: 60
  - Wise: 65

  These figures are reported by Lefkovits 2000, p. 17 n. 69, and for Milik also by Puech 2006, p. 173 n. 26 and p. 179.
  - Puech: **60, or 61 if entry 12 is split into 12 + 12a** (pp. 173 n. 26, 179, 207).
  - Lefkovits: **60**, with #9, #12 and #56 further divisible into sub-items (p. 17 n. 69).
- F1.5 (evidence) Puech: every entry begins at the start of a line **except (3), which begins mid-line at I 6** (p. 179). The count depends on editorial judgement about where a new hiding place begins. The scroll has no explicit separators.

### Readings and numerals

- F1.6 (evidence) **ככ = "karsh", not "talents"**: Puech (p. 174 and n. 40) reads ככ as k(esef) k(arsh), 1 karsh = 10 shekels, 300 karsh = 1 talent. He credits Lefkovits with the idea first. Lefkovits (Appendix A, p. 481) proposes the same: ככ = כסף כרש "silver karsh". Milik and Allegro took ככ as an abbreviation of ככרין "talents" (Lefkovits p. 471 with nn. 1–2). This choice changes the totals by a factor of about 300 for 30 of the sums. The master table records the ככ sums as numbers and leaves the unit explicit.
- F1.7 (evidence) Puech's totals, from his reading (p. 173 nn. 27–34): at least 1,672 talents of silver, 362 of gold, 1,504 unspecified; 5 karsh of gold, 507 karsh of silver, 606.5 karsh unspecified (+80/100/120 in lacunae); 165 gold ingots; 19 bars of silver; 4 staters; 20 minas. His n. 27–31 also gives Lefkovits's differing totals (Lefkovits 2002, 153).
- F1.8 (evidence) Numerals are written sometimes in words and sometimes in numeral signs. In Puech's typesetting the signs are: unit stroke "|", a 10-sign (hook), a 20-sign (shaped like "3"), a 100-sign, a ½-sign (shaped like ף, IX 6). Ranges: Puech index p. 219; values checked against his translation.
- F1.9 (evidence) **Greek letter groups: seven, all in columns I–IV**, always at the end of an entry: ΚΕΝ (I 4), ΧΑΓ (I 12), ΗΝ (II 2), ΘΕ (II 4), ΔΙ (II 9), ΤΡ (III 7), {Ι}ΣΚ (IV 2) (Puech index p. 219; p. 175). They occur in entries 1, 4, 6, 7, 9, 12a and 15. Puech notes that the last of them concerns Koḥlit (15).
- F1.10 (evidence) **Errors inside Puech 2006.** His English translation (pp. 208–216) disagrees with his Hebrew and French:
  - (15): EN "[20+29+(?)]", FR "[20+20+(?)]"
  - (18): EN "two hundred talents", FR/Hebrew ככ = karsh
  - (27): EN "22 k(arsh)", FR "27", numeral 27
  - p. 211: EN entry numbers (31)–(33) should be (30)–(32)
  - (32): EN "six cubits", Hebrew שלוש and FR "trois"
  - (37): EN "79 k(arsh)", FR "70", numeral 70 and n. 30
  - VII 6: the Hebrew print closes a lacuna ("ואר]בע") without opening it; FR "ving[t-qua]tre" shows where it opens.

  **The table follows the Hebrew and the French.**

### Topography flagged for later phases (not analysed yet)

- F1.11 (evidence) On the Valley of Achor, Puech (p. 179) follows Milik and places it NE of Jericho (Wadi Nuweiʿimeh, the Byzantine monastery of Chorembe), citing Eusebius and Jerome. He explicitly rejects the Buqeia. Lefkovits (p. 29) reports that Allegro identified Achor with the Buqeia and that Luria put it near Jericho. The TIR crop (F1.2) labels "Achor Vallis" NW of Jericho. These are three placements to test in Phase 3.
- F1.12 (evidence) Puech's overall geography (p. 175) has two groups.
  - **Entries 1–15** are the ones carrying Greek letters. They are split between Ḥorebbeh in the Valley of Achor (1, 2, 3?) and three caches at or near Koḥlit (4, 11, 15). The rest are "probably" around the Temple enclosure in Jerusalem, following Milik's identifications, or "less easily" in the Jericho region. He adds: "leur localisation précise restera à jamais inconnue" — their exact location will remain unknown forever.
  - **Entries 16–60** follow roughly Koḥlit → Achor (17) → wadi ʿAṣla (18) → Sokokah (= Kh. Qumran) and surroundings (20–27) → Jericho ford (28) → Jericho (29–30) → Doq (31) → Kozeba (32) → Kidron (35) → Shaveh (36–37) → Neṭofah (38) → Tekoa–Bethlehem (39–45) → Beth ha-Kerem (46) → south of Jerusalem (47–49) → around the city walls (50–56) → Gerizim (57) → Beth Sham (58) → Bezek (59) → Koḥlit (60).
  - He identifies Koḥlit with Tell es-Sultan tentatively ("à titre d'hypothèse", p. 175 n. 49) and admits that the name "reste assez difficilement identifiable" (remains rather hard to identify).
  - (Inference, low confidence, to be tested in Phase 3) The more a route is reconstructed from identifications that are themselves uncertain, the more circular it becomes. Puech's order is a hypothesis to test, not evidence.

### Results of the full comparison (added at the end of session 1)

- F1.13 (evidence, checked by script) **Puech and Lefkovits divide the text identically.** All 60 boundaries have the same line ranges. Puech's 12 + 12a = Lef. #12. The 60/64 difference with Milik is therefore a difference with *both* modern editions.
- F1.14 (evidence) **Where Milik divides more finely:**
  - #9: two items (Lef. p. 126)
  - #56: three items (Lef. p. 399)
  - a new entry beginning with ובתכן at V 7 (Puech p. 189 n. 226)
  - #12: two items, but Lef. p. 142 says only "the scholars", without naming Milik

  Milik's last item is #64 in DJD III and was #62 in 1956–57 (Lef. p. 426 n. 2). The documented splits give 65, not 64, so one of them does not apply to Milik, or Milik merges two entries elsewhere. Unresolved without DJD III (Q4).
- F1.15 (evidence, checked by script plus review of every flagged line) **Lefkovits vs Puech:**
  - The consonantal text agrees on 108 of 181 lines.
  - 70 lines differ in reading or restoration.
  - In **22 entries** the difference changes a place, direction, distance/depth, quantity or kind of treasure: 1, 9, 10, 12, 14, 16, 28, 30, 31, 32, 37, 38, 40, 41, 44, 47, 49, 50, 52, 54, 56, 60. See the summary table, §3b.
- F1.16 (evidence) **Numerals** differ between the two editions at III 13, IV 2, VII 2, VII 16 (80/60), VIII 13 (66/67) and XI 7 (none/10). Lefkovits reports that the three facsimile drawings (Baker, Milik, Allegro) themselves disagree at VII 16, VIII 9 (2/4/7), VIII 13 and X 11 (10/20).
- F1.17 (evidence) **Name frequencies in Puech's text:**
  - Koḥlit ×5 (4, 11, 15, 19, 60); the mention in 15 is partly restored.
  - Sekakah ×4 (20, 21, 22, 24).

  Both counts match Puech's own statement (p. 175 n. 49). **Jericho is preserved only in 24 and 54.** In 29 it is Puech's restoration "[של ירחו(?)]", and Lef. leaves that space unrestored.
- F1.18 (evidence) **Lefkovits's notation is inconsistent.**
  - He prints *corrected* forms in some places: אמות where the drawings have גמות (X 6, X 13); ככרין where the scroll has כררין (X 7); הדרומית for הדוומית (XI 2); agent notes on Lef. pp. 331–363.
  - He prints *uncorrected* engraved forms in others: עכון, חפון (IV 6–7).

  Anyone comparing his text letter by letter has to allow for this.
- F1.19 (evidence) **More errors inside the books** (full lists in the extraction notes):
  - Puech's commentary contradicts his printed text at: II 5, where the commentary prefers מתיה but the text keeps m(b)ty; VII 11 (hmšṭḥ with no waw vs printed hmšṭ<w>ḥ); XI 17 (m[ʿrʾ] vs m[ʿrh); XII 6 (the forgotten yod placed at l. 7).
  - Puech's cross-references mis-number his own entries (VII 8 = (30), not (31); IX 17 = (44), not (45)).
  - Lefkovits: his item 5 translation lines are swapped (p. 90); at 12:10 he places צפון "in line 12:11"; at 12:4 he prints גריזין although the scroll has גויזין; and he reports Wolters's reading two ways at I 1 and at I 2–3.
- F1.20 (inference, medium) The editions disagree more on **meaning** than on letters. For example, שדת (I 3) is a "chest" for Puech and a "carrying chair" for Lef.; בדין/כדין (II 11, VII 10, IX 3) are "bars" (Puech) or "pitchers" (Lef.); ככ is karsh for both. Phase 2 (the lexicon) should treat these as a separate layer of uncertainty from the readings.
