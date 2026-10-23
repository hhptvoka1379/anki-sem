# Decisions

| date | decision | reason |
|---|---|---|
| 2026-10-23 | Subagents do not commit; the orchestrator commits and pushes. | Parallel agents committing in one repo race on `.git/index.lock`; one committer keeps staging checkable with `git status`. |
| 2026-10-23 | Page-map agent writes `work/pagemap/page_map.json`; orchestrator validates and copies it to `build/page_map.json`. | `build/` is orchestrator-only (RULES_ORCHESTRATOR). |
| 2026-10-23 | Full-book OCR runs as a plain script (`scripts/ocr_all.sh`, 300 dpi gray, 6 processes) into `work/ocr/`, not as agents. | Mechanical work; no judgment needed; workers then read OCR text + images. 6 not 8 processes to leave room for the page-map agent under the 8-process cap. |
| 2026-10-23 | Template, build script and gate scripts drafted by Sonnet workers in `work/{template,buildscript,gates}/`; orchestrator reviews and promotes to `templates/` and `scripts/`. | User asked to deploy more Sonnet agents while usage is available; orchestrator keeps ownership by reviewing before promotion. |
| 2026-10-23 | Chapter/type deck IDs are generated once by the build script and appended to `build/ids.json`, never changed. | Chapter titles were not known at setup; IDs keyed by `SUBJ-Cnn[-TYPE]` stay stable even if a title is corrected. |
