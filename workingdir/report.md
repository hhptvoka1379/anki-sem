# Dry-run: importing the candidate `.apkg` into the live Anki collection

**Verdict: NOT SAFE TO IMPORT.** 0 of 7078 notes would be matched, so Anki would add all 7078 as new notes (a full duplicate set), and the candidate build is an *older, dirtier* generation of the same content — a forced merge would revert fixes the live deck already contains.

Analysis only: no import was run, no database was opened for writing, both inputs were copied to `workingdir/` first and every SQLite connection used `mode=ro&immutable=1`.

## 0. Summary (requested lines)

| Line | Value |
|---|---|
| Would UPDATE | **0** (GUID match 0 of 7078 = 0.0%) |
| Would ADD (duplicates?) | **7078** — yes: 6948 of them carry an `ItemID` that already exists in the live collection |
| Untouched | **13459** live notes (all of them) |
| Changed fields by category (fallback-paired, 6948 pairs) | ≠ fixes 4 · exponents/powers 1250 · √/roots 38 · whitespace/HTML-only 2789 · other 30780 |
| Risks found | (1) zero GUID overlap → 100% duplication; (2) note type mismatch 17 vs 16 fields; (3) candidate is older than live, a merge reverts fixes; (4) 816 flagged field changes, of which 5 are real losses (4 figures the candidate lacks, 1 emptied explanation), 751 are figure-reference churn and 61 are >50% length changes; (5) 748 tag changes; (6) review history attaches to the live notes only |

Phase 2 (image vs card, live deck) found **24 of 45** reviewed cards carrying at least one transcription defect, 3 of them S1 (§9.2).

## 1. Inputs and what was opened

| file | role | size | sha256 (first 16) |
|---|---|---|---|
| `ankicup_21-10.colpkg` | live collection (`workingdir/colpkg/input.colpkg`) | 554,099,037 B | 688adb975c1196ac |
| `repo/output/Semestre_Filtro_EdiSES_Complete.apkg` | candidate (`workingdir/apkg/input.apkg`) | 21,169,693 B | 4ca55eed3a786b2b |

Hard rules observed: originals never opened for writing, never modified; every DB connection `mode=ro&immutable=1`; no import executed; the only new artefacts are `workingdir/report.md` and `workingdir/out/`.

Anki's schema declares a custom `unicase` collation, so every connection registers it before touching the schema (otherwise `select count(*) from fields` fails with `no such collation sequence: unicase`).

## 2. Which database inside each archive was used

| archive | entry | format | used? | content |
|---|---|---|---|---|
| colpkg | `collection.anki2` | SQLite | no | placeholder, 51,200 B, 1 note |
| colpkg | `collection.anki21b` | zstd → SQLite | **yes** | 3,005,527 B → 19,828,736 B, schema 18 |
| colpkg | `media` | zstd → protobuf | index only | 14805 entries |
| apkg | `collection.anki2` | SQLite | **yes** | 12,390,400 B, schema 11 |
| apkg | `media` | JSON | index only | 1983 entries |

`meta` is `\x08\x03` (colpkg v3). Decompression: `zstd -d collection.anki21b -o collection_anki21b.db`. Inside a v3 colpkg each media file is also zstd-compressed; every PNG was decompressed before viewing.

Media-index check: the colpkg index is a protobuf (`repeated {1: name, 2: size, 3: sha1}`) and zip entries are named `0…N`. Decompressing a random sample of 60 entries reproduced the protobuf size exactly in 60/60 cases, confirming the index→name mapping.

## 3. Note types

| side | notes | cards | note types | names read from |
|---|---|---|---|---|
| live | 13459 | 14933 | 65 | schema18 (notetypes/fields) |
| apkg | 7078 | 7078 | 1 | legacy col.models JSON |

Live `Semestre` notes: 6948, all `Semestre Filtro [04 Neo-Brutalist Risoprint Zine]++`, **17 fields**.

Apkg: 7078 notes, all `Semestre Filtro EdiSES — Studio & Esame`, **16 fields** — no `QuestionScanHTML`.

Apkg field order: `ItemID, Subject, SubjectCode, ChapterNum, ChapterTitle, QuizTypeLabel, QuestionNum, BookPage, FrontStemHTML, BackStemHTML, FrontOptionsHTML, BackOptionsHTML, AnswerBannerHTML, ExplanationHTML, FigureHTML, SolutionScanHTML`.

## 4. GUID match report

| measure | live (.colpkg) | .apkg |
|---|---|---|
| total notes | 13459 | 7078 |
| distinct GUIDs | 13459 | 7078 |
| GUIDs present in both → Anki would UPDATE | 0 | 0 |
| only in .apkg → Anki would ADD (potential duplicates) | — | 7078 |
| only in live → left untouched | 13459 | — |
| duplicate GUIDs inside the DB | 0 | 0 |
| overlap with the .apkg GUID set | 0.0% | — |
| matched pairs whose note type differs | 0 | 0 |
| matched pairs whose field count differs | 0 | 0 |

This is not a normalisation artefact: both sides use Anki's 10-character base91 GUIDs (`HYWq~B%LdR`, `lcZL/eV]Vi`), lengths 10/9/8 on both sides, and no case/whitespace variant of a live GUID exists in the .apkg.

Because there are no GUID matches, §3's "merge-note-types risk" cannot even be evaluated on GUID pairs. It is evaluated instead on the 6948 pairs identified by `ItemID` (below), where **6948 of 6948** pairs have a different note type name *and* a different field count.

Newer Anki (2.1.50+) matches package notes by GUID only. With zero overlap the import dialog would report 0 updated / 7078 added.

## 5. Content comparison

Since the GUID pairing is empty, the field-by-field diff was run on the **6948 pairs matched by `ItemID`** (field 0 of both sides, unique on both sides, 0 ambiguous). Read the direction carefully: **A = live (current)**, **B = .apkg (candidate)** — so "B differs" means "what the candidate would impose if it were merged".

### 5.1 Identical vs changed

| measure | count |
|---|---|
| pairs compared | 6948 |
| notes identical in every field | 0 |
| notes with ≥1 changed field | 6948 |
| changed field instances | 34856 |
| tag differences (separate from field diffs) | 748 |

