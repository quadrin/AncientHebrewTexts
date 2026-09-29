# Photographic reader: strip 13

The Scroll view includes a photograph of the original Copper Scroll in the Jordan Museum, photographed by Osama Shukir Muhammed Amin on 20 January 2020. It opens beside a modern Hebrew reading, morphology/glosses, the project translation and existing editorial notes.

## Image versions

The reader offers three versions of the same photograph. **Grooves** is the default.

| View | File | What it shows |
|---|---|---|
| Grooves | `public/scroll/strip13-grooves.webp` | A groove map: the engraved strokes as dark lines on white. The raking light and the green patina are removed. |
| Relief | `public/scroll/strip13-relief.webp` | The photograph in grey, with noise reduction and local contrast (CLAHE). |
| Photo | `public/scroll/strip13.webp` | The photograph as published, full size (2467 × 4016). |

**Hold for photo** shows the colour photograph without overlays in any view.

Grooves and Relief are computed from the photograph by [`../../tools/photo_trace.py`](../../tools/photo_trace.py) (`enhance`). Grooves is a morphological black-hat of the grey image (Gaussian blur, elliptical kernel about 13 units wide), inverted. It shows grooves that the colour photograph hides under relief shadows and patina. It is an image transform, not a reading: corrosion pits and cracks also appear as dark marks.

### No infrared image of the Copper Scroll

The request was for an infrared image, as for the leather scrolls. None exists for 3Q15:

- The scroll is copper. Infrared imaging of ink on leather does not apply to engraved metal.
- The Leon Levy Dead Sea Scrolls Digital Library lists 3Q15 ("3Q Copper Scroll") with **0 images** (search API, 29 September 2026).
- The clearest published images are the EDF radiographs and the photographs of the galvanoplastic copy in Puech 2006, vol. II. They are copyrighted plates: the reader uses them only as a reference (below) and does not reproduce them.

Other open images checked on Wikimedia Commons (29 September 2026):

- Amin's photograph of strip 13 is the only open photograph of this strip. Its full-size original (2467 × 4016) replaces the 1600-px copy used before.
- "The Copper Scroll 03"–"06" (Mohammad hajeer, 12 July 2026, CC BY-SA 4.0, up to 5552 × 7408) show several strips per frame through display glass, with reflections. Strip 13 is not among them. They may serve for other strips.
- "Part of Qumran Copper Scroll" (1) and (2) show a replica, not the original.

## Coverage and evidence

Eight words cover VII 7–11: ככרין, במערא, בית, הקץ, כדין, של, בדוק and תחת. They are **provisional tracings**, not a diplomatic transcription. The curved metal compresses the sides of the text, and corrosion interrupts strokes.

Every letter of each word is traced, and each stroke names its letter:

- **Solid** strokes follow a groove that this photograph shows.
- **Dashed** strokes are shown by Puech's radiograph of strip 13 (2006, vol. II, p. 385, pl. CCCXLVI) but not by this photograph.

Letters were identified on that radiograph and on Puech's facsimile (p. 413, pl. CCCLXXII). Each word's note in the reader says which strokes are dashed. The weakest word on this photograph is תחת: its left-hand tav lies in shadow where the strip curves away. The Hebrew, glosses, translation and reading notes come from the existing atlas text data, with its existing source attribution.

### Earlier versions

- 28 September 2026: strokes drawn by hand on the 1600-px photograph. The box for ככרין ran into the next word, ארבע, and several strokes did not follow the grooves.
- 29 September 2026 (first revision): strokes carried over from the radiograph by an automatic fit, keeping only pieces that the photograph confirmed. Too few strokes survived, and the words did not read as letters.

The present tracing replaces both.

## Method

The tracing is stored in [`../../registration/photo_tracing_strip13.json`](../../registration/photo_tracing_strip13.json): for each word, its strokes with letter, status (`seen` or `inferred`) and points in reader units. [`../../tools/photo_trace.py`](../../tools/photo_trace.py) turns it into the reader's data:

1. Each letter was read on the radiograph and the facsimile, and its strokes were placed by hand on the full-size photograph and its groove map.
2. `trace` snaps each seen stroke onto the groove map: a shift of up to 4 units, then each point moves up to 2.5 units. It prints the groove response of every stroke. A seen stroke with a weak response (below 0.25) is re-examined and, if the photograph does not show it, set to `inferred`.
3. `trace --update` writes the solid paths, dashed paths and hit boxes into `app/atlas-photo-data.json`.
4. `review` writes local check sheets: the photograph, the photograph with the tracing, and the radiograph carried into the same frame (affine fit and per-word shift, stored in the JSON). The plate images stay local, as in the [plate check](../../plate_check.md).

To extend coverage: add the word to the JSON with its strokes, run `trace` and `review`, and check each stroke against the photograph and the radiograph. Do not place a modern Hebrew font over the photograph and label it a tracing.

## Files and coordinate system

- `app/atlas-photo.tsx`: reader and controls.
- `app/atlas-photo-data.json`: source metadata, image versions, line/word references, boxes, solid and dashed SVG paths, and notes.
- `public/scroll/strip13.webp`, `strip13-grooves.webp`, `strip13-relief.webp`: the three image versions.

The SVG uses a 1000 × 1628 coordinate system for the image, hit regions and tracings together (1 unit = 2.467 px of the original). Zoom and pan change only the SVG viewBox. Mouse, touch and keyboard controls select words; dragging suppresses selection. Reduced-motion preferences disable stroke animation.

## Image attribution and licence

Osama Shukir Muhammed Amin, “Strip 13, part of the Copper Dear Sea Scrolls, from Qumran Cave 3, Jordan Museum.jpg”, 20 January 2020, [Wikimedia Commons source](https://commons.wikimedia.org/wiki/File:Strip_13,_part_of_the_Copper_Dear_Sea_Scrolls,_from_Qumran_Cave_3,_Jordan_Museum.jpg), [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The photograph, the Grooves and Relief images derived from it, and the project tracing overlays are distributed under CC BY-SA 4.0. This asset-specific licence does not relicense the atlas's separately sourced text dataset. Puech's plates are not part of the atlas.
