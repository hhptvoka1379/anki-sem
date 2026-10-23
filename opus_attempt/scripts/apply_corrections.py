"""Apply hand corrections (from the orchestrator's scan checks) to an extracted.jsonl in place.

  apply_corrections.py <extracted.jsonl> <corrections.jsonl>
corrections.jsonl lines: {"id", "set": {field: value, ...}, "why": str}. Each applied fix is noted in
worker_notes; an id that is not in the file is an error, so a stale correction never passes silently.
"""
import json, sys

recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
by_id = {r["id"]: r for r in recs}
bad = 0
for c in map(json.loads, open(sys.argv[2])):
    r = by_id.get(c["id"])
    if not r:
        print("ERROR unknown id", c["id"])
        bad += 1
        continue
    r.update(c["set"])
    r["worker_notes"] = (r.get("worker_notes") or "") + "; corrected: " + c["why"]
with open(sys.argv[1], "w", encoding="utf-8") as f:
    for r in recs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("applied corrections; errors=%d" % bad)
sys.exit(1 if bad else 0)
