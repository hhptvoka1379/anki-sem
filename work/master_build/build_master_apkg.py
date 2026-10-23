#!/usr/bin/env python3
"""Master Anki v3 .apkg builder for Semestre Filtro (7,078 notes / 7,082 cards / 8,234 standalone media files)."""
from __future__ import annotations

import html
import json
import re
import shutil
import sqlite3
import sys
import time
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import zstandard
from anki.collection import Collection, ExportAnkiPackageOptions

from patches_130_restored import build_clean_130
from clean_563_and_ud_tags import (
    ITEM_SPECIFIC_OVERRIDES,
    classify_ud_tag,
    clean_ocr_fragment,
    derive_cloze_synonyms,
)
from explanations_bio_118 import BIO_118
from explanations_chim_189 import CHIM_189
from explanations_fis_127 import FIS_127
from extract_delta_media import clean_live_figure_html, extract_all_delta_media
from symbol_and_ocr_fixes import EXPLICIT_CARD_PATCHES, load_v5_rows, v5_field_ok

MCQ_MID = 1813027267
CLOZE_MID = 1481924269089
MOD_FLOOR = 1792780000

OFFLINE_FONT_CSS = """@font-face {
  font-family: "Space Grotesk";
  src: url("_SpaceGrotesk-Variable.ttf") format("truetype");
  font-weight: 400 700;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Space Mono";
  src: url("_SpaceMono-Regular.ttf") format("truetype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Space Mono";
  src: url("_SpaceMono-Bold.ttf") format("truetype");
  font-weight: 700;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: "Syne";
  src: url("_Syne-Variable.ttf") format("truetype");
  font-weight: 700 800;
  font-style: normal;
  font-display: swap;
}
"""

EXTRA_SHARED_CSS = """
.expl-box.is-wrong-review {
  border-color: #b91c1c;
  box-shadow: 4px 4px 0px #ef4444;
}
.sf-canvas.sf-dark .expl-box.is-wrong-review {
  border-color: #fca5a5;
  box-shadow: 4px 4px 0px #ef4444;
}
.note-box {
  margin-top: 10px;
  padding: 9px 12px;
  border: 2px solid #111111;
  background: #fef9c3;
  color: #111111;
  font-size: 13px;
  line-height: 1.48;
}
.sf-canvas.sf-dark .note-box {
  background: #27272a;
  color: #fde047;
  border-color: #facc15;
}
.sf-acc-badge {
  display: inline-block;
  margin-left: 8px;
  padding: 1px 8px;
  font-size: 12px;
  font-weight: 700;
  background: #86efac;
  color: #111111;
  border: 2px solid #111111;
}
"""

CLOZE_TYPED_JS = """
  (function() {
    var accEl = document.querySelector('.sf-acc-data');
    var typeEl = document.getElementById('typeans');
    if (!accEl || !typeEl) return;
    if (typeEl.querySelector('.typeGood') && !typeEl.querySelector('.typeBad') && !typeEl.querySelector('.typeMissed')) return;
    var arrow = typeEl.querySelector('#typearrow');
    var typed = '';
    if (arrow) {
      for (var n = typeEl.firstChild; n; n = n.nextSibling) {
        if (n.nodeName === 'BR') break;
        if (n.classList && n.classList.contains('typeMissed')) continue;
        typed += n.textContent || '';
      }
    } else {
      typed = typeEl.textContent || '';
    }
    var subMap = {'₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5','₆':'6','₇':'7','₈':'8','₉':'9','⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5','⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁺':'+','⁻':'-'};
    var greekMap = {'α':'alfa','β':'beta','γ':'gamma','δ':'delta','ε':'epsilon','θ':'theta','λ':'lambda','μ':'mu','π':'pi','ρ':'rho','σ':'sigma','τ':'tau','φ':'phi','Φ':'phi','ω':'omega','Ω':'omega','Δ':'delta '};
    function normAns(s) {
      var x = (s || '').replace(/[₀-₉⁰-⁹⁺⁻]/g, function(ch){ return subMap[ch] || ch; });
      x = x.replace(/[αβγδεθλμπρστφΦωΩΔ]/g, function(ch){ return greekMap[ch] || ch; });
      x = x.normalize('NFD').replace(/[\\u0300-\\u036f]/g, '').toLowerCase();
      x = x.replace(/[’`]/g, "'").replace(/[-–—]/g, ' ');
      x = x.replace(/^\\s*(?:(?:il|lo|la|i|gli|le|un|uno|una)\\s+|(?:l|un|dell|nell|all|sull)'\\s*)/, '');
      return x.replace(/\\s+/g, ' ').trim();
    }
    var nt = normAns(typed);
    if (!nt) return;
    var variants = (accEl.getAttribute('data-acc') || '').split('|');
    var matched = variants.some(function(v) { return v && normAns(v) === nt; });
    if (matched) {
      typeEl.innerHTML = '<span class="typeGood">' + typed.replace(/&/g,'&amp;').replace(/</g,'&lt;') + '</span> <span class="sf-acc-badge">✓ Risposta equivalente accettata</span>';
    }
  })();
"""


