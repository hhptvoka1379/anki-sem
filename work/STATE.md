# STATE

- Branch: arena/d5111e50-anki-sem (Arena session branch; the platform fixes this
  branch name, so explanations/run-1 cannot be created/used in this session.
  All work, commits and pushes stay on this branch. No PR will be opened.)
- Workpack extracted directly into work/ (zip is flat: PROMPT.md, questions.db,
  validate.py, export_reasons.py, etc. live in work/, no subfolder).
- Zip was on main (commit d06dd4e), not on this branch's base; retrieved with
  `git show main:uncommented_questions_workpack.zip` into work/.
- Initial DB query: pending = 5902 (matches TASK.md section 2.3).
- Current counts (from DB query): done = 2752, flagged = 173, pending = 2977.
- Last processed ord = 2924; next pending ord = 2925.
- Last checkpoint commit: 262ba0f (HEAD; checkpoint commits are the 'checkpoint:' ones).
- Open questions asked to the user: none.
