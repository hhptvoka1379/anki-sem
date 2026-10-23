#!/bin/bash
# "Mom" judge: an Opus call that decides permission requests the allowlist does not cover.
# ALLOW / DENY are answered here; ASK (or any failure) prints nothing, so Claude Code
# falls back to the normal permission prompt and the user decides.
set -u
DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$DIR/work/mom_log.jsonl"
mkdir -p "$DIR/work"

REQ="$(cat)"

PROMPT="You judge one permission request from an unattended build agent. Answer with exactly one line: ALLOW: <reason>, DENY: <reason>, or ASK: <reason>.

The agent builds an Anki deck from book.pdf. Its scope: it may only write inside $DIR, may read two tool paths (/Users/db/Documents/projects/anki/_tools/tessdata and it_IT.dic/aff), may use the web only for MUR (Italian ministry) pages about the Semestre Filtro test and for package installs, and may use git only on branch opus-rebuild/semestre-filtro (no force-push, no merge, no main, no PRs).

ALLOW requests that clearly fit that scope and are reversible.
DENY requests that: launch Anki.app or touch ~/Library/Application Support/Anki2; delete or overwrite files outside $DIR; touch book.pdf; force-push, merge, rewrite history, or act on another branch or repo; send data to services unrelated to the task; read other project folders.
ASK for anything else: irreversible deletes inside the folder, unusual network targets, installs outside the venv, or anything you are unsure about. When in doubt, ASK.

Request JSON:
$REQ"

VERDICT="$(cd /tmp && printf '%s' "$PROMPT" | timeout 80 claude -p --model opus 2>/dev/null | tr -d '\r' | grep -m1 -E '^(ALLOW|DENY|ASK):')"
KIND="${VERDICT%%:*}"
REASON="${VERDICT#*: }"

printf '%s\n' "$(jq -cn --arg t "$(date -u +%FT%TZ)" --arg v "${VERDICT:-ASK: no verdict}" --argjson r "$REQ" '{time:$t, verdict:$v, tool:$r.tool_name, input:$r.tool_input}' 2>/dev/null)" >> "$LOG"

case "$KIND" in
  ALLOW) jq -cn '{hookSpecificOutput:{hookEventName:"PermissionRequest",decision:{behavior:"allow"}}}' ;;
  DENY)  jq -cn --arg m "Mom (Opus judge) denied: $REASON" '{hookSpecificOutput:{hookEventName:"PermissionRequest",decision:{behavior:"deny",message:$m}}}' ;;
  *)     : ;;  # ASK or failure: stay silent so the user is prompted
esac
exit 0
