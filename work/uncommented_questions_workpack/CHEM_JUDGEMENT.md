# Items needing chemistry adjudication (not auto-fixed)

These were deliberately left alone: each needs a content decision, not a
mechanical replacement. Give this file to the heftier model together with the
question scan (`scan` filename) where available.

Rule for whoever decides: state (a) the corrected text, (b) whether the key
letter stays, (c) confidence. Do not edit the deck until approved.

---

## 1. CHIM-C09-COMM-006 — p. 130 (commentato)

Q: *Quali sono i prodotti di una reazione tra un ossido metallico e un acido?*
Key: **A. Sale più acqua** (options A–E are fine).

Problem is in `ExplanationHTML`:

> … Ad esempio: CaO + 2 HC] + Call + H20. lì sale si form…

After the HCl pass this is:

> … CaO + 2 HCl + Call + H20. lì sale si form…

Decide: `Call` → `CaCl₂`? `H20` → `H₂O`? `lì` → `il`? And is the coefficient
`2 HCl` right for `CaO + 2 HCl → CaCl₂ + H₂O` (yes, if that is the intended
equation)?

## 2. CHIM-C09-NCOM-128 — p. 143

Q: *Nella seguente reazione di ossido-riduzione: Zn + 2HCl — ZnCl₄ + H₂*
Key: **D. lo zinco si ossida e l'idrogeno si riduce**

Problems: `ZnCl₄` should almost certainly be `ZnCl₂`; the arrow `—` should be
`→`; option C `lozincosi ossida` (spacing), option E `si riduce è Il cloro`
(`è` → `e`, `Il` → `il`).

Decide: corrected stem and options; key letter D seems right (`Zn → Zn²⁺`,
`2H⁺ → H₂`).

## 3. CHIM-C10-COMM-001 — p. 147 (commentato)

Q: *Se a una soluzione acquosa di AgNO₃ si aggiunge una soluzione di HCl:*
Key: **E. precipita cloruro d'argento**

Problem is in `ExplanationHTML`:

> … La reazione è: AgNO, + HC] — AgCl + HNO, e rappresenta u…

After the HCl pass: `AgNO, + HCl — AgCl + HNO,`.
Decide: `AgNO,` → `AgNO₃`, `HNO,` → `HNO₃`, `—` → `→`?
`AgNO₃ + HCl → AgCl↓ + HNO₃`.

## 4. CHIM-C10-COMM-030 — p. 151 (commentato)

Q: *La formula H,S0,, secondo la nomenclatura tradizionale corrisponde a:*
Key: **D. l'acido solforoso**

`H,S0,,` is OCR for **H₂SO₃**. Decide whether the stem is corrected to
`H₂SO₃` (consistent with D) and whether the explanation mentions the
distinction H₂SO₃ (solforoso) vs H₂SO₄ (solforico).

## 5. CHIM-C11-NCOM-015 — p. 171

Q: *Quale/i dei seguenti acidi è/sono monoprotico/i in soluzione acquosa?
L CH₃COOH 2.HNO₃ 3.H₃PO₄*
Key: **A. Solole2**

Options: `A) Solole2`, `B) Solo 1`, `C) Solo 2`, `D) Solo 3`, `E) Solo 2e3`.

Likely intended: stem numbering `1. CH₃COOH  2. HNO₃  3. H₃PO₄`; option A
`Solo 1 e 2`; option E `Solo 2 e 3`. Chemically CH₃COOH and HNO₃ are
monoprotic, H₃PO₄ is triprotic → A (`Solo 1 e 2`) fits the key. Confirm and
fix the text.

## 6. CHIM-C11-NCOM-034 — p. 173

Q: *Quale dei seguenti ioni, secondo la definizione di Brønsted-Lowry, può
comportarsi solo come acido?*
Key: **E. NH;**

Options are OCR-mangled: `A) S02` (SO₂? SO₃²⁻?), `B) HPO` (HPO₄²⁻?),
`C) OH-`, `D) HSO;` (HSO₄⁻?), `E) NH;` (NH₄⁺?).

Key E makes sense only if E is **NH₄⁺** (can only donate a proton).
Decide the intended species for A, B, D, E; keep E if it is NH₄⁺.

## 7. CHIM-C11-NCOM-037 — p. 173

Q: *Quale dei seguenti composti reagisce con acqua per formare un acido
ossigenato?*
Key: **A. (1,0,**

Options: `A) (1,0,`, `B) Na,O` (Na₂O), `C) NH₃`, `D) Al,O,` (Al₂O₃),
`E) KOH`. `(1,0,` is unrecoverable without the scan; likely an acidic oxide
(e.g. CO₂ / SO₃ / Cl₂O). Needs the scan, not a guess.

## 8. CHIM-C11-NCOM-051 — p. 175

Q: *Se in una soluzione acquosa la concentrazione degli ioni ossidrile è
10⁻⁵ moli/litro, la concentrazione degli ioni idrogeno deve essere:*
Key: **E. 107 moli/litro**

With `Kw = 10⁻¹⁴`, `[H⁺] = 10⁻¹⁴ / 10⁻⁵ = 10⁻⁹`. So the key text `107` is
almost certainly `10⁻⁹`, and option B `10°` may also be `10⁻⁹` — i.e. the
letter may be wrong, or two options are the same after OCR. Options include
`10⁴`, `10°`, `10⁻³`, `10⁻⁵`, `107`. **Needs adjudication with the scan.**

## 9. CHIM-C11-NCOM-007 — p. 170

Q: *Un acido è una sostanza che:*
Key: **C. cede ioni H°**

`H°` is OCR for `H⁺` (degree sign instead of superscript plus). Decide the
text fix only: `cede ioni H⁺` (key stays C).

---

### How these get fixed

Once decided, the same pipeline script (`31_fix_text_defects.py`) can take
literal replacements (add them to `NOTE_FIXES` keyed by `ItemID`), or a small
one-off patch can be applied with the same safety guarantees (Anki closed,
`Connection.backup`, single transaction, stats fingerprint unchanged).