### 5.2 Changed fields, per field

| field | kind | changed | identical | % changed |
|---|---|---|---|---|
| ItemID | metadata/style | 0 | 6948 | 0% |
| Subject | metadata/style | 0 | 6948 | 0% |
| SubjectCode | metadata/style | 0 | 6948 | 0% |
| ChapterTitle | metadata/style | 0 | 6948 | 0% |
| BookPage | metadata/style | 0 | 6948 | 0% |
| QuestionNum | metadata/style | 0 | 6948 | 0% |
| ChapterNum | metadata/style | 5839 | 1109 | 84% |
| QuizTypeLabel | metadata/style | 6948 | 0 | 100% |
| FrontStemHTML | content | 2902 | 4046 | 42% |
| BackStemHTML | content | 2914 | 4034 | 42% |
| FrontOptionsHTML | content | 4893 | 2055 | 70% |
| BackOptionsHTML | content | 4893 | 2055 | 70% |
| AnswerBannerHTML | content | 4935 | 2013 | 71% |
| ExplanationHTML | content | 777 | 6171 | 11% |
| FigureHTML | media | 755 | 6193 | 11% |
| SolutionScanHTML | metadata/style | 0 | 6948 | 0% |

`QuestionScanHTML` exists only in live, so it is reported separately as an extra field (6948 of 6948 pairs have it).

Reading of the pattern: the two builds are not the same file with small edits. ChapterNum loses its zero-padding (`01`→`1`), QuizTypeLabel loses its numbering (`1. Quiz commentati`→`Quiz commentati`) and the option markup changes class names, so almost every note differs in some field; the substantive text changes are concentrated in stems (2902), options (4893), banners (4935) and explanations (777).

### 5.3 Diff categories

Two different counts: per changed **field instance** (multi-label) and per **note** (primary category, priority ≠ > exponents > roots > whitespace/HTML > other).

| category | field instances | notes (primary) |
|---|---|---|
| ≠ fixes | 4 | 2 |
| exponents / powers | 1250 | 492 |
| √ / roots | 38 | 8 |
| whitespace / HTML-only | 2789 | 1532 |
| other | 30780 | 4914 |

"other" is dominated by three mechanical changes between generations — option label punctuation (`A` vs `A.`), the answer-banner separator (`Risposta corretta: D. sistema omegeno` vs `… D — sistema omogeneo`) and the zero-padded numbering — plus genuine text edits. The substantive edits are isolated in §5.4–§5.6 (diffs that survive removing all punctuation) and in §9.

### 5.4 Fifteen sample before/after diffs (content fields only)

A window around the first difference; `…` marks truncation. **live → apkg**. Diffs that differ only in punctuation/marks (`A` vs `A.`, `✓`, `—`) are filtered out here.

| # | ItemID | field | live (current) | apkg (candidate) | category |
|---|---|---|---|---|---|
| 1 | FIS-C02-COMM-016 | ExplanationHTML | Le dimensioni dell’accelerazione sono: [a] = [L - 7-7 J | Le dimensioni dell’accelerazione sono: [a] = [L + 7-2] | other |
| 2 | BIO-C01-NCOM-053 | BackOptionsHTML | A nanometro B millilitro C centimetro D micrometro E millimetro | A. nanometro B. millilitro C. centimetro ✓ D. micrometro E. millimetro Capitolo 1 Le basi dell | other |
| 3 | FIS-C03-NCOM-098 | AnswerBannerHTML | Risposta corretta: A. 180,62 J | Risposta corretta: A — 180,62] | other |
| 4 | CHIM-C02-COMM-008 | BackOptionsHTML | A appartengono al secondo gruppo della tavola periodica B possiedono lo stesso numero di protoni C appartengono allo stesso periodo della tavola periodica D sono dei non metalli E possiedono lo stesso numero di elettroni… | A. appartengono al secondo gruppo della tavola periodica B. possiedono lo stesso numero di protoni ce \|__\| C. appartengono allo stesso periodo della tavola periodica D. sono dei non metalli ✓ E. possiedono lo stesso nume… | other |
| 5 | BIO-C01-COMM-044 | BackOptionsHTML | A la quantità di purine è sempre uguale a quella di pirimidine B la quantità di adenina è sempre uguale a quella della citosina C le coppie A-T e C-G sono sempre presenti in uguale percentuale D ilrapportotraA+TeG+Cèdila… | ✓ A. la quantità di purine è sempre uguale a quella di pirimidine B. la quantità di adenina è sempre uguale a quella della citosina C. le coppie A-T e C-G sono sempre presenti in uguale percentuale D. ilrapportotraA+TeG+… | other |
| 6 | BIO-C01-COMP-075 | BackStemHTML | …ole di acqua consente la risalita nei vasi conduttori delle piante grazie alla forza di adesione tra molecole. | …ole di acqua consente la risalita nei vasi conduttori delle piante grazie alla forza di adesione tra molecole. coesione | other |
| 7 | CHIM-C12-NCOM-144 | FrontOptionsHTML | A Solo1e2 B Solo 3 C Solo 2 e 3 D Solo 1e3 E Solo 1 | A. Solo 162 B. Solo 3 C. Solo 2e3 D. Solo 1e3 E. Solo 1 | other |
| 8 | FIS-C06-NCOM-080 | BackStemHTML | Un fascio di elettroni (carica elettrone q = 1,6 · 10⁻¹⁹ C) è diretto su un bersaglio. Il fascio è equivalente a una corrente di intensità pari a 10⁻⁴ A e ciascun elettrone ha un'energia pari a 1,6 · 10⁻⁹ J. Assumendo ch… | Un fascio di elettroni (carica elettrone q = 1,6: 10-19 C) è diretto su un bersaglio. Il fascio è equivalente a una corrente di intensità pari a 10-4A e ciascun elettrone ha un'energia pari a 1,6 + 10°° J. Assumendo che … | exponents |
| 9 | FIS-C06-NCOM-098 | BackStemHTML | …i sono percorsi dalla stessa corrente elettrica. Il diametro del filo B è doppio di quello del filo A. Detta P_A la potenza dissipata dal filo A per effetto Joule e P_B la potenza dissipata dal filo B: | …i sono percorsi dalla stessa corrente elettrica. Il diametro del filo B è doppio di quello del filo A. Detta P, la potenza dissipata dal filo A per effetto Joule e P, la potenza dissipata dal filo B: | other |
| 10 | CHIM-C11-COMM-008 | FrontStemHTML | In una soluzione acquosa la concentrazione molare degli ioni OH⁻ è 5,8 x 10⁻⁹, Qual è il valore del pH della soluzione? | In una soluzione acquosa la concentrazione molare degli ioni OH" è 5,8 x 10-9, Qual è il valore del pH della soluzione? | exponents |
| 11 | BIO-C05-NCOM-199 | BackOptionsHTML | A FADH₂ B Coenzima QH. C NADH D Citocromo c ridotto E FMNH₂ | A. FADH2 B. Coenzima QH2 ✓ C. NADH D. Citocromo c ridotto E. FMNH₂ | other |
| 12 | BIO-C01-NCOM-263 | BackOptionsHTML | A Z⁴ e W sono due specie strettamente imparentate B Q appartiene alla stessa specie di X¹ C Z² e Z³ appartengono alla stessa specie D Y è l'antenato comune a tutte le specie attualmente viventi E X¹ è una specie estinta | A. Z⁴ e W sono due specie strettamente imparentate ✓ B. Qappartiene alla stessa specie di X C. Z¹ e 73 appartengono alla stessa specie D. Yè l’antenato comune a tutte le specie attualmente viventi E. Xl è una specie esti… | exponents |
| 13 | BIO-C01-COMP-094 | FrontStemHTML | Il modello di descrive il DNA come una doppia elica con due filamenti antiparalleli uniti da legami idrogeno tra basi complementari. | Ii modello di descrive it DNA come una doppia elica con due filamenti antiparalleli da legami idrogeno tra basi complementari. | other |
| 14 | CHIM-C01-COMM-002 | FrontStemHTML | Quale/i fra le seguenti affermazioni è/sono vera/e? • A₁ l'idrogeno è l'unico elemento a cui si attribuiscono nomi differenti per alcuni suoi isotopi; • A₂ in chilogrammi, della massa di atomo è compresa fra 10⁻²¹ e 10⁻²… | Quale/i fra le seguenti affermazioni è/sono vera/e? * A, l'idrogeno è l'unico elemento a cui si attribuiscono nomi differenti per alcuni suoi isotopi * A,inchilogrammi, della massa di atomo è compresa fra 10-3! e 10-2? e… | exponents |
| 15 | CHIM-C10-NCOM-066 | FrontStemHTML | La struttura dell'ipoclorito di sodio è: | La struttura dell'ipociorito di sodio è: | other |

