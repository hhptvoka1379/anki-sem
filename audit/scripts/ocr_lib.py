"""OCR helpers: preprocess a crop, detect blank rules, run Tesseract, compare."""
import difflib
import html
import json
import os
import re
import subprocess
import tempfile
import unicodedata

import numpy as np
from PIL import Image

TESSDATA = "/Users/db/Documents/projects/anki/_tools/tessdata"
BLANK_SPAN = re.compile(
    r'<span[^>]*class="blank-slot"[^>]*>(.*?)</span>', re.I | re.S)
TAG = re.compile(r"<[^>]+>")
OPT = re.compile(
    r'<span class="opt-letter">\s*([A-E])\s*</span>\s*'
    r'<span class="opt-body">(.*?)</span>', re.I | re.S)
WS = re.compile(r"\s+")
UNDERSCORES = re.compile(r"_{3,}|-{4,}|\.{4,}")


def plain(text: str) -> str:
    """Card HTML -> plain text with <BLANK> for blank slots."""
    if not text:
        return ""
    # sentinel first: "<BLANK>" itself would be eaten by the tag stripper
    t = BLANK_SPAN.sub(" \x00BLANK\x00 ", text)
    t = TAG.sub(" ", t)
    t = html.unescape(t).replace("\u00a0", " ")
    t = t.replace("\x00BLANK\x00", "<BLANK>")
    return WS.sub(" ", t).strip()


def options(text: str):
    """[(letter, plain option text)] from the options field."""
    if not text:
        return []
    return [(m.group(1).upper(), WS.sub(" ", html.unescape(TAG.sub(" ", m.group(2)))).strip())
            for m in OPT.finditer(text)]


def strip_blanks(text: str) -> str:
    return WS.sub(" ", UNDERSCORES.sub(" ", text.replace("<BLANK>", " "))).strip()


def normalise_ocr(text: str) -> str:
    """Lowercase, rejoin line-break hyphenation, collapse blank runs,
    drop question numbers and option letters."""
    t = text.lower().replace("\u00a0", " ")
    t = re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", t)
    t = re.sub(r"\s+", " ", t)
    t = UNDERSCORES.sub(" <blank> ", t)
    t = re.sub(r"^\s*\d{1,3}\s*[.)]\s*", "", t)
    t = re.sub(r"(?:^|\s)[a-e]\s*[.)]\s+", " ", t)
    return WS.sub(" ", t).strip()


def otsu(gray: np.ndarray) -> int:
    hist = np.bincount(gray.ravel(), minlength=256).astype(np.float64)
    total = gray.size
    sum_all = np.dot(np.arange(256), hist)
    w_b = np.cumsum(hist)
    sum_b = np.cumsum(np.arange(256) * hist)
    w_f = total - w_b
    with np.errstate(divide="ignore", invalid="ignore"):
        m_b = sum_b / w_b
        m_f = (sum_all - sum_b) / w_f
        var = w_b * w_f * (m_b - m_f) ** 2
    var = np.nan_to_num(var)
    return int(np.argmax(var))


def scale_for(width: int) -> int:
    """Target roughly 300 dpi for these crops (they are ~150-200 dpi scans)."""
    if width < 900:
        return 3
    if width < 1400:
        return 2
    return 1


def find_rules(black: np.ndarray) -> list:
    """Long thin horizontal runs = fill-in blanks (underscores/rules).

    Tesseract routinely drops these, so they are detected geometrically.
    """
    h, w = black.shape
    min_len = max(30, int(w * 0.10))
    rows = []
    for y in range(h):
        row = black[y]
        if row.sum() < min_len:
            continue
        # merge runs separated by <= 4 px
        xs = np.flatnonzero(row)
        start = prev = xs[0]
        for x in xs[1:]:
            if x - prev <= 4:
                prev = x
                continue
            if prev - start + 1 >= min_len:
                rows.append((y, start, prev))
            start = prev = x
        if prev - start + 1 >= min_len:
            rows.append((y, start, prev))
    if not rows:
        return []
    # group rows into bands
    bands = []
    cur = [rows[0]]
    for r in rows[1:]:
        if r[0] - cur[-1][0] <= 1 and not (r[2] < cur[0][1] - 5 or r[1] > cur[0][2] + 5):
            cur.append(r)
        else:
            bands.append(cur)
            cur = [r]
    bands.append(cur)
    out = []
    for band in bands:
        y0, y1 = band[0][0], band[-1][0]
        x0 = min(b[1] for b in band)
        x1 = max(b[2] for b in band)
        width, height = x1 - x0 + 1, y1 - y0 + 1
        if height <= max(12, h * 0.25) and width / max(height, 1) >= 5:
            out.append({"x0": int(x0), "x1": int(x1), "y0": int(y0), "y1": int(y1)})
    return out