def strip_google_fonts_html(tpl_html: str) -> str:
    return re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com">.*?rel="stylesheet">',
        "",
        tpl_html,
        flags=re.S,
    )


def upgrade_css(css: str) -> str:
    cleaned = re.sub(r"@import\s+url\(['\"]https://fonts\.googleapis\.com[^)]+\)\s*;\s*", "", css)
    cleaned = cleaned.replace(
        'font-family: "Space Grotesk", sans-serif;',
        'font-family: "Space Grotesk", -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;',
    )
    cleaned = cleaned.replace(
        'font-family: "JetBrains Mono", monospace;',
        'font-family: "Space Mono", ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;',
    )
    return OFFLINE_FONT_CSS + cleaned + EXTRA_SHARED_CSS


def html_to_plain(s: str) -> str:
    if not s:
        return ""
    out = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    return html.unescape(out)


def plain_to_html(s: str) -> str:
    return html.escape(s, quote=False).replace("\n", "<br>")


def clean_cloze_html(s: str) -> str:
    """Unescape entities, clean OCR/symbol defects, and single-escape HTML while preserving <sup>...</sup> tags."""
    if not s:
        return ""
    tmp = s.replace("<sup>", "\x01SUP\x02").replace("</sup>", "\x01/SUP\x02")
    tmp = re.sub(r"<br\s*/?>", "\n", tmp, flags=re.I)
    tmp = html.unescape(tmp)
    tmp = clean_ocr_fragment(tmp)
    tmp = html.escape(tmp, quote=False).replace("\n", "<br>")
    return tmp.replace("\x01SUP\x02", "<sup>").replace("\x01/SUP\x02", "</sup>")


def parse_options_html(opts_html: str) -> dict[str, str]:
    pairs = re.findall(
        r'<span class="opt-letter">([A-E])</span><span class="opt-body">(.*?)</span>',
        opts_html,
        flags=re.S,
    )
    return {k: v for k, v in pairs}


def render_options_html(opts_html: dict[str, str], correct_letter: str | None) -> str:
    parts = ['<div class="options">']
    for k in ["A", "B", "C", "D", "E"]:
        if k not in opts_html:
            continue
        cls = "opt correct" if (correct_letter and k == correct_letter) else "opt"
        parts.append(
            f'<div class="{cls}"><span class="opt-letter">{k}</span><span class="opt-body">{opts_html[k]}</span></div>'
        )
    parts.append("</div>")
    return "".join(parts)


def extract_cloze_targets(cloze_stem_html: str) -> list[str]:
    return [html.unescape(m.split("::")[0]) for m in re.findall(r"\{\{c\d+::(.*?)\}\}", cloze_stem_html)]


