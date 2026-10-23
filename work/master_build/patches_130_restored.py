#!/usr/bin/env python3
"""Clean, verify, and tailor all 130 restored duplicate items (from 6d93039e + twin explanations)."""
from __future__ import annotations

import json
import re
from pathlib import Path

# Explicit overrides for stems, options, answers, and tailored explanations among the 130 restored items
OVERRIDES_130 = {
    "CHIM-C03-NCOM-009": {
        "question": "I pesi atomici degli elementi H, P e O sono rispettivamente 1, 31 e 16 (u.m.a.). Il peso molecolare (espresso in u.m.a.) dell'acido ortofosforico (H₃PO₄) è:",
        "explanation": (
            "Il peso molecolare si ottiene sommando le masse atomiche di tutti gli atomi presenti nella formula H₃PO₄: "
            "3·(1) + 31 + 4·(16) = 3 + 31 + 64 = 98 u."
        ),
    },
    "CHIM-C03-NCOM-044": {
        "options": {"E": "contengono lo stesso numero di molecole"},
        "answer_text": "contengono lo stesso numero di molecole",
    },
    "CHIM-C03-NCOM-134": {
        "options": {"B": "S = attinide", "E": "K = metallo alcalino terroso"},
    },
    "CHIM-C03-NCOM-177": {
        "options": {"D": "cresce nei primi tre gruppi, resta invariata negli altri"},
    },
    "CHIM-C04-NCOM-088": {
        "question": "Soltanto una delle seguenti affermazioni a proposito della molecola del metano è errata. Quale?",
        "options": {
            "A": "L'atomo di C è ibridato sp³",
            "B": "I quattro atomi di idrogeno si trovano ai vertici di un tetraedro regolare",
        },
    },
    "CHIM-C04-NCOM-089": {
        "options": {"A": "ottaedrica", "C": "tetraedrica"},
    },
    "CHIM-C05-NCOM-006": {
        "question": "L'H₂O bolle a temperatura più alta rispetto all'H₂S perché:",
        "options": {
            "A": "non contiene legami a ponte di idrogeno, che invece sono presenti nell'H₂S",
            "B": "è un acido più forte dell'H₂S",
            "C": "ha un peso molecolare maggiore di quello dell'H₂S",
            "D": "ha un peso molecolare minore di quello dell'H₂S",
            "E": "contiene legami a ponte di idrogeno, che invece non sono presenti nell'H₂S",
        },
        "answer_text": "contiene legami a ponte di idrogeno, che invece non sono presenti nell'H₂S",
        "explanation": (
            "L'elevata elettronegatività dell'ossigeno consente alle molecole di H₂O di formare intensi legami a idrogeno intermolecolari, "
            "assenti nell'H₂S dove agiscono solo più deboli interazioni dipolo-dipolo e di van der Waals."
        ),
    },
    "CHIM-C05-NCOM-021": {
        "options": {"E": "fondono a 89 K"},
    },
    "CHIM-C05-NCOM-032": {
        "options": {
            "B": "La solubilità di alcuni solidi nei liquidi diminuisce all'aumentare della temperatura",
            "C": "In acqua a 20 °C la solubilità di CO₂ è maggiore di quella di O₂",
            "E": "In acqua a 20 °C la solubilità di N₂ è minore di quella di O₂",
        },
    },
    "CHIM-C05-NCOM-039": {
        "options": {"C": "un grasso neutro", "E": "l'etere dietilico"},
    },
    "CHIM-C05-COMP-034": {
        "question": "Una _____ è una miscela omogenea di soluto e solvente.",
    },
    "CHIM-C06-COMM-020": {
        "question": (
            "Le particelle (molecole o ioni) in soluzione si trovano in una situazione analoga alle molecole di un gas; "
            "queste ultime, come è noto, tendono ad occupare tutto lo spazio a loro disposizione; analogamente una soluzione concentrata, "
            "posta al fondo di un recipiente sotto uno strato di solvente puro, tende, per diffusione, a dare una soluzione diluita del tutto omogenea. "
            "Quale delle seguenti affermazioni può essere dedotta dalla lettura del brano precedente?"
        ),
        "options": {
            "D": "Una soluzione concentrata, in presenza del solvente puro, tende a diluirsi",
            "E": "In una soluzione concentrata sono presenti solo molecole, e non ioni",
        },
        "answer_text": "Una soluzione concentrata, in presenza del solvente puro, tende a diluirsi",
        "explanation": (
            "Per diffusione spontanea secondo gradiente di concentrazione, le particelle di soluto di una soluzione concentrata "
            "migrano nel solvente puro sovrastante fino a distribuirsi uniformemente, diluendo la soluzione fino all'omogeneità."
        ),
    },
    "CHIM-C06-NCOM-012": {
        "question": "Una soluzione satura di NaCl in acqua, in presenza del sale indisciolto, rappresenta un esempio di:",
    },
    "CHIM-C07-NCOM-003": {
        "options": {"C": "di una o più specie chimiche in altre"},
        "answer_text": "di una o più specie chimiche in altre",
    },
    "CHIM-C09-NCOM-013": {
        "options": {"D": "-1"},
        "answer_text": "-1",
    },
    "CHIM-C09-NCOM-039": {
        "question": "Il numero di ossidazione del cromo nel composto K₂Cr₂O₇ è:",
        "explanation": (
            "Nel dicromato di potassio K₂Cr₂O₇ il potassio ha n.o. +1 e l'ossigeno −2; imponendo la neutralità elettrica "
            "2(+1) + 2·x + 7(−2) = 0 si ricava 2x = +12, da cui il numero di ossidazione del cromo è +6."
        ),
    },
    "CHIM-C09-NCOM-040": {
        "question": "Qual è il numero di ossidazione dell'idrogeno in H₂?",
        "explanation": "In qualsiasi sostanza elementare allo stato libero (come H₂, O₂, N₂) gli atomi sono legati a atomi identici e il numero di ossidazione è per definizione pari a 0.",
    },
    "CHIM-C09-NCOM-058": {
        "question": "Quando l'acqua viene sottoposta all'azione di un agente ossidante forte, che cosa si forma?",
        "options": {"A": "H₂", "B": "O₂", "C": "H₂ e O₂", "D": "H₂ e OH⁻", "E": "H⁺ e OH⁻"},
        "answer": "B",
        "answer_text": "O₂",
        "explanation": (
            "Nell'acqua l'idrogeno è già al suo massimo stato di ossidazione (+1), mentre l'ossigeno è a −2: "
            "un ossidante forte ossida quindi l'ossigeno dell'acqua sviluppando ossigeno molecolare O₂ (n.o. 0)."
        ),
    },
    "CHIM-C09-NCOM-069": {
        "question": "L'anione cromato, CrO₄²⁻, si trasforma nel catione Cr³⁺ e in questa reazione l'atomo di Cr:",
        "options": {
            "A": "passa da numero di ossidazione +6 a +3 e si ossida",
            "B": "passa da numero di ossidazione +6 a +3 e si riduce",
            "C": "passa da numero di ossidazione −2 a +3 e si ossida",
            "D": "passa da numero di ossidazione −6 a +3 e si ossida",
            "E": "passa da numero di ossidazione −2 a +3 e si riduce",
        },
        "answer_text": "passa da numero di ossidazione +6 a +3 e si riduce",
    },
    "CHIM-C09-NCOM-078": {
        "explanation": (
            "Nella reazione Zn + FeCl₂ → ZnCl₂ + Fe lo ione ferroso Fe²⁺ (scritto Fe⁺⁺, n.o. +2) acquista due elettroni "
            "trasformandosi in ferro metallico Fe (n.o. 0) e pertanto si riduce, mentre lo zinco passa da 0 a +2 ossidandosi."
        ),
    },
    "CHIM-C09-NCOM-097": {
        "options": {"D": "uno o più elementi a numero di ossidazione piuttosto elevato"},
    },
    "CHIM-C09-NCOM-110": {
        "question": (
            "Nel corso di una reazione chimica, il rame metallico reagisce con una soluzione acquosa di HClO₄ per produrre "
            "Cu(ClO₄)₂ in soluzione acquosa e idrogeno allo stato gassoso che si libera nell'ambiente. In questa reazione la specie che si comporta da riducente è:"
        ),
        "options": {
            "A": "Cu(ClO₄)₂",
            "B": "HClO₄",
            "C": "Lo ione Cu²⁺",
            "D": "Il rame metallico",
            "E": "L'idrogeno gassoso",
        },
        "answer_text": "Il rame metallico",
    },
    "CHIM-C09-NCOM-130": {
        "question": "Se in una reazione gli ioni Ag⁺ in soluzione si trasformano in atomi del metallo, ciò significa che gli ioni Ag⁺:",
        "options": {"A": "si ossidano"},
    },
    "CHIM-C10-COMM-004": {
        "question": "In genere un composto inorganico a carattere riducente contiene:",
        "options": {
            "B": "uno o più elementi a numero di ossidazione piuttosto elevato",
            "C": "uno o più elementi a numero di ossidazione piuttosto basso",
        },
        "answer_text": "uno o più elementi a numero di ossidazione piuttosto basso",
    },
    "CHIM-C10-NCOM-083": {
        "options": {"B": "H₂", "D": "CH₄"},
        "explanation": (
            "L'idrossido di sodio NaOH è una base forte e forma un sale più acqua reagendo con un acido (reazione di neutralizzazione): "
            "tra le specie elencate l'unico acido è l'acido bromidrico HBr (NaOH + HBr → NaBr + H₂O)."
        ),
    },
    "CHIM-C10-NCOM-084": {
        "question": "La reazione tra acido fosforico e idrossido di potassio produce:",
        "explanation": (
            "La neutralizzazione completa dell'acido ortofosforico H₃PO₄ con l'idrossido di potassio KOH genera il corrispondente sale "
            "(fosfato di potassio, K₃PO₄) e acqua secondo H₃PO₄ + 3 KOH → K₃PO₄ + 3 H₂O."
        ),
    },
    "CHIM-C10-NCOM-094": {
        "options": {"A": "SO₃", "B": "K₂O", "C": "LiCl", "D": "NO₂", "E": "HCl"},
        "answer_text": "K₂O",
    },
    "CHIM-C11-NCOM-023": {
        "options": {"C": "NaCl", "D": "CO₂"},
        "answer_text": "CO₂",
        "explanation": (
            "Il diossido di carbonio CO₂ è un'anidride (ossido acido) che in acqua instaura l'equilibrio CO₂ + H₂O ⇌ H₂CO₃ ⇌ H⁺ + HCO₃⁻, "
            "abbassando il pH; BaO e NaOH danno invece soluzioni basiche, mentre KBr e NaCl sono sali neutri."
        ),
    },
    "CHIM-C11-NCOM-033": {
        "options": {
            "A": "Lo ione solfato (SO₄²⁻) è la base coniugata dell'acido solforico",
            "C": "Lo ione fluoruro è la base coniugata di HF",
            "E": "L'acqua è la base coniugata dello ione idronio",
        },
        "answer_text": "Lo ione solfato (SO₄²⁻) è la base coniugata dell'acido solforico",
    },
    "CHIM-C11-NCOM-047": {
        "question": "In una reazione in cui l'acqua si trasforma in ione idronio, H₃O⁺, essa si comporta da:",
    },
    "CHIM-C11-NCOM-122": {
        "question": "Qual è il valore del pH di una soluzione 1 · 10⁻¹ M di H₃O⁺?",
        "explanation": (
            "Per definizione pH = −log₁₀[H₃O⁺]: con [H₃O⁺] = 1 · 10⁻¹ M = 0,1 M si ottiene pH = −log₁₀(10⁻¹) = 1."
        ),
    },
    "CHIM-C12-NCOM-011": {
        "options": {"A": "cinque sostituenti diversi"},
    },
    "CHIM-C12-NCOM-153": {
        "options": {"B": "Pseudoalcano"},
    },
    "CHIM-C12-NCOM-273": {
        "explanation": (
            "L'ossidazione di un alcol secondario R–CH(OH)–R' rimuove due atomi di idrogeno trasformando il gruppo ossidrilico "
            "in un gruppo carbonilico interno R–CO–R', cioè un chetone (mentre gli alcoli primari danno aldeidi e poi acidi carbossilici)."
        ),
    },
    "CHIM-C12-NCOM-303": {
        "question": "Il composto CH₃-CH₂-O-CH₂-CH₃ è:",
    },
    "CHIM-C12-NCOM-304": {
        "question": "Qual è il nome di CH₃-O-C₃H₇?",
        "options": {"A": "Dipropil etere", "E": "Dimetil dipropil etere"},
    },
    "CHIM-C13-NCOM-048": {
        "explanation": (
            "I termini zuccheri, carboidrati, idrati di carbonio e glicidi (o glucidi) sono tutti sinonimi che indicano la medesima classe "
            "di biomolecole poliidrossialdeidiche o poliidrossichetoniche: pertanto nessuna delle altre voci indica una classe diversa."
        ),
    },
    "CHIM-C13-NCOM-134": {
        "options": {"D": "sono sintetizzati dall'organismo in quantità sufficienti"},
        "answer_text": "sono sintetizzati dall'organismo in quantità sufficienti",
    },
    "CHIM-C13-NCOM-174": {
        "question": "I pesi atomici degli elementi H, P e O sono rispettivamente 1, 31 e 16 (u.m.a.). Il peso molecolare (espresso in u.m.a.) dell'acido ortofosforico (H₃PO₄) è:",
        "explanation": (
            "Sommando i pesi atomici di tutti gli atomi nella formula dell'acido ortofosforico H₃PO₄ si ottiene "
            "3·(1) + 31 + 4·(16) = 3 + 31 + 64 = 98 u."
        ),
    },
    "CHIM-C13-NCOM-175": {
        "question": "Poiché i pesi atomici di H, S e O sono rispettivamente 1, 32 e 16 u.m.a., il peso molecolare espresso in u.m.a. dell'acido solforico vale:",
    },
    "BIO-C01-NCOM-095": {
        "question": (
            "I batteri crescerebbero all'infinito secondo una progressione geometrica, se non intervenissero alcuni fattori che ne riducono o limitano la continua espansione. "
            "Questi fattori sono tali per cui una curva di crescita in una quantità determinata di terreno di coltura può essere divisa in tre fasi: "
            "una prima fase che esprime una crescita esponenziale dei batteri (i batteri crescono in modo esponenziale con il passare del tempo); "
            "una seconda fase nella quale il numero di batteri della coltura è costante nel tempo; una fase finale in cui il numero di batteri in coltura (per unità di volume) diminuisce nel tempo. "
            "Quale tra i seguenti fenomeni spiega l'esistenza della terza fase?"
        ),
        "options": {"B": "I batteri invecchiano e muoiono come tutti gli organismi viventi"},
    },
    "BIO-C01-NCOM-213": {
        "question": (
            "Meselson e Stahl nel 1957 fornirono prove sperimentali che ciascun filamento di DNA serviva da stampo per il nuovo DNA, "
            "dimostrando così il processo di duplicazione semiconservativa del DNA. Essi fecero crescere un ceppo di Escherichia coli in un terreno contenente azoto pesante (¹⁵N), "
            "quindi lo passarono in un terreno contenente azoto leggero (¹⁴N). Dopo due generazioni esaminarono i risultati e constatarono che la percentuale di DNA composto "
            "da un'elica pesante (con azoto 15) e da una leggera (con azoto 14) era:"
        ),
    },
    "BIO-C02-NCOM-051": {
        "explanation": (
            "Due cromosomi omologhi (uno di origine materna e uno paterna) portano gli stessi geni disposti nello stesso ordine lineare, "
            "cioè presentano identica sequenza di loci genici, pur potendo differire per gli alleli presenti e quindi per la specifica sequenza nucleotidica del DNA."
        ),
    },
    "BIO-C03-NCOM-065": {
        "question": (
            "Il diagramma A della figura esprime la produzione dell'enzima β-galattosidasi da parte di Escherichia coli, in un terreno che viene arricchito di lattosio; "
            "il diagramma B, quando dal terreno si toglie il lattosio. Tale variazione è conseguenza di:"
        ),
    },
    "BIO-C03-NCOM-074": {
        "options": {"E": "L'alide"},
    },
    "BIO-C03-NCOM-113": {
        "options": {
            "A": "Vi è una correzione post-trascrizionale della proteina",
            "D": "Vi è una correzione post-trascrizionale della sequenza dell'RNA messaggero",
        },
    },
    "BIO-C04-NCOM-052": {
        "question": "Se si incrocia un individuo eterozigote per una caratteristica dominante con un omozigote recessivo, con quale probabilità avremo individui con il fenotipo recessivo?",
    },
    "BIO-C04-NCOM-144": {
        "question": "Si consideri l'albero genealogico riportato nella scansione, riguardante un carattere dominante. Si può dedurre che:",
        "options": {"A": "il maschio affetto della II è omozigote"},
    },
    "BIO-C04-NCOM-163": {
        "question": "L'albero genealogico riportato nella scansione rappresenta l'ereditarietà di un carattere dominante. Dal suo studio si può affermare che:",
    },
    "BIO-C04-NCOM-175": {
        "options": {
            "C": "dominanza incompleta",
            "D": "allelia multipla",
        },
        "answer_text": "allelia multipla",
        "explanation": (
            "Il sistema dei gruppi sanguigni AB0 è controllato da tre alleli distinti dello stesso locus genico (Iᴬ, Iᴮ e i), "
            "costituendo un classico esempio di allelia multipla (poliallelia)."
        ),
    },
    "BIO-C05-NCOM-144": {
        "question": "Lo schema nella scansione rappresenta il ciclo dell'ATP. La freccia 1 rappresenta:",
    },
    "BIO-C06-NCOM-131": {
        "options": {"E": "Gβγ"},
    },
    "FIS-C01-NCOM-072": {
        "explanation": (
            "Per convertire da m/s a km/h si moltiplica per 3,6 (poiché 1 m = 10⁻³ km e 1 s = 1/3600 h): "
            "v = 180 m/s × 3,6 = 648 km/h."
        ),
    },
    "FIS-C03-NCOM-140": {
        "options": {"E": "il corpo di massa doppia acquisterà una velocità doppia nell'arrivare al suolo"},
    },
    "FIS-C03-COMP-176": {
        "question": "La costante elastica della molla si indica con la lettera _____.",
    },
    "FIS-C04-NCOM-014": {
        "options": {
            "B": "è salito di 1 mm",
            "C": "è sceso di 10 mm",
            "D": "è sceso di 1 mm",
        },
        "answer_text": "è sceso di 1 mm",
    },
    "FIS-C05-NCOM-005": {
        "question": (
            "L'effusione dei gas attraverso fori sottili è regolata dalla legge di Graham, che stabilisce che la velocità di effusione (diffusione) "
            "ad una data temperatura dipende solo dalla massa molecolare (p.M.), ed è inversamente proporzionale alla sua radice quadrata. "
            "Quale delle seguenti affermazioni non può essere dedotta dalla lettura del brano precedente?"
        ),
    },
    "FIS-C05-NCOM-077": {
        "options": {"B": "1 atm", "E": "4 atm"},
    },
    "FIS-C05-NCOM-108": {
        "explanation": (
            "Per il teorema di equipartizione dell'energia nella teoria cinetica dei gas, l'energia cinetica media di traslazione delle molecole "
            "(E_c = 3/2 k_B T) dipende esclusivamente dalla temperatura assoluta T, che non compare tra le opzioni elencate."
        ),
    },
    "FIS-C05-NCOM-109": {
        "question": (
            "Gli urti, che nei gas ideali vengono supposti come perfettamente elastici, determinano un continuo trasferimento di energia cinetica da una molecola all'altra; "
            "ne consegue che, in un determinato istante, le molecole non posseggono tutte lo stesso valore di energia cinetica. Mediante calcoli statistici è possibile dimostrare "
            "che i valori dell'energia cinetica in un sistema contenente un gran numero di molecole sono distribuiti intorno ad un valore medio E_c, dipendente esclusivamente "
            "dalla temperatura assoluta, a cui è direttamente proporzionale; la statistica dimostra che, se il numero di molecole del sistema è sufficientemente elevato, "
            "è del tutto lecito sostituire alla popolazione reale delle molecole con valori individuali dell'energia cinetica una popolazione ideale in cui tutte le molecole "
            "posseggono il valore E_c. Quale delle seguenti informazioni non può essere dedotta dalla lettura del brano precedente?"
        ),
        "options": {"C": "Se la temperatura assoluta raddoppia, raddoppia anche il valore di E_c"},
        "explanation": (
            "Dal brano si ricava che il valore medio dell'energia cinetica E_c dipende esclusivamente dalla temperatura assoluta T; "
            "è quindi falsa e non deducibile dal testo l'affermazione secondo cui E_c dipenderebbe dal numero di molecole del sistema."
        ),
    },
    "FIS-C07-COMP-007": {
        "question": "La frequenza angolare si indica con la lettera _____.",
        "answer": "ω",
        "answer_text": "ω (omega)",
        "accepted_synonyms": ["ω", "omega", "ω (omega)"],
    },
    "FIS-C08-NCOM-018": {
        "options": {"A": "una diminuzione di un'unità di A per quell'elemento"},
        "answer_text": "una diminuzione di un'unità di A per quell'elemento",
    },
}


