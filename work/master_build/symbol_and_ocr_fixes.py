#!/usr/bin/env python3
"""Comprehensive symbol, chemical formula, Greek, unit, OCR, and textbook-errata remediation across all 7,078 notes."""
from __future__ import annotations

import json
import re
import subprocess
from typing import Any

_RICH_CHARS = set("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻αβγδεζηθικλμνξοπρστυφχψωΔΩ")
_GLUED_OR_GARBLE_RE = re.compile(
    r"[a-zàèéìòù]{17,}|DNA polimerasi [6aBy]\b|‘[0-9A-Za-z]|\bjHe\b|\$He\b|\bGX\b|\belettoni\b|\bSalo1|\bGrappa:|\bNuoro\b"
)


def load_v5_rows() -> dict[str, dict[str, Any]]:
    """Load pixel-verified v5repo qa_dataset.jsonl (6,948 items, 1-to-1 ItemID match with live collection)."""
    raw = subprocess.check_output(
        ["git", "show", "origin/opus-rebuild/semestre-filtro:v5repo/output/qa_dataset.jsonl"],
        text=True,
    )
    return {r["id"]: r for r in (json.loads(ln) for ln in raw.splitlines() if ln.strip())}


def v5_field_ok(curr_plain: str, v5_plain: str) -> bool:
    """Return True iff v5_plain cleanly improves curr_plain without losing rich Unicode symbols or introducing glued tokens."""
    if not v5_plain or v5_plain == curr_plain:
        return False
    if "\n" in curr_plain and "\n" not in v5_plain:
        return False
    if _GLUED_OR_GARBLE_RE.search(v5_plain) and not _GLUED_OR_GARBLE_RE.search(curr_plain):
        return False
    cleaned_curr = re.sub(r"(?:[a-zàèéìòùA-Z]{2,}[²³⁴]|[0-9A-Z]+[₃₄](?=\s|$))", "", curr_plain)
    c_rich = {ch for ch in cleaned_curr if ch in _RICH_CHARS}
    v_rich = {ch for ch in v5_plain if ch in _RICH_CHARS}
    if c_rich - v_rich:
        return False
    return True


