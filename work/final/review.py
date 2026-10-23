#!/usr/bin/env python3
"""Scan-backed review queue for the cards that still lack a verified answer/explanation.

  python3 work/final/review.py next [N] [TYPE]   # show the next N queued cards + stack their scan crops
  python3 work/final/review.py apply      # read a JSON list of fixes on stdin, validate, append
  python3 work/final/review.py status     # queue progress

Queue order: page-291 derived keys (7) -> missing explanations (439) -> other disputed keys.
Crops come from import/full-anki-folder:audit/media/<ID>.png (the deck's QuestionScanHTML images).

Fix record (one per card, appended to fixes.jsonl):
  {"id", "verdict": "fixed" | "human",          # human = cannot be settled from the scan
   "question"?, "options"?: {A..E}, "answer_text"?, "back_stem"?,   # only when the scan shows a different text
   "key": <letter or cloze term as printed / verified>,
   "explanation": <Italian, plain text>, "accepted_answers"?: [...],
   "evidence": <what the crop shows>, "note"?: <human-facing note, e.g. key dispute>}
Answer keys are never changed here: a disagreement with the printed key is recorded with verdict "human".
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MASTER = HERE / "master.jsonl"
FIXES = HERE / "fixes.jsonl"
REVIEW = HERE / "review"
CROP_REF = "origin/import/full-anki-folder:audit/media/{}.png"

TAG = re.compile(r"</?[a-zA-Z][^>]*>")
MD = re.compile(r"(\*\*|__|`|^#{1,6}\s|\[[^\]]*\]\([^)]*\))", re.M)


def load_master():
    return [json.loads(l) for l in MASTER.open(encoding="utf-8")]


def load_fixes():
    if not FIXES.exists():
        return {}
    out = {}
    for l in FIXES.open(encoding="utf-8"):
        if l.strip():
            r = json.loads(l)
            out[r["id"]] = r          # last write wins
    return out


def queue(master):
    p291 = [r for r in master if r["key_status"].startswith("derived")]
    missing = [r for r in master if not r["explanation"] and r not in p291]
    disputed = [r for r in master if r["key_status"] == "disputed" and r["explanation"]]
    return p291 + missing + disputed


def show(rec):
    print(f"=== {rec['id']}  [{rec['quiz_type']}] key={rec['answer'] or rec['answer_text']!r}  "
          f"key_status={rec['key_status']}")
    print("Q:", rec["question"])
    if rec["options"]:
        for k, v in rec["options"].items():
            print(f"   {k}. {v}")
    if rec["quiz_type"] == "COMP":
        print("   answer_text:", rec["answer_text"], "| back_stem:", rec["back_stem"])
    if rec["flags"]:
        print("   flag:", rec["flags"][0])
    if rec.get("key_disputes"):
        print("   other key votes:", rec["key_disputes"])
    if rec["explanation"]:
        print("   current explanation:", rec["explanation"][:300])
    for k, v in rec["candidates"].items():
        if v:
            print(f"   cand[{k}]:", v[:300])


def stack(ids, out):
    from PIL import Image, ImageDraw
    ims = []
    for i in ids:
        data = subprocess.run(["git", "-C", str(ROOT), "show", CROP_REF.format(i)],
                              capture_output=True).stdout
        if not data:
            continue
        p = REVIEW / f"{i}.png"
        p.write_bytes(data)
        im = Image.open(p).convert("L")
        if im.width > 900:
            im = im.resize((900, int(im.height * 900 / im.width)))
        lab = Image.new("L", (im.width, 26), 255)
        ImageDraw.Draw(lab).text((4, 6), i, fill=0)
        ims.append(lab)
        ims.append(im)
    if not ims:
        return
    w = max(x.width for x in ims)
    h = sum(x.height for x in ims) + 6 * len(ims)
    canvas = Image.new("L", (w, h), 200)
    y = 0
    for x in ims:
        canvas.paste(x, (0, y))
        y += x.height + 6
    canvas.save(out)


def validate(fx, rec):
    errs = []
    if fx.get("verdict") not in ("fixed", "human"):
        errs.append("verdict must be fixed|human")
    e = fx.get("explanation", "")
    if fx.get("verdict") == "fixed":
        if not (80 <= len(e) <= 600):
            errs.append(f"explanation length {len(e)} not in 80..600")
        if TAG.search(e) or MD.search(e) or "\n" in e:
            errs.append("explanation has HTML/Markdown/newline")
    if rec["quiz_type"] != "COMP" and fx.get("key") and fx["key"] != rec["answer"] \
            and fx.get("verdict") == "fixed":
        errs.append("key differs from printed key: must be verdict=human with a note")
    if "options" in fx and set(fx["options"]) != set("ABCDE"):
        errs.append("options must have A..E")
    if not fx.get("evidence"):
        errs.append("evidence required")
    return errs


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    master = load_master()
    by_id = {r["id"]: r for r in master}
    done = load_fixes()
    q = queue(master)
    if cmd == "status":
        left = [r for r in q if r["id"] not in done]
        print(f"queue {len(q)} | reviewed {len(q) - len(left)} | left {len(left)} | "
              f"fixed {sum(1 for f in done.values() if f['verdict'] == 'fixed')} | "
              f"human {sum(1 for f in done.values() if f['verdict'] == 'human')}")
    elif cmd == "next":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        typ = sys.argv[3] if len(sys.argv) > 3 else None      # optional: COMM | NCOM | COMP
        todo = [r for r in q if r["id"] not in done and (typ is None or r["quiz_type"] == typ)][:n]
        REVIEW.mkdir(exist_ok=True)
        for r in todo:
            show(r)
        stack([r["id"] for r in todo], REVIEW / "batch.png")
        print(f"\ncrops -> {REVIEW / 'batch.png'}")
    elif cmd == "apply":
        items = json.load(sys.stdin)
        bad = 0
        with FIXES.open("a", encoding="utf-8") as fh:
            for fx in items:
                rec = by_id.get(fx.get("id"))
                errs = ["unknown id"] if rec is None else validate(fx, rec)
                if errs:
                    bad += 1
                    print("REJECT", fx.get("id"), errs)
                    continue
                fh.write(json.dumps(fx, ensure_ascii=False) + "\n")
                print("OK", fx["id"], fx["verdict"])
        sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