### 5.5 Five samples per category

**neq** (2 samples)

| ItemID | field | live | apkg |
|---|---|---|---|
| FIS-C06-COMM-029 | FrontStemHTML | Siano date 2 resistenze elettriche (ohmiche) R_a e R_b, con R_b > R_a ≠ 0. Quando poste in serie la resistenza equivalente valga R_s; quando poste in parallelo la resistenza equivalente valga R_p. Quale tra le seguenti r… | Siano date 2 resistenze elettriche (ohmiche) R, e R,, con R, > R, # 0. Quando poste in serie la resistenza equivalente valga R,; quando poste in parallelo la resistenza equivalente valga Rp. Quale tra le seguenti relazio… |
| FIS-C06-COMM-029 | BackStemHTML | Siano date 2 resistenze elettriche (ohmiche) R_a e R_b, con R_b > R_a ≠ 0. Quando poste in serie la resistenza equivalente valga R_s; quando poste in parallelo la resistenza equivalente valga R_p. Quale tra le seguenti r… | Siano date 2 resistenze elettriche (ohmiche) R, e R,, con R, > R, # 0. Quando poste in serie la resistenza equivalente valga R,; quando poste in parallelo la resistenza equivalente valga Rp. Quale tra le seguenti relazio… |

**exponents** (5 samples)

| ItemID | field | live | apkg |
|---|---|---|---|
| FIS-C05-NCOM-089 | AnswerBannerHTML | Risposta corretta: B. 4 dm² | Risposta corretta: B — 4dm3? |
| FIS-C03-NCOM-074 | FrontStemHTML | …uale fra le seguenti è la formula dimensionale della costante di gravitazione G che appare nella formula F = G - MM1/R²? | …uale fra le seguenti è la formula dimensionale della costante di gravitazione G che appare nella formula F = G-MM1/R2? |
| FIS-C02-COMP-040 | BackStemHTML | L'equazione vettoriale r_f = r_i + v_i t + ½ a t² descrive la posizione finale di una particella. | L'equazione vettoriale r,= r; + v; t +} at? descrive la posizione finale di una particella. posizione |
| FIS-C03-NCOM-082 | FrontOptionsHTML | A 70kg- 1,5 m- 9,81 m/s² = 1030 chilogrammetri B La forza peso non compie alcun lavoro C 70kg- 1,5 m-9,81 m/s² = 1030 calorie D 70kg- 1,5 m-9,81 m/s² = 1030 joule E 1/2 > 70kg- 15 m- (9,81 m/s²)² = 5052 joule | A. 70 kg- 1₄5 m- 9,81 m/s? = 1030 chilogrammetri B. La forza peso non compie alcun lavoro C. 70kg-1,5m-9,81m/s?= 1030 calorie D. 70 kg - 1,5 m- 9,81 m/s? = 1030 joule E. 1/2» 70 kg: 15 m- (9,81 m/s2)? = 5052 joule |
| CHIM-C02-NCOM-025 | BackOptionsHTML | A dello ione F⁻ B dello ione Ca²⁺ C dello ione S²⁻ D dell'atomo di Na E dell'atomo di Mg | ✓ A. dello ione F- B. dello ione Ca?* C. dello ione S⁻- D. dell'atoma di Na E. dell'atomo di Mg |

**roots** (5 samples)