def preprocess(path: str, dest: str, scale=None):
    im = Image.open(path).convert("L")
    s = scale or scale_for(im.width)
    if s > 1:
        im = im.resize((im.width * s, im.height * s), Image.LANCZOS)
    arr = np.array(im)
    thr = otsu(arr)
    # Otsu's t means "pixels <= t are class 0"; these crops are often already
    # 1-bit (0/255), where '<' would select nothing and yield a blank image.
    black = arr <= thr
    rules = find_rules(black)
    for r in rules:                      # erase rules so OCR does not emit noise
        black[r["y0"]:r["y1"] + 1, r["x0"]:r["x1"] + 1] = False
    out = np.where(black, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(dest)
    return {"scale": s, "threshold": thr, "rules": rules,
            "width": int(out.shape[1]), "height": int(out.shape[0])}


def run_tesseract(image: str, psm: int = 6):
    """Return (text, [(word, conf)]) using TSV output.

    `tesseract img stdout ... tsv` writes `stdout.tsv` to the CWD instead of
    stdout, so use an explicit output base and read the sidecar file.
    """
    env = dict(os.environ, TESSDATA_PREFIX=TESSDATA)
    base = image + ".ocr"
    cmd = ["tesseract", image, base, "-l", "ita", "--oem", "1",
           "--psm", str(psm), "-c", "tessedit_create_tsv=1"]
    subprocess.run(cmd, capture_output=True, env=env, timeout=180)
    tsv = base + ".tsv"
    text = open(tsv, "rb").read().decode("utf-8", "replace") if os.path.exists(tsv) else ""
    words, lines = [], {}
    for line in text.splitlines()[1:]:
        parts = line.split("\t")
        if len(parts) < 12 or parts[0] != "5":
            continue
        conf = float(parts[10]) if parts[10] not in ("", "-1") else -1.0
        text = parts[11].strip()
        if not text:
            continue
        words.append((text, conf))
        key = (parts[2], parts[3], parts[4])
        lines.setdefault(key, []).append(text)
    text = "\n".join(" ".join(v) for _, v in sorted(lines.items(), key=lambda kv: int(kv[0][1])))
    if not text.strip() and psm != 4:
        return run_tesseract(image, psm=4)
    return text, words


def ocr_crop(path: str, cache: dict, tmpdir: str):
    key = os.path.basename(path)
    if key in cache:
        return cache[key]
    dest = os.path.join(tmpdir, "pp_" + key)
    meta = preprocess(path, dest)
    text, words = run_tesseract(dest)
    confs = [c for _, c in words if c >= 0]
    rec = {
        "text": text,
        "norm": normalise_ocr(text),
        "mean_conf": round(sum(confs) / len(confs), 1) if confs else 0.0,
        "min_conf": round(min(confs), 1) if confs else 0.0,
        "rules": meta["rules"],
        "scale": meta["scale"],
    }
    cache[key] = rec
    return rec


def best_match(segment: str, ocr_tokens: list):
    """Best-matching OCR window for a card segment. Returns (ratio, window)."""
    seg = strip_blanks(segment)
    if not seg:
        return 1.0, ""
    stoks = seg.split()
    n = len(stoks)
    if not ocr_tokens:
        return 0.0, ""
    best = (0.0, "")
    for delta in (-2, -1, 0, 1, 2):
        size = max(1, n + delta)
        for start in range(0, max(1, len(ocr_tokens) - size + 1)):
            window = " ".join(ocr_tokens[start:start + size])
            r = difflib.SequenceMatcher(None, seg, window).ratio()
            if r > best[0]:
                best = (r, window)
    return best


CONFUSABLE = set("lI1iItO0°|!](),")


def _base(word: str) -> str:
    """Strip diacritics: OCR often adds/burns accents (si -> sì)."""
    return "".join(c for c in unicodedata.normalize("NFD", word)
                   if unicodedata.category(c) != "Mn")


def char_swaps(segment: str, window: str):
    """Word-aligned single-character substitutions (sl/si, t/I, O/0, rn/m)."""
    a = strip_blanks(segment).split()
    b = window.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op != "replace":
            continue
        xs, ys = a[i1:i2], b[j1:j2]
        if len(xs) != len(ys):
            continue
        for x, y in zip(xs, ys):
            if not (x.isalpha() and y.isalpha()):
                continue
            if _base(x).lower() == _base(y).lower():
                continue                      # accent-only OCR noise
            if abs(len(x) - len(y)) > 1 or len(x) < 2:
                continue
            if difflib.SequenceMatcher(None, x, y).ratio() < 0.5:
                continue
            if len(x) == len(y):
                diff = [(p, q) for p, q in zip(x, y) if p != q]
                if len(diff) != 1:
                    continue
                p, q = diff[0]
                if (p in CONFUSABLE or q in CONFUSABLE
                        or _base(p) in CONFUSABLE or _base(q) in CONFUSABLE):
                    out.append((x, y))
            elif ("rn" in x.lower() and "m" in y.lower()) or ("m" in x.lower() and "rn" in y.lower()):
                out.append((x, y))
    return out


def token_type_diffs(segment: str, window: str):
    """A lone digit/symbol in the card where the crop has a word (e.g. 0 for Il)."""
    a = strip_blanks(segment).split()
    b = window.split()
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op != "replace" or (i2 - i1) != (j2 - j1):
            continue
        for x, y in zip(a[i1:i2], b[j1:j2]):
            if re.fullmatch(r"[0-9]{1,3}", x) and y.isalpha() and len(y) >= 1:
                out.append((x, y))
    return out
