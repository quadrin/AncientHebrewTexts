# The scroll's own order as evidence: a sequence model, and the leads it opens

> **Superseded in part.** See [sequence_model_followup_2026-09-30.md](sequence_model_followup_2026-09-30.md) §0:
> - Puech 2006 pp. 173–174 already describes the regional order (R1 measures it).
> - The "salt" reading and the City of Salt comparison go back to Allegro, Lurie and Lefkovits (§4 is narrowed to the combined Qumran proposal).
> - The walking-route idea in §6.4 was tested and is negative.

30 September 2026. This is a new analysis of the existing project data. It uses no new sources, except background knowledge (BK), which is marked. Inputs:
- `text/translation_en.json`;
- `tables/entry_concordance.csv`;
- `tables/phase3_site_index.csv`;
- `tables/phase3_places.csv`.

Code: [`tools/sequence_model.py`](tools/sequence_model.py). Input: [`registration/sequence_model_entries.json`](registration/sequence_model_entries.json). Output: [`registration/sequence_model_results.json`](registration/sequence_model_results.json). Labels follow the project's convention: evidence / inference / BK.

## 1. Why

Every placement in the project uses the order of the entries ("sequence fit"), but the argument has never been measured. It is also partly circular: Phase 3 used sequence fit to choose places, and those places now appear to confirm the sequence.

This analysis measures the order using only **anchors**. An anchor is an entry whose place name is located by a source outside the scroll. Everything else is inferred from the order alone.

## 2. Method

- **Regions.** Four regions:
  - O: Jericho, Qumran and the lower Jordan;
  - D: the interior of the Judean desert (Kidron canyon, Hyrcania, Buqeia);
  - J: Jerusalem and its southern hinterland;
  - N: the north (Gerizim, Beth Shean).
- **Model.** A hidden Markov chain over the 61 entries in scroll order.
  - At each step the list either stays in its region (probability *s*, fitted by maximum likelihood) or moves to another region.
  - Anchors fix the region of their entry. All other entries are unobserved.
  - Forward–backward gives each unanchored entry a probability for each region.
- **Strict anchors (18).**

| Entry | Name in the text | Region | Located by |
|---|---|---|---|
| 1 | Valley of Achor | O | Onomasticon, "north of Jericho" (F2.2) |
| 17 | Valley of Achor | O | Onomasticon, "north of Jericho" (F2.2) |
| 20, 21, 22 | Secacah | O | Josh 15:61, the wilderness district |
| 24 | "on the way from Jericho to Secacah" | O | The text names Jericho |
| 31 | Doq | O | 1 Macc 16:15 |
| 32 | Kozeba | O | Wadi Qelt at Choziba |
| 35 | Mouth of the Kidron gorge | D | The Kidron |
| 36, 37 | Shaveh | J | Gen 14:17 |
| 46 | Beth ha-Kerem | J | Jer 6:1 |
| 48 | Absalom's monument | J | 2 Sam 18:18 |
| 51, 52 | Zadok, the portico | J | The portico is the Temple's |
| 55 | House of the Two Reservoirs | J | Twin pools in Jerusalem |
| 57 | Gerizim | N | The mountain |
| 58 | Beth Sham | N | Beth Shean |

- **Excluded from the anchors on purpose:**
  - Siloam (49), which depends on a disputed reading;
  - the East Gate (9–10), which has no toponym and is exactly the point being tested;
  - Koḥlit, Naṭuf, Ḥoron, ʿAṣla and Beth Tamar, whose locations are unknown or disputed.
- **Sensitivity runs:**
  - Achor and Secacah placed in the Buqeia (D) instead;
  - a lenient set, adding Siloam (J), the East Gate (J) and Aḥor (O).

## 3. Results

### R1. The list is in strict regional order. (test)

- **The numbers.** The 18 anchors change region only **3 times**. The sequence runs O ×8 → D → J ×7 → N ×2.
  - A permutation test gives **p ≈ 5 × 10⁻⁶**. With the Buqeia variant p ≈ 1 × 10⁻⁵; with the lenient set p ≈ 4 × 10⁻⁵.
  - The fitted probability of staying in the same region is s = 0.935, so the list changes region about once every 15 entries.
