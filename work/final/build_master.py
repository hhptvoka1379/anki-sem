#!/usr/bin/env python3
"""Consolidate every answer/explanation source in the repo into one master file.

Output: work/final/master.jsonl (one record per question, all 6,948 deck items)
        work/final/gaps.md       (what is still missing / unverified, by category)

Sources (read-only, fetched from git by blob; nothing is modified):
  v5      import/full-anki-folder:v5repo/output/qa_dataset.json  all 6,948 items, book commentary
  wp      work/questions.db (this branch)                          live-corrected text for 5,902 + my reasons
  ex      work/questions.db `examples`                             4 explanations already in the deck
  cc, d5  arena/cc130265, arena/d5111e50 questions.db               second-opinion reasons
  opus    opus-rebuild:opus_attempt/build/verification.jsonl       CHIM C01 re-extraction + explanations
  k0, k9  arena/0c0900a2 answers.jsonl, arena/9d2e065b answer_key  independent keys for 257 items

Precedence for the shipped explanation:
  book commentary (COMM)  >  this branch 'done' (validated, audited)  >  examples
  Everything else stays a *candidate* (cc/d5/opus/k0/k9) until re-verified: never auto-shipped.
"""
import json
import re
import sqlite3
import subprocess
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
PAGE_291 = {f"CHIM-C11-COMM-{n:03d}" for n in range(17, 24)}


def git_bytes(ref_path: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), "show", ref_path],
                          check=True, capture_output=True).stdout


def git_sqlite(ref_path: str, name: str) -> sqlite3.Connection:
    tmp = OUT / f".{name}.db"            # git-ignored scratch, deleted at the end
    tmp.write_bytes(git_bytes(ref_path))
    return sqlite3.connect(tmp)


