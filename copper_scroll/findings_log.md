# Findings log

A running record, newest session first. Each entry says whether it is **evidence** (what a
source says, with page) or **inference** (with reason and confidence). "BK" marks background
knowledge that does not come from the files in this repo.

---

## Session 2 — 2026-09-28 (DJD III; Phase 2: landmark lexicon)

### Method notes

- F2.1 (evidence, corpus check) **A lemma search alone gives false attestations for many scroll terms.** The first concordance run matched the scroll words to Strong's lemmas and stems in the WLC, and to stems in the Mishnah. A check of the matched forms against the WLC lemmas showed that these are homographs, not the scroll's sense:

  | Term (scroll sense) | What the Bible hits really are |
  |---|---|
  | אשיח/אשוח 'basin' | the verb שיח 'muse' (Strong 7878) |
  | שית 'pit' | שיח 'bush' / 'complaint' |
  | רובד 'pavement, terrace' | רביד 'necklace' |
  | משח 'measure' | משח 'anoint' |
  | יגר 'cairn' | the verbs 'fear' / 'sojourn' (only Gen 31:47 is relevant) |
  | צוק 'cliff' | צוק 'distress' (the relevant verse is 1 Sam 14:5, מצוק) |
  | חריץ 'trench' | 'threshing sledge', 'cheese slice' |
  | שובך 'dovecote' | 'thick branches'; a personal name |
  | כחלת (place name) | Ezek 23:40 'you painted (your eyes)' |
  | נפש 'funerary monument' | 683 verses of 'soul, life' |
  | יד 'monument' | 1,446 verses of 'hand' |

  I corrected the search (`terms_fix` in the scratchpad) to use exact forms, phrases or chosen verses for these terms. Every change has a note that says why. **Consequence:** raw hit counts are not evidence of usage. The lexicon reports only hits checked for sense.

### Eusebius on Achor (firsthand, Klostermann's Greek and Jerome's Latin)