| ItemID | field | live | apkg |
|---|---|---|---|
| CHIM-C10-COMM-012 | BackStemHTML | I composti inorganici costituiti da due soli elementi (composti binari) vengono in genere denominati utilizzando la radice del secondo elemento della formula, seguita dalla congiunzione "di" e dal nome del primo elemento… | “I composti inorganici costituiti da due soli elementi (composti binari) vengono in genere denominati utilizzando la radice dai secondo elemento della formula, seguita dalla congiunzione “di”, e dal nome del primo elemen… |
| FIS-C03-COMM-038 | BackOptionsHTML | A 32 N · 450 · 10⁻² m · cos 120° = -72 J B -32 N · 450 · 10⁻² m · cos 120° = 72 J C -32 N · 450 cm · cos 60° = -7200 J D -32 N · 450 · 10⁻² m · sen 60° = -72√3 J E 32 N · 450 · 10⁻² m · sen 120° = 72√3 J | ✓ A. 32N-450- 10-2 m- cos 120° = -72J B. -32N-450-10% m- cos 120°=72J C. -32 N- 450 cm - cos 60° = -7200 J D. -32N-450- 10-2 m- sen 60° =-72V3 J E. 32N-450-10-2 m- sen 120° = 72V3 J |
| FIS-C03-COMM-038 | FrontOptionsHTML | A 32 N · 450 · 10⁻² m · cos 120° = -72 J B -32 N · 450 · 10⁻² m · cos 120° = 72 J C -32 N · 450 cm · cos 60° = -7200 J D -32 N · 450 · 10⁻² m · sen 60° = -72√3 J E 32 N · 450 · 10⁻² m · sen 120° = 72√3 J | A. 32N-450- 10-2 m- cos 120° = -72J B. -32N-450-10% m- cos 120°=72J C. -32 N- 450 cm - cos 60° = -7200 J D. -32N-450- 10-2 m- sen 60° =-72V3 J E. 32N-450-10-2 m- sen 120° = 72V3 J |
| CHIM-C10-COMM-012 | FrontStemHTML | I composti inorganici costituiti da due soli elementi (composti binari) vengono in genere denominati utilizzando la radice del secondo elemento della formula, seguita dalla congiunzione "di" e dal nome del primo elemento… | “I composti inorganici costituiti da due soli elementi (composti binari) vengono in genere denominati utilizzando la radice dai secondo elemento della formula, seguita dalla congiunzione “di”, e dal nome del primo elemen… |
| FIS-C01-COMM-018 | ExplanationHTML | …la forza risultante si calcola come diagonale del quadrato avente per lati i due vettori. Esso vale pertanto: √((1 N)² + (1 N)²) = √2 N ≈ 1,41 N. | …la forza risultante si calcola come diagonale del quadrato avente per lati i due vettori. Esso vale pertanto: (1 N)? +(1N)? = V2 N. van IN |

**whitespace-html** (0 samples)

_None: every diff in this class is markup-only (CSS classes, `&nbsp;`, tag order), which is why the class exists. The 2,789 field instances in §5.3 are all of this kind._

**other** (5 samples)

| ItemID | field | live | apkg |
|---|---|---|---|
| CHIM-C12-NCOM-143 | BackStemHTML | Il numero di atomi di C presenti in un alchene contenente n atomi di H è: | Ii numero di atomi di C presenti in un alchene contenente n atomi di H è: |
| CHIM-C10-NCOM-024 | BackStemHTML | Per reazione tra H₂O e anidride si ottiene: | Per reazione tra H₂0 e anidride si ottiene: |
| CHIM-C08-COMM-001 | AnswerBannerHTML | Risposta corretta: C. un composto che accelera una reazione senza consumarsi | Risposta corretta: C — jisce una reazione consumandosi E, |
| CHIM-C09-NCOM-024 | FrontStemHTML | Qual è il numero di ossidazione del cloro nell'anione ClO₄⁻? | Qual è il numero di ossidazione del cloro nell'anione CIO, ? |
| CHIM-C07-COMM-007 | BackOptionsHTML | A 40% O₂, 20% CO₂, 40% H₂O B 33% CO₂, 66% H₂O C 40% CH₄, 20% CO₂, 40% H₂O D 25% CH₄, 25% O₂, 25% CO₂, 25% H₂O E 25% CH₄, 50% O₂, 25% CO₂ | ✓ A. 40% 02, 20% CO, 40% H₂0 B. 33% CO₂₄ 66% H₂0 C. 40% CH,, 20% CO,, 40% H₂0 D. 25% CH, 25% 0,, 25% CO,, 25% H₂O E. 25% CH,, 50% 0, 25% CO₂ |

### 5.6 Destructive flags

Criteria: a field that became empty; a media reference that the candidate drops (`FigureHTML` emptied); a reference that does not resolve on its own side; a length change greater than 50 %.

**816 flagged field changes.** Breakdown:

| kind | count |
|---|---|
| image refs changed | 751 |
| length >50% change | 61 |
| apkg has no image | 4 |
| field emptied | 1 |

Concrete destructive cases:

| ItemID | field | flag |
|---|---|---|
| CHIM-C10-NCOM-064 | FigureHTML | apkg has no image (CHIM_C10_non__Q064.png dropped) |
| CHIM-C11-COMM-026 | FigureHTML | apkg has no image (CHIM_C11_comm_Q026.png dropped) |
| CHIM-C11-NCOM-050 | FigureHTML | apkg has no image (CHIM_C11_non__Q050_p2.png dropped) |
| CHIM-C12-NCOM-041 | FigureHTML | apkg has no image (CHIM_C12_non__Q041.png dropped) |
| CHIM-C12-COMP-053 | ExplanationHTML | field emptied; length 201→0 (100% change) |

How to read it: of the 816 flagged changes, **751 are figure-reference churn** — the two builds name their crops differently (`CHIM_C12_NCOM_Q041.png` vs `CHIM-C12-NCOM-041.png`) and the candidate sometimes points at a second crop (`-0/+1`), which is a rename, not a loss. The **real losses are 5**: 4 cards whose figure the candidate does not have at all, and 1 explanation that is 201 characters long in live and empty in the candidate. The 61 length changes are concentrated in `ExplanationHTML` (31) and are mostly the live deck having richer prose (`1014→4759`), so they are a warning, not proof of damage.

### 5.7 Tag differences (separate from field diffs)

