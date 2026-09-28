# Phase 2 summary: the landmark lexicon

Session 2, 2026-09-28. Desk research on texts only. This summary interprets words; it does not point to any place to dig.

"BK" marks background knowledge that does not come from the files. Page numbers are printed pages:
- Puech 2006: Puech's edition (STDJ 55)
- Lef.: Lefkovits 2000
- DJD: Milik, DJD III (1962)
- ADAJ: Milik 1960

## 1. What was done

- **121 terms.** Every landmark, place name, direction word and measure word in the scroll, by category:

  | Category | Terms |
  |---|---|
  | Built structures and monuments | 43 |
  | Place names | 36 |
  | Natural features | 19 |
  | Water installations | 14 |
  | Direction, measure and procedure words | 9 |

- **Meanings.** For each term the lexicon gives the meaning in each edition, with page:
  - Puech 2006, commentary pp. 179–206;
  - Lefkovits 2000;
  - Milik 1960 (ADAJ);
  - Milik 1962 (DJD III): section C, *Mots et objets*, 212 entries; section D, *Sites et monuments*, 75 entries; Addenda pp. 299–302. All three were read from the page images in this session.

  It also gives the BDB and Jastrow entries. Where the editions read or interpret a word differently, every position is recorded.
- **Attestations** in:
  - the Hebrew Bible (WLC);
  - the Mishnah;
  - Josephus (Greek and English);
  - Eusebius's Onomasticon (Wolf's English, checked against Klostermann's Greek where it mattered).

  Hits were **checked for sense**. Homographs are excluded and named, and counts that were not fully checked say so.
- **Where it lives.**

  | File | In the repo? | Contents |
  |---|---|---|
  | `copper_scroll_landmark_lexicon.csv` | No, local only | The full lexicon. It quotes the editions, so it is delivered directly |
  | `tables/landmark_lexicon_index.csv` | Yes | Term, category, entries, confidence, and the counts and references of the attestations |

## 2. Main results

### 2.1 The vocabulary is post-biblical

Non-place terms, by where the meaning is attested (as checked; see the lexicon for the counts):

| Attested in | Terms | Examples |
|---|---|---|
| Bible and Mishnah | 34 | בור, נחל, קבר, חצר, פתח, מעלות |
| Mishnah only (not in the Bible in this sense) | 15 | שית 'pit', אמה 'conduit', ביב 'drain', שובך 'dovecote', כוך 'burial niche', נפש 'funerary monument', אכסדרה, מסמא |
| Bible only | 18 | יגר (only Gen 31:47, Aramaic), מקרה 'cool room' (Judg 3:20, 24), שן הסלע (1 Sam 14:4), בבואך as a route idiom (Gen 10:19; 25:18) |
| Neither corpus | 18 | Greek loanwords (פרסטלון, אסטאן), rare technical words (מזקא, זרב, רוי, שלף), and words that exist only in one editor's reading (קיבוץ, הכסח) |

(Inference, high confidence) The scroll's technical vocabulary for installations and tombs is that of the Mishnah and of Aramaic, not of the Bible. So Mishnaic and Aramaic usage is the right guide to what a word describes. Biblical usage is a guide mainly for the place names. (Milik's DJD section B, on the language, was not read in this session.)

### 2.2 How secure the meanings are

- **High confidence: 47 terms.** Examples: cistern, wadi, tomb, steps, corner, cubit.
- **Medium: 44.**
- **Low: 30.**

For many low-confidence terms the problem is the **reading**, not the dictionary. In these, the editions read letters so differently that **the kind of landmark changes**:

