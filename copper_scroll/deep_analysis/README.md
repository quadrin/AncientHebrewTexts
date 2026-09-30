# Deeper analysis code (30 September 2026)

Code and outputs for the report [*Reading the list from the inside*](../deeper_analysis_2026-09-30.md) (`deeper_analysis_2026-09-30.md`). The scripts and outputs came in `deeper_analysis_code_2026-09-30.zip`; the report came separately. The section numbers in the table below refer to the report.

The analysis tests the order of the entries in the scroll: whether place names recur in runs, whether direction words, dig depths and vocabulary change between blocks of entries, whether the Greek-letter gaps mark changes, and whether the Jerusalem and Jericho blocks follow a short walking route.

## Running

Python 3 with numpy (all scripts), scikit-image (`route_jer.py`) and Pillow (`dem.py`). Each script finds its inputs relative to its own folder, so it runs from any working directory:

```
python3 copper_scroll/deep_analysis/build.py
python3 copper_scroll/deep_analysis/features.py
python3 copper_scroll/deep_analysis/tests.py
python3 copper_scroll/deep_analysis/vocab.py
python3 copper_scroll/deep_analysis/vocab_blocks.py      # and the others, in any order
```

Run `build.py` and `features.py` first; the other scripts read `features.json`. `vocab_blocks.py`, `changepoint.py`, `splitscan.py`, `rotation.py` and `greek_groups.py` execute the first part of `vocab.py` (the concept map) and do not need its output. `hmm_fine.py` has no inputs.

`route_jer.py` also needs `dem.npz`, a terrain grid (`dem`, with the Web Mercator tile zoom `Z` and origin tiles `tx0`, `ty0`, 256 px per tile). Run `dem.py` first to make it. It downloads 32 Mapzen/AWS Terrarium tiles. Or put a `dem.npz` in this folder, or set `DEM_NPZ` to its path.

The original `dem.py` came in an earlier bundle and is not in the repository. The `dem.py` here was written on 30 September 2026 from the terrain described in the [follow-up report](../sequence_model_followup_2026-09-30.md) §1: Terrarium tiles at zoom 11 covering 31.55–32.60 N and 35.10–35.62 E. It gives the same 32 tiles and the same elevation range (−423 m to 1,021 m), and `route_jer.py` then gives a `route_jer.json` byte-identical to the delivered one.

## Scripts

| Script | What it does | Output | Report section |
|---|---|---|---|
| `build.py` | Reads `../web/scroll-text.js` (ETCBC/Abegg, CC BY-NC 4.0), `../text/translation_en.json` and `../tables/entry_concordance.csv`. Writes one record per entry (Hebrew words, lemmas, numeral signs, translation) | `entries_full.json` (not in git) | data |
| `features.py` | Per-entry features: place names, direction words (regex, final nun handled, קדרון excluded), aspect words, dig depths, stated talents and formula flags. Fixes the I 6 boundary between entries 2 and 3 (Puech p. 179) | `features.json` (not in git) | data |
| `tests.py` | T1 name adjacency (permutation), T2 orientation (Fisher/hypergeometric), T3 depth (Mann–Whitney permutation), T6 record formula | `tests_results.json` | §1, §2, §4, §6 |
| `vocab.py` | Landmark concept map (fixed before the tests), Bernoulli naive Bayes, leave-one-out and label permutation | `vocab_results.json` | §5.2 |
| `vocab_blocks.py` | Chi-square permutation test of vocabulary between blocks | `vocab_blocks.json` | §3.1 |
| `changepoint.py` | Sliding-window vocabulary change-point scan | `changepoint.json` | §5.3 |
| `splitscan.py` | Rank of the anchor split 35/36 among all splits of 20–56 | `splitscan.json` | §2.2, §4 |
| `rotation.py` | Rotation (circular shift) test that keeps local runs | `rotation.txt` (printed output) | §0, §2.2, §4 |
| `greek_groups.py` | Are the Greek-letter gaps change points? (exact, 11,440 placements) | `greek_groups.txt` (printed output) | §5.1 |
| `dem.py` | Downloads the terrain tiles and writes the grid (added in the repository; see above) | `dem.npz` (not in git) | — |
| `route_jer.py` | Exact walking-route test for the Jerusalem block and the Jericho block (Tobler cost on the terrain tiles; places from `../tables/phase3_places.csv`) | `route_jer.json` | §5.4 |
| `hmm_fine.py` | Three-sub-district sequence model for entries 1–35, with two placements of Achor | `hmm_fine.json` | §7 |

Random seeds are fixed in each script. `greek_groups.py` and `route_jer.py` enumerate all cases and have no random part.

## Choices fixed in the code

