# Follow-up to the sequence model: priority, a walking-route test, and entries 2–19

> **Repository note (added on merge).**
> - Later reports correct this one. The [deeper analysis](deeper_analysis_2026-09-30.md) §8.1 changes entries 2 and 14 in the §2 table to "Neither" (revised tally: Jericho 7, Temple 4, Neither 7) and says that this file carries the correction. The copy merged here does not; the table and tally below are as received. The same report (§5.1) withdraws the depositor-group prediction of §2, and the [tests on old surveys and plans](leads_on_old_plans_2026-09-30.md) (§1, §8.1) correct §0.3: Lefkovits 2000 already proposed that Melah is the City of Salt near Secacah.
> - `route.py`, `route_var.py` and the first report, `sequence_model_and_new_leads_2026-09-30.md`, are not in the repository. [`deep_analysis/dem.py`](deep_analysis/README.md) rebuilds the terrain described in §1, and `deep_analysis/route_jer.py` reproduces the Jericho-block row of the §1 table (17.0 h; median 20.3 h; best 10.4 h; p = 0.16) by exact enumeration.

30 September 2026. This follows `sequence_model_and_new_leads_2026-09-30.md` and corrects it where needed. Labels: evidence / inference / BK. Code: `route.py` and `route_var.py`, with the public terrain tiles they download.

## 0. Corrections to the first report (read first)

1. **Puech already noticed the order.** Puech 2006 pp. 173–174 (Puech_3 text layer, "Les répartitions des premier et second groupements…"):
   - He separates the first fifteen entries (the Greek-letter group) from the rest.
   - He says the second group "semble reprendre en gros la séquence géographique précédente", starting from Koḥlit.
   - He calls both orders coherent and "difficilement dû au pur hasard".
   - He names the Kidron as the "point de passage obligé" between the Jericho–Secacah area and the Tekoa–Jerusalem area.

   The first report's R1 is therefore a **measurement of Puech's observation**, using independent anchors and a permutation test, not a discovery. The conflict test in R2 and the model's probabilities for each entry remain new to the project.
2. **The "salt" reading and the City of Salt are not new.**
   - Lefkovits pp. 103–105 (item 6) records Allegro, Lurie, Pixner, Wolters, Beyer and Wise for "salt pit". Allegro links it to the Temple's Salt Chamber.
   - Lurie places the salt pit "below the steps in Haruba', in the Valley of Achor", i.e. in the Jericho area. Lefkovits lists "Salt City (Josh. 15:62)" among comparable place names.
   - Allegro wonders whether the salt is "a natural feature, from which the 'City of Salt' got its name".
   - Puech 2006 reads II 1 as ***hmlḥ* "le sel"** (p. 182 and nn. 141–143). At III 8 and III 11 (p. 184) he prefers *mlh* "embankment/esplanade" and calls *bmlḥ* "dans la saline" "peu vraisemblable pour ces deux entrées".
   - Puech also discusses Ir ha-Melaḥ elsewhere, but places it at ʿAin el-Ghuweir – ʿAin et-Turabeh, "entre Sokokah et ʿEn Gaddi" (p. 176 n. 62, after Bar-Adon).
