# Image vs card review — mistake hunt (live collection)

Method: 8 review sub-agents, 45 distinct cards, each crop viewed with vision; 6 agents
finished, 2 aborted on context (their cards were re-allocated). 4 findings were re-checked
by me directly against the PNG (marked ✔vision).
Cards are drawn from the **live** collection (`collection.anki21b`), sample seed 20261021.

## Headline

24 of the 45 reviewed cards (53%) carry at least one transcription defect versus the book crop.
3 are S1 (meaning or answer destroyed), the rest S2 (misleading) or S3 (cosmetic).
Chemistry is the worst subject: 16 of 25 chemistry cards defective (8 of 12 biology, 2 of 8 physics).

## Verdict table (verbatim evidence)

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

## Mistake types found that were not on the watch-list

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

## Counts

- cards reviewed: 45 (chemistry 25, biology 12, physics 8)
- cards with ≥1 CARD WRONG: 24 (53%); chemistry 16/25, biology 6/12, physics 2/8
- severity: S1 = 3 (C09-COMP-032, C07-COMM-027, C09-NCOM-053), S2 ≈ 22, S3 ≈ 12 rows
- BOOK INCONSISTENT: 1 (CHIM-C09-COMM-001)
- UNVERIFIABLE: 1 (CHIM-C04-NCOM-085 `sp³`/`sp¹`), plus all non-commentati answer keys, which
  the book does not print in the question crop.
- This is a 45-card convenience-stratified sample, not a probability sample: treat 67% as an
  indication of rate, not as a precise population estimate.