def nfc(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", s or "")).strip()


def load_reasons(con):
    return {i: {"status": s, "reason": r or "", "flags": json.loads(f or "[]")}
            for i, s, r, f in con.execute("select id,status,reason,flags from questions")}


def main():
    v5 = json.loads(git_bytes("origin/import/full-anki-folder:v5repo/output/qa_dataset.json"))
    v5_meta = {k: v for k, v in v5.items() if k != "items"}
    v5 = v5["items"]
    wp_con = sqlite3.connect(ROOT / "work/questions.db")
    wp_con.row_factory = sqlite3.Row
    wp = {r["id"]: dict(r) for r in wp_con.execute("select * from questions")}
    ex = {r["id"]: dict(r) for r in wp_con.execute("select * from examples")}
    cc = load_reasons(git_sqlite(
        "origin/arena/cc130265-anki-sem:work/uncommented_questions_workpack/questions.db", "cc"))
    d5 = load_reasons(git_sqlite("origin/arena/d5111e50-anki-sem:work/questions.db", "d5"))
    opus = {json.loads(l)["id"]: json.loads(l) for l in git_bytes(
        "origin/opus-rebuild/semestre-filtro:opus_attempt/build/verification.jsonl"
    ).decode().splitlines() if l.strip()}
    k0 = {json.loads(l)["id"]: json.loads(l) for l in git_bytes(
        "origin/arena/0c0900a2-anki-sem:answers.jsonl").decode().splitlines() if l.strip()}
    k9 = {json.loads(l)["id"]: json.loads(l) for l in git_bytes(
        "origin/arena/9d2e065b-anki-sem:answer_key_output.jsonl").decode().splitlines() if l.strip()}

    fixes = {}
    fpath = OUT / "fixes.jsonl"
    if fpath.exists():
        for l in fpath.open(encoding="utf-8"):
            if l.strip():
                f = json.loads(l)
                fixes[f["id"]] = f
    master = []
    for r in v5:
        i = r["id"]
        qt = {"commentati": "COMM", "non_commentati": "NCOM", "completamento": "COMP"}[r["quiz_type"]]
        w = wp.get(i)
        rec = {
            "id": i, "subject_code": r["subject_code"], "chapter_num": r["chapter_num"],
            "chapter_title": r["chapter_title"], "quiz_type": qt, "qnum": r["qnum"],
            "page": r.get("question_book_page"),
            # text: live-corrected workpack copy when available, else v5
            "question": w["question"] if w else r["question"],
            "options": ({k: w[f"option_{k.lower()}"] for k in "ABCDE"} if w and qt != "COMP"
                        else r.get("options")),
            "answer": (w["answer"] if w else r["answer"]) if qt != "COMP" else "",
            "answer_text": w["answer_text"] if w else r.get("answer_text"),
            "back_stem": w["back_stem"] if w else None,
            "accepted_answers": [],          # cloze: filled by the accepted-answers pass
            "text_source": "live(workpack)" if w else "v5",
            "explanation": "", "explanation_origin": None,
            "key_status": "book",            # book | derived(no printed key) | disputed
            "flags": [], "candidates": {}, "key_votes": {},
        }
        # ---- shipped explanation, by precedence
        if qt == "COMM" and nfc(r.get("explanation")):
            rec["explanation"] = nfc(r["explanation"])
            rec["explanation_origin"] = "book"
        if w and w["status"] == "done":
            rec["explanation"], rec["explanation_origin"] = w["reason"], "generated:0c53ca03"
        elif w and w["status"] == "flagged":
            rec["flags"] = json.loads(w["flags"])
        if i in ex and not rec["explanation"]:
            rec["explanation"], rec["explanation_origin"] = ex[i]["reason"], "deck-example"
        if i in PAGE_291:
            rec["key_status"] = "derived(no printed key: book p.291 missing)"
            if rec["explanation_origin"] == "book":
                rec["explanation_origin"] = "generated:v5(not book; p.291 missing)"
        # ---- candidates (never shipped without re-verification)
        for name, src in (("cc130265", cc), ("d5111e50", d5)):
            s = src.get(i)
            if s and s["status"] == "done" and s["reason"] != rec["explanation"]:
                rec["candidates"][name] = s["reason"]
        if i in opus:
            o = opus[i]
            rec["candidates"]["opus"] = o.get("explanation", "")
            rec["key_votes"]["opus"] = o.get("final_key")
        for name, src in (("k0", k0), ("k9", k9)):
            if i in src:
                rec["key_votes"][name] = src[i].get("letter") or src[i].get("answers")
                if src[i].get("reason"):
                    rec["candidates"][name] = src[i]["reason"]
        if qt != "COMP":
            dis = {k: v for k, v in rec["key_votes"].items()
                   if isinstance(v, str) and v and v != rec["answer"]}
            if dis or any(f.startswith("key: suspect") for f in rec["flags"]):
                rec["key_status"] = "disputed" if rec["key_status"] == "book" else rec["key_status"]
                rec["key_disputes"] = dis
        fx = fixes.get(i)
        if fx and fx["verdict"] == "fixed":
            for k in ("question", "options", "answer_text", "back_stem", "accepted_answers"):
                if k in fx:
                    rec[k] = fx[k]
            rec["explanation"] = fx["explanation"]
            rec["explanation_origin"] = "scan-verified:0c53ca03"
            rec["also_correct"] = fx.get("also_correct", [])
            rec["note"] = fx.get("note", "")
            rec["evidence"] = fx["evidence"]
            rec["resolved_flags"], rec["flags"] = rec["flags"], []
            if rec["key_status"] == "disputed":
                rec["key_status"] = "book(scan-verified)"
        elif fx:
            rec["note"], rec["evidence"] = fx.get("note", ""), fx["evidence"]
            rec["key_status"] = "human-decision"
        master.append(rec)

    with open(OUT / "master.jsonl", "w", encoding="utf-8") as fh:
        for rec in master:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # ---- gap report
    tot = Counter(r["quiz_type"] for r in master)
    has = Counter(r["quiz_type"] for r in master if r["explanation"])
    missing = [r for r in master if not r["explanation"]]
    miss_cand = [r for r in missing if r["candidates"]]
    by_prefix = Counter((r["flags"][0].split(":")[0] if r["flags"] else "none") for r in missing)
    by_type_prefix = defaultdict(Counter)
    for r in missing:
        by_type_prefix[r["quiz_type"]][r["flags"][0].split(":")[0] if r["flags"] else "none"] += 1
    disputed = [r for r in master if r["key_status"] == "disputed"]
    lines = [
        "# Gap report — master.jsonl", "",
        f"Total items: **{len(master)}** ({dict(tot)})", "",
        "| type | total | answer key present | explanation present | explanation missing |",
        "|---|---:|---:|---:|---:|",
    ]
    for t in ("COMM", "NCOM", "COMP"):
        keyed = sum(1 for r in master if r["quiz_type"] == t and
                    (r["answer"] in list("ABCDE") if t != "COMP" else nfc(r["answer_text"])))
        lines.append(f"| {t} | {tot[t]} | {keyed} | {has[t]} | {tot[t]-has[t]} |")
    lines += ["", f"Missing explanations: **{len(missing)}**; of these, **{len(miss_cand)}** have an "
              "unverified candidate from another branch.", "",
              "Missing, by flag prefix: " + ", ".join(f"`{k}` {v}" for k, v in by_prefix.most_common()), "",
              "Missing, by type × prefix: " + "; ".join(
                  f"{t}: " + ", ".join(f"{k} {v}" for k, v in c.most_common())
                  for t, c in by_type_prefix.items()), "",
              f"Cloze notes with accepted alternative answers: "
              f"{sum(1 for r in master if r['quiz_type']=='COMP' and r['accepted_answers'])} / {tot['COMP']}", "",
              f"Keys derived without a printed key (p.291): {len(PAGE_291)} → "
              + ", ".join(sorted(PAGE_291)), "",
              f"Disputed keys: **{len(disputed)}**", "",
              "| id | book key | other votes | flag |", "|---|---|---|---|"]
    for r in disputed:
        lines.append(f"| {r['id']} | {r['answer']} | {r.get('key_disputes') or ''} | "
                     f"{(r['flags'][0][:90] if r['flags'] else '')} |")
    (OUT / "gaps.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    for f in OUT.glob(".*.db"):
        f.unlink()
    print("\n".join(lines[:22]))


if __name__ == "__main__":
    main()