def cloze_to_back_stem(cloze_stem_html: str) -> str:
    def _repl(m: re.Match) -> str:
        inner = m.group(1).split("::")[0]
        return f'<span class="blank-filled">{inner}</span>'

    return re.sub(r"\{\{c\d+::(.*?)\}\}", _repl, cloze_stem_html)


def format_explanation_html(expl_plain: str, errata_note: str | None = None) -> str:
    main = plain_to_html(expl_plain.strip())
    if errata_note:
        note = plain_to_html(errata_note.strip())
        return f'{main}<div class="note-box">{note}</div>'
    return main


def ensure_live_sqlite(live_sqlite: Path) -> None:
    src_apkg = Path("/tmp/arena-coding-uploads/currnet_no_images.apkg.md")
    with zipfile.ZipFile(src_apkg) as zf:
        with zf.open("collection.anki21b") as s:
            raw = zstandard.ZstdDecompressor().stream_reader(s).read()
    live_sqlite.parent.mkdir(parents=True, exist_ok=True)
    live_sqlite.write_bytes(raw)


def main() -> None:
    root = Path("/home/user/anki-sem")
    cache_dir = root / "work/.cache"
    full_media_dir = cache_dir / "full_media"
    manifest = extract_all_delta_media(full_media_dir, include_full_live_media=True)
    restored_fig_html: dict[str, str] = manifest["restored_fig_html"]
    restored_sol_html: dict[str, str] = manifest["restored_sol_html"]

    clean_130 = build_clean_130(root / "work/opus_handoff/special_sets/missing_130_restored.jsonl")
    guid_map = json.loads((root / "work/opus_handoff/target_schema/guid_map_7078.json").read_text())
    v5_rows = load_v5_rows()

    bespoke: dict[str, dict] = {}
    bespoke.update(CHIM_189)
    bespoke.update(BIO_118)
    bespoke.update(FIS_127)

    # Load all 7,078 chunk records indexed by ItemID
    chunk_records: dict[str, dict] = {}
    for pth in sorted((root / "work/opus_handoff/chunks").rglob("chunk_*.jsonl")):
        for ln in pth.read_text().splitlines():
            r = json.loads(ln)
            chunk_records[r["id"]] = r
    assert len(chunk_records) == 7078, f"Expected 7078 chunk records, got {len(chunk_records)}"

    # Prepare clean working copy of live collection (read-only from currnet_no_images.apkg.md)
    live_sqlite = cache_dir / "live_collection.sqlite"
    ensure_live_sqlite(live_sqlite)
    work_db = cache_dir / "master_build_col.anki2"
    work_media = cache_dir / "master_build_col.media"
    work_db.unlink(missing_ok=True)
    shutil.rmtree(work_media, ignore_errors=True)
    shutil.copyfile(live_sqlite, work_db)

    col = Collection(str(work_db))

    # 1. Upgrade both notetypes (offline fonts, Cloze scan <details>, tolerant typed_answer JS, wrong-pick highlight)
    m_mcq = col.models.get(MCQ_MID)
    m_mcq["css"] = upgrade_css(m_mcq["css"])
    m_mcq["tmpls"][0]["qfmt"] = strip_google_fonts_html(m_mcq["tmpls"][0]["qfmt"])
    mcq_back = strip_google_fonts_html(m_mcq["tmpls"][0]["afmt"])
    mcq_back = mcq_back.replace(
        "o.classList.add('user-wrong');",
        "o.classList.add('user-wrong'); var eb = document.querySelector('.expl-box'); if (eb) eb.classList.add('is-wrong-review');",
    )
    m_mcq["tmpls"][0]["afmt"] = mcq_back
    col.models.save(m_mcq)

    m_cloze = col.models.get(CLOZE_MID)
    m_cloze["css"] = upgrade_css(m_cloze["css"])
    cloze_front = strip_google_fonts_html(m_cloze["tmpls"][0]["qfmt"])
    cloze_front = cloze_front.replace(
        '{{#QuestionScanHTML}}<div class="scan-wrap"><div class="scan-label">Dal libro · p. {{BookPage}}</div><div class="scan-box">{{QuestionScanHTML}}</div></div>{{/QuestionScanHTML}}',
        '{{#QuestionScanHTML}}<details class="orig-scan"><summary>Scansione originale della domanda (p. {{BookPage}})</summary>{{QuestionScanHTML}}</details>{{/QuestionScanHTML}}',
    )
    m_cloze["tmpls"][0]["qfmt"] = cloze_front
    cloze_back = strip_google_fonts_html(m_cloze["tmpls"][0]["afmt"])
    cloze_back = cloze_back.replace("})();\n</script>", CLOZE_TYPED_JS + "\n})();\n</script>")
    m_cloze["tmpls"][0]["afmt"] = cloze_back
    col.models.save(m_cloze)

    # 2. Update all 6,948 live notes in place (preserving 100% of live GUIDs)
    updated_live = 0
    v5_stem_upgrades = 0
    v5_opt_upgrades = 0
    v5_expl_upgrades = 0
    fig_cleaned_count = 0

    for nid in col.find_notes(""):
        note = col.get_note(nid)
        iid = note.fields[0]
        rec = chunk_records[iid]
        sw = rec.get("solved_work") or {}
        cc = sw.get("cc130265") or {}
        c0 = sw.get("0c53ca03") or {}
        patch = bespoke.get(iid)
        ovr = ITEM_SPECIFIC_OVERRIDES.get(iid, {})
        xpatch = EXPLICIT_CARD_PATCHES.get(iid, {})
        v5r = v5_rows.get(iid)
        is_cloze = note.mid == CLOZE_MID

        if not is_cloze:
            stem_plain = html_to_plain(note.fields[8])
            if (
                v5r
                and not (patch and "question" in patch)
                and "stem" not in ovr
                and "question" not in xpatch
            ):
                v5_q = (v5r.get("question") or "").strip()
                if v5_field_ok(stem_plain, v5_q):
                    stem_plain = v5_q
                    v5_stem_upgrades += 1

            stem_plain = clean_ocr_fragment(stem_plain)
            for old_s, new_s in xpatch.get("question_replacements") or []:
                stem_plain = stem_plain.replace(old_s, new_s)
            if "question" in xpatch:
                stem_plain = clean_ocr_fragment(xpatch["question"])
            if "stem" in ovr:
                stem_plain = clean_ocr_fragment(ovr["stem"])
            if patch and "question" in patch:
                stem_plain = clean_ocr_fragment(patch["question"])

            stem_html = plain_to_html(stem_plain)
            note.fields[8] = stem_html
            note.fields[9] = stem_html

            raw_opts = parse_options_html(note.fields[10])
            v5_opts = (v5r.get("options") or {}) if v5r else {}
            x_opts = xpatch.get("options") or {}
            opts_html: dict[str, str] = {}
            for k, v_html in raw_opts.items():
                opt_plain = html_to_plain(v_html)
                if (
                    k in v5_opts
                    and not (patch and "options" in patch and k in patch["options"])
                    and f"opt_{k.lower()}" not in ovr
                    and k not in x_opts
                ):
                    v5_o = (v5_opts.get(k) or "").strip()
                    if v5_field_ok(opt_plain, v5_o):
                        opt_plain = v5_o
                        v5_opt_upgrades += 1

                opt_plain = clean_ocr_fragment(opt_plain)
                if k in x_opts:
                    opt_plain = clean_ocr_fragment(x_opts[k])
                if f"opt_{k.lower()}" in ovr:
                    opt_plain = clean_ocr_fragment(ovr[f"opt_{k.lower()}"])
                if patch and "options" in patch and k in patch["options"]:
                    opt_plain = clean_ocr_fragment(patch["options"][k])
                opts_html[k] = plain_to_html(opt_plain)

            m_ans = re.search(r"Risposta corretta:\s*([A-E])\b", note.fields[12])
            ans_letter = m_ans.group(1) if m_ans else rec["remediated_card"]["answer"]
            if patch and "answer" in patch:
                ans_letter = patch["answer"]

            note.fields[10] = render_options_html(opts_html, None)
            note.fields[11] = render_options_html(opts_html, ans_letter)
            ans_body = opts_html.get(ans_letter, "")
            if "answer_banner" in ovr:
                note.fields[12] = ovr["answer_banner"]
            else:
                note.fields[12] = f"Risposta corretta: {ans_letter}. {ans_body}"
        else:
            if "cloze_stem" in xpatch:
                cloze_stem = clean_cloze_html(xpatch["cloze_stem"])
            elif patch and "cloze_stem" in patch:
                cloze_stem = clean_cloze_html(patch["cloze_stem"])
            else:
                cloze_stem = clean_cloze_html(note.fields[8])

            note.fields[8] = cloze_stem
            note.fields[9] = cloze_to_back_stem(cloze_stem)

            targets = extract_cloze_targets(cloze_stem)
            extra_syns = list((patch.get("accepted_synonyms") if patch else None) or []) + list(
                xpatch.get("accepted_synonyms") or []
            )
            syns = derive_cloze_synonyms(targets, extra_syns or None, cc.get("flags"))
            disp_ans = "/".join(targets)
            if patch and "answer_text" in patch and len(targets) == 1:
                disp_ans = patch["answer_text"]
            acc_attr = html.escape("|".join(syns), quote=True)
            note.fields[12] = (
                f"Risposta corretta: {html.escape(disp_ans, quote=False)}"
                f'<span class="sf-acc-data" data-acc="{acc_attr}" hidden></span>'
            )

        # ExplanationHTML (100% populated + .note-box errata_note caveats)
        errata_note = (patch.get("errata_note") if patch else None) or xpatch.get("errata_note")
        if patch and "explanation" in patch:
            expl_plain = clean_ocr_fragment(patch["explanation"])
        elif "explanation" in xpatch:
            expl_plain = clean_ocr_fragment(xpatch["explanation"])
        elif note.fields[13].strip():
            curr_expl = html_to_plain(note.fields[13].strip())
            if v5r:
                v5_expl = (v5r.get("explanation") or "").strip()
                if v5_expl and v5_field_ok(curr_expl, v5_expl):
                    curr_expl = v5_expl
                    v5_expl_upgrades += 1
            expl_plain = clean_ocr_fragment(curr_expl)
        elif cc.get("status") == "done" and (cc.get("reason") or "").strip():
            expl_plain = clean_ocr_fragment(cc["reason"])
        elif c0.get("status") == "done" and (c0.get("reason") or "").strip():
            expl_plain = clean_ocr_fragment(c0["reason"])
        else:
            raise RuntimeError(f"Live item {iid} has no explanation!")

        for old_e, new_e in xpatch.get("explanation_replacements") or []:
            expl_plain = expl_plain.replace(old_e, new_e)
        note.fields[13] = format_explanation_html(expl_plain, errata_note)

        # FigureHTML cleanup (strip 34 bogus text-duplicate crops + apply 12 tight clean_fig_* crops)
        old_fig = note.fields[14]
        new_fig = clean_live_figure_html(old_fig)
        if new_fig != old_fig:
            fig_cleaned_count += 1
        note.fields[14] = new_fig

        # Tags: preserve live tags, sync con_figura with cleaned FigureHTML, attach MUR 2026 ud:: and dup::
        full_text = html.unescape(f"{note.fields[8]} {note.fields[10]} {note.fields[12]}")
        ud_tag = classify_ud_tag(rec, full_text)
        kept_tags = [
            t
            for t in note.tags
            if not t.startswith("ud::") and not t.startswith("dup::") and t != "con_figura"
        ]
        kept_tags.append(ud_tag)
        for dt in rec.get("dup_tags") or []:
            tag_val = dt if dt.startswith("dup::") else f"dup::{dt}"
            if tag_val not in kept_tags:
                kept_tags.append(tag_val)
        if note.fields[14].strip():
            kept_tags.append("con_figura")
        note.tags = kept_tags

        col.update_note(note)
        updated_live += 1

    assert updated_live == 6948, f"Expected 6948 updated live notes, got {updated_live}"

    # 3. Add all 130 restored items
    subj_meta = {
        "CHIM": ("Chimica e Propedeutica Biochimica", "chimica"),
        "BIO": ("Biologia e Genetica", "biologia"),
        "FIS": ("Fisica", "fisica"),
    }
    qtype_labels = {
        "COMM": ("Quiz commentati", "commentati"),
        "NCOM": ("Quiz non commentati", "non_commentati"),
        "COMP": ("Quiz a completamento", "completamento"),
    }

    added_restored = 0
    for iid, item in sorted(clean_130.items()):
        rec = chunk_records[iid]
        ginfo = guid_map[iid]
        mid = int(ginfo["mid"])
        did = int(ginfo["did"])
        is_cloze = mid == CLOZE_MID
        xpatch = EXPLICIT_CARD_PATCHES.get(iid, {})

        model = col.models.get(mid)
        note = col.new_note(model)
        note.guid = ginfo["guid"]

        scode = rec["subject_code"]
        sname, mtag = subj_meta[scode]
        cnum = str(int(rec["chapter_num"]))
        ctitle = rec["chapter_title"]
        qt_raw = rec["quiz_type"]
        if qt_raw in ("COMM", "NCOM", "COMP"):
            qlabel, qtag = qtype_labels[qt_raw]
        else:
            rev = {
                "commentati": ("Quiz commentati", "commentati"),
                "non_commentati": ("Quiz non commentati", "non_commentati"),
                "completamento": ("Quiz a completamento", "completamento"),
            }
            qlabel, qtag = rev[qt_raw]

        qnum = str(int(rec["qnum"]))
        bpage = str(rec["question_book_page"])

        note.fields[0] = iid
        note.fields[1] = sname
        note.fields[2] = scode
        note.fields[3] = cnum
        note.fields[4] = ctitle
        note.fields[5] = qlabel
        note.fields[6] = qnum
        note.fields[7] = bpage

        if not is_cloze:
            q_plain = clean_ocr_fragment(xpatch.get("question", item["question"]))
            q_esc = plain_to_html(q_plain)
            opts_esc = {}
            x_opts = xpatch.get("options") or {}
            for k, v in item["options"].items():
                opts_esc[k] = plain_to_html(clean_ocr_fragment(x_opts.get(k, v)))
            ans_l = item["answer"]
            note.fields[8] = q_esc
            note.fields[9] = q_esc
            note.fields[10] = render_options_html(opts_esc, None)
            note.fields[11] = render_options_html(opts_esc, ans_l)
            note.fields[12] = f"Risposta corretta: {ans_l}. {opts_esc[ans_l]}"
        else:
            cstem_raw = xpatch.get("cloze_stem", item["question"])
            raw_ans = (item.get("answer_text") or item.get("answer") or "").strip()
            cloze_ans = "ω" if raw_ans == "ω (omega)" else raw_ans
            if "{{c1::" not in cstem_raw:
                cstem_raw = re.sub(r"_{2,}", f"{{{{c1::{cloze_ans}}}}}", cstem_raw, count=1)
                cstem_raw = cstem_raw.replace(" .", ".")
                if not cstem_raw.endswith((".", "?", "!")):
                    cstem_raw += "."
            cstem = clean_cloze_html(cstem_raw)
            note.fields[8] = cstem
            note.fields[9] = cloze_to_back_stem(cstem)
            targets = extract_cloze_targets(cstem)
            extra_syns = list(item.get("accepted_synonyms") or []) + list(xpatch.get("accepted_synonyms") or [])
            syns = derive_cloze_synonyms(targets + ([raw_ans] if raw_ans else []), extra_syns or None)
            disp_ans = raw_ans or "/".join(targets)
            acc_attr = html.escape("|".join(syns), quote=True)
            note.fields[12] = (
                f"Risposta corretta: {html.escape(disp_ans, quote=False)}"
                f'<span class="sf-acc-data" data-acc="{acc_attr}" hidden></span>'
            )

        expl_plain = clean_ocr_fragment(xpatch.get("explanation", item["explanation"]))
        err_note = xpatch.get("errata_note") or item.get("errata_note")
        note.fields[13] = format_explanation_html(expl_plain, err_note)
        note.fields[14] = restored_fig_html.get(iid, "")
        note.fields[15] = f'<img src="restored_{iid}.png">'
        note.fields[16] = restored_sol_html.get(iid, "")

        full_text = html.unescape(f"{note.fields[8]} {note.fields[10]} {note.fields[12]}")
        ud_tag = classify_ud_tag(rec, full_text)
        tags = [
            f"capitolo::{scode}_cap_{int(rec['chapter_num']):02d}",
            f"materia::{mtag}",
            f"pagina::{bpage}",
            f"tipo::{qtag}",
            ud_tag,
            "restored::dedup_130",
        ]
        twin_id = ginfo.get("kept_twin_id")
        if twin_id:
            tags.append(f"dup::{twin_id}")
        if note.fields[14].strip():
            tags.append("con_figura")
        note.tags = tags

        col.add_note(note, did)
        added_restored += 1

    assert added_restored == 130, f"Expected 130 restored notes, got {added_restored}"
    assert col.note_count() == 7078, f"Expected 7078 total notes, got {col.note_count()}"
    assert col.card_count() == 7082, f"Expected 7082 total cards, got {col.card_count()}"

    # 4. Copy all 8,234 standalone media files (8,230 PNGs + 4 offline fonts) into col.media.dir()
    media_dir = Path(col.media.dir())
    copied_media = 0
    for mf in sorted(full_media_dir.iterdir()):
        if mf.is_file():
            shutil.copy2(mf, media_dir / mf.name)
            copied_media += 1
    assert copied_media == 8234, f"Expected 8234 staged media files, got {copied_media}"

    col.close()

    # Guarantee strict mod > 1792777729 floor across notes, cards, notetypes, templates
    now_ts = max(MOD_FLOOR, int(time.time()))
    con = sqlite3.connect(work_db)
    con.execute("UPDATE notes SET mod = ? WHERE mod < ?", (now_ts, now_ts))
    con.execute("UPDATE cards SET mod = ? WHERE mod < ?", (now_ts, now_ts))
    con.execute("UPDATE notetypes SET mtime_secs = ? WHERE mtime_secs < ?", (now_ts, now_ts))
    con.execute("UPDATE templates SET mtime_secs = ? WHERE mtime_secs < ?", (now_ts, now_ts))
    con.commit()
    con.close()

    # Re-open via official Anki engine and export standalone Anki v3 .apkg with all media
    out_apkg = root / "work/master_build/Semestre_Filtro_Master_7078.apkg"
    out_apkg.unlink(missing_ok=True)
    col = Collection(str(work_db))
    exported_cards = col.export_anki_package(
        out_path=str(out_apkg),
        options=ExportAnkiPackageOptions(
            with_scheduling=False,
            with_deck_configs=False,
            with_media=True,
            legacy=False,
        ),
        limit=None,
    )
    col.close()
    print(
        f"Stats: v5_stem={v5_stem_upgrades}, v5_opt={v5_opt_upgrades}, v5_expl={v5_expl_upgrades}, "
        f"fig_cleaned={fig_cleaned_count}, media={copied_media}"
    )
    print(f"Exported {out_apkg} ({out_apkg.stat().st_size / (1024*1024):.2f} MB), cards={exported_cards}")


if __name__ == "__main__":
    main()
