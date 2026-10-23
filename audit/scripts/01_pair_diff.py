"""Stage 1, steps 1-2: pair live vs v5 by ItemID, then diff field by field.

Read-only. Writes out/pairing.json, out/diff.json, out/changed_fields.json.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import common as C


def field_map():
    """Live schema-18 fields vs v5 legacy col.models JSON, compared by name."""
    live = C.connect(C.LIVE_DB)
    live_fields = [r[0] for r in live.execute(
        "select name from fields where ntid=? order by ord", (C.LIVE_MODEL,))]
    v5 = C.connect(C.V5_DB)
    models = json.loads(v5.execute("select models from col").fetchone()[0])
    model = list(models.values())[0]
    v5_fields = [f["name"] for f in sorted(model["flds"], key=lambda f: f["ord"])]
    return live_fields, v5_fields, model.get("name"), model.get("type")


def classify(live: str, v5: str) -> str:
    if live == v5:
        return "identical"
    if C.norm_ws(live) == C.norm_ws(v5):
        return "html_ws_only"
    if C.norm_sup(live) == C.norm_sup(v5):
        return "superscript"
    if C.norm_roots(live) == C.norm_roots(v5):
        return "root"
    if C.alnum_only(live) == C.alnum_only(v5):
        return "other_symbol"
    if C.nfc(live) == C.nfc(v5):
        return "unicode_nfc"
    return "rewrite"


def index(notes, key_pos):
    idx = {}
    for note in notes:
        idx.setdefault(note[key_pos], []).append(note)
    return idx


def main() -> None:
    live_fields, v5_fields, model_name, model_type = field_map()
    mapping = ("identical names and order" if live_fields == v5_fields else
               {i: [live_fields[i] if i < len(live_fields) else None,
                    v5_fields[i] if i < len(v5_fields) else None]
                for i in range(max(len(live_fields), len(v5_fields)))})

    live = C.live_notes()          # (note_id, item, fields)
    v5 = C.v5_notes()              # (note_id, guid, item, fields)
    live_index = index(live, 1)
    v5_index = index(v5, 2)

    live_dups = sorted(k for k, v in live_index.items() if len(v) > 1)
    v5_dups = sorted(k for k, v in v5_index.items() if len(v) > 1)
    paired = sorted(set(live_index) & set(v5_index))
    live_only = sorted(set(live_index) - set(v5_index))
    v5_only = sorted(set(v5_index) - set(live_index))
    ambiguous = [k for k in paired
                 if len(live_index[k]) > 1 or len(v5_index[k]) > 1]

    conflicts = []
    for item in paired:
        lf = live_index[item][0][2]
        vf = v5_index[item][0][3]
        if (lf[1], lf[2], lf[3]) != (vf[1], vf[2], vf[3]):
            conflicts.append({
                "ItemID": item,
                "live": {"Subject": lf[1], "SubjectCode": lf[2], "ChapterNum": lf[3]},
                "v5": {"Subject": vf[1], "SubjectCode": vf[2], "ChapterNum": vf[3]},
            })

    cat_names = ("identical", "html_ws_only", "superscript", "root",
                 "other_symbol", "unicode_nfc", "rewrite")
    cats = {name: 0 for name in cat_names}
    per_field = {name: {k: 0 for k in cat_names} for name in C.FIELD_NAMES}
    samples = {k: [] for k in cat_names}
    changed, destructive = [], []
    note_status = {"identical": 0, "changed": 0}

    for item in paired:
        lnid, lf = live_index[item][0][0], live_index[item][0][2]
        vnid, vf = v5_index[item][0][0], v5_index[item][0][3]
        note_changed = False
        for i, name in enumerate(C.FIELD_NAMES):
            a = lf[i] if i < len(lf) else ""
            b = vf[i] if i < len(vf) else ""
            cat = classify(a, b)
            cats[cat] += 1
            per_field[name][cat] += 1
            if cat == "identical":
                continue
            note_changed = True
            rec = {"ItemID": item, "field": name, "category": cat,
                   "live": a, "v5": b, "live_note_id": lnid, "v5_note_id": vnid}
            changed.append(rec)
            if len(samples[cat]) < 5:
                samples[cat].append(rec)
            la, lb = len(C.norm_ws(a)), len(C.norm_ws(b))
            reasons = []
            if b.strip() == "" and a.strip() != "":
                reasons.append("v5 EMPTY")
            if a.strip() == "" and b.strip() != "":
                reasons.append("live EMPTY")
            if C.images(a) and not set(C.images(a)) <= set(C.images(b)):
                reasons.append("image lost in v5")
            if C.sounds(a) and not set(C.sounds(a)) <= set(C.sounds(b)):
                reasons.append("sound lost in v5")
            if la and lb and (lb < la * 0.5 or lb > la * 2):
                reasons.append(f"length {la}->{lb}")
            if reasons:
                destructive.append({**rec, "reasons": reasons})
        note_status["changed" if note_changed else "identical"] += 1

    general, seen = [], set()
    for rec in changed:
        if rec["ItemID"] in seen:
            continue
        seen.add(rec["ItemID"])
        general.append(rec)
        if len(general) == 15:
            break

    out = {
        "field_mapping": {
            "live_fields": live_fields, "v5_fields": v5_fields,
            "mapping": mapping, "v5_model_name": model_name,
            "v5_model_type": model_type,
        },
        "counts": {
            "live_notes": len(live), "v5_notes": len(v5),
            "paired": len(paired), "live_only": len(live_only),
            "v5_only": len(v5_only), "ambiguous": len(ambiguous),
            "live_duplicate_itemids": len(live_dups),
            "v5_duplicate_itemids": len(v5_dups),
            "itemid_conflicts": len(conflicts),
            "notes_identical": note_status["identical"],
            "notes_changed": note_status["changed"],
        },
        "live_only_sample": live_only[:20], "v5_only_sample": v5_only[:20],
        "live_duplicates": live_dups[:20], "v5_duplicates": v5_dups[:20],
        "ambiguous": ambiguous[:20], "conflicts": conflicts[:20],
        "diff_categories": cats, "per_field": per_field, "samples": samples,
        "general_samples": general, "destructive": destructive,
    }

    os.makedirs(C.OUT, exist_ok=True)
    with open(f"{C.OUT}/pairing.json", "w") as fh:
        json.dump({k: out[k] for k in
                   ("field_mapping", "counts", "live_only_sample", "v5_only_sample",
                    "live_duplicates", "v5_duplicates", "ambiguous", "conflicts")},
                  fh, indent=2, ensure_ascii=False)
    with open(f"{C.OUT}/diff.json", "w") as fh:
        json.dump({k: out[k] for k in
                   ("diff_categories", "per_field", "samples", "general_samples",
                    "destructive")}, fh, indent=2, ensure_ascii=False)
    with open(f"{C.OUT}/changed_fields.json", "w") as fh:
        json.dump(changed, fh, ensure_ascii=False)

    print(json.dumps(out["counts"], indent=2))
    print("diff_categories:", json.dumps(cats))
    print("destructive:", len(destructive))
    print("mapping:", mapping if isinstance(mapping, str) else "MISMATCH")


if __name__ == "__main__":
    main()
