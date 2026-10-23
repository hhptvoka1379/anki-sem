"""Generated explanations (PROMPT.md §5.6) with DeepSeek, then an independent check pass.

  ds_explain.py draft-jobs --extracted X --verification V --workdir DIR    (needs final keys)
  deepseek_batch.py DIR/draft_jobs.jsonl DIR/draft_results.jsonl --mode batch ...
  ds_explain.py check-jobs --extracted X --verification V --workdir DIR
  deepseek_batch.py DIR/check_jobs.jsonl DIR/check_results.jsonl --mode batch ...
  ds_explain.py collect --workdir DIR      -> DIR/explanations.jsonl (only drafts the check passed)

COMM questions use the book's reasoning and are skipped here.
"""
import argparse, json, re, sys
from pathlib import Path

DRAFT = """Per ogni domanda scrivi una spiegazione in italiano della risposta corretta indicata. Scelta multipla: 2-4 frasi che nominano il principio, la formula o la definizione decisiva. Completamento: 1-2 frasi sul perché la parola è giusta. Ricalcola ogni numero. Non inventare nomi, date o costanti. Testo semplice, formule Unicode (H₂O, 10⁻⁹), niente HTML, niente a capo.
Rispondi solo con JSON: {{"explanations": [{{"id": str, "explanation": str}}]}}

{items}"""

CHECK = """Controlla ogni spiegazione: numeri sbagliati (ricalcolali), contraddizioni con la risposta corretta, affermazioni false o non supportate. "ok": true solo se non c'è nessun problema.
Rispondi solo con JSON: {{"checks": [{{"id": str, "ok": bool, "problem": str}}]}}

{items}"""


def load(path):
    return {r["id"]: r for r in map(json.loads, open(path)) if r}


def item(r, v, expl=None):
    lines = ["id: " + r["id"], r["stem"]]
    lines += ["%s. %s" % kv for kv in (r.get("options") or {}).items()]
    lines.append("Risposta corretta: " + v["final_key"])
    if expl is not None:
        lines.append("Spiegazione: " + expl)
    return "\n".join(lines)


def parse(content, field):
    return json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", content.strip()))[field]


def write_jobs(path, prefix, prompt, items, per_job):
    with open(path, "w", encoding="utf-8") as f:
        for i in range(0, len(items), per_job):
            chunk = items[i:i + per_job]
            f.write(json.dumps({"id": "%s-%s" % (prefix, chunk[0][0]), "max_tokens": 12000,
                                "prompt": prompt.format(items="\n\n".join(t for _, t in chunk))},
                               ensure_ascii=False) + "\n")
    print("wrote %s (%d items)" % (path, len(items)))


def results(path, field):
    out = {}
    for res in map(json.loads, open(path)):
        if res.get("status") == "ok":
            for x in parse(res["content"], field):
                out[x["id"]] = x
    return out


def clean(text):
    # Plain text only: the field is rendered as HTML, so no tags and no line breaks.
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", text or "")).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["draft-jobs", "check-jobs", "collect"])
    ap.add_argument("--extracted")
    ap.add_argument("--verification")
    ap.add_argument("--workdir", required=True)
    ap.add_argument("--per-job", type=int, default=15)
    a = ap.parse_args()
    w = Path(a.workdir)
    w.mkdir(parents=True, exist_ok=True)
    if a.cmd in ("draft-jobs", "check-jobs"):
        recs, ver = load(a.extracted), load(a.verification)
        todo = [(i, recs[i], ver[i]) for i in recs if i in ver and recs[i]["quiz_type"] != "COMM" and ver[i].get("final_key")]
        if a.cmd == "draft-jobs":
            write_jobs(w / "draft_jobs.jsonl", "x", DRAFT, [(i, item(r, v)) for i, r, v in todo], a.per_job)
        else:
            drafts = results(w / "draft_results.jsonl", "explanations")
            write_jobs(w / "check_jobs.jsonl", "c", CHECK,
                       [(i, item(r, v, clean(drafts[i]["explanation"]))) for i, r, v in todo if i in drafts], a.per_job)
        return
    drafts = results(w / "draft_results.jsonl", "explanations")
    checks = results(w / "check_results.jsonl", "checks")
    kept, rejected = 0, []
    with open(w / "explanations.jsonl", "w", encoding="utf-8") as f:
        for i, d in drafts.items():
            c = checks.get(i)
            if c and c.get("ok") is True:
                f.write(json.dumps({"id": i, "explanation": clean(d["explanation"])}, ensure_ascii=False) + "\n")
                kept += 1
            else:
                rejected.append((i, (c or {}).get("problem", "not checked")))
    with open(w / "rejected.tsv", "w") as f:
        for i, p in rejected:
            f.write("%s\t%s\n" % (i, p))
    print("drafts=%d kept=%d rejected=%d (see rejected.tsv)" % (len(drafts), kept, len(rejected)))


if __name__ == "__main__":
    main()