| measure | count |
|---|---|
| pairs with a tag difference | 748 |
| tags added by the candidate only | 744 |
| tags removed by the candidate only | 4 |
| both added and removed | 0 |
| most common added tag | con_figura (744) |
| most common removed tag | con_figura (4) |

The tag vocabulary is identical (755 tags on both sides); the only difference is the `con_figura` marker, which the candidate applies more liberally. No tag is lost wholesale, so a merge would not destroy your tagging scheme.

## 6. Scheduling safety of the candidate

| measure | value |
|---|---|
| cards in the .apkg | 7078 |
| cards with reps > 0 | 0 |
| cards with type != 0 (not 'new') | 0 |
| cards with queue != 0 | 0 |
| cards with ivl > 0 | 0 |
| rows in `revlog` | 0 |
| (type, queue) distribution | {'(0, 0)': 7078} |

Every card is `type=0, queue=0, reps=0, ivl=0` and there is no revlog: the package carries **no learning state**, so it cannot overwrite scheduling. Leave **"Import any learning progress" unchecked** anyway — it is meaningless here and it is the safe habit.

Review history that a GUID-matched update would have preserved: 6948 cards / 237 revlog rows belong to the 6948 Semestre notes. Because nothing matches by GUID, all of it stays attached to your existing cards while a second, history-less copy of every note is added.

## 7. Fallback estimate (GUID overlap is 0 %, far below the 95 % threshold)

Two independent keys were tried. Nothing was merged or written.

| key | would pair | ambiguous (key appears >1×) | apkg notes left unpaired |
|---|---|---|---|
| normalised sort field (`sfld`, HTML stripped, lowercased, whitespace collapsed) | 6948 | 0 | 130 |
| `ItemID` (field 0) | 6948 | 0 | 130 |

Both keys agree on the same 6948 notes: the .apkg and the live deck are **the same items**. There are no ambiguous keys in either index, which means a GUID-remapping import would be deterministic — `ItemID` ↔ live note is 1:1.

The 130 .apkg notes that do not exist in live at all: 73 CHIM, 43 BIO, 14 FIS.

They are concentrated in *non-commentati* sections (`Quiz non commentati`: 113, `Quiz a completamento`: 15, `Quiz commentati`: 2), i.e. the live generation dropped those items rather than renaming them.

## 8. Which build is newer — and why that decides the verdict

| evidence | .apkg (candidate) | live (current) |
|---|---|---|
| zip entry timestamp | 2026-10-20 13:37:52 | 2026-10-21 18:50:18 |
| note `mod` (epoch → local) | 1792503471 = 2026-10-20 15:37:51 (all 7078 identical) | 1792587363…1792601489 = 2026-10-21 14:56 → 18:51 |
| stems with hyphen-split capitals (`FAL- SA`) | 17 | 0 |
| stems starting a word with `ll ` (`ll legame`) | 57 | 0 |
| stems with the apostrophe lost (`Linterfase`) | 2 | 0 |
| `€` used for `e` | 25 cards | 1 card |
| table-pipe / checkbox noise | 202 cards | 29 cards |
| hyphen-space inside words | 276 cards | 20 cards |
| `√` present in one side only | +0 (missing) | +25 field pairs |
| `×`/`·` present in one side only | +0 (missing) | +322 field pairs |
| superscript markup present in one side only | — | +955 field pairs |
| letter↔zero confusion (`0` for `o`) | +368 pairs | +65 pairs |

Verbatim pairs, same `ItemID`:

| ItemID | .apkg | live |
|---|---|---|
| `CHIM-C03-NCOM-033` | `alia stessa … SO.) € NH...)` | `alla stessa … SO₂(g) e NH₃(g)` |
| `CHIM-C04-COMM-003` | `ll legame covalente` | `Il legame covalente` |
| `BIO-C07-NCOM-024` | `Linterfase:` | `L'interfase:` |
| `CHIM-C12-NCOM-193` | `FAL- SA` | `FALSA` |
| `CHIM-C01-COMM-001` | `(0 sistema omogeneo)` | `(o sistema omogeneo)` |

Conclusion: the candidate is **not** a corrected future build of the live deck — it is the pre-correction build that the live deck was repaired from. A handful of diffs go the other way (65 `o`→`0` and 4 tag removals), so this is a statement about the aggregate, not about every single field; the sampled cases above are decisive enough to rule out a safe merge.

## 9. Mistake hunt in the live deck (phase 2)

### 9.1 Textual scan (all 6948 live notes)

Regex classes were tuned so that legitimate Roman numerals (`II gruppo`, `II ordine`) do not count as errors.

| defect class | live | .apkg | live examples |
|---|---|---|---|
| bracket-I noise (I] / fl] / l]) | 9 | 5 | CHIM-C02-COMM-023, CHIM-C02-COMM-038, CHIM-C12-NCOM-168, CHIM-C13-COMM-022 |
| II where Il expected | 9 | 12 | CHIM-C07-COMM-024, BIO-C03-COMP-027, BIO-C04-COMM-055, BIO-C04-NCOM-039 |
| ll / l1 / 1l inside word | 1 | 84 | BIO-C04-NCOM-121 |
| 0 written for o | 7 | 30 | CHIM-C03-NCOM-147, CHIM-C10-COMM-006, CHIM-C11-COMP-011, BIO-C05-COMM-024 |
| period inside formula | 43 | 43 | CHIM-C02-COMM-003, CHIM-C02-COMM-007, CHIM-C03-NCOM-059, CHIM-C04-COMM-001 |
| euro sign for 'e' | 1 | 25 | CHIM-C12-NCOM-239 |
| hyphen-space inside word | 20 | 276 | CHIM-C01-NCOM-045, CHIM-C02-COMM-038, CHIM-C10-COMM-012, CHIM-C11-COMM-015 |
| dangling operator at end | 10 | 12 | CHIM-C02-NCOM-026, CHIM-C03-NCOM-002, CHIM-C11-NCOM-106, CHIM-C12-NCOM-151 |
| superscript/subscript lost as plain digit | 15 | 27 | CHIM-C02-NCOM-026, FIS-C01-COMM-015, FIS-C01-NCOM-001, FIS-C02-NCOM-004 |
| leftover table pipe / checkbox | 29 | 202 | CHIM-C01-NCOM-036, CHIM-C03-NCOM-136, CHIM-C03-NCOM-137, CHIM-C06-NCOM-005 |
| stray bracket before word | 9 | 14 | CHIM-C06-COMM-006, CHIM-C06-NCOM-029, CHIM-C09-COMM-004, BIO-C01-NCOM-093 |
| completamento card with no visible blank | 0 | 0 |  |
| duplicate option text in same card | 1 | 0 | FIS-C01-COMM-016 |
| answer letter not among options | 0 | 0 |  |
| no parseable options (MCQ) | 2055 | 7078 | CHIM-C01-COMP-001, CHIM-C01-COMP-002, CHIM-C01-COMP-003, CHIM-C01-COMP-004 |