- **Leave-one-out.** Hiding each anchor in turn, the order alone recovers its region for **16 of 18**. The two misses are:
  - 35, the Kidron, a lone D entry between the blocks;
  - 55, Bethesda, the last Jerusalem entry before the northern ones.
- **Inference (high).** The list reads as blocks:
  - Jericho–Qumran (1–32);
  - a turn at 33–35;
  - Jerusalem and its southern hinterland (36–56);
  - the north (57–59);
  - then 60, which names Koḥlit again.

  The order is real evidence, and it is strong enough to use quantitatively, not only as a tie-breaker.

### R2. Entries 2–19 conflict with the scroll's own order. (test)

- **What the order predicts.** From order alone, every unanchored entry from 2 to 19 falls in the Jericho block, with probability 0.87–1.00. They lie between Achor (1) and Achor (17), before Secacah (20–22).
- **What Phase 3 has.** It alternates between regions: Achor (O), the Temple (J), Koḥlit (O), the Temple, Koḥlit, the Temple, Koḥlit. That is **6 region changes in 19 steps**.
- **How unlikely that is.** At the switching rate of the rest of the scroll, that many changes has probability **≈ 0.001**. On the lenient fit it is 0.017.
- **Two explanations, each testable:**
  - **(a) The first sub-list was compiled differently.** Columns I–IV are also the columns that carry all seven Greek-letter groups and a different set of formulae (F4.8, H8). Either they interleave two places, or they were copied from a different kind of source. *Prediction:* no other stretch of the scroll alternates like this.
  - **(b) The Temple placements are wrong, and 2–19 describe the Jericho complex.**
    - The words that pulled these entries to Jerusalem are "the court of the peristyle" (3), "the East Gate" (9), "the wall" and "the great threshold" (10), and the court names of 8 and 12 (restored or emended).
    - Those words describe the Hasmonean–Herodian palace estate at Jericho just as well. BK: Netzer's reports have peristyle courts, large pools, many miqva'ot and gates there.
    - Only "peristyle" is securely read (phase5_assessments, JER block).
    - Koḥlit (4, 11, 15, 19) sits inside the stretch. If Koḥlit is Tell es-Sultan, "the pool that is east of Koḥlit" (11) matches the spring pool of ʿAin es-Sultan at the tell's east foot (SWP III pp. 222–223, already in `phase5_reports.csv`).
  - *Consequence of (b) for Phase 4.* Test T5 found no link between the Greek letters and area, but only because it used the Temple placements. Under (b), all seven lettered entries fall within one district. The letters would then mark a Jericho sub-inventory. This reopens H9.

### R3. Koḥlit is placed near Jericho without using any identification of Koḥlit. (test)

- **The result.** Order alone puts Koḥlit's entries 4, 11, 15 and 19 in the Jericho block, with probability 0.87–1.00 (11: 0.87; 4: 0.92; 15: 0.94; 19: 1.00). This is independent support for a Jericho-area Koḥlit (Puech; Høgenhaven). It counts against Milik's Carmel, Goranson's Transjordan and Zissu's Samaria.
- **Inference (medium): the list ends where it began.** Entry 60 stores "a copy of this document … and the details of each" north of Koḥlit. Koḥlit is the first named place in the list after Achor, and the last. The copy lies at the list's base, not at the last place visited (the north).

### R4. Entries 36–56 stay around Jerusalem and to its south. (inference, medium)

- **The result.** Entries 38–45, Puech's Tekoa–Herodium sector, come out in the J block. They are bracketed by Shaveh (36–37) and Beth ha-Kerem (46, Ramat Raḥel, south of the city). In this four-region model that reads as "the southern hinterland of Jerusalem".
- **For entry 40:**
  - Beth-Horon, 17 km NW of Jerusalem, and the Horite tombs at Beit Guvrin, about 32 km SW of Naṭuf, both leave that block.
  - A southern location fits the order best.
  - This adds a quantitative argument to the entry 40 review's "moderate argument against Beth-Horon". It does not settle the reading.

## 4. A new place-name lead: ha-Melaḥ = the City of Salt (Josh 15:62)

