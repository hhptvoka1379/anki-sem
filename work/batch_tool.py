#!/usr/bin/env python3
"""Batch helper for work/questions.db strictly following PROMPT.md & TASK.md."""
import json
import os
import random
import re
import sqlite3
import subprocess
import sys
import time

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.dirname(WORK_DIR)
DB_PATH = os.path.join(WORK_DIR, "questions.db")
STATE_PATH = os.path.join(WORK_DIR, "STATE.md")
META_STATE_PATH = os.path.join(WORK_DIR, ".checkpoint_state.json")
BRANCH = "arena/0c53ca03-anki-sem"

TAG = re.compile(r"</?[a-zA-Z][^>]*>")
MD = re.compile(r"(\*\*|__|`|^#{1,6}\s|\[[^\]]*\]\([^)]*\))", re.M)
PLACEHOLDERS = {"da definire", "todo", "tbd", "n/a", "-", "—", "…"}
VALID_PREFIXES = ("ocr: ", "chem: ", "ambiguous: ", "key: suspect", "missing: ")
FORBIDDEN_WORDS = re.compile(
    r"\b(probabilmente|forse|sembra|verosimilmente|parola mancante|il libro|scansione|ocr)\b",
    re.IGNORECASE,
)


def connect_db():
    for attempt in range(5):
        try:
            con = sqlite3.connect(DB_PATH, timeout=30, isolation_level=None)
            con.row_factory = sqlite3.Row
            return con
        except sqlite3.OperationalError:
            if attempt == 4:
                raise
            time.sleep(2)


def load_meta():
    if os.path.exists(META_STATE_PATH):
        with open(META_STATE_PATH, encoding="utf-8") as fh:
            return json.load(fh)
    return {"last_cp_bucket": 0, "last_val100_bucket": 0, "last_commit": "none"}


def save_meta(meta):
    with open(META_STATE_PATH, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=2)


def get_counts(con):
    d = {"pending": 0, "done": 0, "flagged": 0}
    for st, cnt in con.execute("SELECT status, count(*) FROM questions GROUP BY 1"):
        d[st] = cnt
    return d


def write_state(con, meta):
    c = get_counts(con)
    content = (
        f"# Workpack State\n\n"
        f"- **Branch**: `{BRANCH}` (Arena fixed session branch; requested working branch name `explanations/run-1` noted)\n"
        f"- **Done**: {c['done']}\n"
        f"- **Flagged**: {c['flagged']}\n"
        f"- **Pending**: {c['pending']}\n"
        f"- **Total**: {c['done'] + c['flagged'] + c['pending']}\n"
        f"- **Last checkpoint commit**: `{meta['last_commit']}`\n"
        f"- **Open questions to user**: None\n"
    )
    with open(STATE_PATH, "w", encoding="utf-8") as fh:
        fh.write(content)
    return c


