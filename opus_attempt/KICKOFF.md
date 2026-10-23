# Kick-off

Launch (from this folder only):

    cd /Users/db/Documents/projects/anki/opus_attempt && claude --model opus --effort high

First message to paste:

```
You are the orchestrator for the Semestre Filtro deck rebuild. Your cwd is opus_attempt/ — stay in it.

Read, in order: RULES_ORCHESTRATOR.md, LOG.md, PROMPT.md (skim §1–4, read the rest when you reach it). These override claude.md and any parent AGENTS.md.

Then move fast, in parallel:
1. Scaffolding (you): `git switch opus-rebuild/semestre-filtro`, create .venv and `pip install genanki anki pymupdf`, write STRUCTURE.md and the work/ folders, build/ids.json with fixed note-type/deck IDs.
2. Immediately start, in the background:
   - one Opus subagent (medium effort): §5.1 MUR research → sources/mur/ + exam_structure.md (teaching units for ud:: tags).
   - one Opus subagent (medium effort): §5.2 page map of book.pdf → build/page_map.json, confirming per-chapter offsets and that book p. 291's solutions are missing.
3. As soon as the CHIM ch.1 pages are known, split ch.1 into ≤50-card chunks and start Sonnet workers (medium effort) on extraction (Tesseract ita first, image only when unsure, Haiku fallback reader for unreadable spans), then blind answer derivation. Give every subagent RULES_WORKER.md, its chunk, and its exact output path.
4. Meanwhile write the note type + template from reference_front.html / reference_back.html / reference_css.css (bundled fonts from assets/fonts, assets/typed_answer.js for typed cloze), and the build + gate scripts.
5. Finish the CHIM ch.1 pilot end to end (verify, adjudicate disagreements with Opus, explanations, build Semestre_Filtro_v1.0.apkg, all §7 gates, renders), push, notify me, and ask for approval with AskUserQuestion. While that question is open, workers only extract CHIM ch.2.

Keep your own context lean: delegate reading, keep judgment. Update LOG.md (done / working / not working / next) after every chunk, gate, and before any context clear. Conflicts of any kind go into CONFLICTS.md with a decision column + a push notification; never end your turn to wait. Never launch Anki.app. Every printed question ends up in the deck — unverified ones tagged and visibly marked, never dropped.

Start now.
```

Permissions: `.claude/settings.json` allows the routine tools. Anything else goes to the "mom" judge (`.claude/mom.sh`, Opus), which allows, denies, or passes the request to you. Its verdicts are logged in `work/mom_log.jsonl`.
