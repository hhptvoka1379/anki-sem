#!/usr/bin/env python3
"""Build the Semestre Filtro .apkg from extracted.jsonl + verification.jsonl."""
import argparse
import json
import random
import sys
from collections import Counter
from pathlib import Path

import genanki

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fields as F  # noqa: E402

FIELDS = ["ItemID", "Subject", "SubjectCode", "ChapterNum", "ChapterTitle", "QuizTypeLabel",
          "QuestionNum", "BookPage", "FrontStemHTML", "BackStemHTML", "FrontOptionsHTML",
          "BackOptionsHTML", "AnswerBannerHTML", "ExplanationHTML", "FigureHTML",
          "QuestionScanHTML", "SolutionScanHTML", "TypedAnswer", "AcceptedAnswers", "NoteHTML"]
FONTS = ["_SpaceGrotesk-Variable.ttf", "_SpaceMono-Regular.ttf", "_SpaceMono-Bold.ttf",
         "_Syne-Variable.ttf"]
DERIVED_NOTE = "Risposta ricavata: la soluzione non è presente nella scansione"
ROOT_NAME = "Semestre Filtro"
STATUSES = {"verified", "book-corrected", "derived", "unverified"}


def read_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if line.strip():
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError as e:
                    sys.exit("%s line %d: invalid JSON (%s)" % (path, n, e))
    return out


def validate(extracted, verif):
    """Return a list of problems; build refuses if non-empty."""
    problems = []
    ext_ids, ver_ids = {r["id"] for r in extracted}, {v["id"] for v in verif}
    if len(ext_ids) != len(extracted):
        problems.append("duplicate ids in extracted")
    if len(ver_ids) != len(verif):
        problems.append("duplicate ids in verification")
    for i in sorted(ext_ids - ver_ids):
        problems.append("%s: in extracted but not in verification" % i)
    for i in sorted(ver_ids - ext_ids):
        problems.append("%s: in verification but not in extracted" % i)
    ext = {r["id"]: r for r in extracted}
    for v in verif:
        i, st = v["id"], v.get("status")
        if st not in STATUSES:
            problems.append("%s: bad status %r" % (i, st))
        note = (v.get("note_html") or "").strip()
        if st in ("book-corrected", "unverified") and not note:
            problems.append("%s: status %s needs note_html" % (i, st))
        if st == "derived" and DERIVED_NOTE not in note:
            problems.append("%s: status derived needs the note %r" % (i, DERIVED_NOTE))
        key = v.get("final_key")
        if not key:
            problems.append("%s: empty final_key" % i)
        rec = ext.get(i)
        if rec and key and rec.get("options") and key not in rec["options"]:
            problems.append("%s: final_key %r is not an option" % (i, key))
    return problems


