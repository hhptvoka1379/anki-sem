#!/usr/bin/env python3
"""Deterministic MUR 2026 21-tag classifier, 563-item OCR/errata cleaner, and Cloze synonym builder."""
from __future__ import annotations

import re

ALL_21_UD_TAGS = [
    "ud::chim-struttura-atomo",
    "ud::chim-soluzioni",
    "ud::chim-cinetica-equilibrio",
    "ud::chim-acidi-basi-redox",
    "ud::chim-idrocarburi",
    "ud::chim-gruppi-funzionali",
    "ud::chim-biomolecole",
    "ud::bio-organizzazione-vita",
    "ud::bio-genoma-epigenetica",
    "ud::bio-flusso-informazione",
    "ud::bio-genetica-mutazioni",
    "ud::bio-strutture-cellulari",
    "ud::bio-segnalazione",
    "ud::bio-ciclo-cellulare",
    "ud::fis-metodi",
    "ud::fis-meccanica",
    "ud::fis-fluidi",
    "ud::fis-onde",
    "ud::fis-termodinamica",
    "ud::fis-elettromagnetismo",
    "ud::fis-radiazioni",
]

# Functional-group patterns for CHIM-C12 -> ud::chim-gruppi-funzionali (MUR Chimica UD 6)
_CHIM12_UD6_RE = re.compile(
    r"\b("
    r"alcol[ioe]?|alcool\w*|metanolo|etanolo|propanolo|butanolo|glicerolo|glicole|"
    r"fenol[io]|idrochinone|catecolo|resorcina|"
    r"eter[ei]|epossid[ioe]|ossiran\w*|tetraidrofurano|diossano|"
    r"tiol[io]|mercaptan\w*|tioeter[ei]|solfur\w+|disolfur\w+|"
    r"aldeid[ei]|formaldeide|acetaldeide|metanale|etanale|propanale|benzaldeide|"
    r"cheton[ei]|acetone|propanone|butanone|cicloesanone|carbonil\w*|"
    r"emiacetal\w*|emichetal\w*|acetal[ei]|chetal[ei]|immin[ae]|enammin\w*|base di schiff|"
    r"aldol\w*|tautomer\w* cheto-enol\w*|chinon\w*|ubichinon\w*|"
    r"acid[oi] carbossilic\w*|carbossil\w*|formico|acetico|propionico|butirrico|benzoico|"
    r"ossalico|malonico|succinico|fumarico|maleico|citrico|lattico|piruvico|salicilico|"
    r"metanoico|etanoico|propanoico|butanoico|pentanoico|esanoico|"
    r"ester[ei]|esterificazion\w*|fischer|claisen|tioester\w*|acetil-coa|"
    r"latton[ei]|lattam[ei]|anidrid[ei]|alogenur\w* acilic\w*|clorur\w* acilic\w*|acil\s*fosfat\w*|"
    r"ammin[ae]|anilina|metilammina|etilammina|trimetilammina|sali di ammonio quaternari|"
    r"ammid[ei]|urea|decarbossilazion\w*|saponificazion\w*|idrolisi alcalina|"
    r"-oh\b|-cho\b|-cooh\b|-nh2\b|-nh₂\b|-sh\b|r-co-cl|grupp[oi] funzional[ei]"
    r")\b",
    re.I,
)

# Mechanical-waves & harmonic-oscillator patterns for FIS-C07 / FIS-C03 -> ud::fis-onde (MUR Fisica UD 4)
_FIS_ONDE_C03_RE = re.compile(
    r"\b(moto armonico|oscillator\w* armonic\w*|pendolo semplice|pulsazione\s*ω|legge oraria.*cos\(ωt|costante di fase)\b",
    re.I,
)
_FIS_RADIAZIONI_C07_RE = re.compile(
    r"\b("
    r"luce|ottic\w*|rifrazion\w*|snell|indice di rifrazione|angolo limite|riflessione interna totale|"
    r"specchi\w*|lent[ei]|fuoco|distanza focale|diottr\w*|ingrandimento|prisma|"
    r"elettromagnetic\w*|fotone|fotoni|laser|polarizzat\w*|malus|"
    r"raggi\s*(x|gamma|ultravioletti|infrarossi)|ultraviolett\w*|infraross\w*|microonde|onde radio|"
    r"spettro visibile|colori|arcobaleno|fenditur\w*|young|fraunhofer"
    r")\b",
    re.I,
)
_FIS_ONDE_C07_RE = re.compile(
    r"\b("
    r"onda meccanica|onde meccaniche|suono|sonor\w*|acustic\w*|decibel|db\b|doppler|"
    r"corda vibrante|corda tesa|onda stazionaria|onde stazionarie|nodi|ventri|"
    r"onda longitudinale|onde longitudinali|onda trasversale|onde trasversali|"
    r"battimenti|infrasuoni|ultrasuoni|timbro|altezza del suono"
    r")\b",
    re.I,
)