| Line | Reading A | Reading B |
|---|---|---|
| VII 11 | a drying floor (Puech p. 192) | a guard post / fortress (Milik, DJD p. 292) |
| IV 6 | "cavities" (Puech) | "tamarisks" (Milik) |
| III 12–13 | "the body" (Milik's early reading) | a slab over a bone pit (DJD C82) |
| VIII 4 | an engraved inscription (Puech, Lef.) | "the steep part" of a slope (Milik) |
| XII 3 | a burial niche (Puech) | a cistern (Milik) |
| IX 4 | "the second terrace" (Puech) | a place name, Tekelet ha-Šani (Milik) |
| XI 8 | the Temple galleries | a rock "knife" (other readers) |

Findings F2.3 and the lexicon list all of them.

### 2.3 Place names: what is anchored and what is not

- **Anchored in the Bible, Josephus or the Onomasticon, with the main editions agreeing on the area:**

  | Name | Line | Area the editions agree on |
  |---|---|---|
  | Achor | I 1 | valley near Jericho; see 2.5 |
  | Sekakah | Josh 15:61 | Qumran for Puech; the Buqeia village for Milik, but Wadi Qumran for the scroll |
  | Jericho | V 13 | Jericho |
  | Doq | 1 Macc 16:15; Josephus's fortress "Dagon" above Jericho (AJ 13.230; usually equated with Dok, BK) | Jebel Qarantal / ʿAin Duq, NW of Jericho |
  | Kidron | VIII 8 | the lower Kidron towards Mar Saba (Milik, Puech) |
  | Beth ha-Kerem | X 5 | Ramat Raḥel |
  | Absalom's monument | X 12 | 2 Sam 18:18; see 2.5 for which side of Jerusalem |
  | Gerizim | XII 4 | Mount Gerizim |
  | the East Gate | II 7 | Jerusalem, the Temple area |

- **Anchored, but the editions disagree on which place is meant:**
  - Beth-Horon or "Horites" (IX 7; this turns on one word, ים or דרום, see 2.4)
  - Masada (Milik only)
  - Bet Tamar (Milik: near Gibeah; Puech objects that there is no gorge there)
  - Beth Sham = Beth-shean? The scroll's final mem is a problem, because every other source spells the name with nun.
  - Bezek (Puech: Kh. Ibziq in Samaria) or ha-Baruk (Milik: Hebron and Mamre, in his Addenda p. 301)
- **Not anchored.** No ancient text outside the scroll places these:
  - Koḥlit: eleven proposals, from Jericho (Puech p. 175, 181) to Mount Carmel (Milik, DJD D71, p. 274). The only non-scroll attestations are b. Qiddushin 66a and "Koḥlit hyssop" in m. Parah 11:7, and neither gives a location.
  - Manos, Bet ha-MDH / ha-MRH, ʿAṣla (a modern Arabic name only), Aḥiyah / Ḥazor, and "Qe[…]" at VII 3.
- **Place names that exist in only one edition's text** are listed in F2.3:
  - Milik only: Kephar Nebo, Qobʿeh, Tekelet ha-Šani, Bet Eshdatain, Bet Ḥaṣor.
  - Puech only: Koḥlit at IV 1, Aḥiyah, Bezek.
  - Lefkovits only: Janoah at XII 10.

  **Phase 3 must treat these as conditional on one reading.**

### 2.4 Directions and measures

These words decide where on a site a deposit is said to be. They are therefore the main test for any candidate site in Phase 3.

- **ים at IX 7.** Milik and Lefkovits read ים, "the Sea"/west; Puech reads דרום, "south". The editions are split about evenly (lexicon: yam_west). Milik's Upper Beth-Horon rests on "facing the Sea" (DJD D32, p. 268). With "south", that support is gone.
- **Cubits or feet at X 6 and X 13.** Milik reads רגמות, "feet"; the others read אמות, "cubits". It is a small difference in scale, but "feet" in this sense is otherwise unattested in Hebrew (Puech p. 198 n. 380), so confidence in it is low.
- **Depth or distance.**
  - חפור + number is a depth for all editors.
  - רחוק (II 8) and משח (VII 6, IX 1) give horizontal distances.
  - A bare number of cubits is disputed. For example, after בבואך (X 5–6) Lefkovits reads a distance and Milik reads a depth.
- **Relative directions.** בבואך "as you enter" and לסמול "to the left" depend on the approach, and the text does not give it.
- **The unit of length.** The editions assume 45–52.5 cm per cubit (Puech p. 180; Milik uses ½ m, DJD C161). This is an assumption, not something the scroll states.

### 2.5 Contested places: the positions, stated fairly

- **The Valley of Achor (I 1; IV 6).** There are three placements:
  - the Buqeia, SW of Qumran (Allegro, reported by Lef. p. 29; also the Iron Age identification by Noth, and by Cross and Milik);
  - Wadi Nuweiʿimeh, NE of Jericho (Milik, ADAJ p. 143 and DJD D3 p. 262; Puech p. 179 agrees);
  - TIR's "Achor Vallis" label, NW of Jericho (the map crop in the repo).

  The Onomasticon text says "north of Jericho", "beside Galgala" (F2.2). That rules out the Buqeia only for the 4th-century tradition. Milik and Puech agree that the scroll follows that later tradition. Allegro disagrees. The question stays open for Phase 3 (Q13).
- **Absalom's monument (X 12).**
  - Milik puts it in the SW necropolis (Baqʿah), "et non à l'est de la Ville" (DJD D68, pp. 270, 274).
  - Puech puts it SE of the city, in the Kidron below Siloam (p. 199), because of the sequence with entries 46–47.
  - Both use Josephus's "two stadia from the city".
- **Sekakah.**
  - Puech: Sekakah = Kh. Qumran (pp. 175, 188–189).
  - Milik: the biblical village = Kh. es-Samra in the Buqeia, but the scroll's "Sekaka" = the whole Wadi Qumran (ADAJ p. 146; DJD D7, p. 263).
  - Both put entries 20–23 around Qumran.
- **Koḥlit.** See 2.3. No two major editions agree.

### 2.6 Problems found in the method (and fixed)

- **Homographs.** Lemma searches gave false attestations for many terms (F2.1).
- **The English Josephus text contains Whiston's footnotes and his own spellings.** Some hits were in the footnotes, not in Josephus:
  - AJ 5.33 (Achor), AJ 8.81 (east gate), BJ 2.325 (Bethesda).
  - Some names are Whiston's spellings. At AJ 6.78, where Whiston has "Bezek", Niese's Greek reads Βαλᾶ.

  Josephus references in the lexicon were checked against the Greek (Niese numbering).
- **Missed hits.** The automatic search missed some real attestations, which the review added:
  - defective spellings such as הכהן הגדל and השלח;
  - forms written without the article, such as בקעת בית כרם;
  - Mishnaic synonyms.
- **Lexicon lookups.** The Sefaria API often returned a homograph instead of the relevant noun (Jastrow בור "cistern", ברכה "pool"). The lexicon says so where it happened.
- **One agent's claim was corrected.** The claim was that Puech misreports Milik on ha-Baruk. In fact, Milik changed his own view in the DJD III Addenda (p. 301), and Puech (p. 205 n. 494) cites that page.

## 3. What this means for Phase 3

For each entry, the lexicon's `implication_for_locating` field states what the text requires of a site. Examples: a built or rock-cut feature, a spring, a tomb with a court and a pillar, a slope facing a stated direction.

A candidate site will be scored only against these textual requirements and against the published archaeology. Where the requirement depends on one edition's reading, the score will say so.

## 4. Addendum: later studies (added after the new uploads)

- The lexicon now has a column `later_studies_2002_2020`, filled from:
  - *Copper Scroll Studies* (2002): Puech ch. 5, Eshel ch. 6, Elwolde ch. 7, Lange ch. 8, Lefkovits ch. 9, Lubbe ch. 10, Pfann ch. 11, Schiffman ch. 12;
  - Høgenhaven 2020, ch. 3–4.
- There are 314 records, each with author and page, in `lexicon_addendum_records.csv` (local).
- They add three things:
  - comparisons with the Temple Scroll's building terms (Schiffman);
  - aqueduct identifications (Eshel);
  - the arguments on ככ (F2.20).
- They also give 16 position and landmark words that have no lexicon row yet. See F2.19.
- Puech 2015 confirms the Hebrew text used here (F2.14). Its corrigenda resolve the old translation errors (Q10).

## 5. Open questions added

See `open_questions.md`, Q14–Q19.