3. **What is still not found in any source checked.**
   - The combined proposal: that all three *ha-Melaḥ* entries (6, 13, 14) name one site, the City of Salt identified with Kh. Qumran (Noth; Cross & Milik 1956; confirmed on [Wikipedia: City of Salt](https://en.wikipedia.org/wiki/City_of_Salt)), with Secacah as the Buqeia valley and fort above it (Cross & Milik: Kh. es-Samrah; [Wikipedia: Secacah](https://en.wikipedia.org/wiki/Secacah)).
   - The check of "the tomb … on its east side" (14) against the cemetery east of Qumran.
   - Not yet checked: *Copper Scroll Studies* (2002), Høgenhaven 2020, Allegro's commentary in full, and Lurie. Treat the claim as **unverified for priority**.
   - A web search ("Copper Scroll" "City of Salt"; ha-melah / hmlh + Qumran cemetery) found nothing further.

## 1. Walking-route test (test)

**Question.** Was the list written in the order someone walked, so that an entry's position along the route could locate it?

**Method.**
- **Terrain.** Mapzen/AWS Terrarium tiles at zoom 11 (about 64 m per pixel), 32 tiles covering 31.55–32.60 N and 35.10–35.62 E. Elevation runs from −423 m to 1,021 m, as expected.
- **Cost.** Tobler's hiking function, applied as an isotropic slope cost, with least-cost paths from `skimage.graph.MCP_Geometric`. The Dead Sea surface is treated as impassable.
- **Stops.** Only the strict anchors, in scroll order, using the Phase 3 coordinates:

  | Stop | Entries |
  |---|---|
  | Nuweiʿimeh | 1, 17 |
  | Wadi Qumran | 20 |
  | Kh. Qumran | 21–22 |
  | Kuteif | 24 |
  | Doq | 31 |
  | Choziba | 32 |
  | Mar Saba | 35 |
  | Ramat Raḥel | 46 |
  | Kidron monument | 48 |
  | SE corner | 51 |
  | Kidron east | 52 |
  | Bethesda | 55 |
  | Gerizim | 57 |
  | Beth Shean | 58 |

- **Comparison.** The scroll order against 200,000 random orders of the same stops, and against the best possible open path (2-opt, 300 restarts).

**Results.**

| Stops | Scroll order | Random median | Best possible | Scroll order over best | p (random order as good) |
|---|---|---|---|---|---|
| All 14, walking hours | 48.6 h | 105.4 h | ≈ 39.7 h | +22% | ≈ 1 × 10⁻⁵ |
| All 14, straight-line km | 158 km | 367 km | ≈ 126 km | +25% | ≈ 1 × 10⁻⁵ |
| Jericho block (1–35), hours | 17.0 h | 20.3 h | ≈ 10.4 h | +64% | 0.16 |
| Same, Achor in the Buqeia | 14.4 h | 19.6 h | ≈ 9.6 h | +50% | 0.044 |
| Same, Achor and Secacah valley in the Buqeia | 14.4 h | 17.2 h | ≈ 9.6 h | +50% | 0.17 |

Legs within the Jericho block, by walking time:

| Leg | Walking time | Distance |
|---|---|---|
| Nuweiʿimeh → Wadi Qumran | 4.2 h | 15.9 km |
| Wadi Qumran → Kh. Qumran | 0.5 h | 0.8 km |
| Kh. Qumran → Kuteif | 2.6 h | 8.1 km |
| Kuteif → Doq | 2.8 h | 8.3 km |
| Doq → Choziba | 1.5 h | 3.8 km |
| Choziba → Mar Saba | 5.4 h | 17.2 km |

**Inference (medium–high).**
- **Across the scroll**, the order is efficient. That is the regional blocking already found in R1.
- **Within the Jericho block**, it is **not** a walking route: it zigzags north → south → north → west → south, and is no better than a random order (p = 0.16).
- The list was grouped **by district**, not compiled along a path. So position inside a block **cannot** be used to place unplaced entries (for example 25–30 or 33–34). The first report's §6.4 suggestion is withdrawn.
- A weak side result: putting Achor in the Buqeia (Allegro, Eshel) makes the block slightly more route-like (p = 0.044). This is one test among several and within noise. It does not choose between Nuweiʿimeh and the Buqeia.

## 2. Entries 2–19: Temple enclosure or Jericho estate? (evidence and inference)

**Jericho features used** (BK, from summaries of Netzer's excavations: [Wikipedia](https://en.wikipedia.org/wiki/Hasmonean_and_Herodian_royal_winter_palaces); [BibleWalks](https://www.biblewalks.com/jericho/)):
- a Hasmonean palace with an open central courtyard;
- a "courtyard with perimeter columns and a central pool";
- two pairs of swimming pools (18 × 13 m, 3.5 m deep);
- a Herodian pool of 32 × 18 m and a Third Palace pool of 90 × 42 m;
- a Third Palace court of 29 × 19 m with Corinthian columns;
- "many ritual baths", including one with 800 bowls;
- two aqueducts, from Wadi Qelt and from the Naʿaran springs;
- the Second Temple cemetery on the western hills (Hachlili; Wexler, already in `phase5_reports.csv`).

**Temple features** are from the project's JER assessment and the editions' citations: Mishnah Middot; Josephus; Puech pp. 182–184.

| Entry | Landmark | Temple enclosure | Jericho estate / Koḥlit | Leans to |
|---|---|---|---|---|
| 2 | funerary monument (נפש), "third course" | No tomb monuments inside the enclosure (BK: purity) | Cemetery on the western hills | **Jericho** (or the Kidron) |
| 3 | great cistern in "the court of the peristyle" | Porticoes; cisterns under the platform | Peristyle court with a central pool | Neither |
| 4 | Koḥlit mound; conduit; "rock cleft of immersion" | — | Aqueducts; many miqva'ot; Tell es-Sultan | **Jericho** |
| 5 | spiral stairwell (Puech's המסבא) of Manos | *mesibbah* in m. Middot 4:5 (Puech p. 181 n. 136) | Spiral stairs occur in Herodian buildings (Puech cites Kloner) | **Temple** (weak) |
| 6 | cistern of *ha-Melaḥ* under the steps | Salt Chamber, m. Middot 5:3 (Allegro) | Salt / City of Salt; Lurie's Haruba | Neither |
| 7 | cave of the old House of …, third ledge | Caves are not typical of the enclosure | Caves in the cliffs west of Jericho | **Jericho** (weak) |
| 8 | underground chamber in the court of Mattiyah; wood | Wood chamber/court (Middot) | — | **Temple** |
| 9 | cistern opposite "the East Gate", 19 cubits | The East Gate, textually famous | No named east gate reported | **Temple** |
| 10 | cistern under the wall, east; great threshold | The east wall of the enclosure | Palace walls (generic) | **Temple** (weak) |
| 11 | pool east of Koḥlit | — | Spring pool of ʿAin es-Sultan at the tell's east foot; palace pools | **Jericho** |
| 12, 12a | corners of a court (name restored) | Courts of the enclosure | Palace courts | Neither (the name is restored) |
| 13 | pit in *ha-Melaḥ*, north side | Esplanade (Milik, Puech) | City of Salt (this project) | Neither |
| 14 | **tomb** in *ha-Melaḥ*, east side | A tomb at the Temple platform is implausible (BK: purity) | Tomb or cemetery east of the site (Qumran under §0.3) | **Jericho / Qumran** |
| 15 | great cistern in Koḥlit, with a pillar | — | Koḥlit | **Jericho** |
| 16 | conduit, "as you go in", 41 cubits | — | Aqueducts | **Jericho** (weak) |
| 19 | eastern pit north of Koḥlit | — | Koḥlit | **Jericho** |

**Inference (medium).**
- **The tally.** Nine entries lean to Jericho (2, 4, 7, 11, 14, 15, 16, 19, and 17, which is anchored) and four lean to the Temple (5, 8, 9, 10). Five are undecided (3, 6, 12, 12a, 13).
- **What this shows.** The Temple entries rest on Temple-specific terms: the wood court, the *mesibbah*, the East Gate. These are real textual matches and should not be explained away.
- **So the best reading of R2's anomaly is its explanation (a).** The first sub-list genuinely mixes the Jericho area and the Temple. It is not a Jerusalem block that the sequence mislabels.
- **This fits Puech's view** that the Greek letters abbreviate the names of the people responsible for deposits. If the first fifteen entries are arranged **by depositor** rather than by place, alternation between places is expected. From entry 16 on, where there are no letters, the list is arranged by district.
- **Prediction (testable).** Grouping entries 1–15 by the Greek letter that closes each group gives {1}, {2–4}, {5–6}, {7}, {8–9}, {10–12a}, {13–15}. The groups should be coherent in something other than place: kind of treasure, formula, or the offering/tithe vocabulary. Phase 4's tests T6 and T8 did not look at groups defined this way.

## 3. Net effect on the project

- **R1 (regional order):** stands. It is now credited to Puech and measured.
- **R2:** the 2–19 anomaly stands (p ≈ 0.001). Explanation (a), a first sub-list arranged by depositor, is preferred over (b), all of 2–19 at Jericho. Entries 2, 4, 7, 11, 14, 15, 16 and 19 should still be scored for the Jericho area in the atlas. The Temple rating for 14 (a tomb) should be reconsidered.
- **R3 (Koḥlit at Jericho from order alone):** stands.
- **The ha-Melaḥ lead:** narrowed to the combined Qumran / City of Salt proposal. Its priority is unverified, and Puech rejects the salt reading at III 8 and III 11.
- **The walking route:** negative. Inside a district the order is not a path.
- **No site confidence change is proposed.** These are constraints on how to reason, not new identifications.

## 4. Next checks, in order of value

1. The depositor-group test on entries 1–15 (T6/T8 re-run on the groups in §2). It needs only the master table.
2. A priority check for the combined City of Salt proposal: *Copper Scroll Studies* index, Høgenhaven 2020, Allegro 1960 pp. 35–37, 139–142, Lurie pp. 67, 76–79.
3. Atlas: add Jericho-area alternatives for entries 2, 7, 14 and 16. Record the purity argument against a tomb at the Temple for entry 14.