- **Blocks** (`features.py`, from the anchor model R1): A = entries 1–19, B = 20–35 (Jericho and desert), C = 36–56 (Jerusalem and its hinterland), D = 57–60.
- **Hand-coded lists** in `features.py`: proper place names per entry, aspect directions, dig depths in cubits, and stated talents. Personal names that are not places (Manos 5, Mattiyah 8, the Queen 27, the High Priest 28) are left out.
- **Concept map** in `vocab.py`: 22 landmark concepts, each a list of ETCBC lemmas. ים counts as a pool in entries 47 and 49, and as the direction "sea" in entry 40.
- **Anchors** in `hmm_fine.py`: three sub-districts, fixed by entries 20–22 (Secacah) = QB, 31 (Doq) and 32 (Kozeba) = JO, and 35 (Kidron) = DS. Achor (entries 1 and 17) is put in JO (Nuweimeh) or in QB (the Buqeia); two further anchors (28 in JO, 18 Asla in QB) are added one at a time and together.

## Reproduction check

On 30 September 2026 every script except `route_jer.py` was run on the repository at commit `35a9ab5`, first in the bundle's original folder layout and then from this folder. Both runs gave output byte-identical to the delivered `tests_results.json`, `vocab_results.json`, `vocab_blocks.json`, `changepoint.json`, `splitscan.json` and `hmm_fine.json`. `rotation.txt` and `greek_groups.txt` are the printed output of the same run.

Later the same day, `route_jer.py` was run on a `dem.npz` made by `dem.py`. Its output is byte-identical to the delivered `route_jer.json`. Its Jericho block (17.0 h; median 20.3 h; best 10.4 h; p = 0.16) is also the Jericho row of the follow-up report's §1 table, which used 200,000 random orders instead of exact enumeration.

## The report's numbers and these outputs

Checked on 30 September 2026. The counts and p-values in §0, §1 (observed and expected pairs), §2, §3.1 (vocabulary, "dig"), §4 (except Spearman), §5 and §7 are in the outputs above, after rounding. The Holm-adjusted values in §11 follow from the listed p-values.

Some numbers in the report are not in any output file:

| Report | Value | Status |
|---|---|---|
| §1, §11: T1 p | 3.6 × 10⁻⁶, "exact" | `tests.py` gives the permutation estimate 5 × 10⁻⁶ (1 hit in 200,000 shuffles, as the report says). The exact calculation is not in the bundle |
| §1: Shallum at 23; Milik's reading of 15 for T1 | 4 pairs, p ≈ 9 × 10⁻⁵ | Not in the scripts; not re-checked |
| §6, §11: T6 | C(10,5)/C(61,5) ≈ 4 × 10⁻⁵ | Arithmetic checked (4.2 × 10⁻⁵). `tests_results.json` holds a different test: `T6_record.p_cooc` = 2.4 × 10⁻⁴ counts entries (6 with כתבן, entry 8 included), not adjacency |
| §6, §11: scan of 50–55 | 0.005 | `T6_scan.p` = 0.014 includes entry 8's bare וכתבן (6 occurrences). With the five full phrases only (22, 50, 51, 54, 55), the same scan gives 0.005 (re-checked, 200,000 draws) |
| §3.1: round sums | Fisher p = 0.017 | Re-checked from the `features.py` talent list: 7 of 13 against 4 of 26, p = 0.0174 |
| §4: depth against position | Spearman ρ = 0.42, p = 0.031, n = 26 | Re-checked: ρ = 0.424, t = 2.30 on 24 degrees of freedom |
| §3.1: full spelling ככרין | 7 of the first 16, 4 of the 45 later | Taken from the project's T8 (`phase4_summary.md`). On the Abegg text, the `f_kkryn` flag in `features.py` is true in 6 of the first 16 entries (1, 3, 6, 8, 9, 11) and 8 of the 45 later ones. Only `greek_groups.py` uses the flag, as one of its seven features |
| §11: independent check | — | The separate agent's code is not in the bundle |

`entry_features_2026-09-30.csv`, named in the report's Data section, is not in the bundle. `features.py` makes the same per-entry features as `features.json`.

## Changes from the bundle

Only the file paths changed. The bundle expected the scripts in `cs_work/deep/`, next to a clone `AncientHebrewTexts/`. Each script now starts with two lines that set `D` to its own folder, and reads and writes through `D`. `route_jer.py` also reads `DEM_NPZ`. The analysis code is unchanged. `dem.py` is new (see Running).

## Text and data

`build.py` and `features.py` write the Abegg Hebrew text (ETCBC `dss` 2.0.1, CC BY-NC 4.0) into `entries_full.json` and `features.json`. These two files can be made again at any time, so they are in `.gitignore`. The committed outputs hold entry numbers, counts, concept names and statistics, and no Hebrew text.