_CHIM01_SOLUZIONI_RE = re.compile(
    r"\b(miscel\w+|miscugli\w+|soluzion\w+|colloid\w+|sospension\w+|emulsion\w+|fase dispersa|distillazione|filtrazione|cromatografia|decantazione|centrifugazione)\b",
    re.I,
)


def classify_ud_tag(record: dict, full_text: str) -> str:
    """Return exact MUR 2026 ud:: tag (one of ALL_21_UD_TAGS) for any of the 7,078 items."""
    subj = record["subject_code"]
    cnum = int(record["chapter_num"])

    # Honor opus_chim01 per-item UD triage when present
    opus_c01 = (record.get("solved_work") or {}).get("opus_chim01") or {}
    if opus_c01.get("ud") in ALL_21_UD_TAGS:
        return opus_c01["ud"]

    if subj == "BIO":
        return {
            1: "ud::bio-organizzazione-vita",
            2: "ud::bio-genoma-epigenetica",
            3: "ud::bio-flusso-informazione",
            4: "ud::bio-genetica-mutazioni",
            5: "ud::bio-strutture-cellulari",
            6: "ud::bio-segnalazione",
            7: "ud::bio-ciclo-cellulare",
        }[cnum]

    if subj == "CHIM":
        if cnum == 1:
            if _CHIM01_SOLUZIONI_RE.search(full_text):
                return "ud::chim-soluzioni"
            return "ud::chim-struttura-atomo"
        if cnum in (2, 3, 4, 5, 7):
            return "ud::chim-struttura-atomo"
        if cnum == 6:
            return "ud::chim-soluzioni"
        if cnum in (8, 9):
            return "ud::chim-cinetica-equilibrio"
        if cnum in (10, 11):
            return "ud::chim-acidi-basi-redox"
        if cnum == 12:
            if _CHIM12_UD6_RE.search(full_text):
                return "ud::chim-gruppi-funzionali"
            return "ud::chim-idrocarburi"
        if cnum == 13:
            return "ud::chim-biomolecole"

    if subj == "FIS":
        if cnum == 1:
            return "ud::fis-metodi"
        if cnum == 2:
            return "ud::fis-meccanica"
        if cnum == 3:
            if _FIS_ONDE_C03_RE.search(full_text):
                return "ud::fis-onde"
            return "ud::fis-meccanica"
        if cnum == 4:
            return "ud::fis-fluidi"
        if cnum == 5:
            return "ud::fis-termodinamica"
        if cnum == 6:
            return "ud::fis-elettromagnetismo"
        if cnum == 7:
            if _FIS_ONDE_C07_RE.search(full_text) and not _FIS_RADIAZIONI_C07_RE.search(full_text):
                return "ud::fis-onde"
            if _FIS_RADIAZIONI_C07_RE.search(full_text):
                return "ud::fis-radiazioni"
            # General wave kinematics (wavelength, period, frequency, phase) without EM/optics -> ud::fis-onde
            return "ud::fis-onde"
        if cnum == 8:
            return "ud::fis-radiazioni"

    raise ValueError(f"Unhandled subject/chapter: {subj}-C{cnum:02d}")


