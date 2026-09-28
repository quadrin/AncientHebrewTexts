# Qumran aqueduct: survey comparison and registration check

Reviewed 28 September 2026. Follow-up to the [Ilan–Amit plan review](ilan_amit_1989_plan_review.md).

**Result:** a later field-survey map has been recovered and checked. It adds physical features to investigate, but the available control does not justify precise geographic highlights. No site confidence, feature coordinates or public map geometry has been changed.

## A later survey recovered

Philip Reeder and Harry Jol, “Water Resource Utilization at the Qumran Archaeological Site Israel,” *Papers of the Applied Geography Conferences* 29 (2006), pp. 224–234. The [publisher’s contents](https://applied.geog.kent.edu/AGCPapers/2006/AGC2006.htm) links to an [obsolete Flash reader](https://applied.geog.kent.edu/AGCPapers/2006/P224-234/index.html). Its publicly served `Files/1.swf` through `Files/11.swf` contain the pages. Static vector and bitmap extraction recovered the text and figures without executing Flash. Figure 4 was inspected directly at its embedded 1380 × 1044 resolution.

The survey was conducted in 2002. Page 228 describes total-station measurements supplemented by compass, inclinometer and tape in difficult terrain and tunnels; the drafted map was field checked. Figure 4 (p. 229) distinguishes restored channel, preserved channel, collapse, two tunnels and estimated pre-slump route. Page 231 reports a roughly one-metre surviving wall interpreted as a dam, a three-metre boulder, a pothole, and an overflow cut at the upstream end. These are reported observations and interpretations, not new observations by this project. No grid, datum or benchmark-coordinate table is published in the figure. The earthquake and rebuilding sequence on pp. 229–230 is explicitly interpretive.

## Consequence for the candidate features

Ilan–Amit's point 3 remains the first functional comparison for the conduit head. Their point 4 is a proposed dam across the main basin, expressly lacking remains in their account. The later survey's upstream wall must be held as a **separate feature pending correlation**. Similar hydraulic roles do not prove these authors describe the same installation. Nor does a reported rock establish the scroll's partly restored stone landmark.

The two plans also differ in their portrayal and interpretation of the upstream branches. Do not match their tunnel numbers merely by sequence: Ilan–Amit 10/11 and the later Tunnel 1/2 require position, section, elevation and flow-direction comparison. The [feature comparison table](qumran_survey_crosswalk.csv) records these unresolved correspondences.

The later survey adds evidence for physical waterworks, not independent confirmation of Qumran = Sekakah, a named reservoir, a scroll landmark or a deposit. Keep those propositions separate.

## Why the older plan cannot be overlaid as one scaled image

Ilan–Amit Fig. 1 visibly breaks the long plain section near point 18. Its accompanying prose describes more than 200 m between the cliff and settlement. The drawing therefore cannot support one uniform transformation over both the cliff section and the compressed plain section. Its tunnel and regional insets also have separate scales. A north arrow and scale bar alone do not provide geographic control.

## Aerial registration experiment

A north-up copy of Magen–Peleg 2007 Fig. 35, reproduced at [this image URL](https://www.deadseaquake.info/wp-content/uploads/2022/01/Fig35_MagenAndPeleg2007.png), was compared with [Esri World Imagery](https://server.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer). This tests a possible photographic bridge to the older plan; it does not directly georeference Ilan–Amit's drawing.

The imagery mosaic comprises 25 cached tiles at zoom 17, starting at x = 78443, y = 53336. It is 1280 × 1280 pixels in the standard Web Mercator tile grid. Service attribution: Esri, Vantor, Earthstar Geographics, and the GIS User Community. Imagery acquisition date and absolute positional accuracy were not established. Pixel spacing is approximately 1.016 ground metres at Qumran; that is not an accuracy claim.

SIFT matching produced 22 tentative pairs. An affine RANSAC fit retained only five, concentrated in the western portion of the historical photograph. Training RMSE was 1.525 destination pixels. Leave-one-out errors among those five preselected pairs ranged from 3.16 to 9.15 pixels. These are internal diagnostics, not independent validation. Relief, camera perspective and changes to the site further limit an affine fit.

**Decision: reject this fit for publishing feature coordinates or boundaries.** There are no independently surveyed check points and insufficient distributed control. Its small training residual must not be reported as metre-level accuracy. The [audit data](registration/qumran_aerial_trial.json) preserve the actual pairs, transform and limitations; the [verification script](registration/check_trial.py) recomputes the diagnostics without source images.

## Specific next data needed

Obtain the original 2002 survey observations or CAVEPLOT data, benchmark coordinates, horizontal/vertical datum, and station descriptions from the project archive. The published map credits Philip Reeder as its drafter and identifies the John and Carol Merrill Qumran Excavations Project. No request has been sent.

Use those records to locate the later wall and rock, then correlate the older intake and tunnels through distributed stable points. Keep independent points out of the fit to test it. If geographic control remains unavailable, retain a plan-relative comparison and the broad site marker. A coordinate-free source plan is still useful evidence; it is not a precise map overlay.

The reviewed source pages and aerial imagery have not been copied into the public repository. This report records the research state before the subsequent search for original survey data.
