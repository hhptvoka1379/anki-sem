#!/usr/bin/env python3
import sqlite3, subprocess
con = sqlite3.connect("file:questions.db?mode=ro", uri=True, timeout=30)
counts = dict(con.execute("SELECT status, count(*) FROM questions GROUP BY 1").fetchall())
last_ord = con.execute("SELECT max(ord) FROM questions WHERE status != 'pending'").fetchone()[0]
next_ord = con.execute("SELECT min(ord) FROM v_pending").fetchone()[0]
head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True, cwd="..").stdout.strip()
text = f"""# STATE

- Branch: arena/d5111e50-anki-sem (Arena session branch; the platform fixes this
  branch name, so explanations/run-1 cannot be created/used in this session.
  All work, commits and pushes stay on this branch. No PR will be opened.)
- Workpack extracted directly into work/ (zip is flat: PROMPT.md, questions.db,
  validate.py, export_reasons.py, etc. live in work/, no subfolder).
- Zip was on main (commit d06dd4e), not on this branch's base; retrieved with
  `git show main:uncommented_questions_workpack.zip` into work/.
- Initial DB query: pending = 5902 (matches TASK.md section 2.3).
- Current counts (from DB query): done = {counts.get('done', 0)}, flagged = {counts.get('flagged', 0)}, pending = {counts.get('pending', 0)}.
- Last processed ord = {last_ord}; next pending ord = {next_ord}.
- Last checkpoint commit: {head if head else 'none yet'} (HEAD; checkpoint commits are the 'checkpoint:' ones).
- Open questions asked to the user: none.
"""
open("STATE.md", "w", encoding="utf-8").write(text)
print(counts, "last_ord", last_ord, "next_ord", next_ord)
