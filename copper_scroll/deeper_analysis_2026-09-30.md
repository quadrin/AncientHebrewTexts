# Reading the list from the inside: how the Copper Scroll was compiled

> **Repository note (added on merge).** The scripts and outputs from `deeper_analysis_code_2026-09-30.zip` are in [`deep_analysis/`](deep_analysis/README.md), which also compares the numbers below with the script outputs. `entry_features_2026-09-30.csv` is not in the repository; `deep_analysis/features.py` makes the per-entry features again. Of the two earlier reports, [the follow-up](sequence_model_followup_2026-09-30.md) is in the repository, without the §8.1 correction below; the first report is not. The next report, [tests on old surveys and plans](leads_on_old_plans_2026-09-30.md), corrects §2.1 and §8.5 on the priority of ha-Melaḥ as a place.

30 September 2026. Third report in this series, after `sequence_model_and_new_leads_2026-09-30.md` and `sequence_model_followup_2026-09-30.md`. Labels: **evidence** (a count or a quotation you can check), **inference** (my reasoning from it), **BK** (background knowledge, not checked here).

**Approach.** The earlier reports used the places of anchored entries. This one does not use any identification for its main tests. It asks what the text itself shows: which words each entry uses, in which order, and how that changes along the list.

**Data.**
- The Hebrew text is the ETCBC/Abegg transcription in the repo (`web/scroll-text.js`, CC BY-NC 4.0). The entry boundaries come from `tables/entry_concordance.csv`.
- I corrected one boundary: entry 3 starts inside line I 6 (Puech p. 179).
- Every direction word, dig depth and sum was checked by eye against the Hebrew.
- The per-entry features are in `entry_features_2026-09-30.csv`. The scripts are in `deeper_analysis_code_2026-09-30.zip`.

**Blocks.** Blocks are set by position only, and were fixed by the anchor model (R1) before these tests:
- **A:** entries 1–19, the first sub-list. It contains the Greek-letter entries 1–15.
- **B:** entries 20–35, the Jericho–desert block.
- **C:** entries 36–56, Jerusalem and its hinterland.
- **D:** entries 57–60.

---

## 0. Summary

| # | Result | Strength |
|---|---|---|
| 1 | **The list is ordered in two different ways.** From entry 20 on, entries that name the same place stand together: 5 adjacent pairs, where chance gives 0.45 (exact p = 3.6 × 10⁻⁶). In 1–19 the same names are scattered (Koḥlit 4, 11, 15, 19; ha-Melaḥ 6, 13, 14; Achor 1, 17): 1 adjacent pair, where chance gives 1.0. | Strong. Uses no identification |
| 2 | **In 1–19, "north" occurs only in Koḥlit and ha-Melaḥ entries** (6 of those 7 entries, 0 of the other 13; p ≈ 2 × 10⁻⁴). The gate, wall and court entries use only east and south. All five Koḥlit entries in the scroll say "north" (p ≈ 1 × 10⁻⁴). | Strong effect, found after looking at the data |
| 3 | **ha-Melaḥ follows the Koḥlit pattern, not the Temple-like entries.** This weighs modestly against Milik's and Puech's "Esplanade" at III 8 and III 11. It weighs for a named place in the Jericho district. | Inference, moderate |
| 4 | **The first sub-list has its own vocabulary and style.** "Court" occurs only there. Six of the nine entries with a cistern (בור) are there. Seven of its 13 sums are multiples of ten; in 20–56 there are 4 of 26. Few of its entries say "dig". | Moderate. Some counts found after looking |
| 5 | **Vocabulary, orientation and dig depth change between the blocks, but gradually.** Shifted block positions test them against local drift (rotation test): p ≈ 0.03, 0.03 and 0.06. "West" gathers in the Jerusalem-city entries. The Kidron tomb façades face west (checked). | Moderate |
| 6 | **The Greek-letter groups do not mark a change in any feature** (p = 0.39). The prediction in the follow-up (§2) fails. | Negative result |
| 7 | **The phrase כתבן אצלם ("their record beside them") always comes right after "vessels of offering"** (5 of 5; p ≈ 4 × 10⁻⁵, whichever way the entries are divided). Four of the five are at entries 50–55, near the Temple. This favours reading the phrase as part of the offering entry (Puech, Lefkovits) rather than the start of the next one (Milik); see Q5. | Moderate |
| 8 | **The order cannot place Koḥlit inside the Jericho district.** It cannot choose between the Jericho oasis and Qumran–Buqeia. It fits Achor = Buqeia slightly better, with a likelihood ratio of about 2–6. | Weak. Narrows R3 |

