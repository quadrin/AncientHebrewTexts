# The Copper Scroll Atlas

An interactive atlas of the 61 Copper Scroll entries, paired with 37 candidate places from the research repository. The interface uses a parchment register, an inset map and an entry folio.

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

`pages/index.html` and `pages/main.tsx` are the static entry. `vite.pages.config.ts` sets the Pages base path and writes to `../atlas-site/`. The MapLibre worker URL follows the build's base path, so it works both on the hosted Site and under the Pages sub-path.

## Research

The data comes from `quadrin/AncientHebrewTexts`, research snapshot `5220e8bd008cba1ade10ddce42c6c577170206ba` (28 September 2026). The committed CSV files in `research/` preserve the input tables. Run `python research/build_atlas.py` to regenerate `app/atlas-data.json`.

Descriptions are short factual editorial paraphrases, not quoted translations. Hebrew labels reproduce names or selected editorial readings from the public lexicon. Current confidence follows the revised Phase 5 assessment: Siloam is medium and conditional; Ramat Rahel is low; Tell el-Qos is a weak alternative. Three places have no coordinates and remain unpinned.

Pins represent site-level anchors. Filled areas with dashed outlines visualize the gazetteer's approximate precision; they are not surveyed boundaries or deposit locations. The selected candidate is shaded copper, other candidates sage, in both map dimensions. Selection fits the shaded area, including small archaeological anchors. The Siloam coordinate remains an inherited complex-level anchor, not a selected trough or pool. The public index contains a subset of the candidates discussed in the unpublished full assessment.

## Map

MapLibre GL JS renders an OpenFreeMap basemap based on OpenMapTiles and OpenStreetMap, with Mapterhorn elevation tiles. An OpenStreetMap raster fallback handles failure to obtain the primary style. The map uses modern geographical data, not a reconstructed ancient coastline or road network. The 3D control enables actual terrain and a pitched camera, with 1–3× vertical exaggeration.

Map source attribution remains visible. MapLibre's local worker and shared module preserve the package license headers; they come from installed version 6.10.0. If upgrading MapLibre, refresh both files in `public/maplibre/` together.

MapLibre owns each marker's outer `site-marker` element, including its absolute position, transform and terrain visibility classes. Selection changes only the child button. Do not overwrite the outer element's class list or set relative positioning on it: this introduces document-flow offsets and makes pins drift during zoom. Settlement labels use the vector tile `place` category rather than relying on style-layer name prefixes.

## Interaction

- Select an entry, a map pin or a candidate card to link the register, evidence and map.
- Search ancient names, Hebrew labels, entry descriptions or modern candidate names.
- Filter by region or switch between the four-entry shortlist and all 61 entries.
- Sort the register by confidence, ancient name, primary candidate name, region or scroll order. Confidence uses the highest candidate confidence and breaks ties in scroll order. Candidate cards sort independently by confidence, alphabetical name or preferred status; sorting never changes the selection.
- Switch 2D/3D, adjust relief, zoom, orient north, fit the entry or return to the regional view.
- Ground view provides four real photographs with anchored highlight polygons, pan/zoom, keyboard navigation, feature notes and image credits. Source URLs and licenses are recorded in `app/atlas-scenes.json`; images load directly from Wikimedia Commons. Qumran shows an actual aqueduct outlet. Doq and Choziba show terrain context; Siloam shows the larger southern pool, distinguished from the smaller Silwan outlet candidate. No photo is presented as a verified 360-degree panorama or exact deposit identification.
- A separate Google Street View link searches near each mapped anchor. Coverage varies and atlas overlays are not injected into external Google imagery. Other candidates show an explicit photographic coverage gap and shortcuts to the four available scenes.
- Mobile layouts separate register, map and folio into three accessible views.
- Entry hash URLs restore the selected entry.
- Supported WebMCP browsers expose `navigate_scroll_entry` through the same selection handler.

## Validation

The data generator verifies entry and place counts and candidate references. TypeScript and production build checks validate the implementation. The supervised preview service was unavailable in the creation session, so browser interaction, visual rendering and WebMCP runtime validation could not be completed there.

The Site uses the package manager, build scripts and hosting manifest supplied by the Sites starter.


## Feature evidence review

Entries 21, 32, 49, 31 and 55 now have a “Compare features & evidence” dialog. It separates reading, site and exact-feature judgments, exposes source dependencies/access gaps, and states discriminating checks. Other candidates are explicitly marked as not yet assessed on separate axes. Site confidence and existing sorting remain unchanged.

Edit `app/atlas-evidence.json` for the shared Site/Pages content. The narrative dossier is in `research/feature_investigation.md`; its repository-wide copy is `../feature_investigation.md`. Keep both copies aligned. The constraint register is `research/feature_constraints.csv`, mirrored in `../tables/feature_constraints.csv`. Feature polygons remain approximate locality envelopes until surveyed source geometry is obtained.