# Context-guarded symbol, formula, ion, Greek, Svedberg, Roman-numeral, physics-unit, and scan-bleed regexes
SYMBOL_OCR_SUBS: list[tuple[re.Pattern, str]] = [
    # Statement combination OCR fixes
    (re.compile(r"\b(?:Solo|Salo)\s*(?:1|l)\s*e\s*(\d)\b"), r"Solo 1 e \1"),
    (re.compile(r"\b(?:Solo|Salo)(?:1|l)e(\d)\b"), r"Solo 1 e \1"),
    (re.compile(r"\b(?:Solo|Salo)\s*2\s*e\s*3\b"), "Solo 2 e 3"),
    (re.compile(r"\bSalo\s+(\d)\b"), r"Solo \1"),
    (re.compile(r"\bSalo\s+(per|la)\b"), r"Solo \1"),
    (re.compile(r"\bSolo(\d)\b"), r"Solo \1"),
    (re.compile(r"\bdelia\b"), "della"),
    (re.compile(r"\bmoti\s+di\b"), "moli di"),
    (re.compile(r"\bla\s+disposta\b"), "la risposta"),
    (re.compile(r"\b0,\s*1,\s*2\s+0\s+3\b"), "0, 1, 2 o 3"),
    (re.compile(r"\(CH₃CH₂\)₂0"), "(CH₃CH₂)₂O"),
    (re.compile(r"\(NH,C1\)"), "(NH₄Cl)"),
    (re.compile(r"\(NH\.,?\)"), "(NH₃)"),
    (re.compile(r"\(N,\s*0,\s*F\)"), "(N, O, F)"),
    (re.compile(r"atomo\s+di\s+N₂\s+0,\s*F\b"), "atomo di N, O, F"),
    (re.compile(r"\buna\s+mole\s+di\s+0,\s+pesa\b"), "una mole di O₂ pesa"),
    (re.compile(r"\bK,0\b"), "K₂O"),
    # Chemical formulas & zero/comma-for-subscript
    (re.compile(r"H,PO,"), "H₃PO₄"),
    (re.compile(r"H,S0,"), "H₂SO₄"),
    (re.compile(r"\bH,S\b"), "H₂S"),
    (re.compile(r"\bS0,,"), "SO₂,"),
    (re.compile(r"\bS0,\b"), "SO₂"),
    (re.compile(r"\bNH,,"), "NH₃,"),
    (re.compile(r"\baNH,\s*\+\s*bO,\s*->\s*cNO\s*\+\s*6H₂0"), "a NH₃ + b O₂ → c NO + 6 H₂O"),
    (re.compile(r"\bNO\.(?=,|\s|$)"), "NO₂"),
    (re.compile(r"60₂\s*[—–-]\s*6C0,\s*\+\s*6H₂0\s*\+\s*nATP"), "6 O₂ → 6 CO₂ + 6 H₂O + n ATP"),
    (re.compile(r"CH,,0,"), "C₆H₁₂O₆"),
    (re.compile(r"C,,H,,0,,,"), "C₁₂H₂₂O₁₁,"),
    (re.compile(r"C,,H,,"), "C₆H₁₀"),
    (re.compile(r"\bC0,"), "CO₂"),
    (re.compile(r"\bC0₂"), "CO₂"),
    (re.compile(r"\bC02\b"), "CO₂"),
    (re.compile(r"\bCO2\b"), "CO₂"),
    (re.compile(r"\bH₂0\b"), "H₂O"),
    (re.compile(r"\b2H,0\b"), "2 H₂O"),
    (re.compile(r"\bH,\s*0\b"), "H₂O"),
    (re.compile(r"\bH202\b"), "H₂O₂"),
    (re.compile(r"\bH2C03\b"), "H₂CO₃"),
    (re.compile(r"H₄P₂0₇"), "H₄P₂O₇"),
    (re.compile(r"P₂O₅\s*\+\s*2\s*H₂O\s*\+\s*H₄P₂O₇"), "P₂O₅ + 2 H₂O → H₄P₂O₇"),
    (re.compile(r"\bNa0H\b"), "NaOH"),
    (re.compile(r"\bK0H\b"), "KOH"),
    (re.compile(r"\bNacl\b"), "NaCl"),
    (re.compile(r"NaC!"), "NaCl"),
    (re.compile(r"KC\]"), "KCl"),
    (re.compile(r"Al,O,"), "Al₂O₃"),
    (re.compile(r"Hg,Cl,"), "Hg₂Cl₂"),
    (re.compile(r"\bHg₂0\b"), "Hg₂O"),
    (re.compile(r"2HGIO,"), "2 HClO₄"),
    (re.compile(r"Cu\(CIO,\),,"), "Cu(ClO₄)₂,"),
    (re.compile(r"CH,0H-CHOH[⁻-]CH,0H"), "CH₂OH-CHOH-CH₂OH"),
    (re.compile(r"CICR,CH,0H"), "ClCH₂CH₂OH"),
    (re.compile(r"H,€-CO-CH₃"), "H₃C-CO-CH₃"),
    (re.compile(r"\(CH₃C0\)₂0"), "(CH₃CO)₂O"),
    (re.compile(r"R-C0-0-R'"), "R-CO-O-R'"),
    (re.compile(r"CH₃C00CH₂CH₃"), "CH₃COOCH₂CH₃"),
    (re.compile(r"CH₃C00H"), "CH₃COOH"),
    (re.compile(r"CH₃-0-CH₃"), "CH₃-O-CH₃"),
    (re.compile(r"-COCI\b"), "-COCl"),
    (re.compile(r"\bCCI₂\s*HCF₂CCIFH\b"), "CCl₂=CF₂, HCF₂CClFH"),
    (re.compile(r"\bCH³OH\b"), "CH₃OH"),
    (re.compile(r"\bFADH,,"), "FADH₂,"),
    (re.compile(r"\bFADH,\b"), "FADH₂"),
    (re.compile(r"\bFADH,(?=\s|$|<|\.)"), "FADH₂"),
    (re.compile(r"\bFADH\.,"), "FADH₂,"),
    (re.compile(r"\bFADH2\b"), "FADH₂"),
    (re.compile(r"\bNADH₄\s+"), "NADH, "),
    (re.compile(r"\bCO\.(?=\s|$|<)"), "CO₂"),
    (re.compile(r"\bQH\."), "QH₂"),
    (re.compile(r"\b(molecol[ae]|mol[ei]|PM\.)\s+di\s+O,(?=\s|$)"), r"\1 di O₂"),
    (re.compile(r"\b(molecol[ae]|mol[ei]|PM\.)\s+di\s+N,(?=\s|$)"), r"\1 di N₂"),
    (re.compile(r"\b(molecol[ae]|mol[ei])\s+di\s+H,(?=\s|$)"), r"\1 di H₂"),
    (re.compile(r"\b(litri|moli|mole)\s+di\s+CH,(?=\s|$)"), r"\1 di CH₄"),
    (re.compile(r"\bmoli\s+di\s+0(?=\s|$|,)"), "moli di O₂"),
    (re.compile(r"(?<![0-9A-Za-z.,])0₂(?![0-9])"), "O₂"),
    (re.compile(r"\bLO,\s+viene"), "L'O₂ viene"),
    (re.compile(r"\bLATP\b"), "L'ATP"),
    # Ions & charges
    (re.compile(r"OH[”\"]"), "OH⁻"),
    (re.compile(r"\[OH\]"), "[OH⁻]"),
    (re.compile(r"\[H30\*\]"), "[H₃O⁺]"),
    (re.compile(r"H30°\s+0\s+OH⁻"), "H₃O⁺ o OH⁻"),
    (re.compile(r"H30[°*]"), "H₃O⁺"),
    (re.compile(r"H\*\s*\+"), "H⁺ +"),
    (re.compile(r"\bioni\s+H['’]"), "ioni H⁺"),
    (re.compile(r"\bH[’']\s+in\s+soluzione"), "H⁺ in soluzione"),
    (re.compile(r"Ca\*\*"), "Ca²⁺"),
    (re.compile(r"Ca⁴⁺"), "Ca²⁺"),
    (re.compile(r"Ca²⁴"), "Ca²⁺"),
    (re.compile(r"Fe³⁺⁺"), "Fe³⁺"),
    (re.compile(r"\b0\s+Rh[”\"-]"), "0 Rh⁻"),
    (re.compile(r"\b(AB|A|B)\s+Rh-(?=\s|$|<)"), r"\1 Rh⁻"),
    (re.compile(r"\be\"\s*[—–→-]\s*"), "e⁻ → "),
    (re.compile(r"\bCi-CI\b"), "Cl-Cl"),
    (re.compile(r"\batomi\s+F,\s*CI\s+e\s+Br\b"), "atomi F, Cl e Br"),
    (re.compile(r"\bCanali\s+del\s+CI\b"), "Canali del Cl⁻"),
    # Thermodynamics & Greek & Molecular Biology
    (re.compile(r"\bAG\s*([<>]|=\s*0)"), r"ΔG \1"),
    (re.compile(r"\bAG°"), "ΔG°"),
    (re.compile(r"\bAH\s*([<>]|=\s*0)"), r"ΔH \1"),
    (re.compile(r"\bAS\s*([<>]|=\s*0)"), r"ΔS \1"),
    (re.compile(r"\bAK\s*([<>]|=\s*0)"), r"ΔK \1"),
    (re.compile(r"\bB-ossidazione\b"), "β-ossidazione"),
    (re.compile(r"\bIl\s+DNA\s+polimerasi\s+6\b"), "La DNA polimerasi δ"),
    (re.compile(r"\bDNA\s+polimerasi\s+6\b"), "DNA polimerasi δ"),
    (re.compile(r"\bDNA\s+polimerasi\s+è(?=\s|$|<)"), "DNA polimerasi ε"),
    (re.compile(r"\bTubulina\s+y\b"), "Tubulina γ"),
    (re.compile(r"\by-tubulina\b"), "γ-tubulina"),
    (re.compile(r"\bActina\s+[8B]\b"), "Actina β"),
    (re.compile(r"\bImportina\s+a\b"), "Importina α"),
    (re.compile(r"\bSubunità\s+a\b"), "Subunità α"),
    (re.compile(r"\bSubunità\s+B\b"), "Subunità β"),
    (re.compile(r"\bFattore\s+p\b"), "Fattore ρ"),
    (re.compile(r"\bp-dipendente\b"), "ρ-dipendente"),
    (re.compile(r"\b070\b"), "σ⁷⁰"),
    (re.compile(r"\bNFxB\b"), "NF-κB"),
    (re.compile(r"\ba5ft1\b"), "α₅β₁"),
    (re.compile(r"\bintegrina\s+af\b"), "integrina αβ"),
    (re.compile(r"\bPIk1\b"), "Plk1"),
    (re.compile(r"\bPIkl\b"), "Plk1"),
    (re.compile(r"\bPIk\b"), "Plk"),
    (re.compile(r"\bWeel\b"), "Wee1"),
    (re.compile(r"\bpl6\b"), "p16"),
    (re.compile(r"\bPexS\b"), "Pex5"),
    (re.compile(r"\bRabS\b"), "Rab5"),
    (re.compile(r"\bsnRNP\s+Ul\b"), "snRNP U1"),
    (re.compile(r"\bUl\s+snRNP\b"), "U1 snRNP"),
    (re.compile(r"\bCAMP\b"), "cAMP"),
    (re.compile(r"\bfosfolipasi\s+A\."), "fosfolipasi A₂"),
    # Svedberg & Cell-cycle & Genetics & Roman numerals
    (re.compile(r"5,85"), "5,8S"),
    (re.compile(r"\brRNA\s+55\b"), "rRNA 5S"),
    (re.compile(r"\brRNA\s+185\b"), "rRNA 18S"),
    (re.compile(r"\brRNA\s+165\b"), "rRNA 16S"),
    (re.compile(r"23\$"), "23S"),
    (re.compile(r"\bfase\s+\$(?=\s|$|[.,;)])"), "fase S"),
    (re.compile(r"\b(in|da|fase)\s+GO\b"), r"\1 G₀"),
    (re.compile(r"\bGO,\s*M₄\s*T₄X\b"), "G₀, M, T, X"),
    (re.compile(r"\bfase\s+G,(?=\s|$|[.,;)])"), "fase G₁"),
    (re.compile(r"fasi\s+G,,\s*S,\s*G,"), "fasi G₁, S, G₂"),
    (re.compile(r"2\"\s*=\s*(\d+)"), r"2n = \1"),
    (re.compile(r"3°\s*-\s*5[’']"), "3'-5'"),
    (re.compile(r"5['’]\s*-\s*3\""), "5'-3'"),
    (re.compile(r"5['’]\s*→\s*3\""), "5' → 3'"),
    (
        re.compile(
            r"\b(Complesso|polimerasi|pol|Topoisomerasi|profase|metafase|anafase|telofase|meiosi|meiotica|Anafase|Profase|Metafase|Telofase)\s+Il\b"
        ),
        r"\1 II",
    ),
    (re.compile(r"\bComplesso\s+1\s+\(NADH"), "Complesso I (NADH"),
    (re.compile(r"citocromo\s+be;"), "citocromo bc₁"),
    (re.compile(r"\bI,\s*Il\s+e\s+Ill\b"), "I, II e III"),
    (re.compile(r"\bIntroni\s+di\s+gruppo\s+le\s+Il\b"), "Introni di gruppo I e II"),
    (re.compile(r"\bal\s+i\s+gruppo\b"), "al I gruppo"),
    (re.compile(r"\bnel\s+gruppo\s+i\s+della\b"), "nel gruppo I della"),
    (re.compile(r"\bprofase\s+i\s+della\s+meiosi\b"), "profase I della meiosi"),
    (re.compile(r"\bmeiosi\s+i\s+sia\s+in\s+meiosi\s+II\b"), "meiosi I sia in meiosi II"),
    (re.compile(r"\bTelofase\s+\|"), "Telofase I"),
    # Word splits / merges & Cloze OCR
    (re.compile(r"dal\s+toni\s+che"), "daltoniche"),
    (re.compile(r"al\s+le\s+le"), "allele"),
    (re.compile(r"su\s+per\s+famiglia"), "superfamiglia"),
    (re.compile(r"che\s+mio\s+tassi"), "chemiotassi"),
    (re.compile(r"\btradizionale\s+e\s+post-traduzionale"), "traduzionale e post-traduzionale"),
    (re.compile(r"\bcontrollo\s+tradizionale\s+negli\s+eucarioti"), "controllo traduzionale negli eucarioti"),
    (re.compile(r"^LV\s+\{\{c1::"), "L'{{c1::"),
    (re.compile(r"\}?\}\s+0\s+pili\b"), "}} o pili"),
    (re.compile(r"DNA\s+e\s+RNA₁\s+molecole"), "DNA e RNA, molecole"),
    (re.compile(r"(\d+)⁻\s+settimana"), r"\1ª settimana"),
    (re.compile(r"\{\{c1::cromosomi\}\}\s+sono\s+46₄\s+"), "{{c1::cromosomi}} sono 46, "),
    (re.compile(r"\b(20|12|No|p53|AB)[₃]\s+"), r"\1, "),
    (re.compile(r"\b(Si|GAP|distanza\s+d|resistenza\s+R)[₄]\s+"), r"\1, "),
    (re.compile(r"\bLAMP\s+ciclico\b"), "L'AMP ciclico"),
    (re.compile(r"^\[GPCR\b"), "I GPCR"),
    (re.compile(r"^IRTK\b"), "Gli RTK"),
    (re.compile(r"^6\s+\{\{c1::ciclo\}\}"), "Il {{c1::ciclo}}"),
    (re.compile(r"^LAPC/C\b"), "L'APC/C"),
    (re.compile(r"^GHioni\b"), "Gli ioni"),
    (re.compile(r"reticolo\)\}\}\s+fonico\b"), "reticolo}} ionico"),
    (re.compile(r"reticolo\}\}\s+fonico\b"), "reticolo}} ionico"),
    (re.compile(r"\bAuoruro\b"), "fluoruro"),
    (re.compile(r"^41\s+\{\{c1::punto\s+di\s+fusione\}\}"), "Il {{c1::punto di fusione}}"),
    (re.compile(r"^01\s+\{\{c1::punto\s+di\s+ebollizione\}\}"), "Il {{c1::punto di ebollizione}}"),
    (re.compile(r"^N\s+\{\{c1::litio\}\}"), "Il {{c1::litio}}"),
    (re.compile(r"R-COOR!"), "R-COOR'."),
    (re.compile(r"\{\{c1::ATP\}\}\s*«dipendente"), "{{c1::ATP}}-dipendente"),
    (re.compile(r"\bOmV\b"), "0 mV"),
    (re.compile(r"\[\s*nucleoli\b"), "I nucleoli"),
    (re.compile(r"N-glicosilazioni⁻"), "N-glicosilazioni?"),
    (re.compile(r"Terra-Luna⁻"), "Terra-Luna?"),
    (re.compile(r"transizione\s+G1-S⁻"), "transizione G1-S?"),
    # Physics units, scientific notation & symbols
    (re.compile(r"g/cm[’']"), "g/cm³"),
    (re.compile(r"\bohmmetro\b"), "ohm · metro"),
    (re.compile(r"mol-!"), "mol⁻¹"),
    (re.compile(r"mol!(?=\s|=)"), "mol⁻¹"),
    (re.compile(r"10!°"), "10¹⁰"),
    (re.compile(r"10s\"!"), "10 s⁻¹"),
    (re.compile(r"\bns\"!"), "n s⁻¹"),
    (re.compile(r"\bparial\b"), "pari a 1"),
    (re.compile(r"\bparia1\b"), "pari a 1"),
    (re.compile(r"m/sin(\d+)s\b"), r"m/s in \1 s"),
    (re.compile(r"1,2\s*x\s*105\b"), "1,2 × 10⁵"),
    (re.compile(r"Gm,m,"), "Gm₁m₂"),
    (re.compile(r"\bn,\s*=\s*4/3"), "n₁ = 4/3"),
    (re.compile(r"\bn,\s*=\s*1\b"), "n₂ = 1"),
    (re.compile(r"\be,\s*=\s*2\b"), "ε_r = 2"),
    (re.compile(r"\bcasi\s+C,\s*D,\s*E\s*1\+"), "casi C, D, E"),
    (re.compile(r"\bL\s*=\s*I\s*w\b"), "L = I ω"),
    (re.compile(r"cos\(wt\s*\+"), "cos(ωt +"),
    (re.compile(r"\bdi\s+w\s+è\s+radianti\b"), "di ω è radianti"),
    (re.compile(r"\bw\s+t\s*\+\s*\{\{c1::"), "ω t + {{c1::"),
    (re.compile(r"\bIl\s+parametro\s+t\s*=\s*m/b\b"), "Il parametro τ = m/b"),
    (re.compile(r"\bv\s*=\s*vo\s*\+\s*at\b"), "v = v₀ + at"),
    (re.compile(r"\bFx\s+\{\{c1::Δt\}\}"), "F × {{c1::Δt}}"),
    (re.compile(r"J/mol-K"), "J/(mol·K)"),
    # Scan margin bleeds
    (
        re.compile(
            r"\s+(?:SS\s*255|os\s*PZ|os\s*PP|acs\s*OZ\s*I|uss\s*PP\s*I|PAR\s*cs|css\.\s*JP|iss\s*=|238\s*=|177\.\s*°|i\s+es|=\s*ee)\s*$"
        ),
        "",
    ),
]