**Synthesis (inference).** The first sub-list interleaves two groups of entries:
- named places in the Jericho district, described from a north frame;
- unnamed built features described with Temple vocabulary and an east/south frame.

The first sub-list also differs from the rest in five ways (§3.1):
- three found here: the order, the vocabulary and the round sums;
- two already in the project: the late start of "dig", and the full spelling ככרין.

Entries 1–19 probably come from a different source list than entries 20–60. That is the project's H8 ("a separate sub-list", rated "partly supported"), which now rests on five markers instead of two. §3 gives predictions you can test on site plans.

---

## 1. Two ways of ordering the list (T1, evidence)

**Test.** In each sub-list I counted adjacent pairs of entries that share a place name. I compared the count with 200,000 random orders of the same entries.

| Sub-list | Entries | Same-name pairs | Adjacent pairs, observed | Expected by chance | p |
|---|---|---|---|---|---|
| 1–19 (with 12a) | 20 | 10 | **1** (13–14, ha-Melaḥ) | 1.0 | P(≥1) = 0.68; P(≤1) = 0.74 |
| 20–59 | 40 | 9 | **5** (20–21, 21–22, 22–23, 36–37, 51–52) | 0.45 | **3.6 × 10⁻⁶** (exact; 200,000 shuffles gave 1 hit) |

- **Sensitivity.** With Puech's permitted "Shallum" at 23 there are 4 adjacent pairs; chance gives 0.40 (p ≈ 9 × 10⁻⁵). With Milik's reading of 15 (no Koḥlit), 1–19 still has 1 adjacent pair.
- **Inference (high).** From entry 20 on, the compiler wrote all the entries for one named place together. In 1–19 he returned to Koḥlit four times and to ha-Melaḥ three times, between other entries. By place names, the first sub-list is no more grouped than a random order.
- **What is new.** Puech (pp. 173–174) saw that the two groups differ. This test measures the difference and shows its kind: the first group is not ordered by place at all.
- **Why this matters.** The sequence model (R1–R3) assumes that neighbours are near each other. For 1–19 that assumption is weak. The model's probabilities for entries 2–16 (0.87–1.00 in the Jericho district) should be read as "between two Achor entries", not as positions on a route.

## 2. Orientation words (T2)

Counts of entries with each direction word (evidence; ים "sea" is counted as west only at IX 7, entry 40):

| Block | Entries | East | North | South | West |
|---|---|---|---|---|---|
| A (1–19) | 20 | 7 | 6 | 1 | 1 |
| B (20–35) | 16 | 5 | 3 | 0 | 1 |
| C (36–56) | 21 | 2 | 2 | 3 | 6 |
| D (57–60) | 4 | 0 | 1 | 0 | 0 |

### 2.1 The north frame of Koḥlit and ha-Melaḥ (evidence; found after looking at the data)

| Entry | Place | Direction words |
|---|---|---|
| 4 | Koḥlit (mound) | "at the edge of the conduit, **on the north**" |
| 11 | Koḥlit | "the pool east of Koḥlit, in the **northern** corner" |
| 13 | ha-Melaḥ | "the pit in ha-Melaḥ, on its **north** side … under the western corner" |
| 14 | ha-Melaḥ | "the tomb in ha-Melaḥ, on its east side, on its **north** side" |
| 15 | Koḥlit (restored by Puech) | "the pillar on its **north** side" |
| 19 | Koḥlit | "the eastern pit **north of** Koḥlit" |
| 60 | Koḥlit | "the pit on the **north** side of Koḥlit" (the plates show a clear בצפון) |
| 6 | ha-Melaḥ | no direction |
| 9, 10, 12, 12a | unnamed gate, wall, court | east (East Gate; "under the wall, on the east"; "the other corner, the eastern one"), south ("the south corner"). **No north** |

- **Inside 1–19.** North occurs in 6 of the 7 Koḥlit and ha-Melaḥ entries, and in 0 of the other 13 entries. Fisher p = 1.8 × 10⁻⁴.
  - Taking only entries that have some direction word: 6 of 6 against 0 of 5, p = 0.0022.
  - With Milik's reading of 15 (no Koḥlit): 5 of 6 against 1 of 14, p = 0.0022.
