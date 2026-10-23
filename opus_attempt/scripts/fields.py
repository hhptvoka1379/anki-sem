"""Field HTML generation. All HTML structure lives here so it can be aligned with
work/template/sample_fields.json in one place. Class names follow reference_css.css."""
import re
from html import escape

BLANK = "_____"
TYPE_LABELS = {"COMM": "Quiz commentati", "NCOM": "Quiz non commentati", "COMP": "Quiz a completamento"}


def esc(text):
    return escape(text or "", quote=True)


def _stem(stem, mode, answer=""):
    """mode 'front' -> blank slot; 'back' -> filled mint answer. MCQ stems have no blank."""
    parts = (stem or "").split(BLANK)
    if len(parts) == 1:
        return '<div class="stem-text">%s</div>' % esc(stem)
    if mode == "front":
        fill = '<span class="blank-slot">%s</span>' % BLANK
    else:
        fill = '<span class="blank-filled">%s</span>' % esc(answer)
    return '<div class="stem-text">%s</div>' % fill.join(esc(p) for p in parts)


def front_stem(rec):
    return _stem(rec["stem"], "front")


def back_stem(rec, final_key):
    return _stem(rec["stem"], "back", final_key)


def _options(rec, correct=None):
    rows = []
    for letter, text in rec["options"].items():
        cls = "opt correct" if letter == correct else "opt"
        rows.append('<div class="%s"><span class="opt-letter">%s</span><span class="opt-text">%s</span></div>'
                    % (cls, esc(letter), esc(text)))
    return '<div class="options">%s</div>' % "".join(rows)


def front_options(rec):
    return _options(rec) if rec.get("options") else ""


def back_options(rec, final_key):
    return _options(rec, final_key) if rec.get("options") else ""


def answer_banner(rec, final_key):
    if rec.get("options"):
        return "Risposta corretta: %s. %s" % (esc(final_key), esc(rec["options"][final_key]))
    return "Risposta corretta: %s" % esc(final_key)


def explanation(text):
    return esc(text)


def figure(rec):
    if not rec.get("figure"):
        return ""
    return '<img class="fig" src="%s" alt="">' % esc(rec["figure"])


def scan(filename, alt):
    return '<img src="%s" alt="%s">' % (esc(filename), esc(alt)) if filename else ""


def note(note_html):
    # note_html comes from the verification record as ready-made HTML/text; kept verbatim.
    return note_html or ""
