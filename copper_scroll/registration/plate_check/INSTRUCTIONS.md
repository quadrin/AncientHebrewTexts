# Reading task: engraved Hebrew inscription (blind protocol)

You are one of several independent readers. Your job is to record what the images show, letter by letter, with honest uncertainty. You are NOT asked to identify the text, restore it, or make it meaningful.

## Material
Each item code (P01 ... P30) has three images in `items/`:
- `Pxx_A.png` - photograph of a metal electrotype (galvanoplastic) copy of the inscription, lit to show relief. The letters were punched/engraved into sheet metal; on the copy they appear as raised or sunken strokes with shadows.
- `Pxx_B.png` and `Pxx_C.png` - X-radiographs of the original metal fragments. Several separately X-rayed strips are placed side by side; the same letters can appear twice in overlapping strips, and strips are not joined seamlessly. Letters show as grooves or thickness changes.

The **target line** is the one marked by the green triangles in the left and right margins. The line above and below are included for context only. All three images show the same target line at roughly the marked height, though the strips may be offset by up to half a line.

The script is the Jewish square script (Hebrew/Aramaic letters), read right to left. Some lines also contain small Greek capital letters, and some contain numeral signs (vertical strokes, hook-shaped signs and other symbols) rather than letters. Letter forms on this object are unusual: the engraver's letters are blocky and some letters are easily confused (e.g. ו/י/ר/ד, ב/כ, ה/ח/ת, מ/ט/ס, final ם vs ן).

## Rules
- Use only the images in `items/`. Do not open any other file in the environment, do not search the web, and do not try to recognise the text or recall any published reading. If you think you recognise the text, say so in `notes` and still report only what you see.
- You may make enlarged or contrast-adjusted crops of the item images with Python/PIL for your own inspection. Save them only under your own folder `work_<READER>/`.
- Do not guess to make words. Record each letter position as: certain, probable, possible, or illegible. An unreadable position is "?". A stretch you cannot count is "[...]".
- When the A image and the B/C images disagree, say so for that position.

## Stage 1 (blind transcription) - do this for every item FIRST
For each assigned item, transcribe the whole target line right to left and grade each letter. Write all Stage 1 results to `out/<READER>_stage1.json` BEFORE you open `QUESTIONS.md`.

Stage 1 format: a JSON object keyed by item code:
```
{"P01": {"transcription": "Hebrew string with ? for illegible and [...] for gaps; separate words by a space where a space is visible",
         "letters": [{"pos": 1, "read": "ב", "grade": "certain|probable|possible|illegible", "alternatives": ["כ"], "evidence": "A clear; B shows ...; C broken"}],
         "greek_or_numerals": "describe any Greek letters or numeral signs and their shapes/count",
         "image_quality": "which image was most useful and why",
         "notes": "anything else (damage, cracks, corrections, letters above/below the line, cancelled letters)"}}
```
`pos` counts from the right edge of the line.

## Stage 2 (targeted questions)
Only after the Stage 1 file is written, open `QUESTIONS.md` and answer the questions for your items. Do not change your Stage 1 file after reading the questions; if you now see something differently, record that in Stage 2 with the reason.
Write `out/<READER>_stage2.json`: keyed by item code, each a list of {"q": question number, "answer": ..., "grade": certain|probable|possible|cannot tell, "evidence": "which image, which strip, what stroke features"}.

Finish with a short message listing the files written and any items where you could not locate the target line.
