# TIR Iudaea–Palaestina: digital-copy search

## Copper Scroll Atlas

The Copper Scroll project identifies ancient place names and tests specific locations against textual, archaeological and geographic evidence. Research includes individual caves, cisterns, channels, pools, tombs and other described features, with coordinates or bounded candidate areas and explicit uncertainty. See the [research instructions](copper_scroll/AGENTS.md).

The interactive [Copper Scroll Atlas source](copper_scroll/atlas/README.md) pairs 61 scroll entries with 37 candidate places. It includes 2D maps, 3D terrain, approximate candidate shading, confidence and name sorting, four annotated ground photographs, and each entry's lines of the scroll with a translation and the editions' readings. See the atlas README for local setup and research provenance.

[Atlas on GitHub Pages](https://quadrin.github.io/AncientHebrewTexts/copper_scroll/atlas-site/) (public, static build) · [Hosted atlas](https://copper-scroll-atlas.alexkesin.chatgpt.site) · Access to the hosted Site follows its existing sharing settings.

## Copper Scroll research page

The [Copper Scroll research page](https://quadrin.github.io/AncientHebrewTexts/copper_scroll/web/) opens with the full text of the scroll, column by column, with an English translation. Each Hebrew word opens its meaning and the editions' readings, and each entry opens its place identification. The Hebrew is Martin Abegg's transcription from the ETCBC Dead Sea Scrolls dataset (CC BY-NC 4.0); the translation and notes were written for this project. The page then summarises the desk research in `copper_scroll/`: every proposed identification of the scroll's named places, scored against the text and the published archaeology, with site-level maps and tests of the Greek letters. Source: [`copper_scroll/web/index.html`](copper_scroll/web/index.html); notes and tables: [`copper_scroll/README.md`](copper_scroll/README.md).

Checked 27 September 2026. No complete publicly readable book, institutional ebook, or complete full-resolution map sheet was verified. Five publicly downloadable map details were verified in Peter Pilhofer's lecture PDFs: three from the North sheet and two credited to the TIR overview map. This package preserves those source PDFs and their embedded images, plus a Roman-roads figure credited to the 1994 volume in an Edinburgh thesis.

## Fourth search: further North-sheet reproduction

Joseph Patrich, “City and Its Countryside. An Archaeological-Cartographical Approach,” hosted by the Institut d’Estudis Catalans:
https://publicacions.iec.cat/repository/pdf/00000290/00000087.pdf

The 17-page PDF downloaded successfully. On PDF p. 2 / printed p. 50, figure 2 shows a grayscale TIR-based map covering Apollonia, Caesarea, Mount Carmel, Legio and part of Samaria. The caption names Kenneth G. Holum’s proposed Caesarea administrative region and credits cartography to Joseph Patrich, based on TIR. The first page explicitly identifies the 1994 Tsafrir–Di Segni–Green volume. The author overlays administrative boundaries, so the illustration is an annotated regional extract rather than an unaltered full sheet. Its embedded JPEG is 1887 × 2943 pixels. I visually checked the page and extracted the original embedded image without resampling. The map page and preceding attribution page are included in `Patrich_TIR_map_and_attribution.pdf`; the image is `north_carmel_caesarea_patrich_annotated.jpeg`.

Further checks this round:

- DAI Zenon record https://zenon.dainst.org/Record/000157454 describes the book with five folded maps, with reference holdings in Rome (`Lex 925 [19] (Israel)`) and Damascus (`Dam KAR TIR Pal`). Record https://zenon.dainst.org/Record/000899183 gives the Frankfurt RGK reference copy (`Jt 19`). Both live pages were retrieved and inspected. Neither exposes a book/map download.
- Survey of Israel https://www.gov.il/en/service/purchasing_maps explicitly describes paper-map ordering. It does not list these historical sheets or establish a digital supply route.
- Carmen Obied’s Southampton thesis, https://eprints.soton.ac.uk/397264/, cites TIR as a supplementary archaeological source. The landing page lists one thesis PDF, with no supplementary map file. The exact linked PDF returned 404 through web retrieval; no map reproduction was verified.
- Adam Pažout’s 2026 article https://doi.org/10.1007/s10816-026-09766-4 links a new Zenodo deposit, https://doi.org/10.5281/zenodo.17953712. Its data-availability statement describes terrain rasters, road vectors and model outputs; it does not identify TIR raster scans. The files have not been checked and this is not a TIR-file discovery.

The complete gazetteer and all five complete folded maps remain unverified for public digital access. No enquiries or orders were sent.

## Third search: additional map and file-history checks

### Roman-roads map reproduction credited to the 1994 volume

G. Findlater, *Imperial Control in Roman and Byzantine Arabia: A Landscape Interpretation of Archaeological Evidence in Southern Jordan* (University of Edinburgh, 2004), printed p. 380 / PDF p. 385, figure 59, reproduces a map headed “Roman Roads in Judaea and Arabia.” Its caption credits Tsafrir et al. 1994. The thesis PDF downloaded successfully and the figure was visually checked. It shows a black-and-white regional road network; this is not a verified reproduction of any of the five folded color sheets.

- Thesis: https://era.ed.ac.uk/bitstream/1842/9789/1/Findlater2004.pdf
- Catalogue: https://era.ed.ac.uk/handle/1842/9789
- Packaged page: `Findlater_2004_fig59_p380.pdf`
- Original embedded scan image: `roads_map_credited_to_TIR_Findlater.jpeg`, 1611 × 2300 pixels, including page caption and margins.

Kinneret College's Roman Roads and Milestones project also exposes a one-page PDF with this map title:
https://milestones.kinneret.ac.il/wp-content/uploads/2018/02/ROLL_ROMAN_ROAD.pdf
The web retrieval service identified it as a one-page PDF. A direct local download returned 403, so that file is linked rather than packaged; its native image resolution was not verified. It is a related Roman-roads overview, not established as one of the five TIR pocket maps.

The same project hosts a paper with a further TIR-based Caesarea/Legio detail (figure 2, printed p. 50):
https://milestones.kinneret.ac.il/wp-content/uploads/2018/02/Tepper_Legio.pdf
Its indexed caption credits the 1994 TIR map. Direct retrieval returned 403; not packaged or counted as a newly inspected image.

Pilhofer's 2016/17 lecture also reproduces “Von Jerusalem nach Gaza” on PDF p. 5 / printed p. 213:
https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung16/Paragraph21.pdf
Downloaded and visually inspected. Its image is again 760 × 1160 pixels, covering the same area as the already packaged older lecture crop; it is not an additional complete map.

### GIS repository history checked

Public version-history endpoint:
https://uj.rodbuk.pl/api/datasets/:persistentId/versions?persistentId=doi:10.26106/YNTA-FF42

It exposes versions 1.0, 2.0, 3.0, 4.0 and 4.1. None lists either source TIFF as a file. The older roads archive, https://uj.rodbuk.pl/api/access/datafile/1193, was downloaded and is byte-for-byte identical to the previously inspected DSpace archive. It contains shapefile components and a README. The newer roads archive is file 5074. Thus the two named TIFFs remain a specific enquiry lead, not a public-file discovery.

### Zurich map-set record

https://uzb.swisscovery.ch/discovery/fulldisplay?adaptor=Local+Search+Engine&context=L&docid=alma990019194690205508&lang=de&vid=41SLSP_UZB%3AUZB

The live public record was opened in a browser. It describes five maps plus X + 263 pages of explanatory text, dated 1993–1994, and lists physical holdings at ZB Kartensammlung, call number `LKS 91 ASC 501: HI 36`. It exposes no digital-viewer or download link; ordering options require sign-in. The record explicitly numbers the sheets using the book's p. V: 1 Sinai overview; 2 North; 3 South; 4 Synagogues; 5 Churches. These publication numbers must not be assumed to match the Polish project's locally assigned TIFF filenames.

### Academy numeric-file inspection

From the previously obtained Wayback index, I selected all 48 purely numeric PDF filenames with archived payload sizes above 2 MB and retrieved their current public URLs. Forty-five contained readable, nonempty PDFs. Two returned zero bytes; one parsed as a zero-page PDF without embedded attachments. Text extraction, page counts and visual inspection of image-only first pages identified newsletters, reports, event notices and other Academy publications. None was the requested gazetteer or a folded TIR map. This was a bounded check of 48 candidates, not an exhaustive inspection of the Academy repository. The two JSON inspection logs are included under `evidence/`.

### Additional exclusions

Di Segni's Academia profile lists the matching title under *Journal of the American Oriental Society* (1998), with text naming reviewer Anson F. Rainey. It is a review, not the book scan:
https://independent.academia.edu/LeahDiSegni

The Hebrew University church corpus has a bibliographic entry for the complete book, database entry 8622. Indexed content gives a citation without a file link; live requests to its bibliography pages returned a server error. No accessible book was verified there.

An Internet Archive advanced search for `title:(tabula imperii romani)` returned three records: two historical maps and the 1976 Naissus/Dyrrhachion/Scupi/Serdica/Thessalonike volume. None was Iudaea–Palaestina.

## Second search: new findings

The complete book and complete sheets remain unfound as publicly readable/downloadable files. The following findings are additions to the first search, not full-sheet or book-scan successes.

### Identifiable TIFF source files in a university research project

Michał Marciak, Daniel Sobczyński and colleagues, “Jesus’ Itineraries in the Light of GIS Research: Three Case Studies,” The Biblical Annals 15/3 (2025), 551–592, state on printed p. 558 that their project digitized relevant TIR maps. The referenced volume is specifically Tsafrir–Di Segni–Green 1994.

- Article: https://czasopisma.kul.pl/index.php/ba/article/view/18331
- PDF: https://czasopisma.kul.pl/index.php/ba/article/download/18331/16194/101310
- Institutional PDF: https://ruj.uj.edu.pl/server/api/core/bitstreams/b0283188-c8bc-4fc1-9f3b-bd96a393f1b5/content
- Dataset: https://ruj.uj.edu.pl/handle/item/307393
- DOI: https://doi.org/10.26106/ynta-ff42
- Older public roads ZIP: https://ruj.uj.edu.pl/server/api/core/bitstreams/a4ebdf92-30a6-4c7e-864d-bfb98a381e1c/content
- Newer Dataverse record: https://uj.rodbuk.pl/dataset.xhtml?persistentId=doi:10.26106/YNTA-FF42
- Public metadata: https://uj.rodbuk.pl/api/datasets/:persistentId/?persistentId=doi:10.26106/YNTA-FF42
- Newer roads ZIP: https://uj.rodbuk.pl/api/access/datafile/5074

I downloaded the older ZIP and inspected the DBF source field. It explicitly names `Tsafrir_map3.tiff` (53 road features) and `Tsafrir_map4.tiff` (16 road features). This is evidence of specific raster source filenames used by the project. It does not establish their resolution, whether they cover complete sheets, or which sheets the numbers denote. The ZIP contains shapefile components and a README, not the TIFFs. The updated Dataverse deposit, version 4.1, lists 16 ZIP files containing research datasets; no standalone TIR raster or book file is listed. The older repository record lists nine ZIPs. Searches for the exact TIFF names found no public download.

The public dataset ZIP and a plain-text extraction of its source-field values are included in this package. This is a concrete existing-file enquiry lead: ask the project team whether they can lawfully supply the two TIFFs or identify their source institution and reproduction route. Email addresses printed in the 2025 article: Daniel Sobczyński, daniel.sobczynski@uj.edu.pl; Michał Marciak, michal.marciak@uj.edu.pl. No contact was made.

### Additional downloadable map excerpt

https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung/Paragraph29.pdf

PDF page 4, printed page 152, figure 2, “Von Jerusalem nach Gaza.” The footnote explicitly credits the 1994 TIR overview map. I downloaded and visually checked it. The embedded grayscale image is 760 × 1160 pixels and appears sideways on the page. The source PDF and original embedded JPEG are included. It remains a crop, not a full sheet.

Another publicly displayed crop appears in the European Association of Archaeologists’ Winter 2026 project overview:
- https://www.e-a-a.org/EAA/News___Publications/TEA_87_content/Project_Overview.aspx
- Figure 2 image: https://www.e-a-a.org/images/eaa/TEA%2087/po2.jpg
The caption explicitly identifies its upper panel as a TIR Iudaea/Palaestina detail. The web retrieval tool could display it, but a direct local download returned HTTP 403; it is linked here, not packaged. The related Itiner-e deposit https://zenodo.org/records/17122148 contains road vectors, bibliography and data documentation, not the original TIR sheets.

### Hebrew University: all five separately catalogued sheets

The live public HUFind Geo catalogue returned all five as physical map records dated 1993. I opened each full record. Each offers Get It and physical holdings; none exposed View Online, a digital viewer, or an image-download link during the unauthenticated check. Their existence is not evidence of digitization. Catalogue header warns that guest access displays partial results.

| Sheet | Alma record ID | Scale | Physical copies shown |
|---|---|---|---|
| North | 990020176730203701 | 1:250,000 | 3 |
| South | 9920743962803701 | 1:250,000 | 2 |
| Eretz Israel and Sinai | 9920743962703701 | 1:1,000,000 | 3 |
| Churches | 990020126430203701 | 1:400,000; Negev/Sinai inset 1:2,000,000 | 3 |
| Synagogues | 9920743962903701 | 1:400,000 | 3 |

Exact record URLs:
- https://huji.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma990020176730203701&context=L&vid=972HUJI_INST:HUJI_CARTO&lang=en
- https://huji.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma9920743962803701&context=L&vid=972HUJI_INST:HUJI_CARTO&lang=en
- https://huji.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma9920743962703701&context=L&vid=972HUJI_INST:HUJI_CARTO&lang=en
- https://huji.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma990020126430203701&context=L&vid=972HUJI_INST:HUJI_CARTO&lang=en
- https://huji.primo.exlibrisgroup.com/discovery/fulldisplay?docid=alma9920743962903701&context=L&vid=972HUJI_INST:HUJI_CARTO&lang=en

Location: Humanities & Social Sciences Library, second-floor Map Collection. Call-number family: MAP KC 900B (HIS) [9], followed by sh. north / sh. south / Eretz Israel and Sinai / churches / synagogues. The North record identifies the associated book as DS 103.5 T78.

HUJI’s https://geohub.huji.ac.il/ states that scanned maps can be ordered, sometimes for a fee, and that HUJI members can download available files via the catalogue. This is a general service, not confirmation these five maps are scanned. Its catalogue is therefore an additional authorized reproduction-enquiry route.

### Book: additional access checks

Google Books has alternative identifiers `8XJtAAAAMAAJ` and `F6WStAEACAAJ` as well as the supplied `T2eMxgEACAAJ`. The first displays the same Michigan origin and August 25, 2008 digitization date. Google’s public ViewAPI returned `preview: noview`, `can_download_pdf: false`, and `can_download_epub: false` for all three. No page restrictions were bypassed.

- https://books.google.com/books?id=8XJtAAAAMAAJ
- https://books.google.com/books?id=F6WStAEACAAJ
- Public metadata query: https://books.google.com/books?jscmd=viewapi&bibkeys=8XJtAAAAMAAJ,T2eMxgEACAAJ,F6WStAEACAAJ&callback=ProcessGBSBookInfo

Internet Archive advanced catalogue searches for the ISBN and the TIR title combined with Iudaea/Palaestina/Tsafrir returned no matching item. Broader creator results did not reveal this book. These are scoped negative findings, not proof that no copy exists online.

Other checks: TIR-FOR’s publication page https://tir-for.iec.cat/index.php/publicacions/ lists this volume as H/I-36 but provides no full-text link. Academy file https://www.academy.ac.il/SystemFiles/24738.pdf is a ten-page Onomasticon preliminary excerpt, not the TIR book. The 2022 Academy catalogue’s “digital volume—in preparation” refers to Onomasticon volume III, not TIR. A related Polish 2022 book PDF was inspected and did not supply a complete TIR sheet.

## Verified downloadable map details from the first search

Host: Peter Pilhofer's website, https://www.die-apostelgeschichte.de/
Course page: https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung18/vorlesung18.html
Course: Die Apostelgeschichte III, winter semester 2018/19.

| Image in this package | Source PDF | PDF page / printed page | Coverage | Embedded resolution |
|---|---|---|---|---|
| north_galilee_ptolemais | Paragraph65.pdf | 4 / 656, figure 13 | Acre/Ptolemais, Galilee, Sea of Galilee region; displayed sideways in source | 2544 × 3508 |
| north_caesarea_samaria | Paragraph66.pdf | 4 / 664, figure 14 | Caesarea and Samaria | 3508 × 2544 |
| north_samaria_jerusalem | Paragraph66.pdf | 5 / 665, figure 15 | Southern Samaria, Jerusalem, northern Dead Sea area | 3508 × 2544 |
| overview_jerusalem_caesarea | Paragraph71ff.pdf | 6 / 720, figure 19 | Jerusalem–Caesarea and adjacent Jordan Valley | 723 × 648 |

Direct source files:
- https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung18/Paragraph65.pdf
- https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung18/Paragraph66.pdf
- https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung18/Paragraph71ff.pdf
- https://www.die-apostelgeschichte.de/lehrveranstaltungen/vorlesung18/Titelei.pdf

The illustration credits in Titelei.pdf, printed pages xvi–xvii, explicitly attribute figures 13–15 to the TIR North sheet, edited by Tsafrir, Di Segni and Green, Jerusalem 1994. Figure 19 is credited to an excerpt of the TIR overview map. Its identity as the separate Eretz Israel and Sinai sheet was not independently established.

All four source PDFs returned actual PDF bytes without authentication. The four map pages were rendered and visually checked. The images in this package were extracted at their embedded resolution without resampling, recoloring or reconstruction. They are cropped reproductions and omit the complete sheets' borders/legends. No open reuse licence was established; this package records access and attribution, not publication permission.

## LMU: Beilage I investigation

Current record: https://edoc.ub.uni-muenchen.de/8200/
PDF: https://edoc.ub.uni-muenchen.de/8200/1/Fortner_Sandra.pdf
DOI: 10.5282/edoc.8200
URN: urn:nbn:de:bvb:19-82009

The record dates the dissertation/oral examination to 5 July 2005 and its electronic deposit to 13 March 2008.

Public file metadata:
- EPrints document ID: 4794
- EPrints file ID: 8850
- Filename: Fortner_Sandra.pdf
- File size: 20,211,220 bytes in EP3 XML
- MD5: 132b69fbdcca632c48e33aff8253b0e1
- Access: public

Inspected exports:
- https://edoc.ub.uni-muenchen.de/cgi/export/8200/XML/edoc-eprint-8200.xml
- https://edoc.ub.uni-muenchen.de/cgi/export/eprint/8200/DIDL/ediss-eprint-8200.xml
- https://edoc.ub.uni-muenchen.de/cgi/export/eprint/8200/XMETADISSPLUS/ediss-eprint-8200.xml
- https://edoc.ub.uni-muenchen.de/cgi/oai2?verb=GetRecord&metadataPrefix=oai_dc&identifier=oai:edoc.ub.uni-muenchen.de:8200

EP3 XML contains one document and one file. DIDL and OAI identify the same PDF. XMetaDissPlus explicitly declares fileNumber=1. Inspection of the PDF found 435 A4 pages and zero embedded attachments. These checks complement the prior inspection that found the Beilage I credit but no full North sheet.

Archive evidence:
- https://web.archive.org/web/20080518194407/http://edoc.ub.uni-muenchen.de:80/8200/
- https://web.archive.org/cdx/search/cdx?url=edoc.ub.uni-muenchen.de/8200/*&output=json&filter=statuscode:200&collapse=urlkey

The May 2008 archived landing page links only Fortner_Sandra.pdf. The CDX response has four unique entries: landing page, PDF and two generated thumbnails. The old /archive/00008200/ route resolves to the current record; its separate CDX query returned an empty list. No separately exposed Beilage I file was found. This does not exclude a staff-held deposit file or a physical enclosure.

Concrete LMU follow-up: ask repository staff whether the original 2008 deposit or the physical copies contain Beilage I, using document 4794, eprint 8200 and print shelfmarks 0001/UMC 16841, 0001/UMC 16842 and 0001/UMC 16843. Contact page: https://edoc.ub.uni-muenchen.de/contact.html

## NLI: all five sheets remain unresolved for digital access

| Component | Record | Additional verified catalogue identifier |
|---|---|---|
| North and South | https://www.nli.org.il/en/maps/NNL_ALEPH990040826280205171/NLI | Israel 362; 94.3 × 69 cm each |
| Eretz Israel and Sinai | https://www.nli.org.il/he/maps/NNL_ALEPH990040824310205171/NLI | Israel 360; one color sheet, 68 × 44 cm |
| Churches | https://www.nli.org.il/en/maps/NNL_ALEPH990040826190205171/NLI | System 990040826190205171 |
| Synagogues | https://www.nli.org.il/en/maps/NNL_ALEPH990040824190205171/NLI | Israel 359 |

NLI book record discovered in indexed results: https://www.nli.org.il/en/books/NNL_ALEPH990012863420205171/NLI

Search-indexed content for the North/South record shows Map, Location & Availability and Save, plus Prohibition of Copying, without a Download action. Some search hits show download controls belonging to OTHER maps whose related-items lists mention TIR; these are not evidence of TIR downloads.

Direct requests to the four records returned 403. A browser visit to the North/South record showed a Cloudflare human-verification challenge. No challenge was solved and no access restriction was bypassed. Consequently no live viewer, IIIF manifest, Rosetta IE/FL identifier or full-resolution file was verified for any of the four records. Catalogue presence alone does not establish that a digital master exists.

Official reproduction route, verified from NLI's indexed service page:
https://www.nli.org.il/en/at-your-service/reference/view-and-order-items
Use the section "Ordering a Digital Scan or File by Email". NLI directs users to the catalogue record's scan-request options or its scan-request form; each item requires a separate request. Supply the four record IDs and specify both North and South under the two-sheet record. Ask first whether existing digital masters can be supplied. NLI checks copyright and other limitations before fulfillment. The published service targets are 14 business days after payment for standard service or 3 for express; availability for these particular maps remains unconfirmed.

## Academy and Michigan

Academy live entry:
https://academy.ac.il/ShopEng/Entry.aspx?entryId=21090&nodeId=1534
It advertises a hardbound publication and exposes no book PDF/ebook link in the inspected HTML. The only PDF link on that page is bookstore regulations.

Older catalogue:
https://www.academy.ac.il/SystemFiles/Catalogue2008-E.pdf
It is a publication catalogue, not the book.

Wayback PDF index inspected:
https://web.archive.org/cdx/search/cdx?url=academy.ac.il/SystemFiles/*&output=json&filter=mimetype:application/pdf&filter=statuscode:200&collapse=urlkey
It returned 3,013 archived PDF URL records, including SystemFiles2015 paths and catalogues. No filename clearly identifying the requested title appeared. Many files have opaque numeric names; their full contents were not exhaustively inspected. The plausible /SystemFiles/21090.pdf and /SystemFiles/172.pdf requests returned zero bytes, not PDFs. An attempted broader filtered Academy CDX query timed out. No legacy book scan was located.

HathiTrust:
https://catalog.hathitrust.org/Record/002887598
https://catalog.hathitrust.org/Record/002887598.marc
The record remains Limited (search only). Its MARC gives Michigan Alma ID 990028875980106381, OCLC 35015373, physical barcode 39015031815007 and Buhr location C 698722. The digital identifier is mdp.39015031815007. The MARC enumerates five map components but lists only one digital item; this does not establish that the maps were scanned or rule out other records.

Michigan's corresponding catalogue URL returned 403 in this environment:
https://search.lib.umich.edu/catalog/record/990028875980106381
Separate map holdings/digitization records remain unverified. Princeton and Stanford catalogue requests also encountered access/challenge pages. Targeted indexed searches across other map/repository leads produced no verified additional complete sheet or book scan; this was not an exhaustive direct search of every named library's holdings.

## Recommended next inquiries

1. NLI Eran Laor Cartographic Collection/reproduction service: whether the four records have existing digital master files; if so, request an authorized reproduction or remote-viewing route.
2. LMU repository staff: whether the original deposit or physical dissertation enclosures preserve Beilage I separately.
3. Peter Pilhofer: whether the source image files used for figures 13–15 came from a larger North-sheet scan and whether an authorized full-sheet copy can be supplied.

No inquiries or orders were sent.
