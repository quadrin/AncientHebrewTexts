# The Copper Scroll Atlas

An interactive atlas of the 61 Copper Scroll entries, paired with 37 candidate places from the research repository. The interface pairs a dark place register with an open map workspace and a white reading folio. The entry panel separates Places, Text and Evidence into keyboard-accessible tabs; candidate sites appear first. Compact headers, larger controls and a single-panel layout on screens up to 1100px keep the research usable on smaller displays.

## Run locally

Use Node.js 24 and pnpm 11.25.0 (the version pinned in `package.json`). From the repository root:

```sh
cd copper_scroll/atlas
corepack pnpm install --frozen-lockfile
corepack pnpm dev
```

Open the local address printed by the development server. Run `corepack pnpm build` for a production build, and `corepack pnpm exec tsc --noEmit --incremental false` for the type check. No map API key is required. Basemap, elevation and photograph loading need an internet connection.

This directory contains the source deployed as the [Copper Scroll Atlas](https://copper-scroll-atlas.alexkesin.chatgpt.site), including the marker-positioning fix. The hosted Site retains its existing access settings. `.openai/hosting.json` identifies that Site and contains no credentials; local execution does not require a Sites connection. The initial GitHub import comes from Site source commit `ce7728e84d85422322ea8e3af661ea7d5f904ae2`.

## GitHub Pages build

A static build of the same atlas is published with GitHub Pages at <https://quadrin.github.io/AncientHebrewTexts/copper_scroll/atlas-site/>. It renders the same `Atlas` component, data, maps and ground views, without the Next.js/vinext server shell or ChatGPT sign-in. The built files are committed in `../atlas-site/`.

To rebuild it after a change, from this directory:

```sh
corepack pnpm install --frozen-lockfile
corepack pnpm exec vite build --config vite.pages.config.ts
```

After building, delete `../atlas-site/research/qumran-video-comparison.html` before committing. It embeds frames from a watermarked stock-video preview and archival photographs whose reuse terms have not been checked, so it is left out of the public build until that use is cleared. The page that links to it, `research/entry21-comparison.html`, is published.

`pages/index.html` and `pages/main.tsx` are the static entry. `vite.pages.config.ts` sets the Pages base path and writes to `../atlas-site/`. The MapLibre worker URL follows the build's base path, so it works both on the hosted Site and under the Pages sub-path.

## Research

Follow [`../AGENTS.md`](../AGENTS.md) to investigate and map specific sites and individual features. Add candidate coordinates, feature outlines and spatial hypotheses with their sources, assumptions and uncertainty. Update their precision as evidence improves.

The data comes from `quadrin/AncientHebrewTexts`, research snapshot `5220e8bd008cba1ade10ddce42c6c577170206ba` (28 September 2026). The committed CSV files in `research/` preserve the input tables. Run `python research/build_atlas.py` to regenerate `app/atlas-data.json`.

Descriptions are short factual editorial paraphrases, not quoted translations. Hebrew labels reproduce names or selected editorial readings from the public lexicon. Current confidence follows the revised Phase 5 assessment: Siloam is medium and conditional; Ramat Rahel is low; Tell el-Qos is a weak alternative. Kh. Ibziq (entry 59) is lowered to low after Zertal's survey (29 September 2026, a dated revision in `research/build_atlas.py`). A second run the same day updated the evidence texts for entries 31, 40, 57 and 59 (Magen on Gerizim, Garbrecht & Peleg, *HA* 40, Jeremias) without changing any confidence; see `../source_extractions_2026-09-29.md`. Three places have no coordinates and remain unpinned.

Current pins use the gazetteer's site anchors. Filled areas with dashed outlines show their approximate positional precision. Each geometry should state whether it represents a site anchor, an observed feature footprint or a modeled candidate area. The selected candidate is shaded copper, other candidates sage, in both map dimensions. Selection fits the shaded area, including small archaeological anchors. The current Siloam coordinate anchors the pool complex; individual pool, outlet and trough candidates require their own feature records. The public index contains a subset of the candidates discussed in the unpublished full assessment.

## The Scroll view

**Scroll**, beside 2D, 3D and Ground, replaces the map with the whole text of the scroll in the atlas's parchment style. A strip of bronze tablets selects a column, laid out right to left like the scroll; the three sheets are separated. Each line gives the English, the line number and the Hebrew. Entry headings use the register's style; selecting one selects that entry in the register, the map and the field note, and the view stays on the scroll. Selecting an entry elsewhere brings its lines into view. Words and underlined phrases open the same reading cards as the field note. `#entry-21/scroll` opens the view at an entry; `#scroll` opens it at the current one. The field note's **Open the scroll** and the footer's **Read the scroll** switch to this view.

## The photographic reader

**Read the photograph** in Scroll opens a photograph of original strip 13 with eight provisional word tracings in VII 7–11. **Grooves** (the default), **Relief** and **Photo** switch between a groove map, a contrast-enhanced grey image and the photograph itself. Each letter is traced: solid strokes follow grooves the photograph shows; dashed strokes are shown only by Puech's radiograph of the strip. Select a word on the photograph or the word strip to see Hebrew lettering, glosses, the project translation and editorial notes. Pan, zoom, adjust trace opacity or hold the comparison control to inspect the photograph alone. **Full scroll text** returns to the existing column reader. The direct link is `#scroll/photo`; existing entry links retain their typeset view. Coverage and sources are recorded in [the photographic reader note](research/photographic_reader.md).

## The text in each field note

The Text tab in each field note shows the entry's lines of the scroll: the Hebrew, from Martin G. Abegg Jr.'s transcription in the ETCBC Dead Sea Scrolls dataset (CC BY-NC 4.0), and an English translation written for this project. Selecting a Hebrew word shows its parts, their meanings and any notes; selecting an underlined phrase shows how the editions read it, with pages from the research files. The data is `app/atlas-text.json`, loaded as a separate chunk the first time a field note opens. `../tools/build_scroll_notes.py` writes it from `../text/`, together with the text and translation page (`../web/`); rebuild both after changing the translation or the notes. The full scroll, column by column, is at <https://quadrin.github.io/AncientHebrewTexts/copper_scroll/web/>.

## Map

MapLibre GL JS renders an OpenFreeMap basemap based on OpenMapTiles and OpenStreetMap, with Mapterhorn elevation tiles. An OpenStreetMap raster fallback handles failure to obtain the primary style. The map uses modern geographical data, not a reconstructed ancient coastline or road network. The 3D control enables actual terrain and a pitched camera, with 1–3× vertical exaggeration.

Map source attribution remains visible. MapLibre's local worker and shared module preserve the package license headers; they come from installed version 6.10.0. If upgrading MapLibre, refresh both files in `public/maplibre/` together.

MapLibre owns each marker's outer `site-marker` element, including its absolute position, transform and terrain visibility classes. Selection changes only the child button. Do not overwrite the outer element's class list or set relative positioning on it: this introduces document-flow offsets and makes pins drift during zoom. Settlement labels use the vector tile `place` category rather than relying on style-layer name prefixes.

## Interaction

- Select an entry, a map pin or a candidate card to link the register, evidence and map.
- Search ancient names, Hebrew labels, entry descriptions or modern candidate names.
- Filter by region or switch between the four-entry Highlights view and all 61 entries.
- Sort the register by confidence, ancient name, primary candidate name, region or scroll order. Confidence uses the highest candidate confidence and breaks ties in scroll order. Candidate cards sort independently by confidence, alphabetical name or preferred status; sorting never changes the selection.
- Switch 2D/3D, adjust relief, zoom, orient north, fit the entry or return to the regional view.
- Ground view provides four real photographs with anchored highlight polygons, pan/zoom, keyboard navigation, feature notes and image credits. Source URLs and licenses are recorded in `app/atlas-scenes.json`; images load directly from Wikimedia Commons. Qumran shows an actual aqueduct outlet. Doq and Choziba show terrain context; Siloam shows the larger southern pool, distinguished from the smaller Silwan outlet candidate. The current scenes are photographs with annotated visible features; record camera geometry and the evidence for each candidate highlight when adding scenes.
- A separate Google Street View link searches near each mapped anchor. Coverage varies and atlas overlays are not injected into external Google imagery. Other candidates show an explicit photographic coverage gap and shortcuts to the four available scenes.
- Mobile layouts separate register, map and folio into three accessible views.
- Entry hash URLs restore the selected entry.
- Supported WebMCP browsers expose `navigate_scroll_entry` through the same selection handler.

## Validation

The data generator verifies entry and place counts and candidate references. TypeScript and production build checks validate the implementation. The supervised preview service was unavailable in the creation session, so browser interaction, visual rendering and WebMCP runtime validation could not be completed there.

The Site uses the package manager, build scripts and hosting manifest supplied by the Sites starter.


## Feature evidence review

Entries 21, 32, 49, 31 and 55 now have a “Compare features & evidence” dialog. It separates reading, site and exact-feature judgments, exposes source dependencies/access gaps, and states discriminating checks. Other candidates are explicitly marked as not yet assessed on separate axes. Site confidence and existing sorting remain unchanged.

Edit `app/atlas-evidence.json` for the shared Site/Pages content. The narrative dossier is in `research/feature_investigation.md`; its repository-wide copy is `../feature_investigation.md`. Keep both copies aligned. The constraint register is `research/feature_constraints.csv`, mirrored in `../tables/feature_constraints.csv`. Refine locality envelopes into feature outlines or modeled candidate areas as sources permit, recording the geometry method and positional uncertainty.