- **Across the scroll.** All five Koḥlit entries say north, while 12 of the 61 entries do. Hypergeometric p = 1.3 × 10⁻⁴.
- **Inference (medium).** The Koḥlit and ha-Melaḥ entries were written from one spatial frame, and the gate, wall and court entries from another. Two explanations:
  - (a) the two groups are in different places;
  - (b) they are different parts of one complex.
- **Consequence for ha-Melaḥ (inference, moderate).**
  - ha-Melaḥ uses the Koḥlit frame and is written like a place name: "the pit **that is in** ha-Melaḥ", "the tomb **that is in** ha-Melaḥ".
  - This favours a named place in the Jericho district over the Temple Esplanade of Milik (DJD pp. 272–274) and Puech 2006 (p. 184).
  - It does not decide which place. Candidates in the City of Salt tradition are Kh. Qumran (Noth; Cross & Milik 1956) and ʿAin el-Ghuweir (Bar-Adon; Puech p. 176 n. 62).
  - Kh. Qumran conflicts with Secacah = Qumran (Puech; the project's anchors 21–22). Milik's own view makes Secacah the whole Wadi Qumran (ADAJ p. 146), which lessens the conflict but does not remove it.
- **Consequence for Koḥlit (spatial inference).** Any candidate for Koḥlit must have its conduit, cistern, pits and tombs on the north side of the reference landmark. For Puech's Tell es-Sultan:
  - The frame points **north** of the tell. There the project already records a cemetery north and west of the tell, with tombs down to the Roman period (Sala 2014 p. 117, via `phase5_summary.md`). That fits "tombs at its mouth" (60) and "north of Koḥlit" (19, 60).
  - It points away from the Hasmonean–Herodian palaces **south** of the tell. So the palaces' pools and aqueducts should not be counted as support for the Koḥlit entries. Phase 5 already keeps them apart.
  - Entry 11, "the pool **east** of Koḥlit", fits the spring at the tell's east foot. The reservoir there is undated (`readings.json`, e11).

### 2.2 East and west: a gradual change, not a switch at the district boundary

- **Tests (evidence).** The counts are entries that have east and not west, against entries that have west and not east.

  | Comparison | East : west | p |
  |---|---|---|
  | Anchored blocks, B (20–35) against C (36–56) | 5 : 1 against 2 : 6 | Fisher 0.051 |
  | A and B together, against C | 12 : 2 against 2 : 6 | 0.0083 |
  | Aspect words only ("facing X", "entrance from X") | 3 : 0 against 1 : 4 | 0.071 |
- **Where the change is.** Tried against every split of entries 20–56, the anchor boundary 35|36 ranks only 8th of 26. The largest contrast is at splits between 42 and 47. The west words are 36, 40, 47, 48, 52 and 56, most of them in the Jerusalem-city entries.
- **Rotation test** (the same block sizes, shifted along the scroll; this keeps local runs intact): the actual blocks rank 2nd of 61 (p ≈ 0.03).
- **Physical reading (inference).** The Kidron tombs are cut in the valley's east escarpment and face west, towards the Temple Mount (evidence):
  - Benei Ḥezir: façade "oriented roughly west-southwest" ([Wikipedia](https://en.wikipedia.org/wiki/Tomb_of_Benei_Hezir));
  - Zechariah: the decorated façade is "only the western side" ([Wikipedia](https://en.wikipedia.org/wiki/Tomb_of_Zechariah));
  - Yad Avshalom: "on the eastern side of Kidron valley", "facing the old city" ([BibleWalks](https://www.biblewalks.com/avshalomtomb/)).

  So "on the west side" of Absalom's monument (48) fits the façade side of the Kidron monument. "The top of the rock facing west" (52) and the Shaveh "facing west" (36) fit the Kidron's east slope.
- **Two open questions this bears on (weak).**
  - Q22: the Shaveh is the King's Valley (Puech p. 194 n. 304; Høgenhaven p. 77, who takes it as the Kidron) rather than Milik's Baqʿa plain. "Facing west" is odd for a plain.
  - Q18: Absalom's monument is in the Kidron rather than in the south-west necropolis.
- **Caveat.** Puech reads "facing **south**" (דרום) at IX 7 (entry 40), where the plates lean to ים (`readings.json`, e40). This moves one count.

## 3. What the first sub-list is (synthesis; inference)

**3.1 Five ways in which entries 1–19 differ from the rest (evidence; court and cistern count as one marker, vocabulary).**

| Marker | 1–19 | Later entries | Test |
|---|---|---|---|
| Entries for the same place stand together | no (1 of 10 pairs) | yes (5 of 9, in 20–59) | §1 |
| "Court" (חצר) | 3 entries (3, 8, 12) | 0 | — |
| Cistern (בור) | 6 of the 9 entries that have it | 3 (45, 56, 59) | vocabulary: A against B p = 0.0005; A against C p = 0.008 |
| Sums that are multiples of ten | 7 of 13 (900, 200, 70, 70, 40, 40, 10) | 4 of 26 in 20–56 (5 of 29 with 57–59) | Fisher p = 0.017 against 20–56 (found after looking) |
| Entries that say "dig" | 5 of 20 | 21 of 37 in 20–56 | — (known: חפור starts at II 14; project T8) |
| Full spelling ככרין | 7 of the first 16 | 4 of the 45 later entries | project T8 |

**3.2 Two groups inside 1–19.**

| Group | Entries | Frame | Content markers |
|---|---|---|---|
| (i) Named places in the Jericho district | 1, 17 (Achor); 4, 11, 15, 19 (Koḥlit); 6, 13, 14 (ha-Melaḥ); 18 (ʿAṣla) | north (and east) | tithe and seventh-year produce at the Koḥlit mound (4) |
| (ii) Unnamed built features | 8, 9, 10, 12, 12a (probably 3 and 5) | east and south | see the list below |
| Not assigned | 2 (monument), 7 (cave), 16 (conduit) | — | — |

Content markers of group (ii):
- the East Gate (9);
- the wall and the "great threshold" (10);
- courts (3, 8, 12);
- the מסבה of Middot (5, Puech);
- in entry 12, a vessel set in the vocabulary of the Temple lists. It has מזרקות, מנקיות and קשות (קסאות in the scroll), as in Exod 25:29 (the libation vessels of the table) and Jer 52:19 (the gold and silver vessels taken from the Temple) (evidence: [Sefaria Exod 25:29](https://www.sefaria.org/Exodus.25.29), [Jer 52:18–19](https://www.sefaria.org/Jeremiah.52.18-19)).

"The great cistern" is also a Temple name: m. Eruvin 10:14, "from the Cistern of the Exiles and from the Great Cistern (הבור הגדול)" ([Sefaria](https://www.sefaria.org/Mishnah_Eruvin.10.14)). It is not specific, though: entry 15 has "the great cistern that is in Koḥlit".

**3.3 Reading.** The groups come in runs, not in strict alternation: 8–12a are mostly group (ii), and 13–19 are group (i). The Greek letters do not follow the runs (§5). The best current reading is the follow-up's explanation (a), sharpened:
- entries 1–19 come from a separate list;
- that list mixed deposits in the Jericho district (Achor, Koḥlit, ha-Melaḥ) with deposits in a walled precinct with courts and an East Gate, most probably the Temple;
- the regional register starts at entry 20.

Explanation (b), a single built complex in the Jericho district with gates and courts, is not excluded by the text. It is less likely given the Temple vessel set and the East Gate.

**3.4 Predictions you can test on published plans.**
- **P1 (ha-Melaḥ as a place in the Jericho district).** A site should have:
  - a cistern under steps (6);
  - a pit on its north side, whose entrance is under a western corner (13);
  - a tomb on its east side, in its north part (14).

  Check Kh. Qumran first. Its main cemetery lies east of the settlement, and a small north cemetery lies "ten minutes' walk north" of it ([Wikipedia: Qumran cemetery](https://en.wikipedia.org/wiki/Qumran_cemetery)). Check ʿAin el-Ghuweir second (Bar-Adon 1977).
- **P2 (Koḥlit = Tell es-Sultan).** North of the tell there should be:
  - a conduit at the north edge of the mound (4);
  - pits (19, 60), with tombs at the mouth of one of them (60);
  - a great cistern with a pillar on its north side (15).

  Check PEF Sheet XVIII (already in the project), the Sellin–Watzinger and Kenyon plans, and Sala 2014 for the line of the northern cemetery and of the ʿAin Duk / Naʿaran aqueducts.
- **P3 (Kidron).** The "chamber facing north" of 36 should be on a west-facing slope. The Silwan / Mount of Olives tomb surveys can test this.

## 4. Dig depths (T3)

| Block | Digs | Mean (cubits) | Median |
|---|---|---|---|
| A (1–19) | 5 | 7.0 | 4 |
| B (20–35) | 13 | 6.4 | 6 |
| C (36–56) | 8 | 11.9 | 10.5 |

- **Tests (evidence).**
  - C against B: Mann–Whitney U = 83.5 of 104, so a C dig is deeper than a B dig 80% of the time. Two-sided permutation p = 0.020.
  - Depth against position in the scroll: Spearman ρ = 0.42, p = 0.031 (n = 26).
  - 35|36 is not a special split: rank 5 of 15. Rotation test: rank 3 of 52 (p ≈ 0.06).
- **Confound (evidence).** Four of the eight digs in C are in a "chamber" (צריח): 24, 11, 8.5 and 16 cubits. Such chambers occur almost only in C.
- **Inference (low).** The deep digs are "go down in a chamber or shaft", not holes dug in soil. The depth trend follows the kind of landmark, not the district as such.
- **Physical check (evidence).** The graves at the Qumran cemetery are 0.8–2.5 m deep (Wikipedia, above). "Dig three" in entry 14 (about 1.3–1.5 m) falls in that range. But 3 cubits is the commonest depth in the scroll, so it does not discriminate.

## 5. Tests that failed or are weak

1. **The Greek-letter groups (T5, negative).**
   - Method: entries 1–16 have 16 gaps. The letters close entries 1, 4, 6, 7, 9, 12a and 15, so they mark 7 of the gaps. I measured how far the features change across each gap (named place, north, dig, ככרין, a sum, gold, built-feature words, landmark words).
   - Result: the change at the lettered gaps is no larger than at the others. Exact p = 0.39 over 11,440 placements. No single feature is enriched at the lettered gaps (all P ≥ 0.29).
   - The follow-up's prediction (§2) fails: the letters do not close groups that share place, formula or treasure. This agrees with the project's H7 (end-of-entry markers) and H14 (no system found).
2. **Can the vocabulary tell where 1–19 belongs?** A Bernoulli naive Bayes classifier over 22 landmark concepts, trained on B against C, classifies 25 of 37 correctly by leave-one-out. A label-permutation test gives p = 0.061. That is too weak to classify 1–19. Most entries in 1–19 lean slightly towards C, because cisterns and pits occur in C and not in B. Courts occur in neither.
3. **Sharp vocabulary breaks.** A sliding-window scan finds no sharp break at 19|20, 35|36 or 56|57 (pointwise p = 0.15–0.65). The strongest local change is at 45|46 (pointwise p ≈ 0.002; p ≈ 0.10 for the whole scan). The blocks differ in vocabulary taken as wholes (rotation p ≈ 0.03), but the change is gradual.
4. **Walking route in the Jerusalem block (T7, weak).** Exact enumeration of all orders:

   | Stops | Scroll order | Median of all orders | Best order | p (walking) | p (km) |
   |---|---|---|---|---|---|
   | Strict anchors: 46, 48, 51, 52, 55 | 1.91 h | 2.86 h | 1.66 h | 0.33 | 0.17 |
   | With Naṭuf (38) and Siloam (49) | 5.84 h | 10.37 h | 5.16 h | 0.044 | 0.037 |
   | Jericho block (for comparison) | — | — | — | 0.16 | 0.15 |

   The Jerusalem block reads a little more like a route, south to north: Naṭuf → Ramat Raḥel → the Kidron → the city's east side → Bethesda. The evidence is weak and rests on two non-strict anchors.

## 6. The phrase כתבן אצלם (T6)

**The reading is disputed** (`readings.json`, g-ktbn; Q5):
- Puech 2006 reads ובתכן / בתכן (p. 189 n. 226).
- Milik 1960 translates "and near there", and he makes the phrase begin the next item. Pixner, García Martínez, Vermes and Lange follow him.
- Pfann reads "their accounts with them".
- Puech and Lefkovits end the entry with the phrase.
- The text shown, with כ, says "their record beside them".

**Evidence.**
- The full phrase occurs 5 times: V 7, XI 1, XI 4, XI 11 and XI 15 (entries 22, 50, 51, 54 and 55 on Puech's division). Entry 8 has only the bare word וכתבן, after "wood".
- **Each of the five comes right after "vessels of offering"** (כלי דמע, sometimes with a number). Entries 22, 50, 51, 54 and 55 all have this order.
- דמע occurs in 10 entries, so the chance that all five fall after it is C(10,5)/C(61,5) ≈ **4 × 10⁻⁵**.
- The order of the words does not depend on where the entry boundary is drawn. On Milik's division, a count by entries instead gives 2 of 6: the independent check flagged this, and it is why I count adjacency, not entries.
- Four of the five occurrences lie in the six entries 50–55: the upper pool, the south-east corner portico with the tomb of Zadok, the tomb of the common people, and Bethesda. Scan p = 0.005.

**Inference (medium).**
- The phrase belongs to the offering vessels. This favours the division of Puech and Lefkovits (the phrase ends the entry) over Milik's (it opens the next), and it fits Pfann's sense. If the phrase opened the next item, its link with offering vessels, and not with any other treasure, would be a coincidence.
- This bears on **Q5**. It does not settle the letter, כ or ב.
- On the כ reading, consecrated vessels were deposited with their own written record, most of them close to the Temple. That fits an evacuation of Temple property. It does not prove that the treasure was real (Weitzman's "both at the same time" reading: *HTR* 108 (2015) 423–447).

## 7. The finer sequence model (T8)

- **Model.** Three sub-districts: Jericho oasis, Qumran–Buqeia, and the desert or Kidron gorge.
- **Anchors.** 20–22 in Qumran–Buqeia; 31 and 32 in the Jericho oasis; 35 in the desert. Kuteif (24) is left out because it lies between the two sub-districts.

| Achor | Fitted stickiness s | Koḥlit 4 / 15 / 19 in Achor's sub-district | ha-Melaḥ 6 / 13 / 14 in Achor's sub-district |
|---|---|---|---|
| Wadi Nuweiʿimeh (Jericho oasis) | 0.73 | 0.47 / 0.56 / 0.29 (19 leans to Qumran–Buqeia, 0.60) | 0.38 / 0.41 / 0.47 |
| Buqeia | 0.86 | 0.67 / 0.76 / 0.97 | 0.57 / 0.61 / 0.67 |

- **Likelihood ratio, Buqeia against Nuweiʿimeh:** 2.6 (s = 0.8), 5.8 (s = 0.9), 12 (s = 0.95). With each variant at its own fitted s, about 2.4.
- **Inference.**
  - R3 stands only at district level: Koḥlit is in the Jericho district.
  - Inside the district, the order cannot choose between Tell es-Sultan and a place in Qumran–Buqeia.
  - The order fits Achor in the Buqeia slightly better: Allegro; Eshel; the Iron Age identification of Noth, Cross and Milik. This agrees with the weak route result in the follow-up (p = 0.044). The evidence is anecdotal and does not overturn Milik's and Puech's late-tradition Achor.

## 8. Corrections to the earlier reports

1. **Follow-up §2 table.** Entries 2 and 14 should read **"Neither"**, not "Jericho":
   - The funerary monument of 2 could be a Kidron monument.
   - Puech's French puts the tomb of 14 **east of** the Esplanade, which is plausible in the Kidron. My "tomb at the Temple is implausible" argued against a reading that nobody holds.
   - Revised tally:
     - Jericho: **7** (4; 7, weak; 11; 15; 16, weak; 19; and 17, which is anchored);
     - Temple: **4** (5, weak; 8; 9; 10, weak);
     - Neither: **7** (2, 3, 6, 12, 12a, 13, 14).

   The follow-up file now carries this correction. §2.1 above adds a separate argument (the north frame) that moves 6, 13 and 14 towards the Koḥlit side. It is not a location score.
2. **R3** is narrowed as in §7.
3. **The depositor-group prediction** in the follow-up is withdrawn (§5.1).
4. **East and west, and dig depth,** are gradual trends along the list, not switches at the district boundary.
5. **The priority of the ha-Melaḥ = City of Salt combination** is still unverified. The follow-up §4.2 lists the sources to check.

## 9. New since the last report (not read)

- **S. Gibson, "What was the purpose of the Copper Scroll found in Cave 3Q at Qumran?"**, *Eretz-Israel* 36 (2025/2026), pp. 32*–48*.
  - What the news reports say:
    - The scroll is a ledger of contributions or assets for the Bar Kokhba revolt. The language is "early Mishnaic Hebrew, characteristic of the mid-to-late second century CE".
    - Joan Taylor re-examined Cave 3Q with Gibson.
    - The document kept at Koḥlit may have held the donors' names.
    - One report quotes entry 2 as "Ben Rabbah, of Beit Shalisha: 100 ingots of gold". That would be a personal name where the editions read בנפש בנדבך השלשי ("in the funerary monument, in the third course"). It may be Gibson's reading, or the reporter may have garbled it. Check it in the article.
  - Sources: [Arkeonews, 1 June 2026](https://arkeonews.net/mysterious-dead-sea-copper-scroll-may-hide-the-financial-secrets-of-a-failed-jewish-revolt/); [Israel365, 17 May 2026](https://israel365news.com/418175/the-copper-scrolls-hidden-secret-was-it-bar-kochbas-war-chest/).
  - **I have not read the article.** If the entry-2 reading is right, it matters for §3: a personal name in 1–19 would support a list of persons. A second-century date also matters for Milik's dating argument for "Solomon's reservoir" (Q37).
- *Haaretz*, "The Mysterious Copper Scroll and the End of Days" (7 May 2026): the fetch was refused (robots.txt). Not read.

## 10. Background checks made for this report (evidence)

- **b. Qiddushin 66a**: "שהלך לכוחלית שבמדבר וכיבש שם ששים כרכים", "went to Koḥlit **in the wilderness** and conquered sixty towns there" ([Sefaria](https://www.sefaria.org/Kiddushin.66a)).
  - The project records this as the only attestation outside the scroll. It gives a region ("in the wilderness"), not a place.
  - [Wikipedia](https://en.wikipedia.org/wiki/Kohlit) calls it "an area east of the Jordan River". That is an interpretation, not the text.
- **Cave 3Q** lies "about two kilometers north of Qumran" ([Encyclopedia.com](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/copper-scroll)).
- **Qumran cemeteries.**
  - The main cemetery is east of the site.
  - Small cemeteries lie to the north ("ten minutes' walk") and to the south (across Wadi Qumran).
  - The graves are 0.8–2.5 m deep, most with the head to the south.
  - Source: [Wikipedia](https://en.wikipedia.org/wiki/Qumran_cemetery).
- **The Kidron tomb façades** face west (§2.2).

## 11. All tests, with a correction for testing many things

The Holm correction is applied across the 16 tests below. "Found after looking" means that I saw the pattern while reading the table, before I tested it.

| Test | p | Holm-adjusted | How the test arose |
|---|---|---|---|
| Names grouped in 20–59 (T1) | 3.6 × 10⁻⁶ | 6 × 10⁻⁵ | Planned (idea from the earlier session) |
| כתבן אצלם always right after offering vessels (T6) | 4 × 10⁻⁵ | 6 × 10⁻⁴ | Found after looking |
| All Koḥlit entries say north (T2e) | 1.3 × 10⁻⁴ | 0.002 | Planned (noticed earlier) |
| North only in Koḥlit and ha-Melaḥ entries, 1–19 (T2d) | 1.8 × 10⁻⁴ | 0.0024 | Found after looking. Overlaps with T2e |
| Vocabulary, 1–19 against 20–35 (T4) | 5 × 10⁻⁴ | 0.006 | Planned |
| The phrase clusters at 50–55 (scan) | 0.005 | 0.055 | Found after looking |
| Vocabulary, 1–19 against 36–56 | 0.0077 | 0.076 | Planned |
| East and west, 1–35 against 36–56 (T2b) | 0.0083 | 0.076 | Found after looking |
| Vocabulary, 20–35 against 36–56 | 0.015 | 0.12 | Planned |
| Depth, 20–35 against 36–56 (T3) | 0.020 | 0.14 | Planned |
| Jerusalem route, lenient stops (T7) | 0.044 | 0.26 | Planned |
| East and west, 20–35 against 36–56 (T2a) | 0.051 | 0.26 | Found after looking |
| Vocabulary classifier, leave-one-out (T4b) | 0.061 | 0.26 | Planned |
| Aspect words only (T2c) | 0.071 | 0.26 | Found after looking |
| Jerusalem route, strict stops | 0.33 | 0.67 | Planned |
| Greek-letter gaps (T5) | 0.39 | 0.67 | Planned (the follow-up's prediction) |

The round-sums count in §3.1 (p = 0.017, found after looking) is not in the table. Adding it would not change which tests survive.

**The tests that survive the correction:** the two ways of ordering (§1), the north frame (§2.1), the place of כתבן אצלם after offering vessels (§6), and the separate vocabulary of the first sub-list.

**Independent check.** A separate agent recomputed the counts from the raw repo files (`scroll-text.js`, the concordance and the translation) with its own code, without my scripts. It reproduced:
- every direction count in §2;
- the Fisher and hypergeometric values in §2.1;
- the depths, means, medians and U in §4 (its exact one-sided p is 0.010; without the corrupt entry 38 it is 0.0075);
- the court and cistern counts;
- all the name pairs in §1, where it found every listed name in the Hebrew of its entry.

It flagged two traps. First, a search that ignores the final nun loses "north" in 13 and 15. Second, the entry-level count for כתבן depends on the division. Both are handled above.

## 12. What this analysis does NOT show

- It identifies no site. The spatial statements in §2.1, §2.2 and §3.4 are hypotheses to test on plans.
- Several patterns were found by looking at the data. Their p-values describe; they do not confirm. The north frame and the record formula are large effects, but only a second, independent text could confirm them, and none exists.
- The vocabulary cannot decide whether entries 1–19 are at Jericho or in Jerusalem (§5.2).
- **Text base.** The text is the Abegg/ETCBC transcription with the project's concordance. It differs from Puech in some places:
  - the sums at II 2, III 13 and VIII 13;
  - Shallum at 23;
  - Koḥlit restored at 15;
  - דרום against ים at IX 7.

  Sensitivity was checked for 15 and 23. The reading at IX 7 moves one east/west count.
- The sense "their record" in §6 depends on reading כ (the text shown; Pfann) rather than ב (Puech). The adjacency result holds for both readings.
- The route and sequence results depend on the Phase 3 coordinates and on the choice of anchors.
- The Gibson article and the *Haaretz* piece were not read (§9).

## 13. Next checks, in order of value

1. **P2, Koḥlit = Tell es-Sultan, on the north side.** Use PEF Sheet XVIII and the tell plans to look for a conduit at the tell's north edge, pits to the north, and the line of the northern cemetery (Sala 2014). This tests the north frame directly.
2. **P1, ha-Melaḥ as a place.** On the Humbert–Chambon plan of Kh. Qumran and in the cemetery reports, look for a stepped cistern (6), a pit on the north side entered under a western corner (13), and tombs on the east side, in its north part (14). Repeat for ʿAin el-Ghuweir.
3. **Read Gibson 2025/26 (*Eretz-Israel* 36).** In particular, his reading of entry 2 and his date.
4. **Priority check** for ha-Melaḥ as a place in the Jericho district: *Copper Scroll Studies* (2002), Høgenhaven 2020, Lurie, and Allegro 1960.
5. **The lexicon row `millo`:** search the salt sense (מלח) in the Bible and the Mishnah as a place-name element. The row records that this was not done.
6. **Q5 on the plates:** is it כ or ב in כתבן / בתכן at V 7 and XI 1, 4, 11 and 15? §6 supports Puech's division; only the plates can decide the letter, and so the sense "record".

## Sources

- Repo files: `web/scroll-text.js` (ETCBC dss 2.0.1; Abegg, Bowley and Cook; CC BY-NC 4.0); `tables/entry_concordance.csv`; `tables/phase3_places.csv`; `tables/phase3_site_index.csv`; `tables/landmark_lexicon_index.csv`; `text/readings.json`; `phase5_summary.md`; `findings_log.md`.
- [Sefaria: Kiddushin 66a](https://www.sefaria.org/Kiddushin.66a) · [Mishnah Eruvin 10:14](https://www.sefaria.org/Mishnah_Eruvin.10.14) · [Exodus 25:29](https://www.sefaria.org/Exodus.25.29) · [Jeremiah 52:18–19](https://www.sefaria.org/Jeremiah.52.18-19)
- [Wikipedia: Tomb of Benei Hezir](https://en.wikipedia.org/wiki/Tomb_of_Benei_Hezir) · [Tomb of Zechariah](https://en.wikipedia.org/wiki/Tomb_of_Zechariah) · [Qumran cemetery](https://en.wikipedia.org/wiki/Qumran_cemetery) · [Kohlit](https://en.wikipedia.org/wiki/Kohlit) · [BibleWalks: Yad Avshalom](https://www.biblewalks.com/avshalomtomb/)
- [Encyclopedia.com: Copper Scroll](https://www.encyclopedia.com/religion/encyclopedias-almanacs-transcripts-and-maps/copper-scroll)
- [Arkeonews, 1 June 2026](https://arkeonews.net/mysterious-dead-sea-copper-scroll-may-hide-the-financial-secrets-of-a-failed-jewish-revolt/) · [Israel365, 17 May 2026](https://israel365news.com/418175/the-copper-scrolls-hidden-secret-was-it-bar-kochbas-war-chest/) · [Weitzman, *HTR* 108 (2015)](https://www.cambridge.org/core/journals/harvard-theological-review/article/abs/absent-but-accounted-for-a-new-approach-to-the-copper-scroll/23B38B91A21568F575D5F7F6D2DC5AD4)
