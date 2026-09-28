# Copper Scroll (3Q15): hiding places and Greek letters

Desk research from editions, texts and maps only. **Nothing here proposes or supports excavation.**

This folder is separate from the DSS letter-recogniser project described in the repo's `CLAUDE.md`.

## Phases

1. **Master table of all entries** (done, session 1; see `phase1_summary.md`)
2. Landmark lexicon: Bible, Mishnah, Josephus, Eusebius
3. Site candidates: Pleiades / TIR, scored against written criteria, mapped
4. Greek letters: occurrences and tests of the hypotheses
5. Archaeology check of the top candidates

## Files

| File | In git? | Contents |
|---|---|---|
| `sources.md` | yes | What is in the repo, what is missing, page offsets, encodings |
| `phase1_summary.md` | yes | Entry count, clearest and most damaged entries, recurring terms, sequences |
| `findings_log.md` | yes | Running log, evidence vs inference, with pages |
| `open_questions.md` | yes | Running list of open questions |
| `tables/entry_concordance.csv` | yes | Puech entry ↔ Lefkovits item ↔ line range, plus documented division notes (Milik, Allegro, Luria, Beyer, Wise) |
| `tools/puech_heb.py` | yes | Decoder for Puech 2006's legacy Hebrew font (text layer → Unicode, logical order) |
| `copper_scroll_master_table.csv` | **no** | The master table (61 rows). It contains Puech's full edited text and Lefkovits's text and translation. |
| `variants_long.csv` | **no** | 2,072 reported readings, one per row (scholar, reading, gloss, reporting edition, page, verdict) |
| `puech_lines.csv` | **no** | Puech's text line by line (181 lines), with numeral values and sign notes |

The three files marked **no** reproduce copyrighted edition text. This GitHub repository is public, so they are delivered to you directly rather than committed.

## Master table columns

- `entry_puech`: Puech's entry number (1–60, plus 12a). Puech and Lefkovits use the same boundaries, so the numbers coincide.
- `item_lefkovits`: Lefkovits's item number. Milik's numbers are unknown; see open question Q4 and `division_notes`.
- `col_line`: scroll column:line range.
- `hebrew_puech`: Puech's text (pp. 208–216) with his sigla:
  - `[ ]` lacuna/restoration
  - `[[ ]]` letter supplied by the editor
  - `< >` letter inserted by the engraver (also used here for letters written above or below the line)
  - `{ }` letter cancelled by the engraver
  - `x(y)` engraved x is an error for y
  - `a/b` alternative readings
  - `(?)` uncertain
  - ‖ line break
  - Numerals appear as `‹value›`.
- `variants_lefkovits`: hand-checked differences between Lefkovits's text and Puech's. "subst." marks a difference in place, direction, distance/depth or quantity.
- `variants_milik_secondhand`, `variants_wolters_secondhand`: readings that differ from Puech, as reported by Lefkovits `[Lef. p.]` (Hebrew script) or Puech `[Puech p. n.]` (transliteration). The two reporters sometimes disagree about what Milik or Wolters read.
- `translation_en`: an English rendering written for this project. It follows Puech's reading and his French interpretation, and is not Puech's English translation, which contains errors (see the findings log).
- `landmark_terms`, `direction_distance_depth`, `treasure`: structured from Puech's text. In the treasure column, "ככ" is kept as written. Puech and Lefkovits read it as k(esef) k(arsh), 1 karsh = 10 shekels; Milik and Allegro read "talents".
- `numerals_puech`: the value of each numeral group in Puech's reading.
- `greek_letters`: Puech's reading, and Lefkovits's where it differs.
- `damage_uncertainty_notes`: lines with lacunae, "(?)", engraver's corrections, and insertions or editorial additions, plus notes on letters above or below the line.
- `division_notes`: how other editors divide or number the entry, with source pages.
- `hebrew_lefkovits`, `translation_lefkovits`: Lefkovits's text and translation, read from the scanned images.
- `pages_puech`, `pages_lefkovits`: printed pages of the text and commentary.
- `n_*`: counts used for the clarity ranking.

## Method in brief

- **Puech:** the Hebrew was decoded from the PDF text layer, then all 181 lines were checked visually and all 33 numeral groups checked against his own totals (p. 173).
- **Lefkovits:** his Hebrew OCR is unusable, so every Hebrew word, including every reading he quotes from other scholars, was read from page images in eight parallel passes. The automatic Puech–Lefkovits comparison was then reviewed line by line.
- **Puech's commentary:** pp. 179–206 were extracted phrase by phrase: variant readings, his verdict on each, his notes on letter shapes and damage, and place claims (kept for Phase 3).
