# Evaluation Task: Is the "Semestre Filtro EdiSES" Anki deck fit for exam study?

## 0. Mission and ground truth
You are evaluating a generated Anki deck for an Italian medical-school entrance exam (*test d'ingresso*, EdiSES "Eserciziario Unico per il Semestre Filtro 2"). Work read-only against `/Users/db/Documents/projects/anki/repo`. Produce an evidence-backed verdict a skeptical physician-educator would accept.

Known facts (verify, do not assume):
- `output/qa_dataset.jsonl` has 7,078 records; mirrors in `.json`/`.csv`; `output/Semestre_Filtro_EdiSES_Complete.apkg`; `output/figures/` (929 PNGs); `output/verification_report.json`; pipeline in `extractor/`; claims in `README.md`.
- Fields: `id` (e.g. `CHIM-C01-COMM-001`), `global_index`, `subject`, `subject_code`, `chapter_num`, `chapter_title`, `quiz_type` (`commentati` MCQ+book commentary, `non_commentati` MCQ+key only, `completamento` fill-in), `qnum`, `question_book_page`, `answer_book_page`, `question`, `options` (A–E or null), `answer`, `answer_text`, `explanation` (commentati only), `figure_files`, `anki_deck`.
- Source PDF: `Eserciziario Unico per il Semestre Filtro  2-lite-trim.pdf` (902 pages, double space in filename). Pages are scans with only a partial text layer, and contain handwritten student annotations. Tools: `pdftoppm`, `pdftotext`, `pdfimages`; Python at `/Users/db/Documents/projects/anki/.venv/bin/python` (PIL available). No tesseract. You can view rendered PNGs directly — do so; do not rely on `pdftotext` alone.
- PDF page index ≠ printed book page. The trimmed PDF has had blank pages removed, so the offset varies by chapter (roughly +9 early, +6 mid, +1 late). Derive the mapping empirically per chapter before adjudicating any card.
- The deck uses one basic note type (`Semestre Filtro EdiSES — Studio & Esame`) with 16 fields for all 7,078 cards, including `completamento`. Front shows stem + options; back shows highlighted option, answer banner, explanation, optional question crop, optional solution crop. 868 records carry `figure_files`; 1,036 commentati notes carry a `sol_*` solution crop; 1,983 media files total.

## 1. Hard rules
1. Treat every README/verification_report number as a claim, not a fact. Recompute each independently from the artifacts.
2. Never modify `output/`, `extractor/`, or the PDF. Write only `EVAL_REPORT.md` at repo root plus a scratch dir under `/private/var/folders/.../T/`.
3. Every assertion needs a record ID, a verbatim excerpt, and either a page number or a command that reproduces it. No unsupported adjectives.
4. Report uncertainty. A defect rate from 20 cards is an anecdote; label it as such.
5. Distinguish **extraction defect**, **book defect**, and **unresolved**. The book itself has errors; the repo documents four "verbatim book typos": `CHIM-C01-NCOM-010`, `CHIM-C01-NCOM-069`, `CHIM-C10-NCOM-038`, `CHIM-C12-NCOM-157`.

## 2. Adjudicate the claims (≈1 h)
Recompute from scratch:
- 7,078 parity across jsonl/json/csv and apkg note/card counts; 84 subsections; contiguous `1..N`; 5,008 MCQs with 5 distinct options and key ∈ options; 2,070 blanks with `_____`; 1,043 non-empty explanations; "zero defects"; "1,984+ figures"; 84 subdecks.
- Read `extractor/verify.py` and list which invariants are vacuous, self-referential, or whitelisted. Specifically open the four "book typo" IDs: preliminary inspection shows duplicated option text (e.g. `CHIM-C01-NCOM-010` has `C` and `E` both "Ne"; `-069` has `A` and `E` identical; `CHIM-C10-NCOM-038` has `B` and `D` identical; `CHIM-C12-NCOM-157` has `A` and `D` both "2"). Test the hypothesis that the whitelist launders extraction errors: render the answer-key page and decide per item.
- Inspect `CHIM-C11-COMM-017`…`023`. README says book page 291 is missing and these seven keys were *derived by calculation*. Check whether cards or metadata disclose that the keys are inferred rather than sourced; treat undisclosed inference as a blocking defect.
- Count actual distinct figure files, media entries, and cards referencing them. Explain any 929 vs 1,983 vs 868 discrepancy.

## 3. Sampling design (pre-register before looking)
Full-corpus deterministic checks (all 7,078): HTML/escaping sanity, answer ∈ options, `answer_text` ≈ option text, blank count, duplicate stems (preliminary signal: ~79 duplicate stems / ~84 extra cards — confirm and classify as book repetition vs extraction duplication), tag/deck consistency, media existence, figure filename reuse.

Manual review frames:
- **Primary stratified frame:** 5 cards per each of 84 `subject×quiz_type×chapter` subsections (seed `random.seed(20261020)`), n=420. This gives ±4.8 pp at p=0.5 overall and covers every chapter/type.
- **Cell-level estimates:** if any `subject×quiz_type` cell has <40 reviewed cards, report its CI as wide (±15 pp) rather than quoting a point estimate.
- **Random cross-check:** 150 uniform random cards, to detect bias in the stratified pick.
- **Adversarial frame (150):** physics/chemistry items containing digits, units, sub/superscripts, `10^`, `×`, `mol`, `V`, `Ω`; options containing "tutte/nessuna delle precedenti"; very short options (<3 chars); options ending in "-"; figure-bearing cards; explanations containing OCR artifacts (`(0 `, `Il legame`, `ossidrite`, `isatopi`); the whitelist IDs.

Minimum defensible total: 420 reviewed cards. To estimate a defect rate with 95% CI ±5 pp at p=0.5 you need n=384 (`n = z²p(1−p)/e²`); for ±3 pp at p≈0.15 you need ≈545. State which denominator each rate uses.

## 4. Source adjudication (≈2–3 h)
1. Derive the PDF-page ↔ printed-book-page offset empirically: render candidate pages with `pdftoppm -r 200 -f N -l N -png`, locate a known question, record the offset, and use it consistently. Do not guess.
2. For every manual sample card, open its question page and answer page. Score fidelity against the page image.
3. Classify each discrepancy: extraction (OCR/crop/column/merge) → book typo → unresolved (state why). OCR'ing the scan to adjudicate is itself fallible; when the image is ambiguous, mark unresolved rather than blaming extraction.
4. For `commentati`, determine whether `explanation` is genuine book commentary (verbatim-ish, preserves book style and OCR quirks, matches the commentary page) or LLM paraphrase/hallucination. Judge 20 explanations against their `answer_book_page`; quantify.

## 5. Quality dimensions — pass/fail criteria
Score each dimension on the reviewed sample plus deterministic corpus checks. Pass = ≥95% of sampled cards clean on that dimension.
- **(a) Fidelity:** fails on meaning-changing OCR (digit/letter swaps `0`↔`O`, `OV`↔`0 V`), mangled units/subscripts/superscripts, dropped negation, truncated or reflowed options, merged answer columns.
- **(b) Answer key:** fails if key ∉ options, `answer_text` ≠ keyed option, key contradicts the book, or key is domain-wrong. Blind-solve 60 MCQs (20/subject) without seeing the key; report agreement and adjudicate disagreements against the page.
- **(c) Well-formedness:** single defensible answer; no give-away by length/formatting; no duplicated options; blanks solvable and unique from context alone (test 30 blanks cold).
- **(d) Explanations:** present, correct, consistent with key, specific, not a restatement, not hallucinated.
- **(e) Media:** referenced file exists; image legible at mobile size; crop belongs to that question; is it a real diagram or merely a redundant crop of the question text (preliminary: `CHIM_C01_comm_Q001.png` is a crop of Q1's stem and options)? Does any crop leak the answer?
- **(f) Anki UX:** template inspection via unzip + sqlite3; check cloze/fill rendering (`completamento` is a basic card with a blank slot — no typed answer, no auto-grading), HTML escaping (`&#x27;`, `<`, `&`), front-side answer leakage, images on mobile, tags, 84-subdeck hierarchy depth, grading burden (self-graded recall vs MCQ drilling).
- **(g) Duplication:** exact and near-duplicate stems/answers; whether duplication is book-intended or extraction-induced.
- **(h) Coverage:** 28 chapters present; compare against the book TOC; missing page 291; whether high-yield topics are represented.
- **(i) Study value:** compare against studying the PDF directly and against student-made cards.

## 6. Severity and quantification
Assign per card: **S1 blocking** (unanswerable, wrong key, missing/broken media, blank unsolvable), **S2 meaning-changing** (typo/garble alters the fact or makes a distractor defensible), **S3 cosmetic** (accents, spacing, markup; no effect on answer), **S0 clean**.
Report: counts, defect rate per dimension per `subject×quiz_type` with Wilson 95% CIs, severity distribution, and **estimated studyable-as-is cards** = (S0+S3 proportion) × 7,078 with CI. Show the arithmetic.

## 7. Repair economics
Classify defects by fix cost: (i) deterministic rule/regex/dictionary (units, `0`/`O`, subscripts, escaping), (ii) needs re-crop/re-OCR of specific pages, (iii) needs human/book adjudication. Estimate counts, minutes per class, total hours, and whether repair beats regenerating from source. State what fraction is automatable.

## 8. Decision rubric
- **Usable as-is:** ≥95% studyable, zero S1 in the 420 sample (rule of three ⇒ <0.75% at 95%), key errors <1%, UX passes.
- **Usable after cleanup:** ≥85% studyable, S1+S2 <15%, ≥80% of defects deterministically fixable, repair <20 h.
- **Not usable:** S1+S2 >25%, key errors >3%, or repair requires full re-OCR (>60 h).
Then answer plainly: would you personally use these cards for this exam, and would you recommend them to a student with 3 months and a phone?

## 9. Anti-overfitting and time-box
Budget 6–9 h: 1 claims, 1 corpus stats, 3 card review, 2 source adjudication, 1 report. If less time, shrink samples but keep the random seed and report wider CIs; never present a convenience sample as representative. Re-review 40 cards twice to report intra-rater consistency. Do not generalize from the seed examples I gave — they are hypotheses to test.

## 10. Final report (`EVAL_REPORT.md`)
1. Executive verdict (≤150 words) + decision-rubric classification.
2. Claim audit table: claim | README value | recomputed value | verdict | evidence.
3. Scorecard: dimension | weight | pass rate | 95% CI | grade | verdict.
4. Defect taxonomy with counts, severity, and per-subject/type rates.
5. Evidence appendix: ≥40 rows — ID | field | verbatim deck text | source page/excerpt | classification (extraction/book/unresolved) | severity.
6. Silent-failure findings: key errors, plausible-but-wrong OCR, misassigned figures, formatting give-aways, fabricated/derived keys, paraphrase-as-commentary.
7. Prioritized remediation plan with hours and automation split.
8. One honest paragraph: would you study from these cards?
