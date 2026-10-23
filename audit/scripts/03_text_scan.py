"""Stage 1, step 3: spellcheck + structural scan on live and v5.

Strip HTML/MathJax, scan each field separately, hunspell it_IT.
Allowlist: unknown word appearing in >= 5 distinct notes -> technical term.
"""
import collections
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
import common as C
import ocr_lib as O

HUNSPELL = ["hunspell", "-d", "/Users/db/Documents/projects/anki/_tools/it_IT"]
TEXT_FIELDS = [8, 9, 10, 11, 12, 13]
WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+(?:['\u2019][A-Za-zÀ-ÖØ-öø-ÿ]+)?")
MOJIBAKE = ("\ufffd", "Ã©", "Ã¨", "â€", "Â°")
STOPWORD_START = re.compile(
    r"^\s*\d{1,3}\s+(?:<BLANK>|e|è|il|lo|la|le|gli|i|un|una|sono|si|non)\b", re.I)


def misspelled(words):
    res = subprocess.run(HUNSPELL + ["-l"], text=True, capture_output=True,
                         input="\n".join(words) + "\n")
    return {w for w in res.stdout.split() if w}


def dictionary():
    """it_IT.dic as a set (first line is the entry count; flags after /)."""
    path = "/Users/db/Documents/projects/anki/_tools/it_IT.dic"
    words = set()
    with open(path, encoding="utf-8", errors="replace") as fh:
        next(fh, None)
        for line in fh:
            w = line.split("/")[0].strip().lower()
            if w:
                words.add(w)
    return words


def edits1(word):
    letters = "abcdefghijklmnopqrstuvwxyzàèéìòù"
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    out = set()
    for left, right in splits:
        if right:
            out.add(left + right[1:])                       # delete
            for c in letters:
                out.add(left + c + right[1:])               # substitute
        if len(right) > 1:
            out.add(left + right[1] + right[0] + right[2:])  # transpose
    for left, right in splits:
        for c in letters:
            out.add(left + c + right)                       # insert
    return out


def near_miss(word, vocab):
    """Edit-distance-1 candidates that exist in the dictionary/allowlist."""
    return sorted(w for w in edits1(word) if w in vocab)


def tokens(text):
    plain = O.plain(text)
    for m in WORD_RE.findall(plain):
        w = m.lower()
        if len(w) < 3 or any(ch.isdigit() for ch in w):
            continue
        yield w, m


def collect(notes):
    per_note = collections.defaultdict(set)
    raw = {}
    for _, item, f in notes:
        for idx in TEXT_FIELDS:
            for w, m in tokens(f[idx]):
                per_note[w].add(item)
                raw.setdefault(w, m)
    return per_note, raw


def spell_hits(notes, side):
    per_note, raw = collect(notes)
    words = sorted(per_note)
    # hunspell breaks compounds/apostrophes and reports the parts ("l'aideide"
    # yields "aideide"), so keep only tokens we actually collected
    bad = {w for w in misspelled(words) if w in per_note}
    allow = {w for w in bad if len(per_note[w]) >= 5}
    flagged = sorted((w for w in bad if w not in allow), key=lambda w: len(per_note[w]))
    vocab = dictionary() | allow
    sugg = {w: near_miss(w, vocab)[:4] for w in flagged}
    hits = [{"side": side, "check": "SPELL", "word": w, "original": raw[w],
             "notes": len(per_note[w]), "suggestions": sugg.get(w, [])[:4]}
            for w in flagged]
    return hits, {"unique_words": len(words), "misspelled": len(bad),
                  "allowlisted": len(allow), "flagged": len(flagged),
                  "top_flagged": [(w, len(per_note[w]), sugg.get(w, [])[:3])
                                  for w in flagged[:20]]}


def merged_hits(notes, side):
    """Words where 'è' is glued to the previous/following word (nonè, qualè).

    Validated with hunspell: every part must be a real word.
    """
    occ = collections.defaultdict(list)
    for _, item, f in notes:
        for idx in TEXT_FIELDS:
            for w, _m in tokens(f[idx]):
                if "\u00e8" in w or "\u00e9" in w:
                    occ[w].append((item, C.FIELD_NAMES[idx]))
    bad = {w for w in misspelled(sorted(occ)) if w in occ}
    cands = {}
    for w in bad:
        n = len(w)
        two = [(w[:i], w[i:]) for i in range(2, n)]
        three = [(w[:i], w[i:j], w[j:])
                 for i in range(2, n - 2) for j in range(i + 1, n)]
        cands[w] = two + three
    allparts = {p for parts in cands.values() for part in parts for p in part}
    res = subprocess.run(HUNSPELL + ["-l"], text=True, capture_output=True,
                         input="\n".join(sorted(allparts)) + "\n")
    invalid = {x for x in res.stdout.split() if x}
    hits = []
    for w, options in cands.items():
        chosen = next((p for p in options
                       if not any(x in invalid for x in p)
                       and any(part in ("è", "é") for part in p)), None)
        if not chosen:
            continue
        for item, field in occ[w]:
            hits.append({"side": side, "ItemID": item, "field": field,
                         "check": "MERGED_WORD", "text": w,
                         "candidate": " ".join(chosen), "severity": "S2"})
    return hits, len(hits)


def norm_opt(text):
    """Keep Unicode alphanumerics (subscripts/superscripts carry meaning)."""
    t = O.plain(text)          # keep case: AA vs Aa vs aa are different options
    keep = set("⁺⁻°·×→⇌↑↓±₊₋+-=<>*?!:[]")
    t = "".join(c if (c.isalnum() or c.isspace() or c in keep) else " " for c in t)
    return re.sub(r"\s+", " ", t).strip()


def structure_hits(notes, side, media):
    hits = []
    counts = collections.Counter()

    def add(item, field, check, text, sev, cand=""):
        counts[check] += 1
        hits.append({"side": side, "ItemID": item, "field": field,
                     "check": check, "text": text[:220], "candidate": cand,
                     "severity": sev})

    for _, item, f in notes:
        stem = O.plain(f[8])
        qtype = f[5].lower()
        # 1. completamento without a blank slot
        if "completamento" in qtype and "<BLANK>" not in stem:
            add(item, "FrontStemHTML", "NO_BLANK", stem, "S1")
        # 2. lone digit/symbol where a word should be
        if STOPWORD_START.match(stem):
            add(item, "FrontStemHTML", "LONE_DIGIT", stem, "S2")
        # 3. mojibake
        for idx in TEXT_FIELDS:
            for bad in MOJIBAKE:
                if bad in f[idx]:
                    add(item, C.FIELD_NAMES[idx], "MOJIBAKE", f[idx], "S2")
                    break
        # 4. stray pipe / checkbox glyphs
        if "|" in stem or "|" in O.plain(f[10]):
            add(item, "FrontStemHTML", "STRAY_PIPE", stem or O.plain(f[10]), "S3")
        # 5. hyphen-space (line-break hyphenation not rejoined)
        for m in re.finditer(r"[A-Za-zÀ-ÿ]{2,}-\s+[A-Za-zÀ-ÿ]{2,}", stem):
            add(item, "FrontStemHTML", "HYPHEN_SPACE", m.group(0), "S3")
        # 6. unbalanced MathJax / LaTeX delimiters
        for idx in (8, 13):
            raw = f[idx]
            if raw.count("\\(") != raw.count("\\)") or raw.count("\\[") != raw.count("\\]"):
                add(item, C.FIELD_NAMES[idx], "UNBALANCED_MATH", raw, "S2")
        # 7. empty / truncated stem
        if not stem:
            add(item, "FrontStemHTML", "EMPTY_STEM", "", "S1")
        elif re.search(r"(?:,|\be|\bdi|\bche|\bcon|\bper|-)$", stem):
            add(item, "FrontStemHTML", "TRUNCATED", stem[-120:], "S3")
        # 8. missing media
        for idx in (14, 15, 16):
            for name in C.images(f[idx]):
                if name not in media:
                    add(item, C.FIELD_NAMES[idx], "MISSING_MEDIA", name, "S1")
        # 9. multiple choice integrity
        opts = O.options(f[10])
        if opts:
            seen = {}
            for letter, body in opts:
                key = norm_opt(body)
                if key in seen:
                    add(item, "FrontOptionsHTML", "DUP_OPTIONS",
                        f"{seen[key]} / {letter}: {body}", "S1")
                seen[key] = letter
            for i in range(len(opts)):
                for j in range(i + 1, len(opts)):
                    a, b = norm_opt(opts[i][1]), norm_opt(opts[j][1])
                    if a and b and a != b:
                        r = __import__("difflib").SequenceMatcher(None, a, b).ratio()
                        if r >= 0.95 and min(len(a), len(b)) >= 12:
                            add(item, "FrontOptionsHTML", "NEAR_DUP_OPTIONS",
                                f"{opts[i][0]}={opts[i][1]} / {opts[j][0]}={opts[j][1]}",
                                "S2", "review")
            banner = O.plain(f[12])
            m = re.match(r"Risposta corretta:\s*([A-E])\s*[.)]?\s*(.*)", banner, re.I)
            letters = {l for l, _ in opts}
            if m:
                letter, body = m.group(1).upper(), m.group(2).strip()
                if letter not in letters:
                    add(item, "AnswerBannerHTML", "KEY_NOT_IN_OPTIONS",
                        banner, "S1")
                else:
                    match = next(b for l, b in opts if l == letter)
                    if body and norm_opt(body) != norm_opt(match):
                        add(item, "AnswerBannerHTML", "BANNER_MISMATCH",
                            f"banner={body!r} option={match!r}", "S2")
    return hits, dict(counts)


def media_index():
    """Names of every file shipped in the v5 .apkg (schema 11: JSON in `col`)."""
    path = "/Users/db/Documents/projects/anki/workingdir/tmp/v5apkg/media"
    with open(path) as fh:
        return set(json.load(fh).values())


def main() -> None:
    media = media_index()
    live = C.live_notes()
    v5 = [(nid, item, f) for nid, _guid, item, f in C.v5_notes()]

    stats = {}
    all_hits = []
    for side, notes in (("live", live), ("v5", v5)):
        spell, sstats = spell_hits(notes, side)
        merged, mcount = merged_hits(notes, side)
        struct, scounts = structure_hits(notes, side, media)
        scounts["MERGED_WORD"] = mcount
        sstats["merged_words"] = sorted({h["text"] for h in merged})
        stats[side] = {"spell": sstats, "structure": scounts}
        all_hits.extend(spell)
        all_hits.extend(merged)
        all_hits.extend(struct)
        print(side, "spell:", {k: v for k, v in sstats.items() if k != "top_flagged"},
              "structure:", scounts)

    # where does each hit exist?
    key = lambda h: (h.get("ItemID"), h.get("field"), h["check"], h.get("word"))
    live_keys = {key(h) for h in all_hits if h["side"] == "live"}
    v5_keys = {key(h) for h in all_hits if h["side"] == "v5"}
    for h in all_hits:
        k = key(h)
        h["status"] = ("IN_BOTH" if k in live_keys and k in v5_keys
                       else "ONLY_LIVE" if h["side"] == "live" else "ONLY_V5")

    os.makedirs(C.OUT, exist_ok=True)
    json.dump(all_hits, open(f"{C.OUT}/text_hits.json", "w"), ensure_ascii=False)
    json.dump(stats, open(f"{C.OUT}/text_stats.json", "w"), indent=2, ensure_ascii=False)
    print("total hits:", len(all_hits))


if __name__ == "__main__":
    main()