def apply_symbol_ocr_subs(text: str) -> str:
    if not text:
        return text
    out = text
    for pat, repl in SYMBOL_OCR_SUBS:
        out = pat.sub(repl, out)
    return out


# Explicit per-card patches for remaining scan-verified stems, options, Cloze stems, explanations, and .note-box errata caveats
EXPLICIT_CARD_PATCHES: dict[str, dict[str, Any]] = {
    # ── Biologia e Genetica ──
    "BIO-C01-COMP-080": {
        "accepted_synonyms": ["anfipatiche"],
        "errata_note": "Nota scientifica: in chimica colloidale le molecole puramente apolari tendono a separarsi di fase in acqua (emulsioni instabili), mentre la formazione di micelle stabili è tipica delle molecole anfipatiche dotate di testa polare e coda apolare.",
    },
    "BIO-C01-COMP-115": {
        "cloze_stem": "La variazione di {{c1::energia libera di Gibbs}} (ΔG) indica la spontaneità di una reazione chimica in condizioni cellulari.",
        "accepted_synonyms": ["energia libera di Gibbs", "variazione di energia libera di Gibbs", "energia libera", "ΔG"],
    },
    "BIO-C01-NCOM-098": {
        "question": "Dall'osservazione al microscopio ottico di una cellula si nota che in essa sono presenti mitocondri e ribosomi insieme ad altri organuli. Si può sicuramente escludere che si tratti:",
        "options": {"D": "di un batterio in forte attività metabolica"},
        "errata_note": "Nota scientifica: la presenza di mitocondri (visibili al microscopio ottico, ~1–2 μm) esclude con certezza una cellula procariotica (D); si noti tuttavia che i singoli ribosomi (~20–30 nm) sono al di sotto del potere risolutivo del microscopio ottico (~200 nm) e richiedono il microscopio elettronico.",
    },
    "BIO-C02-NCOM-033": {
        "errata_note": "Nota terminologica: nei quesiti ministeriali italiani con 'cellule germinali' si intendono qui i gameti maturi post-meiotici (spermatozoi e cellule uovo, aploidi n), benché in istologia la linea germinale comprenda anche i precursori pre-meiotici diploidi (spermatogoni, ovogoni, gametociti primari).",
    },
    "BIO-C02-NCOM-059": {
        "question": "L'intera serie di loci di un determinato cromosoma costituisce:",
        "options": {"A": "uno zigote"},
    },
    "BIO-C02-NCOM-060": {
        "question_replacements": [
            ("cromosoma Y°.", 'cromosoma Y".'),
            ("B. La han", "B. Lahn"),
            ("fosseroun", "fossero un"),
        ],
    },
    "BIO-C02-NCOM-072": {
        "errata_note": "Nota didattica: la chiave del testo indica E ('il centromero' nel suo complesso), ma nei manuali EdiSES il centromero è suddiviso nei domini centrale, del cinetocore e di appaiamento (opzione B), quest'ultimo specificamente deputato alla coesione tra cromatidi fratelli.",
    },
    "BIO-C02-NCOM-092": {"options": {"C": "XO"}},
    "BIO-C02-NCOM-119": {
        "errata_note": "Nota molecolare: le ripetizioni trinucleotidiche CAG nell'esone 1 del gene HTT sono propriamente un microsatellite (STR, unità ripetuta di 1–6 bp) e non un minisatellite (VNTR, unità di ~10–100 bp), come impropriamente riportato nella traccia.",
    },
    "BIO-C03-NCOM-038": {
        "question": "Che cos'è l'RNA?",
        "options": {"A": "Acido lattico"},
    },
    "BIO-C03-NCOM-071": {"options": {"A": "alide"}},
    "BIO-C03-NCOM-109": {"options": {"B": "Il codice genetico è l'informazione genetica presente sull'rRNA"}},
    "BIO-C03-NCOM-188": {"options": {"B": "U1"}},
    "BIO-C03-NCOM-215": {
        "options": {
            "A": "L'amminoacil-tRNA sintetasi",
            "B": "La peptidil transferasi",
        }
    },
    "BIO-C04-NCOM-026": {
        "options": {"A": "RR e rr", "B": "Rr e Rr", "C": "RR e RR", "D": "rr e rr", "E": "Rr e RR"}
    },
    "BIO-C04-NCOM-033": {"options": {"E": "rryy"}},
    "BIO-C04-NCOM-040": {
        "question": "Linee pure di piante di bocca di leone con fiori rossi incrociate con piante a fiori bianchi hanno dato luogo a una F₁ costituita da piante con fiori rosa. In F₂ si sono osservati fiori rossi:rosa:bianchi in un rapporto fenotipico di 1:2:1. La spiegazione più probabile è che:"
    },
    "BIO-C04-NCOM-050": {
        "errata_note": "Nota genetica: la formulazione dell'opzione C descrive a rigore la I legge di Mendel (segregazione equifrequente 50:50 dei due alleli di ciascun singolo locus), mentre l'assortimento indipendente (II legge) riguarda l'indipendenza statistica nella trasmissione simultanea di alleli appartenenti a loci distinti non associati.",
    },
    "BIO-C04-NCOM-055": {
        "options": {"A": "aa e aa", "B": "Aa e Aa", "C": "Aa e aa", "D": "AA e Aa", "E": "AA e aa"}
    },
    "BIO-C04-NCOM-075": {
        "question": "Il colore del pelo nei conigli è determinato da un solo gene che ha quattro alleli: aguti (C), cincillà (cᶜʰ), himalayano (cʰ), albino (c). Quanti diversi genotipi sono possibili per il colore del pelo nel coniglio?"
    },
    "BIO-C04-NCOM-082": {"options": {"E": "gg"}},
    "BIO-C04-NCOM-085": {
        "options": {"A": "AABB × AaBb", "B": "AaBb × aabb", "C": "Aa × Aa", "D": "Aa × BbCc", "E": "Aa × Bb"}
    },
    "BIO-C04-NCOM-088": {"question": "Quando avviene il crossing-over?"},
    "BIO-C04-NCOM-105": {
        "errata_note": "Nota citologica: 'in tutte le cellule' (E) si riferisce qui sia alle cellule somatiche sia a quelle germinali nucleate dell'organismo, fatta eccezione per gli elementi terminalmente anucleati come gli eritrociti maturi dei mammiferi.",
    },
    "BIO-C04-NCOM-158": {
        "question_replacements": [("I] riferimento", "Il riferimento"), ("AdeninaGuanina", "Adenina-Guanina")]
    },
    "BIO-C04-NCOM-160": {
        "errata_note": "Nota biomedica: sul piano molecolare l'acondroplasia umana è causata da una mutazione autosomica dominante gain-of-function nel gene del recettore FGFR3 (che inibisce l'ossificazione encondrale), e non dalla carenza di una singola proteina denominata 'condrina' come semplificato nella traccia.",
    },
    "BIO-C04-NCOM-165": {"options": {"B": "di gruppo A e B", "C": "di gruppo A, B o AB"}},
    "BIO-C04-NCOM-182": {"options": {"C": "AB, 0", "D": "A, B, 0"}},
    "BIO-C04-NCOM-184": {"options": {"D": "AB o 0", "E": "A o B"}},
    "BIO-C04-NCOM-185": {
        "options": {"A": "4 diversi genotipi"},
        "errata_note": "Nota genetica: nel sistema ABO solo gli alleli Iᴬ e Iᴮ sono tra loro codominanti, mentre l'allele i (0) è recessivo rispetto a entrambi; proprio tale recessività riduce i 6 genotipi possibili a 4 fenotipi (A, B, AB, 0).",
    },
    "BIO-C04-NCOM-187": {
        "options": {
            "B": "i cui globuli rossi non presentano antigeni A e B",
            "C": "che hanno gruppo sanguigno A o B",
        }
    },
    "BIO-C04-NCOM-211": {"options": {"B": "Y0", "D": "X0"}},
    "BIO-C05-COMP-094": {
        "errata_note": "Nota molecolare: a rigore soltanto il segnale C-terminale PTS1 è un tripeptide consenso (-SKL), mentre il segnale N-terminale PTS2 è una sequenza consenso di circa 9 amminoacidi.",
    },
    "BIO-C05-COMP-098": {
        "errata_note": "Nota molecolare: nell'importazione perossisomiale l'idrolisi di ATP (mediata dalle AAA-ATPasi Pex1/Pex6) è specificamente richiesta per l'esportazione e il riciclo del recettore Pex5 dalla membrana al citosol.",
    },
    "BIO-C05-NCOM-020": {
        "errata_note": "Nota citologica: la desmina (A, risposta indicata dal testo) costituisce i filamenti intermedi muscolari ancorati ai desmosomi cardiaci, mentre la proteina di placca che connette i filamenti intermedi alle caderine desmosomiali è propriamente la desmoplachina.",
    },
    "BIO-C05-NCOM-026": {
        "question": "Il trasporto passivo del glucosio attraverso la membrana cellulare non richiede consumo di ATP. Da dove proviene l'energia necessaria per il trasporto?"
    },
    "BIO-C05-NCOM-106": {
        "question": "In quale delle seguenti strutture cellulari si trova l'RNA? I) Nel nucleo; II) nel citoplasma; III) nei ribosomi.",
        "options": {"A": "In I), in II) e in III)", "B": "Solo in I)"},
    },
    "BIO-C05-NCOM-127": {
        "errata_note": "Nota fisiologica: nell'opzione C ('avviene in tutte le cellule') la traccia contrappone gli organismi eterotrofi/autotrofi eucariotici (entrambi dotati di respirazione cellulare, a differenza della fotosintesi limitata agli autotrofi), prescindendo da cellule specializzate prive di mitocondri (es. eritrociti maturi) o anaerobi obbligati.",
    },
    "BIO-C05-NCOM-174": {
        "options": {"E": "Ran e Rab"},
        "errata_note": "Nota molecolare: le piccole GTPasi Rab regolano specificamente il traffico vescicolare (indirizzamento e attracco delle vescicole), mentre Ran regola il trasporto nucleo-citoplasmatico non vescicolare attraverso il complesso del poro nucleare.",
    },
    "BIO-C05-NCOM-279": {"options": {"E": "O₂"}},
    "BIO-C06-COMM-016": {
        "explanation_replacements": [("integrine a,8,", "integrine α₆β₄")],
    },
    "BIO-C07-COMM-026": {
        "options": {
            "A": "G₁, S, M, T",
            "B": "G₁, S, G₂, M",
            "C": "G₁, G₂, M, C",
        }
    },
    "BIO-C06-COMP-022": {
        "errata_note": "Nota molecolare: in senso stretto solo le Ig-CAM (es. NCAM, ICAM, VCAM) appartengono alla superfamiglia delle immunoglobuline, mentre l'acronimo generale CAM include anche caderine, selectine e integrine.",
    },
    "BIO-C06-COMP-090": {
        "accepted_synonyms": ["oncogene", "proto-oncogene", "protooncogene"],
        "errata_note": "Nota terminologica: a rigore il gene cellulare normale che se mutato promuove proliferazione incontrollata è detto proto-oncogene, mentre la forma mutata iperattiva risultante è l'oncogene.",
    },
    "BIO-C06-NCOM-031": {"options": {"E": "Rb e p53"}},
    "BIO-C06-NCOM-111": {"options": {"E": "laminine"}},
    "BIO-C06-NCOM-179": {"options": {"A": "la via Jak-Stat"}},
    "BIO-C07-COMP-011": {
        "accepted_synonyms": ["Wee1", "Myt1"],
        "errata_note": "Nota biochimica: Wee1 è classificata strutturalmente tra le chinasi a doppia specificità, sebbene nei vertebrati fosforili prevalentemente Tyr15 di Cdk1 mentre la chinasi correlata Myt1 fosforila sia Thr14 sia Tyr15.",
    },
    "BIO-C07-NCOM-009": {
        "options": {
            "A": "M, G₁, G₂, S",
            "B": "G₁, M, G₂, S",
            "C": "G₁, G₂, S, M",
            "D": "G₁, S, G₂, M",
            "E": "S, M, G₁, G₂",
        }
    },
    "BIO-C07-NCOM-023": {"options": {"B": "di quando in quando in tutte le cellule del nostro organismo"}},
    "BIO-C07-NCOM-057": {"options": {"E": "i linfociti"}},
    "BIO-C07-NCOM-076": {
        "errata_note": "Nota terminologica: la replicazione del DNA avviene nella fase S dell'interfase (opzione A nella chiave del testo); il termine 'intercinesi' indica invece propriamente la breve pausa tra meiosi I e meiosi II, nella quale NON avviene duplicazione del DNA.",
    },
    "BIO-C07-NCOM-116": {"options": {"C": "un cavallo"}},
    "BIO-C07-NCOM-125": {"options": {"D": "si svolge per intero nell'ovaio a partire dalla pubertà"}},
    "BIO-C07-NCOM-151": {
        "errata_note": "Nota citologica: i complessi di coesina mantengono uniti i cromatidi fratelli lungo gli assi cromatidici e soprattutto a livello centromerico fino all'anafase (non specificamente alle sole estremità telomeriche).",
    },
    "BIO-C07-NCOM-155": {
        "options": {"D": "Protozoi e metazoi"},
    },
    "BIO-C07-NCOM-174": {"options": {"E": "p21"}},
    "BIO-C07-NCOM-182": {"options": {"A": "Fase S", "E": "G₀"}},

    # ── Chimica e Propedeutica Biochimica ──
    "CHIM-C01-COMM-002": {
        "question_replacements": [("10⁻²¹ e 10⁻²⁹", "10⁻³¹ e 10⁻²⁹")],
    },
    "CHIM-C01-NCOM-039": {"options": {"A": "Oo"}},
    "CHIM-C02-NCOM-002": {"options": {"D": "L'orbita descritta dall'elettrone attorno al nucleo"}},
    "CHIM-C02-NCOM-019": {
        "options": {
            "B": "è indipendente dal valore del numero quantico secondario (l)",
            "E": "è indipendente dal valore del numero quantico principale (n)",
        }
    },
    "CHIM-C03-COMP-023": {
        "cloze_stem": "I semiconduttori sono spesso {{c1::metalloidi}} (semimetalli) come il silicio.",
    },
    "CHIM-C03-NCOM-005": {"options": {"A": "4 g", "B": "12 g", "C": "16 g", "D": "20 g", "E": "8 g"}},
    "CHIM-C03-NCOM-038": {
        "errata_note": "Nota metrologica: nell'opzione D la massa molare dell'acqua è espressa informalmente come '18,01 g' (sottintendendo 'per mole'), mentre l'unità rigorosa della massa molare è g/mol.",
    },
    "CHIM-C03-NCOM-043": {"options": {"A": "11 g", "B": "4 g", "C": "8 g", "D": "10 g", "E": "16 g"}},
    "CHIM-C03-NCOM-052": {"options": {"A": "12 g", "D": "18 g", "E": "6 g"}},
    "CHIM-C03-NCOM-057": {
        "options": {"A": "22 g", "B": "46,5 g", "C": "44 g", "D": "110 g", "E": "15,05 · 10²³ g"}
    },
    "CHIM-C03-NCOM-060": {"options": {"B": "Ba"}},
    "CHIM-C03-NCOM-068": {"options": {"E": "S = Sodio, F = Fluoro, B = Boro"}},
    "CHIM-C03-NCOM-077": {"options": {"D": "N₂O₂", "E": "C₆H₆"}},
    "CHIM-C03-NCOM-078": {"options": {"D": "K", "E": "Al"}},
    "CHIM-C03-NCOM-079": {
        "errata_note": "Nota chimica: la chiave del testo indica E intendendo 0 come stato di ossidazione dello zolfo elementare (S₈), sebbene in senso stretto la valenza dello zolfo nei suoi composti assuma i valori 2, 4 e 6 (rendendo 0 difendibile come 'non valenza').",
    },
    "CHIM-C03-NCOM-095": {"options": {"D": "Cl"}},
    "CHIM-C03-NCOM-102": {"options": {"D": "F₂", "E": "O₂"}},
    "CHIM-C03-NCOM-150": {"options": {"B": "I", "D": "II"}},
    "CHIM-C03-NCOM-155": {"options": {"B": "Cl"}},
    "CHIM-C03-NCOM-156": {"options": {"E": "K"}},
    "CHIM-C03-NCOM-159": {"options": {"C": "Si", "D": "S"}},
    "CHIM-C03-NCOM-179": {
        "question": "Indicare gli alogeni tra i seguenti elementi: Li, Na, Ca, Mg, F, B, Cl, I, Br, U, Ti:",
        "options": {
            "A": "Ca, Mg, F, B",
            "B": "F, Cl, I, Br, U, Ti",
            "C": "F, Cl, I, Br",
            "D": "Li, Na, Ca, Mg, U, Ti",
            "E": "Li, Na, Ca, Mg, B",
        },
    },
    "CHIM-C04-NCOM-006": {"options": {"E": "Il cloruro di sodio è un composto ionico"}},
    "CHIM-C04-NCOM-008": {"options": {"C": "1 legame covalente"}},
    "CHIM-C04-NCOM-037": {"question": "La molecola dell'acido iodidrico HI:"},
    "CHIM-C04-NCOM-053": {"options": {"B": "LiI"}},
    "CHIM-C04-NCOM-054": {"options": {"C": "HCl"}},
    "CHIM-C04-NCOM-057": {
        "question": "I legami covalenti polari presenti nelle molecole d'acqua sono il risultato:",
        "options": {"A": "della differenza di elettronegatività tra l'atomo di H e quello di O"},
    },
    "CHIM-C06-NCOM-006": {"options": {"A": "2 M", "D": "2 m", "E": "5 M"}},
    "CHIM-C06-NCOM-013": {
        "question": "Quanto idrossido di potassio è presente in 25 cm³ di una soluzione di idrossido di potassio 1,5 M? [Si assuma massa atomica relativa: H = 1; O = 16; K = 39]"
    },
    "CHIM-C06-NCOM-028": {"options": {"A": "10 mL", "C": "1 L", "E": "5 L"}},
    "CHIM-C06-NCOM-031": {"options": {"A": "77,9 g", "B": "110 g", "D": "122 g", "E": "120 g"}},
    "CHIM-C06-NCOM-059": {
        "question": "A quale volume bisogna diluire 50 mL di soluzione acquosa di HCl (aq) 6 M per ottenere HCl (aq) 0,2 M?",
        "options": {"A": "1.500 mL", "E": "300 mL"},
    },
    "CHIM-C06-NCOM-063": {
        "question": "A quale volume si devono portare 10 mL di HCl 6 M perché la concentrazione finale sia 0,5 M?",
        "options": {"A": "12 mL", "B": "240 mL", "C": "60 mL", "D": "83 mL", "E": "120 mL"},
    },
    "CHIM-C07-NCOM-031": {"options": {"A": "200 g", "B": "1 kg", "C": "560 g", "D": "56 g", "E": "2 kg"}},
    "CHIM-C07-NCOM-033": {
        "question": "Quanti grammi di CO₂ si ottengono dalla combustione completa di una mole di glucosio nella reazione: glucosio + ossigeno molecolare → acqua + anidride carbonica (peso molecolare del glucosio: 180 u.m.a.)?",
        "options": {"A": "6 g", "B": "150 g", "C": "12 g", "E": "1 g"},
    },
    "CHIM-C07-COMM-016": {
        "question": "La reazione C + O₂ → CO₂ è una reazione:",
    },
    "CHIM-C07-COMM-020": {
        "explanation_replacements": [("2H, + 0, +2 H₂O", "2 H₂ + O₂ → 2 H₂O")],
    },
    "CHIM-C07-NCOM-034": {
        "question_replacements": [("K + 0₂ — K,0", "4 K + O₂ → 2 K₂O"), ("K + O₂ — K,0", "4 K + O₂ → 2 K₂O"), ("K + O₂ — K₂O", "4 K + O₂ → 2 K₂O")],
    },
    "CHIM-C07-NCOM-037": {
        "question": "Indicare la massa di anidride carbonica (PMᵣ 44) che si ottiene da 250 g di CaCO₃ (PMᵣ 100) se la reazione è: CaCO₃ → CaO + CO₂.",
        "options": {"A": "110 g", "B": "250 g", "C": "44 g", "D": "500 g", "E": "125 g"},
    },
    "CHIM-C07-NCOM-040": {"question_replacements": [("10 moti di H₂", "10 moli di H₂")]},
    "CHIM-C07-NCOM-044": {
        "question_replacements": [
            ("ZH’ + Ze\" → H⁻ Ag’ + CI — AgCl Cut — Cu?* + e- 2Cu* — Cu+Cu**", "1) 2H⁺ + 2e⁻ → H₂; 2) Ag⁺ + Cl⁻ → AgCl; 3) Cu⁺ → Cu²⁺ + e⁻; 4) 2Cu⁺ → Cu + Cu²⁺"),
            ("ZH’ + Ze⁻ → H⁻ Ag’ + CI — AgCl Cut — Cu?* + e- 2Cu* — Cu+Cu**", "1) 2H⁺ + 2e⁻ → H₂; 2) Ag⁺ + Cl⁻ → AgCl; 3) Cu⁺ → Cu²⁺ + e⁻; 4) 2Cu⁺ → Cu + Cu²⁺"),
        ]
    },
    "CHIM-C08-COMM-008": {
        "question_replacements": [("250, = 250₂+0₂", "2 SO₃ ⇌ 2 SO₂ + O₂"), ("250, = 250₂+O₂", "2 SO₃ ⇌ 2 SO₂ + O₂")],
        "explanation_replacements": [("2 SO, = 2 SO, + 0,", "2 SO₃ ⇌ 2 SO₂ + O₂")],
    },
    "CHIM-C09-COMM-003": {
        "explanation_replacements": [("Mn²⁺ + 2 e° -Mn", "Mn²⁺ + 2 e⁻ → Mn")],
    },
    "CHIM-C09-COMM-004": {
        "explanation_replacements": [("Zn + FeCl. —ZnCl₂ + Fe", "Zn + FeCl₂ → ZnCl₂ + Fe")],
    },
    "CHIM-C10-COMM-029": {
        "explanation_replacements": [("CO₂ + H₂O = H,CO₂", "CO₂ + H₂O ⇌ H₂CO₃")],
    },
    "CHIM-C11-COMM-033": {
        "options": {
            "A": "Una soluzione 1 M di CH₃COOH e 1 M di HCl",
            "B": "Una soluzione 1 M di NaOH e 1 M di HCl",
            "D": "Una soluzione 1 M di NaOH e 1 M di CH₃COONa",
            "E": "Una soluzione 1 M di CH₃COONa e 1 M di NH₄Cl",
        },
        "explanation_replacements": [("Solo la risposta e può fungere da tampone", "Solo la risposta C può fungere da tampone")],
    },
    "CHIM-C12-COMM-033": {
        "explanation_replacements": [("R-O-R’‘ 0 R,0,", "R-O-R' o R₂O,")],
    },
    "CHIM-C12-COMM-034": {
        "question": "Il composto CH₃-CH₂-NH-CH₂-CH₃ è:",
    },
    "CHIM-C12-NCOM-177": {
        "options": {"B": "CH₃CHO", "D": "CH₃OCH₃", "E": "H₃COCH₃"},
    },
    "CHIM-C08-NCOM-004": {
        "options": {
            "B": "aumenta o diminuisce a seconda che la reazione sia endotermica o esotermica",
            "D": "diminuisce a pressioni inferiori a 1 atm, aumenta per pressioni superiori",
        }
    },
    "CHIM-C08-NCOM-007": {"options": {"E": "III ordine"}},
    "CHIM-C08-NCOM-013": {"options": {"C": "è sempre moli/litri"}},
    "CHIM-C09-COMP-028": {
        "errata_note": "Nota elettrochimica: in una reazione redox completa la spontaneità in condizioni standard dipende dal segno positivo della forza elettromotrice standard della cella ΔE° = E°(catodo) − E°(anodo) > 0 (poiché ΔG° = −nFΔE° < 0).",
    },
    "CHIM-C09-COMP-029": {
        "cloze_stem": "Se il potenziale di riduzione standard è {{c1::negativo}}, la reazione redox non è spontanea.",
        "errata_note": "Nota elettrochimica: la non spontaneità in condizioni standard si riferisce propriamente a una differenza di potenziale standard di cella ΔE° = E°(catodo) − E°(anodo) < 0 (ossia ΔG° > 0).",
    },
    "CHIM-C09-NCOM-007": {"options": {"E": "-6"}},
    "CHIM-C09-NCOM-020": {"options": {"E": "-5"}},
    "CHIM-C09-NCOM-041": {"options": {"B": "-6", "E": "-2"}},
    "CHIM-C09-NCOM-060": {
        "question_replacements": [("2 HBr +1₂ — 2 Hi + Br,,", "2 HBr + I₂ → 2 HI + Br₂,")]
    },
    "CHIM-C09-NCOM-090": {"question": "Nella semireazione K⁺ + e⁻ → K, il potassio:"},
    "CHIM-C09-NCOM-110": {
        "explanation": "La reazione di ossido-riduzione bilanciata è la seguente: Cu + 2 HClO₄ → Cu(ClO₄)₂ + H₂. La specie riducente è quella che riduce l'altra specie e che, quindi, si ossida: il rame passa dallo stato di ossidazione 0 nel rame metallico a +2 in Cu(ClO₄)₂, mentre l'idrogeno passa da +1 in HClO₄ a 0 in H₂. La specie riducente è pertanto il rame metallico."
    },
    "CHIM-C09-NCOM-112": {
        "errata_note": "Nota stechiometrica: la traccia parla di 'una molecola' di metano mentre le opzioni esprimono i prodotti in 'moli' (1 mole di CH₄ + 2 moli di O₂ → 1 mole di CO₂ + 2 moli di H₂O; per una singola molecola si formano 1 molecola di CO₂ e 2 molecole di H₂O).",
    },
    "CHIM-C09-NCOM-129": {
        "question": "Un metallo M sposta il Rame (Cu) da una soluzione acquosa di rame(II) solfato riducendolo allo stato di rame elementare, ma non sposta lo Zinco (Zn) da una soluzione acquosa di zinco(II) solfato. Come devono essere ordinati i tre metalli per rispettare l'ordine di capacità riducente crescente?"
    },
    "CHIM-C10-NCOM-010": {
        "question": "L'anidride solforosa corrisponde alla formula:",
        "options": {"A": "H₂SO₃", "B": "H₂S", "D": "SO₃"},
    },
    "CHIM-C10-NCOM-015": {
        "question": "L'anidride fosforosa corrisponde alla formula:",
        "options": {"D": "P₂O₂"},
    },
    "CHIM-C10-NCOM-020": {"options": {"C": "un acido biprotico"}},
    "CHIM-C10-NCOM-039": {"options": {"C": "ossido mercurico", "D": "la formula Hg₂O non esiste"}},
    "CHIM-C10-NCOM-070": {"question": "Il composto FeCl₂ è:"},
    "CHIM-C10-NCOM-071": {"options": {"B": "IS²⁺"}},
    "CHIM-C10-NCOM-075": {"options": {"C": "I₂Cu₂"}},
    "CHIM-C11-NCOM-057": {
        "options": {
            "A": "la concentrazione di H⁺ aumenta",
            "C": "la concentrazione di H⁺ diminuisce",
            "E": "la concentrazione di OH⁻ aumenta",
        },
        "errata_note": "Nota chimica: aggiungendo un acido ad acqua pura aumenta [H⁺] (opzione A) e conseguentemente il pH si abbassa (opzione D, indicata come risposta corretta dal testo).",
    },
    "CHIM-C11-NCOM-075": {"options": {"D": "0,000001 e 0,0000001"}},
    "CHIM-C11-NCOM-142": {
        "options": {"C": "è sempre superiore a 1", "D": "è inferiore a quello della soluzione B"}
    },
    "CHIM-C11-NCOM-158": {"options": {"E": "basica se il sale è un elettrolita anfotero"}},
    "CHIM-C12-COMM-013": {
        "explanation": "La reazione di ossidazione (combustione) del metano è: CH₄ + 2 O₂ → CO₂ + 2 H₂O. Le moli di CO₂ prodotte sono numericamente uguali alle moli di metano che hanno subito la combustione."
    },
    "CHIM-C12-NCOM-005": {"options": {"B": "presentano la stessa formula grezza o molecolare"}},
    "CHIM-C12-NCOM-010": {
        "options": {
            "A": "nelle quali sullo stesso scheletro molecolare i gruppi o sostituenti identici occupano posizioni diverse"
        },
        "errata_note": "Nota chimica: la definizione riportata nell'opzione A descrive specificamente l'isomeria di posizione; in senso generale gli isomeri sono composti con identica formula molecolare ma diversa concatenazione degli atomi (isomeri costituzionali) o diversa disposizione spaziale (stereoisomeri).",
    },
    "CHIM-C12-NCOM-041": {"options": {"A": "CH₃-CH₂-CH₃", "C": "CH₃-CHO"}},
    "CHIM-C12-NCOM-048": {"question": "Gli alcani sono solubili in H₂O?"},
    "CHIM-C12-NCOM-147": {"options": {"B": "un doppio legame C-O"}},
    "CHIM-C12-NCOM-175": {"options": {"A": "Il gruppo carbonilico"}},
    "CHIM-C12-NCOM-190": {"question": "La formula generale R-O-R' è caratteristica:"},
    "CHIM-C12-NCOM-196": {"options": {"A": "CH₃-CH₂-OH", "B": "H₂C=O"}},
    "CHIM-C12-NCOM-198": {"options": {"C": "R-O-R'"}},
    "CHIM-C12-NCOM-202": {"options": {"E": "CH₃-CH₂-NH-CH₃"}},
    "CHIM-C12-NCOM-209": {
        "options": {
            "B": "Dipende da quanti atomi di azoto l'alcool contiene",
            "C": "Un alchino",
        },
        "errata_note": "Nota di chimica organica: l'esito dell'ossidazione di un alcol dipende dal numero di atomi di idrogeno legati specificamente al carbonio carbinolico (C-OH): gli alcoli primari (2 H in α) danno aldeidi e poi acidi carbossilici, i secondari (1 H in α) danno chetoni, mentre i terziari (0 H in α) resistono all'ossidazione blanda.",
    },
    "CHIM-C12-NCOM-218": {"options": {"A": "CH₃-CO-H"}},
    "CHIM-C12-NCOM-224": {"options": {"B": "CH₃-CH₂-NH"}},
    "CHIM-C12-NCOM-241": {"options": {"C": "ArH"}},
    "CHIM-C12-NCOM-244": {"options": {"B": "CH₃-NO₂"}},
    "CHIM-C12-NCOM-307": {"options": {"B": "R-COOR'", "E": "R-COOH"}},
    "CHIM-C13-NCOM-059": {"options": {"C": "viene ceduta una molecola di H₂", "E": "viene ceduta una molecola di O₂"}},
    "CHIM-C13-NCOM-067": {"options": {"A": "L'albumina", "B": "L'acido pantotenico"}},
    "CHIM-C13-NCOM-075": {
        "question": "Indicare fra i seguenti composti quello che presenta il maggior numero di gruppi ossidrilici:",
        "options": {"C": "pentanolo"},
    },
    "CHIM-C13-NCOM-120": {"options": {"B": "sostanza contenente i gruppi carbossilico ed amminico"}},
    "CHIM-C13-NCOM-159": {"options": {"A": "1 atomo di carbonio"}},
    "CHIM-C13-NCOM-170": {"options": {"D": "Zolfo"}},
    "CHIM-C13-NCOM-176": {
        "question": "Quale tra le seguenti è la formula di un composto avente formula minima CH₂O e peso molecolare 180?",
        "options": {"B": "C₂H₄O₂"},
    },

    # ── Fisica ──
    "FIS-C01-COMP-019": {"cloze_stem": "La lunghezza di un anno luce è circa 9,46 × 10<sup>{{c1::15}}</sup> metri."},
    "FIS-C01-COMP-020": {"cloze_stem": "La distanza dalla Terra alla Luna è circa 3,84 × 10<sup>{{c1::8}}</sup> metri."},
    "FIS-C01-COMP-026": {"cloze_stem": "La lunghezza di un campo di calcio è circa 9,1 × 10<sup>{{c1::1}}</sup> metri."},
    "FIS-C01-COMP-029": {"cloze_stem": "La distanza media Terra-Sole è circa 1,50 × 10<sup>{{c1::11}}</sup> metri."},
    "FIS-C01-NCOM-028": {"options": {"A": "35 kg·m", "B": "1025 kg·cm", "D": "35 kg·cm"}},
    "FIS-C01-NCOM-033": {"options": {"A": "C·s"}},
    "FIS-C01-NCOM-037": {"options": {"B": "newton · metro", "C": "newton · secondo"}},
    "FIS-C01-NCOM-040": {"options": {"E": "watt · sec"}},
    "FIS-C01-NCOM-059": {"options": {"E": "1 grammo"}},
    "FIS-C01-NCOM-064": {"options": {"A": "144 m", "C": "1.852 m", "D": "0,9144 m", "E": "0,3048 m"}},
    "FIS-C01-NCOM-070": {"options": {"B": "10¹⁰", "C": "10⁶", "E": "100"}},
    "FIS-C01-NCOM-080": {"question": "La misura di una massa è risultata essere 20 ± 0,5 mg. Quant'è l'errore relativo?"},
    "FIS-C01-NCOM-093": {
        "question": "Il prodotto scalare tra due vettori è positivo quando l'angolo α che essi formano tra loro è:"
    },
    "FIS-C02-COMP-016": {
        "errata_note": "Nota cinematica: rigorosamente il modulo della velocità istantanea |v| è una grandezza non negativa (|v| ≥ 0), annullandosi negli istanti di quiete o di inversione del moto.",
    },
    "FIS-C02-COMP-057": {
        "cloze_stem": "La velocità istantanea si ottiene come limite della velocità media quando Δt tende a {{c1::zero}}."
    },
    "FIS-C02-COMM-003": {
        "explanation_replacements": [("quota di partenza A secondo la relazione: p= [2h VV g", "quota di partenza h secondo la relazione: t = √(2h/g).")],
    },
    "FIS-C02-COMM-010": {
        "question": "Due sfere S₁ ed S₂ hanno lo stesso diametro e densità rispettivamente di 8 g/cm³ e 16 g/cm³. Cadendo simultaneamente nel vuoto:",
        "options": {
            "A": "la sfera S₂ arriva per prima al suolo",
            "C": "la sfera S₁ arriva per prima al suolo",
            "D": "la sfera S₁ arriva al suolo con un tempo doppio rispetto a quello impiegato da S₂",
        },
        "explanation_replacements": [("r= [2h 8 Quindi", "t = √(2h/g). Quindi")],
    },
    "FIS-C02-NCOM-019": {"options": {"C": "11,0 m/s"}},
    "FIS-C02-NCOM-039": {"options": {"A": "No, i dati non sono sufficienti"}},
    "FIS-C02-NCOM-051": {"options": {"B": "4 · 10⁻²"}},
    "FIS-C03-COMM-015": {
        "question": "Considerate due masse isolate M₁ = m e M₂ = 2m, se F è il modulo della forza gravitazionale agente sulla massa M₁, qual è il modulo della forza gravitazionale agente sulla massa M₂?",
    },
    "FIS-C03-COMM-018": {
        "question": "Sia data una forza costante e di modulo F₁ ≠ 0. Sia inoltre dato un punto A₁ giacente sulla retta di azione di F₁. Il punto A₁ disti L₁ (con L₁ ≠ 0) dal punto di applicazione di F₁. Analogamente, sia data una seconda forza costante, di modulo F₂ ≠ 0, ed un punto A₂ giacente sulla retta di azione di F₂. Sia L₂ ≠ 0 la distanza di A₂ dal punto di applicazione di F₂. Che relazione c'è tra il momento M₁ di F₁ rispetto ad A₁ e il momento M₂ di F₂ rispetto ad A₂?",
        "options": {"C": "M₁ > M₂ se F₁ > F₂ e contemporaneamente L₁ > L₂"},
    },
    "FIS-C03-COMM-028": {
        "options": {"B": "Sì, se il corpo passa dalla velocità V₁ ad una velocità V₂, con V₂ < V₁"},
        "explanation_replacements": [("velocità V, ad una velocità V, inferiore a V,.", "velocità V₁ ad una velocità V₂ inferiore a V₁.")],
    },
    "FIS-C03-COMM-048": {
        "explanation_replacements": [
            ("forze F, che agisce sul corpo è pari a: mm Fx =m'a=2kg-0,57=1N", "forze F_R che agisce sul corpo è pari a: F_R = m · a = 2 kg · 0,5 m/s² = 1 N."),
            ("forza di attrito F, che", "forza di attrito F_a, che"),
            ("F, =F - F,.", "F_R = F - F_a."),
        ],
    },
    "FIS-C04-COMM-002": {
        "explanation_replacements": [
            ("si ha P, = P,.", "si ha P₁ = P₂."),
            ("Quindi: P.>P,=P.,.", "Quindi: P₃ > P₁ = P₂."),
        ],
    },
    "FIS-C04-NCOM-035": {
        "options": {"B": "P = dgh/A, dove A è l'area della sezione della colonna"},
    },
    "FIS-C06-COMM-013": {
        "question": "In un circuito elettrico vi sono una pila da 10 Volt e due resistenze in serie R₁ e R₂. Se la potenza totale è 50 watt e R₂ = 3·R₁, quanto vale R₁ in ohm?",
    },
    "FIS-C02-NCOM-074": {
        "errata_note": "Nota geometrica: in geometria differenziale la curva descritta dal punto nello spazio è propriamente un'elica cilindrica (mentre l'elicoide è una superficie rigata bidimensionale), terminologia spesso confusa nei quesiti tradizionali.",
    },
    "FIS-C03-COMP-035": {
        "cloze_stem": "La relazione che lega la forza di attrito statico massimo alla forza normale è f_s,max = {{c1::μs (mu)}} N.",
        "accepted_synonyms": ["μs", "μ_s", "mu_s", "mu s", "μs (mu)"],
    },
    "FIS-C03-COMP-099": {
        "errata_note": "Nota di meccanica: il lavoro dell'attrito dinamico è sempre negativo rispetto allo spostamento relativo tra le due superfici a contatto (dissipando energia meccanica complessiva), sebbene in un dato riferimento inerziale l'attrito dinamico possa compiere lavoro positivo su un corpo che viene trascinato e accelerato da una superficie in moto (es. nastro trasportatore).",
    },
    "FIS-C03-COMP-100": {
        "errata_note": "Nota di fisica: l'affermazione vale esclusivamente in presenza di sole forze dissipative (senza variazione di energia potenziale); sotto l'azione di forze conservative (es. lancio verticale verso l'alto) la diminuzione di energia cinetica si converte in aumento di energia potenziale.",
    },
    "FIS-C03-COMP-138": {"accepted_synonyms": ["movimento", "moto"]},
    "FIS-C03-COMP-142": {
        "errata_note": "Nota di fisica moderna: la relazione p = mv = 0 per m = 0 vale esclusivamente nella meccanica classica newtoniana; in relatività ristretta e fisica quantistica le particelle prive di massa a riposo (come i fotoni) viaggiano a velocità c e possiedono quantità di moto non nulla p = E/c = h/λ.",
    },
    "FIS-C03-NCOM-002": {"options": {"A": "F · cotg 30°", "B": "F · tg 30°", "E": "F · sen 30°"}},
    "FIS-C03-NCOM-010": {"question": "Quando cessa istantaneamente l'azione di qualunque forza su un corpo di massa m:"},
    "FIS-C03-NCOM-038": {
        "question": "Supponiamo di avere una bilancia di precisione posizionata su di un ascensore in movimento. Se misuriamo il peso di un corpo di massa M, esso sarà:",
        "errata_note": "Nota di dinamica: il peso apparente M(g + a_y) supera Mg ogniqualvolta il vettore accelerazione dell'ascensore è diretto verso l'alto (a_y > 0), condizione che si verifica sia quando l'ascensore sale accelerando (opzione E) sia quando scende decelerando (frenando).",
    },
    "FIS-C03-NCOM-050": {
        "question": "Sapendo che l'accelerazione di gravità vale 9,8 m/s², qual è il peso di un corpo di massa 10 kg?",
        "options": {"A": "9,8 N", "D": "10/9,8 N", "E": "0,98 N"},
    },
    "FIS-C03-NCOM-051": {"options": {"A": "4,9 N", "B": "49 N", "C": "98 N", "E": "50 N"}},
    "FIS-C03-NCOM-058": {
        "question": "Nel S.I., l'unità di misura della costante elastica della molla è:",
        "options": {"A": "N·s", "E": "N·m"},
    },
    "FIS-C03-NCOM-069": {"options": {"E": "5 anni"}},
    "FIS-C03-NCOM-074": {
        "question": "Quale fra le seguenti è la formula dimensionale della costante di gravitazione G che appare nella formula F = G · M₁M₂/R²?"
    },
    "FIS-C03-NCOM-078": {"options": {"A": "2¹/² s", "B": "4 s", "C": "3 s", "E": "2 s"}},
    "FIS-C03-NCOM-083": {
        "options": {
            "A": "massa · densità = accelerazione",
            "C": "massa · velocità = forza",
            "D": "potenza · velocità = forza",
            "E": "massa · spostamento = forza",
        }
    },
    "FIS-C03-NCOM-085": {
        "options": {
            "A": "F·d",
            "C": "non può essere determinato perché dipende dall'angolo tra F e d",
        }
    },
    "FIS-C03-NCOM-090": {
        "errata_note": "Nota sul testo originale: nel volume a stampa non è presente alcun disegno accanto al quesito; l'angolo di 60° indicato è l'angolo compreso tra i vettori forza e spostamento, per cui L = F · s · cos 60° = 4 N × 2 m × 0,5 = 4 J.",
    },
    "FIS-C03-NCOM-091": {"options": {"A": "m·h", "B": "m·g·L", "C": "m·L", "E": "m·g·h"}},
    "FIS-C03-NCOM-092": {"options": {"D": "9,8 J", "E": "0 J"}},
    "FIS-C03-NCOM-093": {
        "question": "Calcolare il lavoro necessario per far muovere di un tratto s = 1 km un carrello su una rotaia rettilinea priva di attrito, utilizzando una forza F = 100 N che forma un angolo α = 30° rispetto alla direzione del moto.",
        "options": {"A": "46 kJ", "D": "87 kJ", "E": "56 kJ"},
    },
    "FIS-C03-NCOM-103": {"options": {"A": "(110/140)²", "E": "(140/110)¹/²"}},
    "FIS-C03-NCOM-113": {
        "options": {
            "C": "L'energia cinetica di un corpo si può misurare in watt · secondi",
            "D": "L'energia cinetica di un corpo si può misurare in kcal · N",
            "E": "L'energia cinetica di un corpo si può misurare in calorie · secondi",
        }
    },
    "FIS-C03-NCOM-114": {"options": {"C": "La potenza si può misurare in N · m/s"}},
    "FIS-C03-NCOM-118": {"options": {"A": "1,5 N", "B": "1 N·m", "C": "1 N/s", "D": "1 J/s", "E": "1 kg/s"}},
    "FIS-C03-NCOM-136": {"options": {"A": "980 kg·m/s"}},
    "FIS-C03-NCOM-140": {
        "explanation": "Trascurando gli attriti, i due corpi sono soggetti alla sola forza peso (conservativa) e vale la conservazione dell'energia meccanica: U_in + K_in = U_fin + K_fin. Partendo entrambi da fermi (K_in = 0) dalla stessa altezza H (U_in = m·g·H) e giungendo al suolo (U_fin = 0, K_fin = ½ m·v²), si ottiene m·g·H = ½ m·v², da cui v = √(2gH), indipendente sia dalla massa sia dall'inclinazione del piano: i due corpi arrivano quindi al suolo con la stessa velocità."
    },
    "FIS-C03-NCOM-148": {
        "options": {
            "B": "newton · metri",
            "C": "chilogrammi · metri · secondi",
            "D": "newton · secondi",
            "E": "metri · secondi",
        }
    },
    "FIS-C03-NCOM-170": {"options": {"C": "si misura in N·s"}},
    "FIS-C03-NCOM-177": {
        "question": "In una bilancia a bracci diseguali, un corpo di massa M₁ = 1,048 kg posto sul braccio di lunghezza L₁ viene equilibrato da una massa M₂ = 995 g posta sull'altro braccio di lunghezza L₂. Il rapporto tra le lunghezze dei bracci, L₁/L₂, è:"
    },
    "FIS-C04-COMP-016": {
        "cloze_stem": "Il flusso in cui non vi è mescolamento trasversale (né vortici) tra strati adiacenti di fluido è detto flusso {{c1::laminare}}.",
        "errata_note": "Nota di fluidodinamica: nel regime laminare gli strati adiacenti scorrono ordinatamente gli uni sugli altri con velocità generalmente diverse (moto relativo di scorrimento, dv/dy ≠ 0, es. profilo parabolico di Poiseuille), senza rimescolamento trasversale.",
    },
    "FIS-C04-NCOM-003": {"options": {"A": "5 g/cm³"}},
    "FIS-C04-NCOM-028": {"question": "Il prodotto litri · atmosfere equivale fisicamente a:"},
    "FIS-C04-NCOM-036": {"options": {"B": "Pa - d·g·h", "C": "d·g·h", "E": "Pa + d·g·h"}},
    "FIS-C04-NCOM-051": {
        "question": "Se immergiamo in acqua (densità = 1 g/cm³) due sfere S₁ ed S₂ che hanno rispettivamente densità di 0,8 g/cm³ e 1,6 g/cm³:",
        "options": {
            "A": "la sfera S₂ galleggia, la sfera S₁ affonda",
            "C": "la sfera S₁ galleggia, la sfera S₂ affonda",
        },
    },
    "FIS-C04-NCOM-066": {
        "options": {
            "C": "Non dipendendo da forze gravitazionali, la spinta di Archimede è presente (con la stessa intensità che assume sulla Terra) in qualunque punto dello spazio e quindi anche sulla superficie della Luna"
        }
    },
    "FIS-C04-NCOM-084": {"options": {"E": "si misura in litri · minuti"}},
    "FIS-C04-NCOM-085": {
        "options": {
            "A": "Data la posizione relativa, la differenza di pressione idrostatica tra gli organi coinvolti nella circolazione polmonare è minore dell'analoga differenza di pressione nella circolazione sistemica",
            "E": "Il volume del sangue immesso nella circolazione polmonare ogni secondo è assai minore di quello immesso nella circolazione sistemica",
        }
    },
    "FIS-C05-NCOM-013": {
        "options": {
            "A": "36,8 cal·g/°C",
            "B": "0,092 cal/(g·°C)",
            "C": "92 kcal·g/°C",
            "D": "9 kcal·g/°C",
            "E": "0,23 cal/(g·°C)",
        }
    },
    "FIS-C05-NCOM-018": {
        "question": "Un metro cubo di un certo metallo (densità relativa = 7; calore specifico = 1/6 kcal/(kg · °C)) ha capacità termica (in kcal/°C) pari a:",
        "errata_note": "Nota dimensionale: la capacità termica C = m · c ha dimensioni di energia fratto temperatura (kcal/°C, qui C = 7000 kg × 1/6 kcal/(kg·°C) = 7000/6 kcal/°C, da cui la risposta E perché nessuna delle frazioni proposte coincide con 7000/6).",
    },
    "FIS-C05-NCOM-021": {
        "question": "Il calore specifico dell'acqua è 1 kcal/(kg · °C); pertanto la quantità di calore necessaria per aumentare di 10 °C la temperatura di 10 kg di acqua è uguale a:",
        "options": {"A": "1 kcal", "C": "1 cal"},
    },
    "FIS-C05-NCOM-062": {
        "question": "Se due corpi, uno di massa M e velocità V₁ ed uno di massa M/4 e velocità V₂ = 2 V₁, si arrestano per attrito:"
    },
    "FIS-C05-NCOM-069": {"options": {"C": "V·T = costante", "E": "V = R·T"}},
    "FIS-C05-NCOM-082": {"options": {"C": "P_f = 3 P₀"}},
    "FIS-C05-NCOM-099": {"options": {"B": "245 cm³"}},
    "FIS-C05-NCOM-103": {"options": {"C": "Sì, e il lavoro compiuto dal gas sarà positivo"}},
    "FIS-C05-NCOM-126": {"options": {"C": "50 J", "D": "10 J"}},
    "FIS-C06-NCOM-016": {"options": {"E": "volt·m; N/m"}},
    "FIS-C06-NCOM-019": {"options": {"A": "0 mC", "B": "1 mC", "E": "10 mC"}},
    "FIS-C06-NCOM-021": {"options": {"A": "N·m", "B": "N·sec", "E": "volt·m"}},
    "FIS-C06-NCOM-022": {"options": {"C": "F = q²E", "D": "F = qE²"}},
    "FIS-C06-NCOM-034": {"options": {"C": "volt·m"}},
    "FIS-C06-NCOM-044": {"options": {"E": "forma con la normale ad S un angolo acuto"}},
    "FIS-C06-NCOM-057": {"options": {"A": "a 1", "B": "a zero", "C": "a infinito"}},
    "FIS-C06-NCOM-065": {"options": {"B": "15 μm"}},
    "FIS-C06-NCOM-075": {"options": {"C": "1 coulomb · 1 secondo", "E": "1 coulomb · 1 farad"}},
    "FIS-C06-NCOM-125": {"options": {"D": "1 volt"}},
    "FIS-C06-NCOM-149": {
        "question": "Tre resistenze in serie R₁, R₂, R₃ equivalgono ad un'unica resistenza R pari a:"
    },
    "FIS-C07-NCOM-014": {
        "options": {"A": "è reale e più piccola rispetto all'oggetto"},
        "errata_note": "Nota ottica: nella traccia 'l'asse ottico della lente' è un refuso del libro per 'il centro ottico della lente' (distanza oggetto 0 < p < f, che in una lente convergente produce un'immagine virtuale, diritta e ingrandita, opzione B).",
    },
    "FIS-C07-NCOM-018": {
        "options": {"A": "500 - 100 = 400 metri", "E": "500 · 100 = 50.000 metri"}
    },
    "FIS-C07-NCOM-048": {
        "errata_note": "Nota di ottica ondulatoria: con passo reticolare d = 4a si ha λL/a = 4 × 8 mm = 32 mm. Nell'approssimazione scolastica dei massimi secondari di singola fenditura a metà tra i minimi (sin θ ≈ (3/2)λ/a) la distanza vale 1,5 × 32 mm = 48 mm (opzione D, indicata dalla chiave); il massimo esatto di I(β) = I₀(sin β/β)² cade invece a tan β = β, ossia β ≈ 1,4303π → y ≈ 45,8 mm.",
    },
}
