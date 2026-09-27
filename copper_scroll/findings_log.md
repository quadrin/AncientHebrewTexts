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
