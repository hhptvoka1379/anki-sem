#!/usr/bin/env bash
# Review one or more commits with Opus before they reach the remote.
# Usage: review_commit.sh <sha> [<sha> ...]
# Writes each review to .git/commit-reviews/<sha>.md and exits 1 if any commit gets FAIL.
set -uo pipefail

repo_root="$(git rev-parse --show-toplevel)"
out_dir="$(git rev-parse --git-dir)/commit-reviews"
mkdir -p "$out_dir"
status=0

for sha in "$@"; do
  full="$(git rev-parse --verify "$sha^{commit}")" || { echo "unknown commit: $sha"; status=1; continue; }
  short="${full:0:10}"
  out="$out_dir/$full.md"

  # Skip binaries and large generated outputs; they are not reviewable as text.
  diff_text="$(git -C "$repo_root" show --format='Commit: %H%nAuthor: %an%nSubject: %s%n%n%b' --no-color "$full" \
    -- . ':!*.png' ':!*.jpg' ':!*.pdf' ':!*.apkg' ':!*.mp3' | head -c 200000)"

  rules="$(cat "$repo_root/opus_attempt/RULES_WORKER.md" 2>/dev/null)"

  prompt="You are reviewing one git commit in an Anki flashcard rebuild.
The commit diff is on stdin. The worker rules are below. Commits come from a worker subagent or from the orchestrator. The orchestrator's trailer is Co-Authored-By: Claude Opus; workers use their own model's trailer. The orchestrator may write root .md files and the decision log. Workers may not.

Check for:
1. Worker commits writing outside work/<agent>/. Anything touching build/, book.pdf, root .md files, assets/, or reference files is a FAIL only if the commit is from a worker. For orchestrator commits, say what it touched in the notes.
2. Invented facts: numbers, names, dates, constants, or answers not supported by the commit's own evidence.
3. Explanations that are not Italian plain text, or contain HTML or line breaks where the rules forbid them.
4. Answers marked high confidence without a stated principle, or disagreements that were hidden instead of logged.
5. Broken data: malformed records, duplicate IDs, missing required fields, or changed fixed note-type and deck IDs.
6. Commit message that does not match the change, or lacks the Co-Authored-By trailer.
7. Anything that claims work was done or verified when the diff does not show it.

Output format, exactly:
First line: VERDICT: PASS or VERDICT: FAIL
Then up to 8 bullets, most severe first. Each bullet: file:line (if known), the problem, and why it matters.
Use FAIL only for items 1, 2, 5, or a clear error. Otherwise PASS with notes.
Be brief. No praise.

=== WORKER RULES ===
$rules"

  printf '%s\n' "$diff_text" | claude -p "$prompt" --model claude-opus-5-5 --effort medium > "$out" 2>"$out.err"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "review failed for $short (exit $rc), see $out.err"
    status=1
    continue
  fi

  verdict="$(grep -m1 -oE 'VERDICT: (PASS|FAIL)' "$out" | sed 's/VERDICT: //')"
  echo "== $short ${verdict:-NO VERDICT} -> $out"
  if [ "$verdict" != "PASS" ]; then
    cat "$out"
    status=1
  fi
done

exit $status