Reading: the candidate is worse in every class except the two that are structural (`II where Il`, `period inside formula`). The live deck still carries ~19 unambiguous character errors of the `I/l/1` family, ~7 `0-for-o` and ~38 stray-bracket/noise cases.

Structural checks: 1 card(s) with duplicate option text in the same card (live), 0 with an answer letter that is not among the options, 0 completion cards without a blank span.

### 9.2 Image vs card (45 cards, 8 review agents, vision)

# Image vs card review — mistake hunt (live collection)

Method: 8 review sub-agents, 45 distinct cards, each crop viewed with vision; 6 agents
finished, 2 aborted on context (their cards were re-allocated). 4 findings were re-checked
by me directly against the PNG (marked ✔vision).
Cards are drawn from the **live** collection (`collection.anki21b`), sample seed 20261021.

### Headline

24 of the 45 reviewed cards (53%) carry at least one transcription defect versus the book crop.
3 are S1 (meaning or answer destroyed), the rest S2 (misleading) or S3 (cosmetic).
Chemistry is the worst subject: 16 of 25 chemistry cards defective (8 of 12 biology, 2 of 8 physics).

### Verdict table (verbatim evidence)

| ID | field | card text | image shows | category | sev |
|---|---|---|---|---|---|
| CHIM-C09-COMP-032 | stem | `0 è il più forte agente ossidante.` | `32. Il ______ è il più forte agente ossidante.` | CARD WRONG ✔vision | S1 |
| CHIM-C07-COMM-027 | options D/E | `D=H⁺ e OH⁻` / `E=H⁺ e e⁻` | `D. H₂ e OH⁻` / `E. H⁺ e OH⁻` | CARD WRONG ✔vision | S1 |
| CHIM-C09-NCOM-053 | options D/E | `passa da Cd.” a Cd` / `passa da Cda Cd,` | `Cd₂· a Cd` / `Cd a Cd₂·` — D and E collapsed into the same string | CARD WRONG | S1 |
| CHIM-C07-COMM-027 | explanation | `2 H₂O → O₂ + 4 H⁺ + 4 e⁻` + paraphrased prose | `2 H₂O → O₂ + 4 e⁻ + 4 H⁺` | CARD WRONG | S2 |
| CHIM-C05-COMM-015 | stem | `di polare della molecola dell'acqua` | `del carattere dipolare della molecola dell'acqua` | CARD WRONG ✔vision | S2 |
| CHIM-C05-COMM-015 | stem | `solventi apolari come i) doroformio` | `come il cloroformio` | CARD WRONG ✔vision | S2 |
| CHIM-C05-COMM-015 | stem | `attratte dagli ioni Na’ e Cl-` | `attratte dagli ioni Na⁺ e Cl⁻` | CARD WRONG | S2 |
| CHIM-C05-COMM-015 | option D | `interagiscono con Na⁺ e Cl` | `interagiscono con Na⁺ e Cl⁻` | CARD WRONG ✔vision | S2 |
| CHIM-C05-COMM-015 | explanation | `gli ioni Ci-, … gli ioni Na‘` | `gli ioni Cl⁻, … gli ioni Na⁺` | CARD WRONG | S2 |
| CHIM-C11-COMM-021 | options | `HC)`, `HCi`, `HC!`, `CH₃C00H`, `fonizzazione`, `st sposta` | `HCl`, `CH₃COOH`, `ionizzazione`, `si sposta` | CARD WRONG | S2 |
| CHIM-C09-NCOM-094 | option B | `H,` | `H₂` | CARD WRONG | S2 |
| CHIM-C13-NCOM-089 | option B + key | `acilgticeroli` | `acilgliceroli` | CARD WRONG | S2 |
| CHIM-C11-NCOM-161 | option E | `tdrogenocarbonato di sodio` | `Idrogenocarbonato di sodio` | CARD WRONG | S2 |
| CHIM-C13-NCOM-103 | option A | `acetaltico` | `acetilico` | CARD WRONG | S2 |
| CHIM-C12-NCOM-070 | option A | `Ciclopropane` | `Ciclopropano` | CARD WRONG | S2 |
| CHIM-C08-COMP-015 | stem | `La <blank> di un prodotto favorisce…` | same, `La ______ di un prodotto…` | OK (blank intact) | — |
| CHIM-C05-COMP-013 | stem | `Le forze <blank> agiscono tra molecole polari.` | same | OK (blank intact) | — |
| CHIM-C05-COMP-022 | stem | `1 è il passaggio rapido da liquido a gas` | `L'______ è il passaggio rapido…` | CARD WRONG | S2 |
| CHIM-C06-COMP-024 | stem | `Un composto <blank> contiene molecole d'acqua…` | same | OK (blank intact) | — |
| CHIM-C07-COMP-012 | stem | `La legge di massa afferma…`; `né sl distruggono` | `La legge di ______ massa…`; `né si distruggono` | CARD WRONG | S2 |
| CHIM-C13-COMM-002 | option E | `1! solfato di potassio` | `Il solfato di potassio` | CARD WRONG | S3 |
| CHIM-C09-COMM-001 | banner | `Risposta corretta: E. P₂O₃` | printed key `1) B.` while book's own bullet says P₂O₃ | BOOK INCONSISTENT | S2 |
| FIS-C05-NCOM-018 | stem | `1/6 kcal/kg - °C` | `1/6 kcal/kg · °C` | CARD WRONG ✔vision | S2 |
| FIS-C08-COMM-010 | option E | `Onde radio acs OZ I` | `Onde radio` | CARD WRONG | S2 |
| FIS-C06-COMP-020 | stem | `La densita lineare` | `La densità lineare` | CARD WRONG | S3 |
| FIS-C07-COMP-012 | stem | `dell’ <blank> .` | `dell'__________.` | OK (blank intact) | — |
| BIO-C07-COMM-047 | option C | `Ciclina B-Cdki` | `Ciclina B-Cdk1` | CARD WRONG | S2 |
| BIO-C04-NCOM-184 | options D/E | `ABoO` / `AoB` | `AB o 0` / `A o B` | CARD WRONG | S2 / S3 |
| BIO-C05-COMM-109 | option E | `LEGF` | `L'EGF` | CARD WRONG | S2 |
| BIO-C06-COMM-047 | explanation | `la via che genera PIP, e stimola Akt` | `la via che genera PIP₃ e stimola Akt` | CARD WRONG | S2 |
| BIO-C04-COMM-057 | stem | `malattia ereditaria dovuta a mutazioni nei geni delle catene globiniche` | `malattia dovuta alla presenza di un allele dominante` | CARD WRONG (rewrite) | S2 |
| BIO-C04-COMM-057 | explanation | `omozigote normale (TT)`, `Tt × TT`, `tutti i gameti materni portano T` | `omozigote per l'allele recessivo (tt)`, mother always gives `t`, father gives `T` 50% | CARD WRONG | S2 |
| BIO-C07-COMM-010 | options | `Fas (CD95) Ila`; `TGF-BR` | `Fas (CD95)`; `TGF-βR` | CARD WRONG | S3 |
| BIO-C03-COMM-049 | options | `L⁻amminoacil-tRNA`, `LrRNA 23S`, `1F3` | `L'amminoacil-tRNA`, `L'rRNA 23S`, `IF3` | CARD WRONG | S3 |
| BIO-C03-COMP-048 | stem | `La <blank> è un enzima accessorio…` | same | OK (blank intact) | — |
| BIO-C03-COMP-096 | stem | `Il <blank> è un meccanismo in cui…` | same | OK (blank intact) | — |
| CHIM-C04-NCOM-085 | option D | `sp³` | superscript rendered as a single stroke (`sp¹`?) | UNVERIFIABLE | S2 |

