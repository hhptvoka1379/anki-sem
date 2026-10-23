# Kick-off

Launch (from this folder only):

    cd /Users/db/Documents/projects/anki/opus_attempt && claude --model opus --effort high

First message to paste:

    Read RULES_ORCHESTRATOR.md, then LOG.md, then PROMPT.md. Start from the "Next" list in LOG.md and run the build end to end as specified, beginning with the scaffolding and the CHIM chapter 1 pilot.

Permissions: `.claude/settings.json` allows the routine tools. Anything else goes to the "mom" judge (`.claude/mom.sh`, Opus), which allows, denies, or passes the request to you. Its verdicts are logged in `work/mom_log.jsonl`.