# Surgical safe OCR replacements applied across stems/options/banners
_SAFE_SUBS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"\bSolole(\d)\b"), r"Solo 1 e \1"),
    (re.compile(r"\bSolo le(\d)\b"), r"Solo 1 e \1"),
    (re.compile(r"\bSolol\s*e\s*(\d)\b"), r"Solo 1 e \1"),
    (re.compile(r"\bIn troni\b"), "Introni"),
    (re.compile(r"\bin troni\b"), "introni"),
    (re.compile(r"\bin ironica\b"), "intronica"),
    (re.compile(r"\bnel nucleo lo\b"), "nel nucleolo"),
    (re.compile(r"\bnelmesosoma\b"), "nel mesosoma"),
    (re.compile(r"\bneiribosomi\b"), "nei ribosomi"),
    (re.compile(r"\bunozigote\b"), "uno zigote"),
    (re.compile(r"\bin su la tor\b"), "insulator"),
    (re.compile(r"\bIncRNA\b"), "lncRNA"),
    (re.compile(r"\belF2\b"), "eIF2"),
    (re.compile(r"\belF4E\b"), "eIF4E"),
    (re.compile(r"\b1F2\b"), "IF2"),
    (re.compile(r"\b1F3\b"), "IF3"),
    (re.compile(r"\bTFILA\b"), "TFIIA"),
    (re.compile(r"\bTF1IH\b"), "TFIIH"),
    (re.compile(r"\bRatl\b"), "Rat1"),
    (re.compile(r"\bPS3\b"), "p53"),
    (re.compile(r"\bfi-globina\b"), "β-globina"),
    (re.compile(r"\b(RNA\s+pol(?:imerasi)?\s+)Il\b"), r"\1II"),
    (re.compile(r"\b(DNA\s+pol(?:imerasi)?\s+)Il\b"), r"\1II"),
    (re.compile(r"\b(Topoisomerasi\s+)Il\b"), r"\1II"),
    (re.compile(r"\b(Polimerasi\s+)Il\b"), r"\1II"),
    (re.compile(r"\b(DNA satellite\s+)a\b"), r"\1α"),
    (re.compile(r"(?<![0-9A-Za-z])0₂\b"), "O₂"),
    (re.compile(r"\bfimbrie 0 pili\b"), "fimbrie o pili"),
    (re.compile(r"\b2400hm\b"), "240 ohm"),
    (re.compile(r"\b200hm\b"), "20 ohm"),
    (re.compile(r"\blatm\b"), "1 atm"),
    (re.compile(r"\bOmC\b"), "0 mC"),
    (re.compile(r"\bSOkW\b"), "50 kW"),
    (re.compile(r"\bOkW\b"), "0 kW"),
    (re.compile(r"\bSkW\b"), "5 kW"),
    (re.compile(r"\bverso lr esterno\b"), "verso l'esterno"),
    # Strip trailing scan margin bleed tokens flagged by cc130265
    (re.compile(r"\s+(?:SS 255|os PZ|acs OZ I|uss PP I|PAR cs|\| = ee|—_ E|\| E)\s*$"), ""),
    (re.compile(r"\s+pass\.\s*=\s*"), " "),
]

ITEM_SPECIFIC_OVERRIDES: dict[str, dict] = {
    "CHIM-C10-NCOM-080": {
        "answer_banner": "Risposta corretta: A. Cs",
        "opt_a": "Cs",
    },
    "CHIM-C11-COMM-018": {
        "opt_c": "si verifica una reazione con produzione di KOH in soluzione acquosa e O₂",
    },
}


def clean_ocr_fragment(text: str) -> str:
    if not text:
        return text
    out = text
    for pat, repl in _SAFE_SUBS:
        out = pat.sub(repl, out)
    return out


_SUB_SUP_MAP = str.maketrans(
    "₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻",
    "01234567890123456789+-",
)

_GREEK_PAIRS = [
    ("α", "alfa"),
    ("β", "beta"),
    ("γ", "gamma"),
    ("δ", "delta"),
    ("ε", "epsilon"),
    ("θ", "theta"),
    ("λ", "lambda"),
    ("μ", "mu"),
    ("π", "pi"),
    ("ρ", "rho"),
    ("σ", "sigma"),
    ("τ", "tau"),
    ("φ", "phi"),
    ("Φ", "phi"),
    ("ω", "omega"),
    ("Ω", "omega"),
    ("Δ", "delta "),
]


def derive_cloze_synonyms(cloze_targets: list[str], extra_synonyms: list[str] | None = None, flags: list[str] | None = None) -> list[str]:
    """Build rich accepted-answer list for tolerant Cloze typed_answer grading."""
    out: list[str] = []
    seen: set[str] = set()

    def _add(v: str) -> None:
        v = v.strip()
        if v and "|" not in v and v.lower() not in seen:
            seen.add(v.lower())
            out.append(v)

    seeds = list(cloze_targets) + list(extra_synonyms or [])
    # Pull single-quoted candidate words from cc130265 'ambiguous:' flags on Cloze cards
    for fl in flags or []:
        if fl.startswith("ambiguous:"):
            for m in re.findall(r"'([^']{1,40})'", fl):
                if not any(w in m.lower() for w in ["...", "___", "prompt", "blank"]):
                    seeds.append(m)

    for s in seeds:
        _add(s)
        # Strip parenthetical glosses e.g. 'α (alfa)' -> 'α' and 'alfa'
        m_par = re.match(r"^(.+?)\s*\(([^()]+)\)\s*$", s)
        if m_par:
            _add(m_par.group(1))
            _add(m_par.group(2))
        # Plain ASCII digits for sub/superscripts e.g. sp³ -> sp3, H₂O -> H2O
        ascii_sub = s.translate(_SUB_SUP_MAP)
        if ascii_sub != s:
            _add(ascii_sub)
        # Greek <-> Italian name variants
        for sym, name in _GREEK_PAIRS:
            if sym in s:
                _add(s.replace(sym, name).replace("  ", " "))
                _add(ascii_sub.replace(sym, name).replace("  ", " "))
    return out