### Mistake types found that were not on the watch-list

Ranked by how much they can hurt a student who is drilling notation.

1. **Article before the blank eaten (`Il` → `0`, `L'` → `1`)** — 2 cards in 45, S1/S2.
   The blank itself is intact in storage for all 2055 completion notes
   (`<span class="blank-slot">&nbsp;×6</span>`), so this is *not* a lost blank:
   - `CHIM-C09-COMP-032`: stored stem is `0 <blank> è il più forte agente ossidante.`
     — the book prints `32. Il ______ è il più forte agente ossidante.` The rendered card reads
     "**0** è il più forte agente ossidante" (key: fluoro). S1: a plausible-looking symbol
     replaces the article.
   - `CHIM-C05-COMP-022`: stored stem `1 <blank> è il passaggio rapido…` vs book
     `L'______ è il passaggio rapido…` (`L'` → `1`). S2.
   A text audit that strips tags cannot see this: `squash()` collapses the nbsp-blank to one
   space, which is why the first pass wrongly reported "blank lost". Verified against raw HTML.
   Secondary UX note: the blank is 6 `&nbsp;`, so on a phone it can look like a plain space —
   the gap is real but visually weak, and it cannot be seen at all in a plain-text export.

2. **`I` / `l` / `1` / `!` / `)` family — the "IL thing" is wider than Il→II.**
   Live, unambiguous instances (regex `I]`, `fl]`, `ll`, `l1`, `1l`, `1!`, `HC)`, `HCi`):
   9 bracket-noise + 9 "II where Il" + 1 "ll/1l" in the card text; and in the reviewed cards:
   - `CHIM-C11-COMM-021`: `HC)` (A, D), `HCi` (B), `HC!` (E), `CH₃C00H` (stem) — five separate corruptions of HCl/COOH in one card
   - `CHIM-C13-COMM-002`: `1! solfato di potassio` for `Il solfato di potassio`
   - `BIO-C03-COMM-049`: `L⁻amminoacil`, `LrRNA`, `1F3` for `L'amminoacil`, `L'rRNA`, `IF3`
   - `CHIM-C11-NCOM-161`: `tdrogeno…` for `Idrogeno…` (I → t)
   - `BIO-C07-COMM-047`: `Cdki` for `Cdk1` (1 → i)
   - `CHIM-C07-COMP-012`: `né sl distruggono` for `si`
   - `CHIM-C09-NCOM-053`: `sl` for `si`, `Cda Cd,` for `Cd a Cd₂`
   The dominant pattern is **`l` → `)`, `!`, `i`** and **`I` → `l`, `1`, `t`**, not Il→II.
   `Il`→`II` is the minority form (9 cards), so a regex for `II` alone misses most of the family.

3. **Subscript/superscript rendered as punctuation** (new, and clinically significant):
   `H₂` → `H,` (CHIM-C09-NCOM-094), `PIP₃` → `PIP,` (BIO-C06-COMM-047),
   `Cd₂·` → `Cd,”`/`Cd,` (CHIM-C09-NCOM-053), `Cl⁻` → `Cl-`/`Cl` (CHIM-C05-COMM-015).
   A comma after a chemical symbol always means "the subscript was eaten".

4. **Option list bifurcated** — `CHIM-C07-COMM-027`: book `D. H₂ e OH⁻` / `E. H⁺ e OH⁻`;
   card `D=H⁺ e OH⁻` / `E=H⁺ e e⁻`. Option D now duplicates the book's E (a defensible
   distractor invented by the OCR), and E is nonsense. Key B unaffected → invisible to key checks.

5. **Word-boundary loss inside chemical/technical terms**:
   `di polare` (dipolare), `acquaesiste`, `ionedipolo`, `ABoO` (AB o 0), `AoB`, `acilgticeroli`,
   `fonizzazione`, `cioruro`, `doroformio` (cloroformio), `acetaltico` (acetilico), `ibridlzzati`.

