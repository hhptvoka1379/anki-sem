"""Validate the converted collection against the untouched input."""
import collections
import importlib.util
import json
import os
import re
import sqlite3
import sys

sys.path.insert(0, os.path.dirname(__file__))
import common as C

spec = importlib.util.spec_from_file_location(
    "conv", os.path.join(os.path.dirname(__file__), "07_cloze_convert.py"))
conv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(conv)

NEW = f"{C.OUT}/cloze/collection_patched.db"
OLD = os.environ.get("SF_INPUT_DB", C.LIVE_DB)
DONOR_MID = 1481924269089
OLD_MID = 1813027267


def con(path):
    db = sqlite3.connect(f"file:{path}?immutable=1", uri=True)
    db.create_collation("unicase", lambda a, b: (a.casefold() > b.casefold())
                        - (a.casefold() < b.casefold()))
    return db


def notes_map(db):
    return {nid: (mid, flds) for nid, mid, flds in
            db.execute("select id, mid, flds from notes")}


def main() -> None:
    old, new = con(OLD), con(NEW)
    checks = []

    def check(name, ok, detail=""):
        checks.append((name, "PASS" if ok else "FAIL", detail))

    check("integrity_check", new.execute("pragma integrity_check").fetchone()[0]
          == "ok", new.execute("pragma integrity_check").fetchone()[0])

    o, n = notes_map(old), notes_map(new)
    check("note count unchanged", len(o) == len(n), f"{len(o)} -> {len(n)}")
    check("note id set unchanged", set(o) == set(n),
          f"{len(set(o) ^ set(n))} symmetric difference")

    changed = [k for k in o if o[k] != n[k]]
    check("exactly 2055 notes changed", len(changed) == 2055, str(len(changed)))
    check("converted notes carry the cloze mid",
          all(n[k][0] == DONOR_MID for k in changed),
          str(collections.Counter(n[k][0] for k in changed)))
    rest = [k for k in o if k not in set(changed)]
    check("untouched notes byte-identical", all(o[k] == n[k] for k in rest),
          f"{len(rest)} notes compared")

    orphan = new.execute("select count(*) from cards c left join notes n "
                         "on n.id=c.nid where n.id is null").fetchone()[0]
    check("no orphan cards", orphan == 0, str(orphan))

    cards = collections.Counter(r[0] for r in new.execute(
        "select nid from cards where nid in (select id from notes where mid=?)",
        (DONOR_MID,)))
    mism = [k for k in changed if cards.get(k, 0) != n[k][1].count("{{c")]
    check("cards match cloze ordinals", not mism, str(mism[:5]))

    ords = new.execute("select min(ord), max(ord) from cards c join notes n "
                       "on n.id=c.nid where n.mid=?", (DONOR_MID,)).fetchone()
    check("card ordinals within 0..1", ords == (0, 1), str(ords))


    bad_syntax = []
    for k in changed:
        flds = n[k][1]
        if "blank-slot" in flds:
            bad_syntax.append((k, "leftover blank-slot"))
        opens = flds.count("{{c")
        closes = len(re.findall(r"\{\{c\d+::.*?\}\}", flds, re.S))
        if opens != closes:
            bad_syntax.append((k, f"{opens} open vs {closes} closed"))
        for body in re.findall(r"\{\{c\d+::(.*?)\}\}", flds, re.S):
            if "::" in body:
                bad_syntax.append((k, "delimiter inside answer"))
    check("cloze syntax well formed", not bad_syntax, str(bad_syntax[:3]))

    fields = [r[0] for r in new.execute(
        "select name from fields where ntid=? order by ord", (DONOR_MID,))]
    old_fields = [r[0] for r in new.execute(
        "select name from fields where ntid=? order by ord", (OLD_MID,))]
    check("new model has 17 fields, same names/order", fields == old_fields,
          f"{len(fields)} fields")

    nt = new.execute("select name, config from notetypes where id=?",
                     (DONOR_MID,)).fetchone()
    kind = dict((f, v) for f, wt, v in conv.parse(nt[1]) if wt == 0).get(1)
    check("note type kind is cloze (1)", kind == 1, str(kind))

    tpl = new.execute("select name, config from templates where ntid=?",
                      (DONOR_MID,)).fetchone()
    check("template uses cloze field",
          b"{{cloze:FrontStemHTML}}" in tpl[1], tpl[0])
    check("template has typed-answer field",
          b"{{type:cloze:FrontStemHTML}}" in tpl[1], "typed answers")

    rev = (old.execute("select count(*) from revlog").fetchone()[0],
           new.execute("select count(*) from revlog").fetchone()[0])
    check("revlog untouched", rev[0] == rev[1], f"{rev[0]} -> {rev[1]}")
    sched = new.execute("select count(*) from cards where reps>0").fetchone()[0]
    check("reviewed cards still 112", sched == 112, str(sched))
    dk = (old.execute("select count(*) from decks").fetchone()[0],
          new.execute("select count(*) from decks").fetchone()[0])
    check("decks untouched", dk[0] == dk[1], str(dk))

    total = new.execute("select count(*) from cards").fetchone()[0]
    expected = old.execute("select count(*) from cards").fetchone()[0] - 2055 + 2059
    check("card total = old - 2055 + 2059", total == expected,
          f"{total} vs {expected}")
    new_only = new.execute("select count(*) from cards c join notes nn "
                           "on nn.id=c.nid where nn.mid=? and c.type=0 "
                           "and c.queue=0", (DONOR_MID,)).fetchone()[0]
    check("converted cards are new (type 0, queue 0)", new_only == 2059,
          str(new_only))

    items = dict((f, v) for f, wt, v in conv.parse(tpl[1]))
    q = items.get(1, b"").decode("utf-8", "replace")
    a = items.get(2, b"").decode("utf-8", "replace")
    refs = set(re.findall(r"\{\{[#^/]?([A-Za-z0-9 _&'-]+)\}\}", q + a))
    special = {"FrontSide", "Tags", "Type", "Deck", "Subdeck", "Card"}
    missing = sorted(r for r in refs
                     if r.split(":")[-1] not in set(fields) and r not in special)
    check("template field refs all exist", not missing, str(missing))
    check("cloze filter on the front template",
          "{{cloze:FrontStemHTML}}" in q, q[:40])
    check("typing marker on the front template",
          "{{type:cloze:FrontStemHTML}}" in q, "needed for the input box")
    check("scan field rendered on the front",
          "{{QuestionScanHTML}}" in q, "question scan")

    for name, verdict, detail in checks:
        print(f"{verdict:4}  {name:44} {detail}")
    bad = [c for c in checks if c[1] == "FAIL"]
    json.dump({"checks": checks, "failures": len(bad)},
              open(f"{C.OUT}/cloze/validation.json", "w"), indent=2)
    print("\nFAILURES:", len(bad))
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
