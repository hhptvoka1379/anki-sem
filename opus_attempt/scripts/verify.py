"""Join extracted records, blind derivations, adjudications and explanations into verification.jsonl
(PROMPT.md §5.4). No model calls.

  verify.py --extracted X.jsonl --derived D.jsonl --ud chim-struttura-atomo --out V.jsonl
            [--adjudications A.jsonl] [--explanations E.jsonl] [--pending P.jsonl]

Agreement (printed key == blind derivation, confidence high/medium) -> verified. Anything else needs
an adjudication record {id, final_key, status, reason: [..], note, by}; until it has one it is written
to --pending and the run exits 1, so a build never ships an undecided card.
"""
import argparse, json, re, sys, unicodedata
from pathlib import Path

ARTICLE = re.compile(r"^(?:(?:il|lo|la|i|gli|le|un|uno|una)\s+|(?:l|un|dell|nell|all|sull)'\s*)", re.I)
NOTE_DERIVED = "Risposta ricavata: la soluzione non è presente nella scansione"


def norm_word(s):
    s = unicodedata.normalize("NFD", (s or "").replace("’", "'"))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower().strip(" .;:")
    return re.sub(r"\s+", " ", ARTICLE.sub("", s))


def load(path):
    if not path or not Path(path).exists():
        return {}
    return {r["id"]: r for r in map(json.loads, open(path)) if r}


def book_explanation(r):
    """COMM reasoning is printed as 'D. <text>'; the letter is already in the banner."""
    text = (r.get("printed_reasoning") or "").strip()
    return re.sub(r"^[A-E]\.\s*", "", text)


def dup_groups(recs):
    seen = {}
    for r in recs:
        sig = norm_word(r["stem"]) + "|" + "|".join(norm_word(v) for v in (r.get("options") or {}).values())
        seen.setdefault(sig, []).append(r["id"])
    return {i: [j for j in ids if j != i] for ids in seen.values() if len(ids) > 1 for i in ids}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--derived", required=True)
    ap.add_argument("--ud", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--adjudications")
    ap.add_argument("--explanations")
    ap.add_argument("--pending", default=None)
    a = ap.parse_args()

    recs = [json.loads(l) for l in open(a.extracted) if l.strip()]
    der, adj, expl = load(a.derived), load(a.adjudications), load(a.explanations)
    dups = dup_groups(recs)
    out, pending = [], []
    for r in recs:
        rid, printed = r["id"], r.get("printed_key")
        d = der.get(rid, {})
        derived, conf = d.get("derived_key"), d.get("confidence", "low")
        comp = r["quiz_type"] == "COMP"
        same = bool(printed and derived) and (norm_word(printed) == norm_word(derived) if comp else printed == derived)
        v = {"id": rid, "printed_key": printed, "derived_key": derived, "derived_by": d.get("derived_by", []),
             "derived_confidence": conf, "derived_principle": d.get("principle", ""), "adjudicated": False,
             "reason": [], "evidence": {"page": r.get("key_page"), "quote": (printed or "")[:80]},
             "dup": dups.get(rid, []), "ud": a.ud, "note_html": ""}
        if rid in adj:
            j = adj[rid]
            v.update(adjudicated=True, status=j["status"], final_key=j["final_key"], reason=j.get("reason", []),
                     note_html=j.get("note", ""), adjudicated_by=j.get("by", ""))
        elif printed and same and conf in ("high", "medium"):
            v.update(status="verified", final_key=printed)
        else:
            pending.append({"id": rid, "quiz_type": r["quiz_type"], "printed_key": printed, "derived_key": derived,
                            "confidence": conf, "principle": d.get("principle", ""),
                            "why": "no printed key" if not printed else ("disagree" if not same else "low confidence")})
            continue
        if v["status"] == "derived" and not v["note_html"]:
            v["note_html"] = NOTE_DERIVED
        v["accepted_answers"] = []
        if comp and v["final_key"]:
            bare = ARTICLE.sub("", v["final_key"]).strip()
            if bare and bare != v["final_key"]:
                v["accepted_answers"].append(bare)
        if r["quiz_type"] == "COMM" and r.get("printed_reasoning"):
            v["explanation"], v["explanation_origin"] = book_explanation(r), "book"
        elif rid in expl:
            v["explanation"], v["explanation_origin"] = expl[rid]["explanation"], "generated"
        else:
            v["explanation"], v["explanation_origin"] = "", ""
        out.append(v)
    with open(a.out, "w", encoding="utf-8") as f:
        for v in out:
            f.write(json.dumps(v, ensure_ascii=False) + "\n")
    if a.pending:
        with open(a.pending, "w", encoding="utf-8") as f:
            for p in pending:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")
    counts = {}
    for v in out:
        counts[v["status"]] = counts.get(v["status"], 0) + 1
    print("records=%d decided=%d pending=%d statuses=%s dup_ids=%d no_explanation=%d" % (
        len(recs), len(out), len(pending), counts, len(dups), sum(1 for v in out if not v["explanation"])))
    sys.exit(1 if pending else 0)


if __name__ == "__main__":
    main()