def load_ids(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


class DeckIds:
    """Looks up deck ids; creates missing ones and records them for write-back."""
    def __init__(self, ids):
        self.map = ids["deck_ids"]
        self.added = {}
        self.used = set(self.map.values())

    def get(self, key):
        if key not in self.map:
            while True:
                new = random.randrange(2 ** 30, 2 ** 31)
                if new not in self.used:
                    break
            self.used.add(new)
            self.map[key] = self.added[key] = new
        return self.map[key]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extracted", required=True)
    ap.add_argument("--verification", required=True)
    ap.add_argument("--templates", required=True)
    ap.add_argument("--media", required=True)
    ap.add_argument("--ids", required=True)
    ap.add_argument("--version", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chapters", nargs="*", help="e.g. CHIM-C01 (only these chapters)")
    ap.add_argument("--fonts", default=str(Path(__file__).resolve().parents[1] / "assets" / "fonts"))
    a = ap.parse_args()

    extracted, verif = read_jsonl(a.extracted), read_jsonl(a.verification)
    problems = validate(extracted, verif)
    if problems:
        print("REFUSING TO BUILD: %d problem(s)" % len(problems), file=sys.stderr)
        for p in problems:
            print("  " + p, file=sys.stderr)
        sys.exit(1)
    vmap = {v["id"]: v for v in verif}

    def chap_key(r):
        return "%s-C%02d" % (r["subject_code"], r["chapter"])
    if a.chapters:
        extracted = [r for r in extracted if chap_key(r) in set(a.chapters)]
        if not extracted:
            sys.exit("no records match --chapters %s" % a.chapters)

    tdir = Path(a.templates)
    for name in ("front.html", "back.html", "style.css"):
        if not (tdir / name).is_file():
            sys.exit("missing template file: %s" % (tdir / name))
    model = genanki.Model(
        load_ids(a.ids)["model_id"], load_ids(a.ids)["model_name"],
        fields=[{"name": n} for n in FIELDS],
        templates=[{"name": "Domanda -> Risposta",
                    "qfmt": (tdir / "front.html").read_text(encoding="utf-8"),
                    "afmt": (tdir / "back.html").read_text(encoding="utf-8")}],
        css=(tdir / "style.css").read_text(encoding="utf-8"))

    ids = load_ids(a.ids)
    dids = DeckIds(ids)
    decks = {}

    def deck(name, key):
        if name not in decks:
            decks[name] = genanki.Deck(dids.get(key), name)
        return decks[name]

    deck(ROOT_NAME, "ROOT")
    media_dir = Path(a.media)
    media_names = set()
    extracted.sort(key=lambda r: (r["subject_code"], r["chapter"], r["quiz_type"], r["question_num"]))

    for r in extracted:
        v = vmap[r["id"]]
        key = v["final_key"]
        subj, code = r["subject"], r["subject_code"]
        ck = chap_key(r)
        chap_name = "%02d — %s" % (r["chapter"], r["chapter_title"].replace("::", ":"))
        tipo = F.TYPE_LABELS[r["quiz_type"]]
        deck("%s::%s" % (ROOT_NAME, subj.replace("::", ":")), code)
        deck("%s::%s::%s" % (ROOT_NAME, subj, chap_name), ck)
        leaf = deck("%s::%s::%s::%s" % (ROOT_NAME, subj, chap_name, tipo), "%s-%s" % (ck, r["quiz_type"][:4]))

        is_comp = r["quiz_type"] == "COMP"
        scan_q = F.scan(r.get("question_crop"), "Scansione della domanda")
        scan_s = F.scan(r.get("solution_crop"), "Soluzione stampata")
        for f in (r.get("question_crop"), r.get("solution_crop"), r.get("figure")):
            if f:
                media_names.add(f)
        fig = F.figure(r)
        fig_back = r.get("figure_side") == "back"
        vals = {
            "ItemID": r["id"], "Subject": F.esc(subj), "SubjectCode": code,
            "ChapterNum": str(r["chapter"]), "ChapterTitle": F.esc(r["chapter_title"]),
            "QuizTypeLabel": tipo, "QuestionNum": str(r["question_num"]),
            "BookPage": str(r["printed_page"]),
            "FrontStemHTML": F.front_stem(r), "BackStemHTML": F.back_stem(r, key),
            "FrontOptionsHTML": F.front_options(r), "BackOptionsHTML": F.back_options(r, key),
            "AnswerBannerHTML": F.answer_banner(r, key),
            "ExplanationHTML": F.explanation(v.get("explanation")),
            "FigureHTML": fig, "QuestionScanHTML": scan_q, "SolutionScanHTML": scan_s,
            "TypedAnswer": key if is_comp else "",
            "AcceptedAnswers": "|".join(v.get("accepted_answers") or []) if is_comp else "",
            "NoteHTML": F.note(v.get("note_html")),
        }
        # A back-only figure must not show on the front; the shared template field cannot
        # tell sides apart, so figure_side=back records are surfaced via the solution scan area.
        if fig_back:
            vals["FigureHTML"] = ""
            vals["SolutionScanHTML"] = fig + scan_s
        tags = ["verify::" + v["status"]] + ["verify::" + x for x in v.get("reason") or []]
        if v.get("ud"):
            tags.append("ud::" + v["ud"])
        tags += ["dup::" + d for d in v.get("dup") or []]
        leaf.add_note(genanki.Note(model=model, fields=[vals[n] for n in FIELDS],
                                   guid=genanki.guid_for(r["id"]), tags=tags))

    media_files = []
    missing = []
    for n in sorted(media_names):
        p = media_dir / n
        (media_files if p.is_file() else missing).append(p if p.is_file() else n)
    for n in FONTS:
        p = Path(a.fonts) / n
        (media_files if p.is_file() else missing).append(p if p.is_file() else str(p))
    if missing:
        sys.exit("missing media files: %s" % ", ".join(map(str, missing)))

    pkg = genanki.Package(list(decks.values()))
    pkg.media_files = [str(p) for p in media_files]
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    pkg.write_to_file(a.out)

    if dids.added:
        ids["deck_ids"] = dids.map  # only adds; existing keys untouched
        with open(a.ids, "w", encoding="utf-8") as fh:
            json.dump(ids, fh, ensure_ascii=False, indent=2)
        print("added deck ids to %s: %s" % (a.ids, json.dumps(dids.added, ensure_ascii=False)))

    print("wrote %s" % a.out)
    for name, d in sorted(decks.items()):
        if d.notes:
            print("  %3d  %s" % (len(d.notes), name))
    print("notes: %d; media: %d (%d images + %d fonts)" %
          (sum(len(d.notes) for d in decks.values()), len(media_files), len(media_names), len(FONTS)))


if __name__ == "__main__":
    main()
