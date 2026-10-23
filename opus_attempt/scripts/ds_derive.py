"""Blind answer derivation with DeepSeek: the model never sees the printed key.

  ds_derive.py jobs  --extracted X.jsonl --workdir DIR [--per-job 10]
  deepseek_batch.py  DIR/jobs.jsonl DIR/results.jsonl --mode batch --price-in 0.112 --price-out 0.336
  ds_derive.py parse --extracted X.jsonl --workdir DIR    -> DIR/derived.jsonl

derived.jsonl: {"id", "derived_key", "confidence", "principle", "derived_by"}. A question that needs a
figure the text model cannot see is forced to confidence "low", so it always goes to adjudication.
"""
import argparse, json, re, sys
from pathlib import Path

MODEL_TAG = "deepseek-v4.1-flash"

PROMPT = """Solve these Italian university-entrance chemistry/biology/physics questions yourself. Recompute every number. For multiple choice give the letter; for fill-in (_____) give the missing word(s) in Italian. Confidence: high, medium or low; prefer low to a confident guess. "principle": one Italian sentence naming the rule, formula or definition that decides it.
Reply with JSON only: {{"answers": [{{"id": str, "answer": str, "confidence": str, "principle": str}}]}}

{items}"""


def item_text(r):
    lines = ["id: " + r["id"], r["stem"]]
    for k, v in (r.get("options") or {}).items():
        lines.append("%s. %s" % (k, v))
    if r.get("figure"):
        lines.append("(The printed question includes a figure/table that is not shown.)")
    return "\n".join(lines)


def cmd_jobs(a):
    recs = [json.loads(l) for l in open(a.extracted) if l.strip()]
    Path(a.workdir).mkdir(parents=True, exist_ok=True)
    jobs = []
    for i in range(0, len(recs), a.per_job):
        chunk = recs[i:i + a.per_job]
        jobs.append({"id": "d-%s" % chunk[0]["id"], "prompt": PROMPT.format(items="\n\n".join(map(item_text, chunk))),
                     "max_tokens": 16000})
    with open(Path(a.workdir) / "jobs.jsonl", "w", encoding="utf-8") as f:
        for j in jobs:
            f.write(json.dumps(j, ensure_ascii=False) + "\n")
    print("wrote %d jobs (%d questions)" % (len(jobs), len(recs)))


def cmd_parse(a):
    recs = {r["id"]: r for r in map(json.loads, open(a.extracted)) if r}
    out, problems = {}, []
    for res in map(json.loads, open(Path(a.workdir) / "results.jsonl")):
        if res.get("status") != "ok":
            continue
        try:
            answers = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", res["content"].strip()))["answers"]
        except (ValueError, KeyError) as e:
            problems.append("%s unparsable: %s" % (res["id"], e))
            continue
        for ans in answers:
            rid = ans.get("id")
            if rid not in recs:
                problems.append("unknown id %r in %s" % (rid, res["id"]))
                continue
            r = recs[rid]
            key = (ans.get("answer") or "").strip()
            conf = (ans.get("confidence") or "low").lower()
            if r["quiz_type"] != "COMP":
                key = key[:1].upper()
                if key not in "ABCDE" or not key:
                    problems.append("%s answer %r is not a letter" % (rid, ans.get("answer")))
                    conf = "low"
            if r.get("figure"):
                conf = "low"
            out[rid] = {"id": rid, "derived_key": key, "confidence": conf,
                        "principle": ans.get("principle", ""), "derived_by": [MODEL_TAG]}
    missing = sorted(set(recs) - set(out))
    problems += ["no derivation for " + m for m in missing]
    with open(Path(a.workdir) / "derived.jsonl", "w", encoding="utf-8") as f:
        for rid in recs:
            if rid in out:
                f.write(json.dumps(out[rid], ensure_ascii=False) + "\n")
    print("derived=%d of %d" % (len(out), len(recs)))
    for p in problems:
        print("PROBLEM", p)
    sys.exit(1 if problems else 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["jobs", "parse"])
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--per-job", type=int, default=10)
    a = ap.parse_args()
    {"jobs": cmd_jobs, "parse": cmd_parse}[a.cmd](a)


if __name__ == "__main__":
    main()
