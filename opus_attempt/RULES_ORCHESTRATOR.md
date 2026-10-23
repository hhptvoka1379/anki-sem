# Rules for the orchestrator (Opus)

Re-read this file, then `LOG.md`, then the `PROMPT.md` section you are working on, after every context clear or restart. Then continue from the "Next" list in `LOG.md`. Never restart finished work.

## Scope
- Your working directory is `opus_attempt/`. Do not read, list, or search other folders, except the two read-only tool paths in `PROMPT.md` §2.
- These rules and `PROMPT.md` override `claude.md` and any parent `AGENTS.md` where they conflict.

## What you own
- The plan, `STRUCTURE.md`, the note type and template, `build/`, the gates, every judgment call, and every message to the user.
- Keep your own context lean: build the scaffolding, then delegate. Read pages and cards only when adjudicating. During setup you may start one Opus subagent for the MUR and page-map work.
- Split all work into chunks of at most 50 cards. Log tokens and time per chunk. Look into any chunk that costs more than 3× the running average.
- Workers (Sonnet, medium effort) do extraction, OCR clean-up, derivation, and explanation drafts. Give each one job, explicit inputs, and an exact output path and format. Point them to `RULES_WORKER.md`.
- Fallback reader (Haiku 5.5): unreadable OCR spans (`PROMPT.md` §5.3).
- Adjudicator (Opus): every disagreement between a worker and the book, and every low-confidence derivation.
- Reviewer (Opus, medium effort): checks each chapter's conflict list before it goes to the user.

## The log (`LOG.md`)
Update it after every chapter, every gate, and before any context clear. It has four sections, always in this order:
1. **Done**: finished work, with counts from queries and the commit hash.
2. **Working**: what is confirmed to work, and how it was checked.
3. **Not working / tried and failed**: what broke, what you tried, and what you learned, so nobody repeats it.
4. **Next**: the concrete next steps, in order.

Also keep `STATE.md` for the per-chapter status table. Keep `DECISIONS.md` for every judgment call and its reason.

## Hard rules
- Never launch Anki.app. If Anki is already running, a second launch ignores `-b` and imports into the user's real profile. This was confirmed in testing. Check imports with the `anki` Python library on a temporary collection (`PROMPT.md` §7 gate 8).
- Never open the user's real collection under `~/Library/Application Support/Anki2/`.
- Write only inside `opus_attempt/`. Do not modify `book.pdf`.
- Web access: the MUR pages (§5.1) only.
- Git: branch `opus-rebuild/semestre-filtro` only. You alone stage `build/` and the root files. Pull with rebase before pushing. Never force-push, merge, or touch `main`. Ask the user before any destructive command.
- Before merging worker output into `build/`, check with `git status` that each worker wrote only in its own folder.

## When to involve the user
- Never end your turn to wait. The user is watching. Use a push notification plus `LOG.md`.
- Pilot (CHIM chapter 1, final v1.0 names and IDs): after it passes the gates, notify the user and ask for approval with `AskUserQuestion`. While it is open, workers only extract CHIM chapter 2. This is the only planned stop.
- Conflicts of any kind go into `CONFLICTS.md` (with a `decision` column the user fills in) as they appear. At chapter end, the Opus reviewer checks them first, then notify. Read new decisions at every checkpoint and apply them.
- If more than 5% of a chapter's cards end up `verify::unverified`: pause that chapter only, notify, and ask with `AskUserQuestion`, listing the cards and reasons. Other chapters keep running.
- Your only Anki collections are temporary ones made with the `anki` library in `work/anki-test/`. The user imports decks into their own Anki.
- If you are blocked by something only the user can fix (a missing file, credentials).
- Otherwise, decide yourself, and record the decision in `DECISIONS.md`.

## Honesty
- Every report starts with the outcome. A failure or skipped step goes in the first sentence.
- Only call something working if a check you ran confirmed it. Name the checks you did not run.
- Never present a number, formula, name, or answer as certain before checking it.
- Claude cannot judge how the cards look and feel on a phone. Describe the renders, and give the user exact steps for the phone check.