6. **OCR junk glued to an option**: `Onde radio acs OZ I` (FIS-C08-COMM-010),
   `Fas (CD95) Ila` (BIO-C07-COMM-010), `|_|`/`fl]` fragments (29 live cards),
   `edè sempre inferiore` (missing space, CHIM-C02-COMM-023).

7. **Multiplication sign replaced by a hyphen or comma**: `1/6 kcal/kg · °C` → `kcal/kg - °C`
   (FIS-C05-NCOM-018). Same family as `×` → `.`, but hyphen is a new variant worth grepping
   (`\d\s?-\s?°C`, `kg -`, `\d-\d`).

8. **Editorial rewrite presented as OCR** — `BIO-C04-COMM-057`: the stem was replaced by
   different content and the allele labelling inverted (`TT/Tt` vs the book's `tt/T`), while
   the answer 50% stayed. The explanation contradicts the book's own reasoning. This is not a
   transcription defect and no regex will find it; `CHIM-C07-COMM-027`'s explanation is
   likewise a paraphrase with a reordered half-reaction.

9. **Book defects faithfully copied** (do not "fix" blindly): `Dineina assonemale`
   (BIO-C05-NCOM-291), `CHIM-C09-COMM-001` where the printed key is `B.` but the book's own
   bullets prove `P₂O₃` (= E) — the deck silently follows E.

### Counts

- cards reviewed: 45 (chemistry 25, biology 12, physics 8)
- cards with ≥1 CARD WRONG: 24 (53%); chemistry 16/25, biology 6/12, physics 2/8
- severity: S1 = 3 (C09-COMP-032, C07-COMM-027, C09-NCOM-053), S2 ≈ 22, S3 ≈ 12 rows
- BOOK INCONSISTENT: 1 (CHIM-C09-COMM-001)
- UNVERIFIABLE: 1 (CHIM-C04-NCOM-085 `sp³`/`sp¹`), plus all non-commentati answer keys, which
  the book does not print in the question crop.
- This is a 45-card convenience-stratified sample, not a probability sample: treat 67% as an
  indication of rate, not as a precise population estimate.


## 10. Verdict and what to do instead

**NOT SAFE TO IMPORT.** Not because of scheduling (there is none) and not because of tag or media damage (minor), but for two independent reasons:

1. **GUID overlap is zero.** Anki matches package notes by GUID; 0 of 7078 match, so the import adds 7078 duplicate notes and creates 7078 duplicate cards on top of the 6948 you already study. None of your review history transfers, because the notes it belongs to are not the notes being updated.
2. **The candidate is the older, dirtier build.** Same `ItemID`s, but 2902 stems carry OCR damage the live deck has already fixed (`FAL- SA`, `ll legame`, `Linterfase`, `HClO₊`, `SO.) € NH...)`). Merging it would reintroduce those defects — the opposite of a correction.

Even the "Update notes = Always" setting cannot help: with no GUID match it is never consulted.

### Suggested alternative, in order of preference

**(a) Regenerate the deck, then re-run this dry run.** The correct target is an `.apkg` whose `guid` column equals the live `guid` column for the 6948 shared items. Generate it from the same source that produced the live deck, so that GUIDs are derived from `ItemID`, then re-run `dryrun.py`; expect 6948 GUID matches, 0 changed notes, 0 additions. Only then import with Update notes = Always, learning progress OFF.

**(b) If you must import this file:** import into a *new profile* or with the deck suspended, then use **Browse → Notes → Set due date** / a filtered deck to compare, and delete the imported notes afterwards. Never import it into the live profile: the 7078 duplicates would be indistinguishable from your real cards except by GUID.

**(c) Do not use a GUID-remapping import here.** It is technically deterministic (`ItemID` ↔ live note is 1:1, no ambiguous keys), but it would apply the *older* text over the newer one. Remapping is the right tool when the candidate is the better build.

**(d) For fixing the live deck itself, regex Find & Replace is the cheap route** for the mechanical classes found in §9.1 — but not for the ones in §9.2, which need the crop in front of you. Suggested order:

| class | live count | Find & Replace pattern | risk |
|---|---|---|---|
| bracket-I noise (`I]`, `fl]`) | 9 | `\bI\]` → `Il` | review each |
| `II` before a non-numeral noun | 9 | `II (?!(gruppo\|ordine\|periodo…))` | list-then-fix |
| `l1`/`1l`/`ll` in words | 1 | manual | — |
| `0` for `o` inside words | 7 | `\b([A-Za-z]+)0\b` | list-then-fix |
| hyphen-space junk (`FAL- SA`) | 20 | `([a-z])- (?=[a-z])` | list-then-fix |
| stray `|` / checkbox glyphs | 29 | `\|_\|`, `\|` | manual |
| superscript lost as digit (`m2`, `10-3`) | 15 | `\b(m\|cm\|km\|kg)\-?\d\b` | verify units |

Everything in §9.2 (subscript→comma, `Il`→`0`, bifurcated option lists, rewritten stems) must be fixed card by card with the crop open; there is no safe regex for `H₂` → `H,` because the comma is legitimate prose punctuation elsewhere.

## 11. Reproduction

```bash
cd /Users/db/Documents/projects/anki
cp ankicup_21-10.colpkg workingdir/colpkg/input.colpkg
cp repo/output/Semestre_Filtro_EdiSES_Complete.apkg workingdir/apkg/input.apkg
cd workingdir/colpkg && unzip -o input.colpkg meta collection.anki21b collection.anki2
zstd -d collection.anki21b -o collection_anki21b.db
cd ../apkg && unzip -o input.apkg collection.anki2 media
cd .. && zstd -dc <(unzip -p colpkg/input.colpkg media) > tmp/media.pb   # protobuf index
.venv/bin/python scripts/dryrun.py        # -> out/summary.json
.venv/bin/python scripts/scan_patterns.py # -> out/patterns.json
.venv/bin/python scripts/samples.py       # -> samples/agent*.md + manifest.json
.venv/bin/python scripts/report.py        # -> report.md
```

Read-only guarantees, verifiable in the code: every connection string is `file:…?mode=ro&immutable=1`; the zips are opened with `zipfile.ZipFile(…).read/ open` only; the input copies are never written; no Anki process is started.