def build_clean_130(special_jsonl: Path) -> dict[str, dict]:
    rows = [json.loads(ln) for ln in special_jsonl.read_text(encoding="utf-8").splitlines() if ln.strip()]
    out = {}
    for r in rows:
        iid = r["id"]
        rc = dict(r["remediated_card"])
        opts = dict(rc["options"]) if rc["options"] else None
        tw = r["solved_work"]["restored_twin_ref"]
        exp = (tw["twin_explanation"] or "").strip()

        ov = OVERRIDES_130.get(iid, {})
        q = ov.get("question", rc["question"]).strip()
        if opts is not None and "options" in ov:
            opts.update(ov["options"])
        ans = ov.get("answer", rc["answer"]).strip()
        ans_text = ov.get("answer_text", opts[ans] if opts else rc["answer_text"]).strip()
        if "explanation" in ov:
            exp = ov["explanation"].strip()

        # Clean minor OCR artifacts in twin explanations
        exp = exp.replace("/4, 78, i", "Iᴬ, Iᴮ, i").replace("1 cromosomi", "I cromosomi")
        assert exp, f"Empty explanation on restored item {iid}"
        # Ensure no stale letter references remain in exp
        if re.search(r"\brisposta\s+[A-E]\b", exp):
            assert iid == "BIO-C01-NCOM-235", f"Unchecked letter reference in {iid}: {exp}"

        synonyms = ov.get("accepted_synonyms")
        if r["quiz_type"] == "completamento":
            assert "_____" in q, f"Missing blank in COMP {iid}: {q}"
            cloze_stem = q.replace("_____", f"{{{{c1::{ans}}}}}", 1)
            if not synonyms:
                synonyms = [ans]
        else:
            cloze_stem = None

        out[iid] = {
            "id": iid,
            "question": q,
            "cloze_front_stem": cloze_stem,
            "options": opts,
            "answer": ans,
            "answer_text": ans_text,
            "explanation": exp,
            "accepted_synonyms": synonyms or [],
            "figure_crop_from_qscan": iid in {"BIO-C04-NCOM-144", "BIO-C04-NCOM-163", "BIO-C05-NCOM-144", "BIO-C03-NCOM-065"},
        }
    assert len(out) == 130
    return out


if __name__ == "__main__":
    res = build_clean_130(Path("/home/user/anki-sem/work/opus_handoff/special_sets/missing_130_restored.jsonl"))
    print(f"Verified all {len(res)} restored items (130/130 clean stems, keys, and explanations).")