- F2.2 (evidence, firsthand: Klostermann, GCS 11.1, 1904) **Eusebius places Achor "north of Jericho" and "near Galgala".**
  - Onom. 18.17–20 (Achor): κεῖται δὲ ἐν βορείοις Ἱεριχοῦς, "it lies to the north of Jericho", and the locals still call it so.
  - Onom. 84.18–20 (Emekachor): πλησίον Ἱεριχοῦς … παρὰ τὴν Γάλγαλα, "near Jericho … beside Galgala".
  - Jerome's Latin agrees: *ad septentrionem Iericus* (19.18–22) and *iuxta Iericho haud procul a Galgalis* (85.18–21).
  - Eusebius puts Galgala "to the east of old Jericho, going toward the Jordan" (Wolf's translation, Wolf n. 311).
  - This checks Milik 1960's citation (F1.25) against the text itself. **Eusebius says "north", not "north-east" or "north-west".** Milik writes that Jewish and Christian traditions placed the valley "au nord-est de Jéricho" (DJD III, section D no. 3, p. 262).
  - (Inference, medium confidence) The "east" in Milik's wording probably comes from the link with Galgala, which lies east of Jericho. The Onomasticon itself fits both Milik's Wadi Nuweiʿimeh and TIR's label NW of Jericho. It does **not** fit the Buqeia, which is SW of Jericho. See Q13.
  - (Inference, medium confidence) For the Copper Scroll this is late evidence (4th century CE). It shows where the *tradition* put Achor, not where the scroll's author put it.

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
- F1.14 (evidence; **superseded by F1.21**) **Where Milik divides more finely:**
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

### Milik 1960 (ADAJ 4–5), uploaded at the end of session 1

- F1.21 (evidence, firsthand: Milik 1960, pp. 139–142) **Milik's 64 items are fully mapped.**
  - Milik 1–8 = Puech 1–8.
  - Milik 9 + 10 = Puech 9 (II 7–8 / II 9).
  - Milik 11–12 = Puech 10–11.
  - Milik 13 + 14 = Puech 12 + 12a.
  - Milik 15–24 = Puech 13–22.
  - Milik 25 = the ובתכן אצלם phrase at the end of V 7 + Puech 23.
  - Milik 26–51 = Puech 24–49.
  - Milik 52–57 = Puech 50–55, except that each בתכן phrase opens the next item.
  - Milik 58 + 59 + 60 = Puech 56 (XI 16–XII 1a / XII 1b–2a / XII 2b–3). Milik 58 also takes the בתכן phrase of XI 15.
  - Milik 61–64 = Puech 57–60.

  So 64 = 60 + 1 + 1 + 2. **The ובתכן phrases move boundaries but add no items.** This clears up the "65 not 64" puzzle in F1.14: Puech's n. 226 describes a boundary shift, not an extra entry.
- F1.22 (evidence, firsthand) **Milik 1960 translates ככ as "talents" everywhere** (e.g. items 16, 17, 22), which confirms F1.6 at first hand. He also calls entry 58 "five talents of gold" (XII 1), where Puech reads "gold 5 k(arsh)".
- F1.23 (evidence, firsthand) **Milik 1960's figures that differ from Puech:**
  - III 13: 13 talents (Puech 14).
  - IV 4: "fort[y on]e cubits" (Puech 14; Lef. 40). This gives three readings of one distance.
  - VII 16: 60 (Puech 80; Lef. 60). This matches Lef.'s report that Milik's drawing shows 60.
  - VIII 9: 4 (Puech 7; Lef. 7). This matches Lef.'s report of Milik's drawing.
  - X 6: "twelve *feet*" (Puech "ten cubits").
  - X 13: "twelve *feet*" (Puech "twelve cubits"). Milik italicises "feet" as uncertain.
  - IX 2: "dig two (cubits)" (Puech: "two holes").

  He agrees with Puech on 23½ at IX 6, 66 at VIII 13 and 42 at XII 3.
- F1.24 (evidence, firsthand) **Milik 1960's readings of disputed places**, in translation:
  - item 40, IX 7: "facing the Sea", agreeing with Lef. against Puech's "south";
  - item 46, IX 17: "aque[duct] of ha-Masad";
  - item 49, X 8: "pool of the vale of …, on the west side", partly agreeing with Lef.'s "western side";
  - item 51, X 15: "pool of the Baths of Siloah";
  - item 56, XI 9: "the Sons of … of Yerah";
  - item 64, XII 10: "the tunnel in the Smooth Rock to the north of Kohlit, which opens towards the north".

  Their place identifications are in the commentary, pp. 143–155. It has been extracted for Phase 3 but not yet analysed.
- F1.25 (evidence, firsthand: Milik 1960 commentary pp. 143–147; flagged for Phase 3, not analysed) **Achor and Sekakah in Milik 1960.**
  - *Achor.* Milik accepts that the Iron Age "Valley of Trouble" is **el-Buqeiʿah**, SW of Jericho (citing Noth 1955; Cross and Milik 1956). He argues that the Copper Scroll's Valley of Achor is the later traditional one: "the broad **Wadi Nuweiʿimeh, northeast of Jericho**". His evidence is Josephus (AJ V 33, 42–4), Eusebius and Jerome (Onomasticon 18, 84: "north of Jericho", "near Galgala"), and Eusebius's remark that the natives still used the name. He places Ḥorebbeh = the Byzantine monastery of Chorembe (John Moschus) "with more probability" near Kh. el-Mafjar.
  - *Sekakah.* Biblical Sekakah = **Kh. es-Samra**, the central ruin of the Buqeia. For the scroll's author, however, "Sekaka" named the whole torrent of **Wadi Qumran**, and "the vale of ha-Sekaka" is the wadi between the cliff and the Dead Sea (p. 146). The aqueduct of V 1–2 is the Qumran aqueduct, and "Solomon's Pool" (V 5–7) is "undoubtedly" the cistern SE of Kh. Qumran (p. 147).
  - Consequence for rule 5: at least three placements of the scroll's Achor must be tested in Phase 3:
    - Buqeia (Allegro, per Lef. p. 29; and a view the uploaded dossier records);
    - Wadi Nuweiʿimeh NE of Jericho (Milik 1960; Puech p. 179);
    - TIR's "Achor Vallis" label NW of Jericho (repo crop).
  - (Inference, **BK**, low confidence, to check in Phase 3) Wadi Nuweiʿimeh is thought to rise NW of Jericho near Naʿaran/ʿAin Duk and run east past Kh. el-Mafjar. If so, TIR's "NW" and Milik's "NE" may label different stretches of one wadi rather than rival sites.
