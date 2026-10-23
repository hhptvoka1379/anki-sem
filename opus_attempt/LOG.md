# Orchestrator log

Update after every chapter, every gate, and before any context clear. See `RULES_ORCHESTRATOR.md`.

## Done
- (pre-run, by the setup session) Confirmed: `anki` Python library 26.9.3 imports an `.apkg` into a temporary collection, and copies media (including fonts with a leading underscore).
- (pre-run) Tested `assets/typed_answer.js` against Anki 26.9.3's real comparison HTML: 9/9 cases correct, including an elided article, a plural variant, accents, and an empty answer.
- (pre-run) The user confirmed on Anki desktop that the typed-answer probe card works.
- (pre-run) Downloaded the fonts the CSS uses into `assets/fonts/` (Space Grotesk, Space Mono, Syne, OFL licences included).

## Working
- On the back side, Anki puts the comparison in `<code id=typeans>`. An exact match is one line. A wrong answer is the typed text, then `<br><span id=typearrow>`, then the expected text. `typed_answer.js` reads the first line, skipping `.typeMissed`.
- The library render (`card.answer()`) leaves `[[type:TypedAnswer]]` in place. For test renders, replace it with `col.compare_answer(expected, typed)`.

## Not working / tried and failed
- `anki -b <folder> file.apkg` while Anki is already running prints "Already running; reusing existing instance" and imports into the real profile. Never launch Anki.app.

## Next
1. Read `PROMPT.md`, `RULES_ORCHESTRATOR.md`, and `RULES_WORKER.md`.
2. Create the branch, the venv, `STRUCTURE.md`, and the folders.
3. §5.1 MUR pages, then §5.2 page map.