def run_validate(allow_pending=True, quiet=True):
    cmd = [sys.executable, os.path.join(WORK_DIR, "validate.py")]
    if allow_pending:
        cmd.append("--allow-pending")
    if quiet:
        cmd.append("--quiet")
    res = subprocess.run(cmd, cwd=WORK_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        sys.stderr.write("VALIDATE FAILED:\n" + res.stdout + res.stderr + "\n")
        sys.exit(1)
    return res.stdout.strip()


def run_checkpoint(con, meta):
    res = subprocess.run(
        [sys.executable, os.path.join(WORK_DIR, "export_reasons.py")],
        cwd=WORK_DIR,
        capture_output=True,
        text=True,
        check=True,
    )
    c = write_state(con, meta)
    msg = f"checkpoint: {c['done']} done / {c['flagged']} flagged / {c['pending']} pending"
    subprocess.run(["git", "add", "work/"], cwd=REPO_DIR, check=True)
    commit_res = subprocess.run(
        ["git", "commit", "-m", msg],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    if commit_res.returncode == 0:
        sha = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=REPO_DIR, text=True
        ).strip()
        meta["last_commit"] = f"{sha} ({msg})"
        save_meta(meta)
        write_state(con, meta)
    pushed = False
    for attempt in range(3):
        p = subprocess.run(
            ["git", "push", "-u", "origin", BRANCH],
            cwd=REPO_DIR,
            capture_output=True,
            text=True,
        )
        if p.returncode == 0:
            pushed = True
            break
        time.sleep(2)
    if not pushed:
        sys.stderr.write(f"GIT PUSH FAILED: {p.stderr}\n")
        sys.exit(2)
    print(f"[CHECKPOINT PUSHED] {meta['last_commit']} | {res.stdout.strip()}")


def format_rows(rows):
    out = []
    for r in rows:
        if r["quiz_type"] == "Quiz non commentati":
            out.append(
                f"[{r['ord']}] {r['id']} | {r['subject_code']} C{r['chapter_num']:02d} ({r['chapter_title']}) p.{r['page']} q.{r['qnum']} | MCQ\n"
                f"  Q: {r['question']}\n"
                f"  A: {r['option_a']} || B: {r['option_b']} || C: {r['option_c']} || D: {r['option_d']} || E: {r['option_e']}\n"
                f"  KEY: {r['answer']} -> {r['answer_text']}"
            )
        else:
            out.append(
                f"[{r['ord']}] {r['id']} | {r['subject_code']} C{r['chapter_num']:02d} ({r['chapter_title']}) p.{r['page']} q.{r['qnum']} | CLOZE\n"
                f"  Q: {r['question']}\n"
                f"  BACK: {r['back_stem']}\n"
                f"  TERM: {r['answer_text']}"
            )
    return "\n".join(out)


def check_item(item, row, existing_reasons):
    st = item["status"]
    reason = item.get("reason", "").strip()
    flags = item.get("flags", [])
    if st == "done":
        if flags:
            raise ValueError(f"{row['id']}: done item must not have flags")
        if not (80 <= len(reason) <= 600):
            raise ValueError(f"{row['id']}: length {len(reason)} outside 80..600")
        if "\n" in reason or "\r" in reason:
            raise ValueError(f"{row['id']}: newline in reason")
        if (reason[0] in "\"'«“" and reason[-1] in "\"'»”") or "$" in reason or "\\frac" in reason:
            raise ValueError(f"{row['id']}: quotes/LaTeX in reason")
        if TAG.search(reason):
            raise ValueError(f"{row['id']}: HTML-like pattern in reason: {TAG.search(reason).group(0)}")
        if MD.search(reason):
            raise ValueError(f"{row['id']}: Markdown pattern in reason: {MD.search(reason).group(0)}")
        if FORBIDDEN_WORDS.search(reason):
            raise ValueError(f"{row['id']}: forbidden hedging/meta word '{FORBIDDEN_WORDS.search(reason).group(0)}'")
        cf = reason.casefold()
        if cf in PLACEHOLDERS or cf == (row["answer_text"] or "").strip().casefold():
            raise ValueError(f"{row['id']}: placeholder/repeat answer_text")
        if cf in existing_reasons:
            raise ValueError(f"{row['id']}: duplicate reason")
        existing_reasons.add(cf)
        return reason, ""
    elif st == "flagged":
        if reason != "":
            raise ValueError(f"{row['id']}: flagged row must have empty reason")
        if not isinstance(flags, list) or not flags:
            raise ValueError(f"{row['id']}: flagged row needs non-empty flags list")
        for f in flags:
            if not isinstance(f, str) or not f.startswith(VALID_PREFIXES):
                raise ValueError(f"{row['id']}: invalid flag {f!r}")
        return "", json.dumps(flags, ensure_ascii=False)
    else:
        raise ValueError(f"{row['id']}: invalid status {st!r}")


def main():
    mode = sys.argv[1]
    con = connect_db()
    meta = load_meta()

    if mode == "init":
        c = write_state(con, meta)
        save_meta(meta)
        print("INIT OK:", c)
        return

    if mode == "fetch":
        n = int(sys.argv[2])
        rows = con.execute(
            "SELECT * FROM v_pending ORDER BY ord LIMIT ?", (n,)
        ).fetchall()
        print(format_rows(rows))
        return

    if mode == "apply":
        next_n = int(sys.argv[2]) if len(sys.argv) > 2 else 75
        raw_lines = [ln.strip() for ln in sys.stdin if ln.strip()]
        items = [json.loads(ln) for ln in raw_lines]
        expected_rows = con.execute(
            "SELECT * FROM v_pending ORDER BY ord LIMIT ?", (len(items),)
        ).fetchall()
        if len(expected_rows) != len(items):
            raise RuntimeError(f"Expected {len(items)} pending rows, found {len(expected_rows)}")

        existing_reasons = {
            r[0].strip().casefold()
            for r in con.execute("SELECT reason FROM questions WHERE status='done'")
        }

        validated = []
        for item, row in zip(items, expected_rows):
            if item["id"] != row["id"]:
                raise RuntimeError(f"Order mismatch: got {item['id']}, expected {row['id']} (ord={row['ord']})")
            reason, flags_str = check_item(item, row, existing_reasons)
            validated.append((row, item["status"], reason, flags_str))

        # Apply strictly in SQLite transactions of at most 25 rows in ord order
        for start in range(0, len(validated), 25):
            chunk = validated[start : start + 25]
            con.execute("BEGIN IMMEDIATE")
            try:
                for row, st, reason, flags_str in chunk:
                    cur = con.execute(
                        "UPDATE questions SET reason = ?, flags = ?, status = ?, "
                        "updated_at = strftime('%Y-%m-%dT%H:%M:%SZ','now') "
                        "WHERE id = ? AND status = 'pending'",
                        (reason, flags_str, st, row["id"]),
                    )
                    if cur.rowcount != 1:
                        raise RuntimeError(f"rowcount={cur.rowcount} for {row['id']}")
                con.execute("COMMIT")
            except Exception:
                con.execute("ROLLBACK")
                raise

            val_out = run_validate(allow_pending=True, quiet=True)
            c = write_state(con, meta)
            save_meta(meta)

            completed = c["done"] + c["flagged"]
            val100_bucket = completed // 100
            if val100_bucket > meta["last_val100_bucket"]:
                meta["last_val100_bucket"] = val100_bucket
                save_meta(meta)
                val_out_100 = run_validate(allow_pending=True, quiet=True)
                last100_done = con.execute(
                    "SELECT ord, id, question, answer, answer_text, back_stem, reason "
                    "FROM questions WHERE ord < ? AND ord >= ? AND status='done' ORDER BY ord",
                    (chunk[-1][0]["ord"] + 1, max(0, chunk[-1][0]["ord"] - 99)),
                ).fetchall()
                sample = random.Random(val100_bucket).sample(
                    last100_done, min(5, len(last100_done))
                )
                print(f"[VAL-100 #{val100_bucket}] {val_out_100}")
                for s in sample:
                    print(
                        f"  SPOT [{s['ord']}] {s['id']} (ans={s['answer']} {s['answer_text']!r}): {s['reason']}"
                    )

            cp_bucket = c["done"] // 250
            if cp_bucket > meta["last_cp_bucket"]:
                meta["last_cp_bucket"] = cp_bucket
                save_meta(meta)
                run_checkpoint(con, meta)

        c = get_counts(con)
        print(f"[APPLIED {len(validated)}] done={c['done']} flagged={c['flagged']} pending={c['pending']}")
        if next_n > 0 and c["pending"] > 0:
            nxt = con.execute(
                "SELECT * FROM v_pending ORDER BY ord LIMIT ?", (next_n,)
            ).fetchall()
            print(f"=== NEXT {len(nxt)} PENDING ===")
            print(format_rows(nxt))


if __name__ == "__main__":
    main()