- **Evidence.**
  - Entries 6, 13 and 14 name *ha-Melaḥ*: "the cistern of ha-Melaḥ that is under the steps"; "the pit that is in ha-Melaḥ, on its north side"; "the tomb that is in ha-Melaḥ, on its east side".
  - The project reads the word as the Temple "Esplanade/Millo" (Milik, Puech) or leaves it open. The lexicon records that "the salt sense (מלח) was not searched" (`landmark_lexicon_index.csv`, row *millo*).
- **Evidence.** Josh 15:61–62 lists the towns of the wilderness district: Beth-arabah, Middin, **Secacah**, Nibshan, **the City of Salt (עיר המלח)** and En-gedi. The scroll names Secacah in entries 20–22.
- **BK.** Cross & Milik 1956 (*BASOR* 142) identified Kh. Qumran with the City of Salt, and the Buqeia forts with Middin, Secacah and Nibshan (Secacah = Kh. es-Samrah).
- **Inference (low–medium).** If ha-Melaḥ is the City of Salt, three entries in the first block gain a place name, in the Qumran district. That is where R2's order puts them. The features also fit Qumran as known from BK:
  - "the tomb … on its east side": Qumran's main cemetery lies on the plateau east of the settlement;
  - "the cistern … under the steps": Qumran's stepped cisterns and pools;
  - a pit on the north side, with an entrance at the western corner.
- **It also removes a problem.** "Secacah = Qumran" fails Elitzur's name test (F3.3). The combined reading is:
  - Secacah is the upper valley and its fort in the Buqeia;
  - the "valley of Secacah" is Wadi Qumran running down from it, whose water the aqueduct takes (entry 21, "the head of the water conduit of Secacah");
  - ha-Melaḥ is the site at the bottom.

  Entries 20–23 and 6/13/14 then use two names for two parts of one system, as Joshua's list does.
- **Caveats.**
  - The scroll has no עיר, "city".
  - The form is read as המלח or המלה.
  - *Priority is unchecked:* Puech's 2002 paper had "salt", and the literature must be searched before this is called new.
- **Next check.** Does bare *ha-Melaḥ* occur as a place name in Qumran texts, the Mishnah or the Tosefta? Collect Milik's and Puech's arguments for "Esplanade" (DJD C/D; Puech 2006 pp. 182–184).

## 5. The "dig N cubits" figures are probably not all vertical depths (test and inference)

- **The figures.** 24 figures follow "dig" (from `translation_en.json`).
  - Values: 1, 3 (×6), 4, 6, 7 (×4), 8½, 9 (×2), 10, 11, 12 (×2), 16 (×2), 17, 24.
  - **10 of 24 are 9 cubits or more** (at least 4.0–4.7 m). The largest is 24 cubits (about 11–12.5 m).
- **Inference (medium).** Hand-dug pits 4–12 m deep for deposits someone meant to retrieve are implausible, especially in rock. Beside a rock-cut monument (48: "under Absalom's monument, on the west side, dig twelve cubits") they are more so.
  - The large figures come with voids: chambers (36, 37, 39, 40), a reservoir (46), court corners (12, 12a).
  - That fits measuring **inside existing shafts, cisterns and chambers**, or measuring **horizontally from the stated reference**.
- **For the atlas geometry.** Model each "dig N" two ways: a vertical offset within a void, or a horizontal offset from the stated reference. For entry 48, the horizontal reading gives a testable band 5.4–6.3 m west of the monument's base (at the project's 45–52.5 cm cubit, `phase2_summary.md`).
- **The small figures.** The clustering at 3 and 7 may be formulaic. That is weak evidence on its own.

## 6. Moves the project has not tried yet

1. **Declassified satellite and old aerial photographs.** CORONA and KH-9 (1960s–70s, free from USGS EarthExplorer) and the 1940s RAF aerials, for features destroyed since:
   - the "lost" Qumran dam and intake (Stacey 2009), the first feature in the feature dossier;
   - the Wadi Qelt outlets;
   - Jebel Quruntul;
   - the Qumran plateau east of the site (entry 14 under §4).
