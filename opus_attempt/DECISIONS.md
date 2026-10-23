# Decisions

| date | decision | reason |
|---|---|---|
| 2026-10-23 | Subagents do not commit; the orchestrator commits and pushes. | Parallel agents committing in one repo race on `.git/index.lock`; one committer keeps staging checkable with `git status`. |
| 2026-10-23 | Page-map agent writes `work/pagemap/page_map.json`; orchestrator validates and copies it to `build/page_map.json`. | `build/` is orchestrator-only (RULES_ORCHESTRATOR). |
| 2026-10-23 | Full-book OCR runs as a plain script (`scripts/ocr_all.sh`, 300 dpi gray, 6 processes) into `work/ocr/`, not as agents. | Mechanical work; no judgment needed; workers then read OCR text + images. 6 not 8 processes to leave room for the page-map agent under the 8-process cap. |
| 2026-10-23 | Template, build script and gate scripts drafted by Sonnet workers in `work/{template,buildscript,gates}/`; orchestrator reviews and promotes to `templates/` and `scripts/`. | User asked to deploy more Sonnet agents while usage is available; orchestrator keeps ownership by reviewing before promotion. |
| 2026-10-23 | Chapter/type deck IDs are generated once by the build script and appended to `build/ids.json`, never changed. | Chapter titles were not known at setup; IDs keyed by `SUBJ-Cnn[-TYPE]` stay stable even if a title is corrected. |
| 2026-10-23 | Burst of extra agents ended at user request (5h limit reset). Running agents finish; new agents only per plan: extraction/derivation workers sized to ≤50-card chunks once the CHIM ch.1 page map exists. | User: "go back to being considerate". |
| 2026-10-23 | Subject badge is lilac for every subject (template overrides the reference per-subject colours). | PROMPT §6 says "lilac banner for the subject". One line in style.css restores per-subject colours if wanted. |
| 2026-10-23 | From now on every subagent is Sonnet, high effort, including the adjudicator and reviewer roles PROMPT.md assigns to Opus; spawn QA agents generously. The running Opus page-map agent finishes as is. | User instruction mid-run: "be very generous with the sonnet high agents... they should be sonnet". Overrides PROMPT §3 model/effort. |
