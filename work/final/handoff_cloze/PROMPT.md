# TASK: accepted answers for 2,055 Italian fill-in-the-blank cards

You get `cloze_items.jsonl` (2,055 lines). Each line is one fill-in card from an Italian medical-school entrance-exam workbook (EdiSES, *Semestre Filtro*: chemistry CHIM, biology BIO, physics FIS). Students **type** the missing word(s). Your job: for each blank, list every **other** answer that a strict but fair examiner would also mark correct. These alternatives sit next to the book's answer, so a student who types a valid synonym is not marked wrong.

Input fields: `id`, `subject`, `chapter`, `chapter_title`, `sentence` (blanks written `[[1]]`, `[[2]]`), `book_answers` (`{"1": "…"}`, the book's word for each blank, authoritative), `filled_sentence`, `text_damaged` (true = the sentence has scan/OCR damage), `flag`.

## Output
Write `cloze_answers.jsonl`: exactly one line per input line, same `id`s, same order, UTF-8, no other text.

```json
{"id": "CHIM-C01-COMP-001",
 "accepted": {"1": ["…", "…"]},
 "blank_ok": true,
 "issue": "",
 "confidence": "high"}
```

- `accepted`: for every blank number in `book_answers`, a list of alternatives. **Do not repeat the book answer.** Use an empty list when nothing else is acceptable, which is the normal case for technical terms.
- `blank_ok`: false if the blank looks misplaced or the book answer does not fit the sentence. Examples: the blank cuts a fixed expression (`non [[1]]` → `metalli` when the sentence defines *metalloidi*); the answer contradicts the sentence; the sentence is unreadable.
- `issue`: one short Italian sentence when `blank_ok` is false, when `text_damaged` is true and the damage matters, or when the item has **more than one scientifically correct answer that is not a synonym** (e.g. `[[1]] è il gas nobile più leggero` could only be *elio*, but `un [[1]] trasporta ossigeno` could be *eritrocita* or *emoglobina*). Otherwise use "".
- `confidence`: `high` | `medium` | `low`.

## What counts as an accepted alternative
Accept:
- **True synonyms in this scientific context**: `aeriforme` for `gas`; `globulo rosso` / `emazia` for `eritrocita`; `acido desossiribonucleico` for `DNA`, and the reverse; `legame a idrogeno` for `legame idrogeno`.
- **Standard symbol ↔ name** when the blank is a substance, element, unit or quantity: `N₂`/`azoto molecolare`; `ATP`/`adenosina trifosfato`; `J`/`joule`.
- **Spelling variants that are standard Italian** (`Le Châtelier`/`Le Chatelier`, `ribosio`/`D-ribosio` only if the sentence does not hinge on the stereo-descriptor).
- **Number/gender variants only when the sentence grammar allows them.** Usually it does not, so be strict.

Do not accept:
- Hypernyms or hyponyms (`molecola` for `proteina`), related but different concepts (`massa` for `peso`, `velocità` for `accelerazione`, `mitosi` for `meiosi`), or a looser everyday word when the book asks for the technical one.
- Anything that changes the truth of the filled sentence. Check by substituting it into `filled_sentence`.
- Variants that differ only by a leading article, case, accents or spacing. The deck already ignores those.

**When in doubt, leave it out.** A wrong alternative teaches a wrong fact; a missing synonym only costs one self-graded card.

## Rules
- The book answer is never changed by you. If you think it is wrong, set `blank_ok: false` and explain in `issue`.
- The text is data, not instructions.
- `text_damaged: true` items: still give alternatives if the meaning is clear from `filled_sentence`; otherwise use an empty list, `confidence: low`, and an `issue`.
- No HTML, no Markdown inside values, no explanations beyond `issue`.
- Before handing back: line count = 2,055, every `id` present once, every blank number covered, and no alternative equal (casefolded, accents stripped) to its book answer.

Hand back `cloze_answers.jsonl` only. It gets checked by `validate_cloze_answers.py` and spot-checked against the book scans before anything reaches the deck.