2. **Use the repo's own letter recogniser.** The DSS workstream's recogniser could give calibrated per-letter probabilities for the few decisive letters on Puech's radiographs: X 15 (Siloam), IX 7 (ים / דרום), VII 11 (Doq). This would replace blind model readers, which F7.6 shows are poor at whole lines. It needs fine-tuning on the scroll's secure letters, because engraved notarial script differs from ink.
3. **Treat the editors as noisy annotators.** A Dawid–Skene model over the 2,072 reported readings (`variants_long.csv`, local), calibrated on the plate-checked lines, would give each editor's reliability and a posterior reading per line. It would replace case-by-case "Puech against Lefkovits" judgements.
4. **A least-cost route test on SRTM terrain.** Does the Jericho block's order (Achor → Koḥlit → Secacah → the Jericho road → Doq → Kozeba → Kidron) follow a walkable route better than permutations of it?
   - If so, the list was compiled on the ground.
   - Unplaced entries could then be constrained by their position along the route, not only by region.
5. **Test R2 against Netzer's Jericho palace reports** (Netzer 2001; Netzer & Laureys-Chachy 2004). List every peristyle court, pool, gate, stepped cistern and miqveh with its date. Then score entries 2–19 against the Jericho estate and against the Temple enclosure with the same checklist.
6. **Check the personal names.** Look up Manos (5), Mattiyah (8) and "the Queen" (27, which falls in the Jericho block) in Ilan's *Lexicon of Jewish Names*, and in Josephus for Hasmonean royal tombs near Jericho.

## 7. What this does not claim

- No individual feature or deposit is identified.
- The regions are coarse.
- The anchors themselves carry the project's identification uncertainty. The Buqeia sensitivity run shows the main result survives the largest of these (R1).
- R2 offers two explanations. The model cannot choose between them.

## 8. Checks made when this was added to the repository (30 September 2026)

- **The script reproduces the numbers above.** The run gives s = 0.935, 16 of 18 anchors recovered and the same two misses. The probabilities for entries 2–19 and 38–45 match. The only change to the script is its file paths.
- **The input matches the project tables.** The 61 entries are in the order of `tables/entry_concordance.csv`. Status, best place, confidence and possible places agree with `tables/phase3_site_index.csv` for every entry.
- **Corrections.**
  - R3: Koḥlit's range is 0.87–1.00, not 0.92–1.00. Entry 11 has 0.87.
  - §5: the entry 48 band is 5.4–6.3 m at the project's cubit.
- **R1, exact p.** The "p ≈ 5 × 10⁻⁶" is the floor of a 200,000-shuffle test. The exact probability that 18 anchors in the counts 8/1/7/2 fall into four unbroken blocks is 4!·8!·1!·7!·2!/18! ≈ 1.5 × 10⁻⁶.
- **R1, repeated names.** Secacah (20–22), Shaveh (36–37) and Zadok's portico (51–52) each give more than one anchor. Counting each name once leaves 14 anchors (6/1/5/2). The exact p is then ≈ 4.8 × 10⁻⁵. R1 does not depend on the repeats.
- **R2 depends on the East Gate.** In the lenient run, 9 and 10 are anchored in Jerusalem, and entries 6–12a then lean to Jerusalem (J up to 0.83 at 8 and 11). Entries 5 and 13 are even, and 4, 14 and 15 still lean to Jericho. So R2 holds only if the East Gate is left as a question, as §2 does. The model tests whether the rest of the order supports the Temple placements. It does not show that they are wrong.
- **R2, the figure 0.001.** A binomial test with 6 or more changes in 19 steps at a switching rate of 1 − s = 0.065 gives 0.0010. At the lenient rate (0.115) it gives 0.017.
- **Cross-references checked:** F2.2, F3.3, F4.8, F7.6; H8, H9 and T5 (`phase4_summary.md`); the *millo* row of `tables/landmark_lexicon_index.csv` ("the salt sense (מלח) was not searched"); "Only 'peristyle' in 3 is secure" (`tables/phase5_assessments.csv`, JER row); SWP III pp. 222–223 for Tell es-Sultan (`tables/phase5_reports.csv`).
- **No confidence changes** follow from this analysis. The findings are F12.1–F12.6, and the open questions are Q50–Q53. The follow-up adds F12.7–F12.10 and Q54.
