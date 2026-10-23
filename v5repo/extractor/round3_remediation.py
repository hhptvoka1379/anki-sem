"""Round-3 deep scan-verified remediation across all 6,948 unique items & embedded media:
1. Removes all 34 false-positive pure-text duplicate crops from `figure_files` / `output/figures/`,
   restores the genuine resistor circuit diagram on `FIS-C06-COMM-034`, and tightly crops all 11
   diagrams that previously bled stem headers or MCQ options A..E into the graphic frame.
2. Fixes all remaining OCR formula, ion-charge, superscript/subscript, running-footer, and Italian
   spelling/word-merge corruptions across questions, options, AND all 1,041 `commentati` explanations.
3. Formats all bulleted (`•`), numbered (`1.`, `2.`, `1)`, `2)`), lettered (`a)`, `b)`), reaction-list,
   and multi-statement questions & explanations with clean hard line breaks (`\\n`).
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Dict, List, Set

from PIL import Image

from extractor.round3_extra_fixes import EXTRA_CARD_OVERRIDES, apply_extra_text_cleanups


BOGUS_TEXT_ONLY_FIGURES: Set[str] = {
    "CHIM_C01_comm_Q002.png",
    "CHIM_C01_non__Q058.png",
    "CHIM_C01_non__Q070.png",
    "CHIM_C01_non__Q107.png",
    "CHIM_C02_comm_Q003.png",
    "CHIM_C02_comm_Q005.png",
    "CHIM_C03_non__Q136_p1.png",
    "CHIM_C06_comm_Q016.png",
    "CHIM_C07_non__Q024.png",
    "CHIM_C07_non__Q035.png",
    "CHIM_C07_non__Q041_p1.png",
    "CHIM_C09_non__Q086.png",
    "CHIM_C09_non__Q091.png",
    "CHIM_C10_non__Q064.png",
    "CHIM_C11_comm_Q026.png",
    "CHIM_C11_non__Q045.png",
    "CHIM_C11_non__Q050_p2.png",
    "CHIM_C11_non__Q054_p1.png",
    "CHIM_C11_non__Q110.png",
    "CHIM_C12_non__Q034.png",
    "CHIM_C12_non__Q041.png",
    "CHIM_C12_non__Q046.png",
    "CHIM_C12_non__Q101.png",
    "CHIM_C12_non__Q115.png",
    "CHIM_C12_non__Q160.png",
    "CHIM_C12_non__Q163.png",
    "BIO_C03_non__Q024.png",
    "BIO_C04_comm_Q048_p1.png",
    "BIO_C04_non__Q035_p1.png",
    "BIO_C05_comm_Q037_p1.png",
    "BIO_C07_non__Q014_p1.png",
    "FIS_C03_non__Q184_p1.png",
    "FIS_C06_non__Q123_p1.png",
    "FIS_C07_non__Q051.png",
}

# Exact y-crop windows (top_y, bottom_y) verified against 300-DPI ink bands (idempotent via height check)
FIGURE_Y_CROPS: Dict[str, tuple[int, int, int]] = {
    # filename: (expected_min_height_before_crop, y0, y1)
    "CHIM_C02_comm_Q025_p2.png": (400, 74, 440),
    "CHIM_C12_non__Q161.png": (300, 100, 175),
    "BIO_C04_comm_Q063.png": (240, 6, 162),
    "BIO_C04_non__Q035_p2.png": (300, 6, 238),
    "BIO_C07_non__Q044.png": (260, 6, 158),
    "BIO_C07_non__Q055.png": (200, 6, 146),
    "FIS_C01_comm_Q025.png": (600, 6, 496),
    "FIS_C01_non__Q090.png": (400, 6, 250),
    "FIS_C04_comm_Q007.png": (170, 6, 109),
    "FIS_C06_comm_Q042_p1.png": (300, 6, 190),
    "FIS_C06_non__Q186.png": (260, 6, 185),
}


def clean_figures_on_disk(fig_dir: Path, clean_media_dir: Path) -> Dict[str, int]:
    removed = 0
    cropped = 0
    for fn in BOGUS_TEXT_ONLY_FIGURES:
        for base in (fig_dir, clean_media_dir):
            p = base / fn
            if p.exists():
                p.unlink()
                removed += 1

    # Restore real resistor circuit diagram for FIS-C06-COMM-034 from its verified question scan
    src_q34 = clean_media_dir / "FIS-C06-COMM-034.png"
    dst_f34 = fig_dir / "FIS_C06_comm_Q034_p1.png"
    if src_q34.exists():
        im34 = Image.open(src_q34).convert("RGB")
        if im34.height >= 400:
            circ = im34.crop((180, 100, 560, 208))
            circ.save(dst_f34)
            shutil.copy2(dst_f34, clean_media_dir / dst_f34.name)
            cropped += 1

    for fn, (min_h, y0, y1) in FIGURE_Y_CROPS.items():
        fp = fig_dir / fn
        if fp.exists():
            im = Image.open(fp).convert("RGB")
            if im.height >= min_h:
                im_c = im.crop((0, y0, im.width, min(im.height, y1)))
                im_c.save(fp)
                cropped += 1
            if clean_media_dir.exists():
                shutil.copy2(fp, clean_media_dir / fn)

    return {"bogus_files_deleted": removed, "diagrams_cropped": cropped}


ROUND3_CARD_OVERRIDES: Dict[str, dict] = {
    "CHIM-C01-COMM-002": {
        "question": (
            "Quale/i fra le seguenti affermazioni è/sono vera/e?\n"
            "• A₁: l'idrogeno è l'unico elemento a cui si attribuiscono nomi differenti per alcuni suoi isotopi;\n"
            "• A₂: in chilogrammi, l'ordine di grandezza della massa di un atomo è compreso fra 10⁻³¹ e 10⁻²⁹;\n"
            "• A₃: ad eccezione dell'idrogeno tutti gli atomi degli altri elementi chimici hanno in egual numero elettroni e neutroni."
        ),
        "explanation": (
            "Le affermazioni sono tutte false:\n"
            "• L'affermazione A₁ è falsa in quanto, oltre agli isotopi dell'idrogeno, cui sono assegnati i nomi prozio, deuterio e trizio, anche ad alcuni isotopi del radon sono assegnati nomi diversi da quello dell'elemento (il Rn-220 è detto thoron e il Rn-219 actinon).\n"
            "• L'affermazione A₂ è falsa in quanto le masse atomiche degli elementi sono comprese tra ordini di grandezza di 10⁻²⁷ e 10⁻²⁵ kg.\n"
            "• L'affermazione A₃ è falsa in quanto tutti gli elementi presentano isotopi, ovvero atomi di uno stesso elemento che hanno uguale numero atomico (numero di protoni) ma diverso numero di massa (protoni + neutroni), poiché differiscono per il numero di neutroni contenuti nel nucleo."
        ),
    },
    "FIS-C07-NCOM-051": {
        "question": (
            "Un fascio di luce monocromatica incide su una fenditura sottile. Nella figura di diffrazione il primo minimo si trova ad un angolo θ rispetto alla posizione centrale. Quali delle seguenti affermazioni sono vere?\n"
            "• 1) Riducendo la larghezza della fenditura, si riduce l'angolo θ.\n"
            "• 2) Aumentando la lunghezza d'onda della luce, aumenta l'angolo θ.\n"
            "• 3) Aumentando la frequenza della luce, aumenta l'angolo θ.\n"
            "• 4) Si vedono zone di luce anche ad angoli maggiori di θ."
        ),
    },
    "CHIM-C07-NCOM-044": {
        "question": (
            "Quante delle seguenti reazioni sono solo ossidazioni (Ox), quante solo riduzioni (Red), quante ossidoriduzioni (Redox)?\n"
            "• 2 H⁺ + 2 e⁻ → H₂\n"
            "• Ag⁺ + Cl⁻ → AgCl\n"
            "• Cu⁺ → Cu²⁺ + e⁻\n"
            "• 2 Cu⁺ → Cu + Cu²⁺\n"
            "• Mg → Mg²⁺ + 2 e⁻"
        ),
    },
    "CHIM-C11-NCOM-100": {
        "question": (
            "Le seguenti soluzioni acquose acide hanno diversi valori di pH:\n"
            "• 1. 0,2 mol dm⁻³ HCl\n"
            "• 2. 0,1 mol dm⁻³ HNO₃\n"
            "• 3. 0,2 mol dm⁻³ H₂SO₄\n"
            "• 4. 0,1 mol dm⁻³ CH₃COOH\n"
            "Quale delle seguenti opzioni rappresenta la sequenza delle soluzioni in ordine crescente di pH (da sinistra a destra)?"
        ),
    },
    "CHIM-C01-NCOM-101": {
        "question": "¹¹₃Li è un isotopo instabile del litio che decade emettendo un protone. Quale sarà il suo prodotto di decadimento?",
    },
    "CHIM-C02-COMM-005": {
        "explanation": "Poiché il peso molecolare dell'acido solforico (MM H₂SO₄) = 98, la massa molare dell'acido solforico è pari a 98 g mol⁻¹, e perciò 5 mol corrispondono a: 5 mol × 98 g mol⁻¹ = 490 g.",
    },
    "CHIM-C02-COMM-007": {
        "explanation": "Se il P.A. di N è 14, il P.M. di N₂ (diazoto) è 28. La massa di una mole di azoto si ottiene semplicemente mettendo l'etichetta g davanti al peso molecolare che è un numero puro. Quindi una mole di N₂ ha una massa di 28 g.",
        "options": {
            "A": "28 atomi di N pesano 28 g",
            "B": "Una molecola di N₂ occupa 22,414 L in condizioni standard",
            "C": "28 molecole di N₂ pesano 1 g",
            "D": "Una mole di N₂ pesa 28 g",
            "E": "Una molecola di N₂ pesa 28 g",
        },
    },
    "CHIM-C02-COMM-021": {
        "question": "Il numero massimo di elettroni contenuto in un orbitale 5f è:",
    },
    "CHIM-C02-COMM-023": {
        "explanation": "Il numero quantico secondario l ha valori che dipendono dal numero quantico principale n (l = 0, 1, 2, ..., n - 1) ed è sempre inferiore a n stesso. Il numero quantico di spin può essere ±1/2. L'unica affermazione falsa è la C, in quanto in realtà è il numero quantico magnetico m_l a dipendere da l (m_l = -l, ..., 0, ..., +l).",
        "options": {
            "A": "Il numero quantico principale n può assumere tutti i valori interi positivi",
            "B": "Il numero quantico secondario l è sempre inferiore al numero quantico principale n",
            "C": "Il numero quantico secondario l dipende dal numero quantico magnetico",
            "D": "Il numero quantico di spin di un elettrone può assumere solo valori seminteri",
            "E": "Il numero quantico magnetico dipende dal numero quantico secondario l",
        },
    },
    "CHIM-C02-COMM-024": {
        "explanation": "Il calcio (Ca) è un metallo alcalino-terroso (II gruppo). I metalli alcalini (Li, Na, K, Rb, Cs, Fr) appartengono al I gruppo della tavola periodica.",
    },
    "CHIM-C02-COMM-035": {
        "question": "Il numero massimo di elettroni contenuto negli orbitali di tipo f, s, d è rispettivamente:",
    },
    "CHIM-C02-COMM-036": {
        "options": {
            "A": "n = 3; l = 1; m = 4; m_s = +1/2",
            "B": "n = 3; l = 1; m = -1/2; m_s = 0",
            "C": "n = 2; l = 3; m = 0; m_s = +1/2",
            "D": "n = 2; l = 3; m = +1/2; m_s = 0",
            "E": "n = 3; l = 1; m = 0; m_s = -1/2",
        },
    },
    "CHIM-C02-COMM-038": {
        "question": "Il numero quantico di spin:",
        "explanation": "Secondo la visione semplificata, lo spin (dall'inglese trottola) può assumere due valori +1/2 e -1/2 corrispondenti ai due versi di rotazione dell'elettrone attorno a se stesso.",
    },
    "CHIM-C02-COMM-040": {
        "explanation": "Il litio è un metallo alcalino e si trova nel primo gruppo della tavola periodica. La configurazione elettronica dell'atomo di litio è 1s² 2s¹. Per perdita dell'unico elettrone dall'orbitale 2s si genera lo ione Li⁺, la cui configurazione elettronica è, quindi, 1s².",
    },
    "CHIM-C02-NCOM-007": {
        "options": {
            "A": "8 elettroni",
            "B": "14 elettroni",
            "C": "6 elettroni",
            "D": "10 elettroni",
            "E": "18 elettroni",
        },
    },
    "CHIM-C03-NCOM-013": {
        "question": "Un composto ha la seguente composizione percentuale in massa:\n• 40,2% K\n• 26,9% Cr\n• 32,9% O\nQual è la formula empirica di tale composto? [Massa atomica relativa: K = 39,1; Cr = 52,0; O = 16,0]",
        "options_patch": {"A": "KCrO₂"},
    },
    "CHIM-C03-NCOM-031": {"options_patch": {"E": "6 × 10²⁴"}},
    "CHIM-C03-NCOM-071": {"options_patch": {"E": "Bronzo"}},
    "CHIM-C03-NCOM-136": {
        "question": "La seguente tabella riporta le energie di ionizzazione successive di un elemento del Periodo 3 della Tavola Periodica degli Elementi. A quale gruppo della Tavola Periodica appartiene questo elemento?",
    },
    "CHIM-C03-NCOM-137": {
        "question": "Nella tabella sottostante sono riportati i valori delle prime otto energie di ionizzazione di un elemento il cui numero atomico è minore di 20. A quale Gruppo della Tavola Periodica appartiene l'elemento?",
    },
    "CHIM-C03-NCOM-149": {"options_patch": {"A": "alla seconda serie di transizione"}},
    "CHIM-C03-COMP-014": {"question": "La _____ è la quantità di sostanza che contiene 6,022 × 10²³ particelle."},
    "CHIM-C04-COMM-006": {
        "explanation": "Nell'ibridazione sp³, gli orbitali dell'atomo sono disposti secondo i vertici di un tetraedro e la forma della molecola o dello ione che contiene l'atomo è tetraedrica.",
    },
    "CHIM-C04-COMM-008": {
        "explanation": "Nell'acido cianidrico è presente un legame σ tra idrogeno e carbonio e un triplo legame tra carbonio e azoto (H–C≡N). Un triplo legame è costituito da un legame σ e due legami π, quindi complessivamente nella molecola sono presenti due legami σ e due legami π.",
        "options": {
            "A": "un legame π e tre legami σ",
            "B": "un legame σ e tre legami π",
            "C": "due legami σ e due legami π",
            "D": "tre legami π",
            "E": "tre legami σ",
        },
    },
    "CHIM-C04-COMM-015": {
        "explanation": "Poiché in entrambe le molecole l'atomo centrale ha ibridazione sp³, esse hanno la stessa struttura tetraedrica.",
    },
    "CHIM-C04-COMM-016": {
        "question": "Numerosi sali di cobalto hanno, allo stato solido, sei molecole d'acqua coordinate al catione Co²⁺; in genere le molecole d'acqua dipolari, coordinate ai cationi, vengono considerate legami ione-dipolo; nel caso in esame, però, i legami tra acqua e Co²⁺ vanno considerati come covalenti molto polarizzati. Quale delle seguenti informazioni NON è contenuta nel brano precedente?",
        "options_patch": {"D": "La polarizzazione dei legami tra acqua e Co²⁺ è assai elevata"},
    },
    "CHIM-C04-NCOM-081": {"question": "Qual è la struttura spaziale di una molecola con ibridazione sp?"},
    "CHIM-C04-NCOM-087": {"question": "Gli orbitali ibridi sp³ del carbonio sono disposti secondo i vertici:"},
    "CHIM-C06-NCOM-005": {"options_patch": {"B": "tripla rispetto alla soluzione I"}},
    "CHIM-C06-NCOM-014": {
        "question": "Il cloruro rameoso (CuCl) ha una solubilità in acqua di circa 4,4 × 10⁻⁴ mol/L. Cosa accadrà alla concentrazione di Cu⁺ se ad 1 L di una soluzione satura di CuCl vengono aggiunte 0,1 mol di CaCl₂?",
        "options_patch": {
            "A": "La concentrazione di Cu⁺ si abbassa per effetto dello ione in comune",
            "D": "La concentrazione di Cu⁺ si innalza perché si abbassa il pH",
            "E": "La concentrazione di Cu⁺ si abbassa perché viene ossidato a Cu²⁺",
        },
    },
    "CHIM-C06-NCOM-050": {
        "question": "I principali ingredienti di una tavoletta di cioccolato al latte sono normalmente gli zuccheri, pari a circa il 47%. Se questi zuccheri sono rappresentati da saccarosio (C₁₂H₂₂O₁₁, MM = 342,31) quante molecole di zucchero sono contenute approssimativamente in una barretta di cioccolato al latte da 50 g?",
    },
    "CHIM-C07-COMM-021": {
        "explanation": "La reazione di ossido-riduzione bilanciata è la seguente: Cu + 2 HClO₄ → Cu(ClO₄)₂ + H₂. La specie riducente è quella che riduce e che, quindi, si ossida. Il rame passa dallo stato di ossidazione 0 nel rame metallico a +2 in Cu(ClO₄)₂, mentre l'idrogeno passa dallo stato di ossidazione +1 in HClO₄ a 0 in H₂. La specie riducente è, quindi, il rame metallico.",
    },
    "CHIM-C09-COMM-006": {
        "explanation": "Gli ossidi metallici sono di natura basica e reagiscono con gli acidi secondo una reazione di neutralizzazione, producendo un sale e acqua. Ad esempio: CaO + 2 HCl → CaCl₂ + H₂O. Il sale si forma dalla combinazione del catione metallico dell'ossido con l'anione dell'acido, mentre l'acqua deriva dalla combinazione degli ioni H⁺ dell'acido con gli ioni O²⁻ dell'ossido. Le altre risposte sono errate: non si formano acido e base (B), né idrossidi (C), né due sali (D), e non ha senso parlare di «sale più debole» (E).",
    },
    "CHIM-C09-NCOM-066": {
        "question": "Nella reazione I₂ + 2 Fe²⁺ → 2 I⁻ + 2 Fe³⁺:",
        "options_patch": {
            "A": "I₂ si ossida e Fe²⁺ si riduce",
            "B": "Fe²⁺ è l'ossidante",
            "D": "I₂ si riduce e Fe²⁺ si ossida",
        },
    },
    "CHIM-C09-NCOM-096": {"question": "La reazione Cu⁺ - 1 e⁻ → Cu²⁺ è una:"},
    "CHIM-C09-NCOM-109": {"question": "Nella reazione: Fe + Cu²⁺ → Fe²⁺ + Cu:"},
    "CHIM-C10-COMM-009": {
        "explanation": "Lo ione ammonio ha formula NH₄⁺. Ha quindi 5 atomi. Pertanto la frase errata è la D. Infatti NH₄⁺ è l'acido coniugato dell'ammoniaca, ha struttura tetraedrica e non può accettare protoni.",
    },
    "CHIM-C10-COMM-015": {
        "question": "Esiste una netta differenza tra il fluoro e gli altri alogeni per quanto concerne i composti ossigenati. Infatti, mentre il F, che presenta struttura elettronica 1s² 2s² 2p⁵, può combinarsi con l'ossigeno solo per dare ossido di difluoro, in cui l'alogeno presenta numero di ossidazione -1, gli altri elementi del settimo gruppo possono formare vari composti ossigenati, nei quali presentano numeri di ossidazione positivi (tutti i valori dispari da +1 a +7). Questo comportamento va messo in relazione con la presenza di orbitali d vuoti negli alogeni a numero atomico superiore; in tali orbitali vuoti si possono sistemare elettroni degli orbitali s oppure p; si determina così la formazione di strutture con elettroni spaiati, ciascuno dei quali può dare origine ad un legame covalente. Quale delle seguenti informazioni può essere dedotta dalla lettura del brano precedente?",
    },
    "CHIM-C10-NCOM-005": {
        "question": "Se un atomo di ossigeno acquista due elettroni, si forma uno ione:",
        "options_patch": {"D": "ossidulo"},
    },
    "CHIM-C11-COMM-007": {
        "explanation": "Una soluzione acquosa avente pH = 4 ha una concentrazione di ioni [H⁺] = 10⁻⁴ M. Analogamente una soluzione dello stesso acido a pH = 2 ha una concentrazione di ioni [H⁺] = 10⁻² M. Perciò per passare da una soluzione all'altra, 1 L va diluito di 100 volte.",
    },
    "CHIM-C11-COMM-008": {
        "explanation": "Per risolvere questo esercizio si può calcolare il pOH e sfruttare successivamente la relazione pH = 14 - pOH:\n• pOH = -log(5,8 × 10⁻⁹) = 8,2\n• pH = 14 - 8,2 = 5,8",
    },
    "CHIM-C11-COMM-027": {
        "explanation": "Se il pH della soluzione è 2, la concentrazione di ioni H⁺ si ottiene così: dato che pH = -log[H⁺], [H⁺] = 10⁻ᵖᴴ = 10⁻² = 0,01 M. Il volume della soluzione è 10 L, quindi complessivamente sono presenti 0,01 M × 10 L = 0,1 mol di H⁺. Questo è anche il numero di moli di NaOH necessarie per la neutralizzazione della soluzione. Di conseguenza 0,1 mol × 40 g/mol = 4 g è la massa di NaOH richiesta dall'esercizio.",
    },
    "CHIM-C11-COMM-035": {"explanation": "La concentrazione degli ioni H⁺ ad un dato pH è uguale a 10⁻ᵖᴴ."},
    "CHIM-C11-COMM-038": {
        "explanation": "Dal pH si ricava la concentrazione molare degli ioni idrogeno: [H⁺] = 10⁻ᵖᴴ. Se ne ricava che minore è il pH, maggiore è [H⁺] e minore è [OH⁻].",
    },
    "CHIM-C11-NCOM-054": {
        "question": "20 g di NaOH sono sciolti in 500 mL di acqua. Qual è il volume minimo di questa soluzione necessario per neutralizzare 25 mL di una soluzione 1 mol/L di H₂SO₄(aq)? (Si assuma massa atomica relativa: H = 1; O = 16; Na = 23; S = 32)",
    },
    "CHIM-C12-COMM-002": {
        "explanation": "Un composto contenente un atomo di carbonio stereogenico (meno propriamente detto «chirale»), cioè un carbonio con ibridazione tetraedrica (sp³) e legato a quattro gruppi diversi, è in grado di ruotare il piano della luce polarizzata. In realtà la domanda è imprecisa: esistono infatti composti in grado di ruotare il piano della luce polarizzata pur essendo privi di atomi di carbonio con ibridazione tetraedrica (es. esaelicene, un idrocarburo policiclico aromatico con soli carboni sp²).",
    },
    "CHIM-C12-COMM-003": {
        "explanation": "Le aldeidi sono molecole organiche in cui è presente il gruppo carbonilico (C=O); gli alcoli sono molecole organiche in cui il gruppo funzionale -OH è legato ad un carbonio ibridato sp³; gli alcheni sono molecole organiche in cui sono presenti doppi legami carbonio-carbonio; le ammidi sono molecole organiche in cui è presente un atomo di azoto legato ad un gruppo carbonilico.",
    },
    "CHIM-C12-COMM-010": {
        "explanation": "L'atomo di carbonio ha ibridazione sp³, quindi gli atomi di idrogeno sono ai vertici di un tetraedro e gli angoli di legame sono di 109°28'. Sebbene i legami C–H siano polarizzati a causa della diversa elettronegatività dei due atomi, la disposizione tetraedrica determina che la somma vettoriale dei momenti dipolari di ciascun legame sia uguale a 0, per cui la molecola è apolare.",
    },
    "CHIM-C12-COMM-011": {
        "explanation": "Il ciclopentano è un idrocarburo ciclico saturo a 5 atomi di carbonio (pent-), non è aromatico, tutti i suoi atomi di C hanno ibridazione sp³ e non dà facilmente reazioni di addizione.",
    },
    "CHIM-C12-COMM-014": {
        "explanation": "Il cicloesene (C₆H₁₀) ha una struttura ad anello («ciclo») formata da 6 atomi di C con un doppio legame C=C («ene»), con 4 atomi di C ibridizzati sp³ e 2 atomi di C (quelli del doppio legame) ibridizzati sp². Come tutti gli alcheni dà reazioni di addizione elettrofila al doppio legame.",
        "options_patch": {"B": "possiede tutti i carboni ibridati sp³"},
    },
    "CHIM-C12-COMM-020": {
        "explanation": "Il benzene (idrocarburo aromatico) è formato da un anello di 6 atomi di carbonio ibridizzati sp² che giacciono su un piano.",
    },
    "CHIM-C12-COMM-022": {
        "explanation": "Il benzene è una molecola ciclica a sei termini in cui sono presenti tre doppi legami carbonio-carbonio coniugati fra loro. Tutti gli atomi di carbonio del benzene sono ibridati sp². L'etilene è l'alchene lineare più semplice in cui è presente un solo doppio legame: i due atomi di carbonio che formano il doppio legame nell'etilene sono anch'essi ibridati sp². Il benzene, a differenza degli alcheni, non dà reazioni di addizione elettrofila ma di sostituzione elettrofila aromatica, poiché l'addizione distruggerebbe il sistema aromatico stabilizzato per risonanza.",
        "options_patch": {"C": "L'ibridazione sp² degli atomi di carbonio"},
    },
    "CHIM-C12-COMM-032": {
        "explanation": "Gli alcani sono idrocarburi saturi in cui sono presenti solo legami semplici carbonio-carbonio; le ammine sono composti organici in cui uno o più gruppi alchilici/arilici sono legati a un atomo di azoto; gli alcoli sono composti organici in cui un gruppo -OH è legato ad un atomo di carbonio ibridato sp³; gli eteri sono composti organici in cui un atomo di ossigeno è legato a due gruppi alchilici/arilici; un'aldeide è un composto organico il cui gruppo funzionale presenta un doppio legame carbonio-ossigeno (C=O, carbonile).",
    },
    "CHIM-C12-NCOM-238": {
        "question": "Qual è il nome del composto ClCH₂CH₂OH?",
        "options_patch": {"A": "2-cloroetanolo", "E": "5-cloroetanolo"},
    },
    "CHIM-C13-COMM-023": {"options_patch": {"A": "adipici"}},
    "BIO-C01-COMM-044": {
        "options_patch": {
            "D": "il rapporto tra A + T e G + C è di 1 a 1",
            "E": "la somma di A + T è uguale alla somma di C + T",
        }
    },
    "BIO-C01-NCOM-058": {"options_patch": {"E": "i funghi"}},
    "BIO-C01-NCOM-192": {
        "options": {
            "A": "C,T e U,A",
            "B": "T,U e C,G",
            "C": "G,A e T,U",
            "D": "T,A e C,G",
            "E": "U,A e T,A",
        }
    },
    "BIO-C01-NCOM-212": {
        "question": "Viene condotto un esperimento per dimostrare che il DNA si replica in modo semiconservativo. Dei batteri Escherichia coli sono stati fatti crescere in un mezzo di coltura in cui la fonte di azoto contiene solamente azoto pesante (¹⁵N). Successivamente, sono stati selezionati i batteri in cui tutto l'azoto nel DNA era ¹⁵N. Questi batteri sono stati poi fatti crescere in un altro terreno, la cui sola fonte di azoto era azoto leggero (¹⁴N), e fatti dividere per tre volte. Dopo la terza divisione, qual è la percentuale di molecole di DNA che contengono sia ¹⁵N che ¹⁴N?",
    },
    "BIO-C02-NCOM-048": {
        "question": "Lo Zonkey è un ibrido sterile che nasce dall'incrocio di una zebra maschio (Equus quagga con numero cromosomico 2n = 44) e un'asina (Equus asinus con numero cromosomico 2n = 62). Qual è il numero di cromosomi presenti nelle cellule somatiche dell'ibrido?",
    },
    "BIO-C03-COMM-021": {
        "question": "Gli enzimi di restrizione ricavati da batteri sono utilizzati nelle tecniche di DNA ricombinante. L'enzima EcoRI taglia il DNA nella sequenza:\n• 5'—G|AATTC—3'\n• 3'—CTTAA|G—5'\nQuando viene usato per tagliare la sequenza:\n• 5'...ATCGAATTCGGACTAA...3'\n• 3'...TAGCTTAAGCCTGATT...5'\nquanti frammenti di DNA si formano?",
    },
    "BIO-C03-COMM-022": {
        "question": "La figura mostra le estremità coesive del DNA di pecora e del DNA umano. Le basi mancanti delle estremità sono le seguenti:",
    },
    "BIO-C04-COMM-035": {
        "explanation": "Trattandosi di una mutazione recessiva legata all'X, il fenotipo daltonico si osserva in omozigosi recessiva nelle femmine (XᵃXᵃ) e in emizigosi nei maschi (XᵃY). Detto Xᴬ l'allele selvatico e Xᵃ l'allele mutato, il padre di Francesca ha genotipo XᵃY; Francesca ha ereditato Xᵃ dal padre e Xᴬ dalla madre, per cui è eterozigote portatrice sana (XᴬXᵃ). Paolo, non essendo daltonico, ha genotipo XᴬY: trasmetterà Xᴬ alle figlie femmine e Y ai figli maschi, mentre Francesca trasmetterà Xᴬ o Xᵃ con probabilità del 50%. Pertanto un figlio maschio avrà il 50% di probabilità di essere sano (XᴬY) e il 50% di essere daltonico (XᵃY); una figlia femmina avrà il 50% di probabilità di essere sana (XᴬXᴬ) e il 50% di essere portatrice sana (XᴬXᵃ).",
    },
    "BIO-C04-COMM-048": {
        "question": "Il diagramma A della figura esprime la produzione dell'enzima beta-galattosidasi da parte di Escherichia coli, in un terreno che viene arricchito di lattosio; il diagramma B, quando dal terreno si toglie il lattosio. Tale variazione è conseguenza di:",
    },
    "BIO-C04-COMM-054": {
        "question": "La figura rappresenta l'albero genealogico di una famiglia, seguita per 3 generazioni. I quadrati e i cerchi pieni indicano, rispettivamente, maschi e femmine affetti da una malattia ereditaria. Di quale tipo di ereditarietà si tratta?",
    },
    "BIO-C04-COMM-056": {
        "question": "Si consideri il seguente albero genealogico (quadrato pieno = maschio ammalato; cerchio pieno = femmina ammalata). Esso rappresenta:",
    },
    "BIO-C04-COMM-058": {
        "question": "L'albero genealogico riportato rappresenta l'ereditarietà di un carattere dominante (quadrato pieno = maschio ammalato; cerchio pieno = femmina ammalata). Dal suo studio si può affermare che:",
    },
    "BIO-C04-COMM-080": {
        "question": "Il seguente albero genealogico riguarda la trasmissione di un carattere monofattoriale non legato al sesso (quadrato pieno = maschio malato; cerchio pieno = femmina malata; quadrato vuoto = maschio sano; cerchio vuoto = femmina sana). Si può sicuramente dedurre che:",
    },
    "BIO-C04-NCOM-135": {"options_patch": {"E": "impossibile da prevedere"}},
    "BIO-C04-NCOM-202": {"options_patch": {"E": "la produzione di una proteina più lunga del normale"}},
    "BIO-C05-COMM-005": {
        "question": "La figura si riferisce ad uno dei meccanismi di trasporto attraverso la membrana cellulare. Si può affermare che:",
    },
    "BIO-C05-COMM-006": {
        "question": "Il meccanismo rappresentato in figura si riferisce all'entrata di molecole dall'esterno all'interno di una cellula. Può essere considerato un fenomeno di:",
    },
    "BIO-C05-COMM-016": {
        "question": "Lo schema rappresenta una parte dell'ultrastruttura di una miofibrilla. La zona compresa tra le due linee verticali è detta:",
    },
    "BIO-C05-COMM-037": {
        "question": "Lo schema rappresenta in modo sintetico le molecole prodotte ad ogni tappa della glicolisi e della respirazione cellulare. Il processo indicato con la freccia 4 è definito:",
    },
    "BIO-C05-NCOM-030": {
        "question": "La figura rappresenta schematicamente due cellule vegetali, 1 e 2, ma in condizioni differenti. Quale delle seguenti affermazioni è CORRETTA?",
    },
    "BIO-C06-NCOM-124": {
        "options": {
            "A": "subunità α, β, γ",
            "B": "tre subunità α",
            "C": "due α e una δ",
            "D": "tre subunità",
            "E": "due β e una γ",
        }
    },
    "BIO-C07-NCOM-114": {
        "question": "Lo schema rappresenta il ciclo vitale di un essere umano. Il processo rappresentato con la lettera B avviene:",
    },
    "BIO-C07-NCOM-115": {
        "question": "Lo schema della figura rappresenta due processi implicati nella riproduzione della specie. Il processo A rappresenta:",
    },
    "FIS-C01-COMM-002": {
        "explanation": "Essendo la densità il rapporto tra massa e volume, il prodotto della densità per l'accelerazione di gravità equivale alla forza peso per unità di volume. Il prodotto d · g ha un valore vicino a 10⁴ nel S.I., dove la densità dell'acqua di mare è circa 10³ kg/m³ e l'accelerazione di gravità 9,8 m/s². Quindi l'unità di misura del prodotto tra queste due grandezze è (kg/m³) · (m/s²) = N/m³, in quanto 1 N = 1 kg·m/s².",
    },
    "FIS-C01-COMM-009": {
        "options": {"A": "Tutte e 4", "B": "3 sì 1 no", "C": "2 sì 2 no", "D": "1 sì 3 no", "E": "Nessuna"},
    },
    "FIS-C01-COMM-015": {
        "explanation": (
            "Esprimendo tutte le intensità delle forze in Newton si ha:\n"
            "• peso di una massa di 20 kg sulla Terra: 20 kg · 9,8 m/s² = 196 N;\n"
            "• 30 N;\n"
            "• 200 Pa · cm² = 200 N/m² · 10⁻⁴ m² = 2 · 10⁻² N;\n"
            "• 2 barie · m² = 0,2 Pa · m² = 0,2 N;\n"
            "• 100 dine = 10⁻³ N.\n"
            "La forza con intensità minore è quindi quella pari a 100 dine."
        ),
        "options_patch": {"D": "2 barie · m²"},
    },
    "FIS-C01-COMM-016": {
        "question": "Siano date tre forze ≠ 0, complanari, tutte e tre applicate all'origine di un sistema piano di assi cartesiani ortogonali, tutte e tre giacenti nel primo quadrante. Per quali dei seguenti valori dei moduli può essere nulla la loro risultante?",
        "explanation": "Per ottenere il vettore risultante si sommano dapprima i vettori F₁ ed F₂ con la regola del parallelogramma ottenendo S₁, e poi S₁ con F₃ ottenendo S₂. Poiché i tre vettori F₁, F₂ ed F₃ sono non nulli e giacciono tutti nel primo quadrante del sistema di assi cartesiani, il vettore somma giacerà anch'esso nel primo quadrante e non sarà mai nullo, qualunque siano i moduli di F₁, F₂ ed F₃.",
        "options_patch": {"B": "F₁ = 3; F₂ = 4; F₃ = 5", "C": "F₁ = 1; F₂ = 7; F₃ = 13", "E": "F₁ = 1; F₂ = 2; F₃ = 4"},
    },
    "FIS-C01-COMM-019": {
        "explanation": (
            "Il prodotto vettoriale tra due vettori a e b ha come risultato un vettore v = a × b (o a ∧ b), caratterizzato da:\n"
            "• modulo pari a |a × b| = |a| · |b| · sin θ, essendo θ l'angolo formato dai due vettori a e b;\n"
            "• direzione perpendicolare al piano individuato dai due vettori a e b;\n"
            "• verso determinato dalla regola della mano destra."
        ),
    },
    "FIS-C01-COMM-025": {
        "question": "Quale dei vettori indicati nei seguenti disegni con i numeri rispettivamente 1, 2, 3, 4, 5 rappresenta il vettore differenza a - b?",
    },
    "FIS-C02-COMM-004": {
        "explanation": "Dalla prima equazione si ricava t² = x/3, che sostituito nella seconda dà y = (4/3)x, rappresentata nel piano cartesiano da una retta passante per l'origine: il moto è quindi rettilineo. La distanza dall'origine è d = √(x² + y²) = √(9t⁴ + 16t⁴) = 5t². Poiché s(t) = 5t² = (1/2)at², il moto è uniformemente accelerato con a = 2 · 5 = 10 m/s².",
    },
    "FIS-C02-COMM-007": {
        "explanation": "La velocità del cane è v_c = 36 km/h = 10 m/s, per cui la sua legge oraria è x_c(t) = 10t. La legge oraria della pecora è x_p(t) = 90 + t. All'incontro x_c = x_p, quindi 10t = 90 + t ⇒ 9t = 90 ⇒ t = 10 s.",
    },
    "FIS-C02-COMM-020": {
        "question": "Consideriamo un tram nel percorso rettilineo fra due fermate. Se per metà percorso l'accelerazione è a = a₀ mentre nella seconda metà è a = -a₀, quale sarà il grafico della velocità? (a₀ è costante positiva; t₀, t₁, t₂ sono gli istanti in cui il tram si trova rispettivamente all'inizio, a metà e alla fine del percorso)",
        "options_patch": {"D": "Diagramma 4"},
    },
    "FIS-C03-COMM-009": {
        "explanation": "Il lavoro è definito come prodotto scalare tra la forza e lo spostamento: L = F · s = F · s · cos θ, dove θ è l'angolo tra i vettori forza e spostamento. Segue pertanto che il lavoro compiuto da una forza perpendicolare allo spostamento è nullo visto che cos(90°) = 0.",
    },
    "FIS-C03-COMM-014": {
        "question": "Su un corpo puntiforme di massa M agiscono contemporaneamente due forze (F₁ e F₂). Se agisse solo la forza F₁ l'accelerazione del corpo sarebbe a₁. Se agisse solo F₂, l'accelerazione sarebbe a₂. Ma poiché agiscono contemporaneamente F₁ e F₂, con quale accelerazione si muoverà il corpo?",
        "explanation": "La risultante delle forze F che agisce sul corpo è la somma vettoriale di F₁ ed F₂. Per il secondo principio della dinamica a = F / M: le accelerazioni a₁ ed a₂ sono dirette e orientate rispettivamente come F₁ ed F₂, e l'accelerazione risultante a è pari alla somma vettoriale a₁ + a₂.",
        "options_patch": {
            "B": "Sempre uguale alla differenza vettoriale a₁ - a₂",
            "C": "Sempre uguale ad a₁, se a₁ è maggiore di a₂",
            "D": "Sempre uguale ad a₂, se a₂ è maggiore di a₁",
            "E": "Uguale al prodotto di a₁ per a₂",
        },
    },
    "FIS-C03-COMM-018": {
        "question": "Sia data una forza costante di modulo F₁ ≠ 0 e un punto A₁ giacente sulla retta di azione di F₁, a distanza L₁ ≠ 0 dal punto di applicazione di F₁. Analogamente, sia data una seconda forza costante di modulo F₂ ≠ 0 ed un punto A₂ giacente sulla retta di azione di F₂, a distanza L₂ ≠ 0 dal punto di applicazione di F₂. Che relazione c'è tra il momento M₁ di F₁ rispetto ad A₁ e il momento M₂ di F₂ rispetto ad A₂?",
        "explanation": "Il momento di una forza F rispetto ad un polo O è M = r × F, con modulo M = r · F · sin θ, dove r · sin θ è il braccio (distanza del polo dalla retta d'azione della forza). Poiché sia A₁ sia A₂ giacciono sulle rispettive rette d'azione (θ = 0°), il braccio è nullo per entrambe e quindi M₁ = M₂ = 0.",
        "options_patch": {"C": "M₁ > M₂ se F₁ > F₂ e contemporaneamente L₁ > L₂"},
    },
    "FIS-C03-COMM-026": {
        "explanation": "Detta ω la velocità angolare dell'aviogetto, la forza centrifuga che agisce sul pilota è F_c = m · ω² · r. Essendo v = ω · r, la forza centrifuga si esprime anche come F_c = m · v² / r.",
    },
    "FIS-C03-COMM-035": {
        "explanation": "La forza centripeta necessaria è data da F_c = m · v² / r.",
    },
    "FIS-C03-COMM-039": {
        "explanation": "La legge di gravitazione universale afferma che due corpi di massa M ed m posti a distanza r si attraggono con una forza F = G · M · m / r², dove G = 6,67 × 10⁻¹¹ N·m²/kg² nel Sistema Internazionale. Nel sistema c.g.s. (1 dina = 10⁻⁵ N, 1 cm = 10⁻² m, 1 g = 10⁻³ kg) si ottiene invece G = 6,67 × 10⁻⁸ dine·cm²/g²: il valore numerico di G dipende quindi dal sistema di unità di misura scelto.",
    },
    "FIS-C03-NCOM-090": {
        "question": "Una forza f costante di intensità 4 N (N = Newton) agisce su di un punto P mentre questo si sposta di 2 m (m = metri) secondo una direzione che forma un angolo di 60° con la direzione della forza stessa, così come illustrato in figura. Calcolare in J (J = Joule) il lavoro compiuto dalla forza al termine dello spostamento.",
    },
    "FIS-C03-NCOM-184": {
        "question": "L'asta in figura è rigida, ha lunghezza l e può ruotare liberamente intorno al punto fisso O al quale è incernierata. L'asta rimane in equilibrio in posizione orizzontale sotto l'azione delle forze verticali p e q. Il punto H, dov'è applicata la forza p, ha distanza 2l/3 dall'estremo O e distanza l/3 dall'altro estremo, dov'è applicata la forza q. Quale delle relazioni seguenti può sussistere fra le intensità p e q delle forze? (Le forze sono misurate in Newton)",
    },
    "FIS-C04-COMM-006": {
        "question": "Sono dati due recipienti di forma e volume diversi (Figura) e riempiti con uno stesso tipo di liquido. Sulla superficie libera dei due recipienti si esercita la stessa pressione atmosferica. Se nei due recipienti si raggiunge la stessa altezza di liquido rispetto alle rispettive superfici di fondo (piane e orizzontali), in quale di essi la pressione sul fondo sarà maggiore?",
    },
    "FIS-C04-COMM-007": {
        "explanation": "Per il teorema di Bernoulli vale P₁ + ρgh₁ + (1/2)ρv₁² = P₂ + ρgh₂ + (1/2)ρv₂². Essendo il condotto orizzontale (h₁ = h₂) e a sezione costante (v₁ = v₂ per l'equazione di continuità), ne consegue che P₁ = P₂ per un liquido ideale.",
    },
    "FIS-C04-NCOM-061": {"options_patch": {"C": "il peso specifico del ghiaccio è superiore a quello dell'acqua"}},
    "FIS-C05-COMM-005": {
        "question": "Un gas ha un volume di 3 m³ ed una pressione di 5 atm. Se si mantiene costante la temperatura, quale volume avrà il gas se si impone una pressione di 15 atm?",
        "explanation": "Dall'equazione di stato dei gas perfetti a temperatura costante (legge di Boyle, P₁V₁ = P₂V₂) si ottiene V₂ = P₁V₁ / P₂ = (5 atm · 3 m³) / 15 atm = 1 m³.",
    },
    "FIS-C05-COMM-012": {
        "explanation": "Detto Q₁ il calore assorbito dalla sorgente a temperatura maggiore e Q₂ il calore ceduto alla sorgente a temperatura inferiore, il rendimento della macchina termica vale η = (|Q₁| - |Q₂|) / |Q₁| = (450 - 150) / 450 = 300 / 450 = 2/3.",
    },
    "FIS-C06-COMM-035": {
        "explanation": "Secondo la legge di Coulomb il modulo della forza tra due cariche Q₁ e Q₂ poste a distanza r nel vuoto è F = k · |Q₁Q₂| / r² con k = 9 × 10⁹ N·m²/C². Se r = 1 m e Q₁ = Q₂ = 1 mC = 10⁻³ C, si ottiene F = 9 × 10⁹ · (10⁻³ · 10⁻³) / 1² = 9 × 10³ N.",
    },
    "FIS-C06-COMM-036": {
        "explanation": "Il modulo della forza magnetica agente su un filo rettilineo di lunghezza L percorso da corrente i in un campo magnetico B è F = i · L · B · sin θ, dove θ è l'angolo tra filo e campo magnetico. La forza è massima quando sin θ = 1, cioè per θ = 90°.",
    },
    "FIS-C06-COMM-041": {
        "question": "Il lavoro per portare due cariche puntiformi ed uguali Q, inizialmente molto distanti fra loro, a distanza a fissata sia L. Quanto sarà il lavoro speso per portare tre cariche dello stesso tipo e valore Q ai vertici di un triangolo equilatero di lato sempre uguale ad a, anch'esse inizialmente a distanze molto grandi tra di loro?",
    },
    "FIS-C06-NCOM-037": {"options_patch": {"B": "50 kW", "D": "100 J"}},
    "FIS-C06-NCOM-039": {
        "question": "Siano M ed N due punti di un campo elettrico. Una carica puntiforme q si sposta da M ad N seguendo uno dei percorsi indicati in figura e le forze del campo compiono il lavoro L. Delle seguenti affermazioni qual è quella corretta?",
    },
    "FIS-C06-NCOM-063": {
        "question": "Nello spazio presente tra le due facce parallele di un condensatore piano a facce parallele è presente dell'aria. Il condensatore è connesso ad un generatore da 100 V a corrente continua. In seguito, un foglio di materiale dielettrico viene inserito tra le due facce parallele del condensatore. I valori di quali grandezze cambiano quando il dielettrico viene inserito tra le due facce parallele?",
    },
    "FIS-C06-NCOM-151": {
        "question": "Si consideri il ramo di un circuito mostrato in figura, ai capi del quale è applicata una differenza di potenziale pari a V. Se ciascuno dei quattro resistori esprime una resistenza pari ad R, si può affermare che:",
    },
    "FIS-C06-NCOM-171": {"options_patch": {"E": "rilucente"}},
    "FIS-C06-NCOM-191": {
        "question": "Un campo magnetico ha direzione perpendicolare al piano cartesiano mostrato in figura ed ha verso uscente. Il campo magnetico è costante al variare della coordinata spaziale y, mentre diminuisce all'aumentare della coordinata spaziale x. In quale dei seguenti casi non si induce alcuna corrente nel circuito C mostrato in figura?",
        "options_patch": {
            "A": "Facendo ruotare il circuito C intorno ad un asse perpendicolare al piano cartesiano e passante per uno dei punti del circuito",
            "B": "Facendo ruotare il circuito C intorno ad un asse solidale con il diametro parallelo all'asse y",
            "E": "Facendo ruotare il circuito C intorno ad un asse solidale con il diametro parallelo all'asse x",
        },
    },
    "FIS-C07-COMM-015": {
        "explanation": "Nel primo strato la luce trasmessa I₁ è 1/2 di quella incidente I₀ (I₁ = I₀/2). Nel secondo strato viene trasmessa la metà di questa (I₂ = I₁/2 = I₀/4), e attraverso il terzo strato passerà ancora la metà: I₃ = I₂/2 = I₀/8.",
    },
    "FIS-C07-COMP-038": {"question": "La relazione n₁ sin θ₁ = n₂ sin θ₂ è la legge di _____ :"},
    "FIS-C08-COMM-009": {"options_patch": {"C": "La differenza di massa convertita in energia"}},
}


EXACT_SUBSTRING_FIXES: List[tuple[str, str]] = [
    # Mid-word period splits across corpus
    ("sini. stra", "sinistra"),
    ("quanti. co", "quantico"),
    ("reattivi. tà", "reattività"),
    ("in in ore di quello del metallo alcalino del. lo", "minore di quello del metallo alcalino dello"),
    ("del. lo", "dello"),
    ("del. la", "della"),
    ("nel. ta", "nella"),
    ("elettro. negatività", "elettronegatività"),
    ("rispet. to", "rispetto"),
    ("possledonalo stesso numero di elettro. ni", "possiedono lo stesso numero di elettroni"),
    ("elettro. ni", "elettroni"),
    ("favori. scono", "favoriscono"),
    ("elettroni. co", "elettronico"),
    ("general. mente", "generalmente"),
    ("10 mi. di", "10 mL di"),
    ("10 ml. da", "10 mL da"),
    ("comporta. mento", "comportamento"),
    ("dissocia. zione", "dissociazione"),
    ("conserva. zione", "conservazione"),
    ("libera. zione", "liberazione"),
    ("metal. lo", "metallo"),
    ("formazio. ne", "formazione"),
    ("azoto. azoto", "azoto-azoto"),
    ("aldeidi. chetoni", "aldeidi, chetoni"),
    ("mate. cola", "molecola"),
    ("ma le cole", "molecole"),
    ("gli cera lo", "glicerolo"),
    ("eucarioti. che", "eucariotiche"),
    ("rendi. mento", "rendimento"),
    ("normal. mente", "normalmente"),
    ("vo). taggio-dipendenti", "voltaggio-dipendenti"),
    ("al. lele", "allele"),
    # Attached spurious superscripts/subscripts on Italian words
    ("possiede⁴", "possiede 4"),
    ("possiede²", "possiede 2"),
    ("pesano²", "pesano 2"),
    ("Gruppo²", "Gruppo 2"),
    ("idrogeno² quelli di cloro in HCt", "idrogeno e quelli di cloro in HCl"),
    ("acquosa²", "acquosa 2"),
    ("Sciogliere⁴", "Sciogliere 4"),
    ("ha pH³", "ha pH 3"),
    ("con acqua² 3 litri", "con acqua a 3 litri"),
    ("posizione³", "posizione 3"),
    ("Maisp³", "Mai sp³"),
    ("contengono⁴", "contengono 4"),
    ("Hardy-Weinberg⁻", "Hardy-Weinberg,"),
    ("presenti²", "presenti 2"),
    ("TATA-less²", "TATA-less?"),
    ("ATP-dipendente⁻", "ATP-dipendente?"),
    ("per³ generazioni", "per 3 generazioni"),
    ("produce²", "produce 2"),
    ("Trasporta²", "Trasporta 2"),
    ("Trasporta³", "Trasporta 3"),
    ("Caz⁺", "Ca²⁺"),
    ("preparano²", "preparano 2"),
    ("N-glicosilazioni⁻", "N-glicosilazioni?"),
    ("caspasi³", "caspasi 3"),
    ("per² ore", "per 2 ore"),
    ("percorrere³", "percorrere 3"),
    ("percorso³", "percorso 3"),
    # Chemical ions, formulas & scientific notation
    ("Cu?*", "Cu²⁺"),
    ("Cu**", "Cu²⁺"),
    ("Cu'*", "Cu²⁺"),
    ("Cu2⁴", "Cu²⁺"),
    ("Fe?*", "Fe²⁺"),
    ("Fe**", "Fe²⁺"),
    ("Fe*'", "Fe²⁺"),
    ("Fe?'", "Fe²⁺"),
    ("Fe3*", "Fe³⁺"),
    ("Fe*3", "Fe³⁺"),
    ("Zn?*", "Zn²⁺"),
    ("Zn**", "Zn²⁺"),
    ("Ca?*", "Ca²⁺"),
    ("Ca**", "Ca²⁺"),
    ("Mn?*", "Mn²⁺"),
    ("Mn*'", "Mn²⁺"),
    ("Pb?*", "Pb²⁺"),
    ("Co?*", "Co²⁺"),
    ("Na*/K*", "Na⁺/K⁺"),
    ("Na‘/K*", "Na⁺/K⁺"),
    ("Na°*", "Na⁺"),
    ("K*", "K⁺"),
    ("Ag*", "Ag⁺"),
    ("[H*]", "[H⁺]"),
    ("(H']", "[H⁺]"),
    ("[OH7]", "[OH⁻]"),
    ("0H7", "OH⁻"),
    ("CIO⁻”", "ClO⁻"),
    ("CLo*", "ClO⁺"),
    ("H,S0,", "H₂SO₄"),
    ("H2S0,", "H₂SO₄"),
    ("H₂SO₄/_,)", "H₂SO₄(aq)"),
    ("H202", "H₂O₂"),
    ("C,(H20),", "Cₙ(H₂O)ₙ"),
    ("02/H20", "O₂/H₂O"),
    ("02₂ CO2", "O₂, CO₂"),
    ("CO: e H20", "CO₂ e H₂O"),
    ("H20", "H₂O"),
    ("FADH2", "FADH₂"),
    ("CO2", "CO₂"),
    ("NHj", "NH₄⁺"),
    ("HCt", "HCl"),
    ("s*p*", "s²p⁵"),
    ("f, s₄ d", "f, s, d"),
    ("s, f₄ g. aq", "s, l, g, aq"),
    ("1s₄ 2s", "1s, 2s"),
    ("A₄ B e e uguali", "A, B e C uguali"),
    ("A₄ B e D", "A, B e D"),
    ("fasi G,, S, G,", "fasi G₁, S, G₂"),
    ("5'-3\"", "5'-3'"),
    ("5' → 3\"", "5' → 3'"),
    ("(*4He)", "(⁴He)"),
    ("Brensted-Lowry", "Brønsted-Lowry"),
    ("BrgnstedLowry", "Brønsted-Lowry"),
    ("Bransted-Lowry", "Brønsted-Lowry"),
    ("Briénsted", "Brønsted"),
    ("Brensted", "Brønsted"),
    ("Bronsted", "Brønsted"),
    ("Schrédinger", "Schrödinger"),
    # Word merges & Italian OCR typos
    ("Ilcitocromoc", "Il citocromo c"),
    ("ilcitocromoc", "il citocromo c"),
    ("Nelterzoliveilo", "Nel terzo livello"),
    ("Ilcitoscheletro", "Il citoscheletro"),
    ("IGPCRsono", "I GPCR sono"),
    ("IGPCRlegano", "I GPCR legano"),
    ("Dopola ", "Dopo la "),
    ("Essendoil ", "Essendo il "),
    ("Essendol’", "Essendo l'"),
    ("Essendol'", "Essendo l'"),
    ("Forzae ", "Forza e "),
    ("Vavambraccio", "L'avambraccio"),
    ("fsecondo ", "f secondo "),
    ("lilavoro", "Il lavoro"),
    ("perionizzarsi", "per ionizzarsi"),
    ("9 mali", "9 moli"),
    ("le mali ", "le moli "),
    ("0,001 mali ", "0,001 moli "),
    ("due mali ", "due moli "),
    ("Quante mali ", "Quante moli "),
    ("in cul ", "in cui "),
    ("Gii alcani", "Gli alcani"),
    ("altre agli isotopi", "oltre agli isotopi"),
    ("uno stessa ", "uno stesso "),
    ("una stesso ", "uno stesso "),
    ("\\eutra", "neutra"),
    ("\\asica", "basica"),
    ("{i numero", "il numero"),
    ("in 100 mi ", "in 100 mL "),
    ("te forze ", "le forze "),
    ("Sein una ", "Se in una "),
    ("Eun ormone", "È un ormone"),
    ("Eunacido", "È un acido"),
    ("Datele seguenti", "Date le seguenti"),
    ("Sela patologia", "Se la patologia"),
    ("In troni", "Introni"),
    ("da ila fotolisi", "dalla fotolisi"),
    ("IT DNA", "Il DNA"),
    ("It DNA", "Il DNA"),
    ("LmRNA", "L'mRNA"),
    ("LrRNA", "L'rRNA"),
    ("LATP", "L'ATP"),
    ("LNOè", "L'NO è"),
    ("LaSRP", "La SRP"),
    ("ItRNA ", "I tRNA "),
    ("Gliesoni", "Gli esoni"),
    ("Gliidruri", "Gli idruri"),
    ("Glielettroliti", "Gli elettroliti"),
    ("Glieterotrofi", "Gli eterotrofi"),
    ("Itlegame", "Il legame"),
    ("Illegamea", "Il legame a"),
    ("IHegame", "Il legame"),
    ("Wlegame fosfodiesterica", "Il legame fosfodiesterico"),
    ("Il legame ionica:", "Il legame ionico:"),
    ("dallo scandio (numero atomico = 21) alto zinco", "dallo scandio (numero atomico = 21) allo zinco"),
    ("è pari 2:", "è pari a:"),
    ("giucosio", "glucosio"),
    ("clorofilia", "clorofilla"),
    ("luraciie", "l'uracile"),
    ("desossiribonucteici", "desossiribonucleici"),
    ("ribonucitetci", "ribonucleici"),
    ("desassiribosio", "desossiribosio"),
    ("gliceroto", "glicerolo"),
    ("idrotisi", "idrolisi"),
    ("idrolist", "idrolisi"),
    ("ammeniaca", "ammoniaca"),
    ("ammontaca", "ammoniaca"),
    ("itirossido", "idrossido"),
    ("tornasote", "tornasole"),
    ("diiuisce", "diluisce"),
    ("diluiril fino a 10L", "diluire fino a 10 L"),
    ("motarita", "molarità"),
    ("deducibiti", "deducibili"),
    ("possiblie", "possibile"),
    ("cpportuna", "opportuna"),
    ("intermoiecolare", "intermolecolare"),
    ("dipalo", "dipolo"),
    ("protonl", "protoni"),
    ("potonio", "polonio"),
    ("diftuoro", "difluoro"),
    ("paliadio", "palladio"),
    ("aicallno", "alcalino"),
    ("slilclo", "silicio"),
    ("doroformio", "cloroformio"),
    ("cioruro", "cloruro"),
    ("miltilitri", "millilitri"),
    ("entaipia", "entalpia"),
    ("eiettronegatività", "elettronegatività"),
    ("conlugata", "coniugata"),
    ("tbridati", "ibridati"),
    ("elettrafila", "elettrofila"),
    ("clettrofila", "elettrofila"),
    ("ammincacido", "amminoacido"),
    ("maitosio", "maltosio"),
    ("cellobloso", "cellobiosio"),
    ("protelna", "proteina"),
    ("altungamento", "allungamento"),
    ("superavvoigimento", "superavvolgimento"),
    ("residio", "residuo"),
    ("coloumb", "coulomb"),
    ("bequerel", "becquerel"),
    ("Seauna ", "Se a una "),
    ("Qualèil ", "Qual è il "),
    ("Qualè ", "Qual è "),
    ("Sesirimane ", "Se si rimane "),
    ("Sesiidralizza ", "Se si idrolizza "),
    ("Seunmulo ", "Se un mulo "),
    ("Fatleta ", "l'atleta "),
    (" @ stato fornito", " è stato fornito"),
    ("@una forma", "è una forma"),
]


def format_list_linebreaks(text: str) -> str:
    """Ensure every bullet item (`•`) and every multi-item numbered/lettered statement list starts cleanly on a new line."""
    if not text:
        return text

    # Normalize inline bullets (`•`, `▪`, `◦`) onto their own clean lines when preceded by non-newline text
    text = re.sub(r"(?<!\n)\s*([•▪◦])\s*", lambda m: f"\n• ", text)
    text = text.lstrip("\n")

    # Multi-item inline numbered lists `1. ... 2. ...` (only when BOTH `1.` and `2.` exist on single line!)
    if "\n" not in text and re.search(r"(?:[:\?])\s*1\.\s*\S.+\s2\.\s*\S", text):
        text = re.sub(r"(?<=[:\?])\s*(?=1\.\s*\S)", "\n", text, count=1)
        text = re.sub(r"(?<!\n)\s+(?=[2-6]\.\s*[A-Za-zÀ-ÿ0-9\(])", "\n", text)
        # Preserve final trailing question sentence on its own line (`... 3. ... Quale/Quali ...?`)
        text = re.sub(r"\s+(?=(?:Qual[ei]|Scegliere|Indicare)\b[^?]+\?$)", "\n", text)

    # Multi-item inline parenthesized lists `1) ... 2) ...` or `(1) ... (2) ...` or `a) ... b) ...`
    if "\n" not in text and re.search(r"(?:[:\?])\s*1\)\s*\S.+\s2\)\s*\S", text):
        text = re.sub(r"(?<=[:\?])\s*(?=1\)\s*\S)", "\n", text, count=1)
        text = re.sub(r"(?<!\n)\s+(?=[2-6]\)\s*\S)", "\n", text)

    if "\n" not in text and re.search(r":\s*\(1\)\s*\S.+\(2\)\s*\S", text):
        text = re.sub(r"(?<=:)\s*(?=\(1\)\s*\S)", "\n", text, count=1)
        text = re.sub(r";?\s+(?=\([2-5]\)\s*\S)", ";\n", text)

    if "\n" not in text and re.search(r":\s*a\)\s*\S.+;\s*b\)\s*\S", text):
        text = re.sub(r"(?<=:)\s*(?=a\)\s*\S)", "\n", text, count=1)
        text = re.sub(r";\s*(?=[b-e]\)\s*\S)", ";\n", text)

    # Clean up spaces on each line without collapsing `\n`!
    lines = [re.sub(r"[ \t]{2,}", " ", ln).strip() for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln)


def _clean_text_field(val: str) -> str:
    if not val:
        return val
    s = val
    for old, new in EXACT_SUBSTRING_FIXES:
        if old in s:
            s = s.replace(old, new)
    s = apply_extra_text_cleanups(s)
    # Leading OCR `li ` / `fl] ` at start of sentence -> `Il `
    s = re.sub(r"^(?:li|fl\])\s+([a-zà-ÿ])", lambda m: "Il " + m.group(1), s)
    s = re.sub(r"(?<=\.\s)li\s+([a-zà-ÿ])", lambda m: "Il " + m.group(1), s)
    s = format_list_linebreaks(s)
    return s


def apply_round3_remediation(items: List[dict]) -> Dict[str, int]:
    stats = {"items_updated": 0, "bogus_figure_refs_removed": 0, "multiline_formatted": 0}
    for r in items:
        cid = r["id"]
        before = (r["question"], repr(r.get("options")), r.get("explanation"), repr(r.get("figure_files")))

        # 1. Strip bogus text-only figures from item record
        if r.get("figure_files"):
            kept = [fn for fn in r["figure_files"] if fn not in BOGUS_TEXT_ONLY_FIGURES]
            stats["bogus_figure_refs_removed"] += len(r["figure_files"]) - len(kept)
            r["figure_files"] = kept

        # 2. Apply card-level exact overrides first (ROUND3 base + pixel-verified EXTRA overrides)
        for ov in (ROUND3_CARD_OVERRIDES.get(cid), EXTRA_CARD_OVERRIDES.get(cid)):
            if ov:
                if "question" in ov:
                    r["question"] = ov["question"]
                if "explanation" in ov:
                    r["explanation"] = ov["explanation"]
                if "options" in ov:
                    r["options"] = dict(ov["options"])
                if "options_patch" in ov and r.get("options"):
                    for k, v in ov["options_patch"].items():
                        r["options"][k] = v

        # 3. Apply deterministic corpus-wide cleanups & list line-break formatting
        r["question"] = _clean_text_field(r["question"])
        if r.get("options"):
            for k in list(r["options"].keys()):
                r["options"][k] = _clean_text_field(r["options"][k])
            if r.get("answer") in r["options"]:
                r["answer_text"] = r["options"][r["answer"]]
        if r.get("explanation"):
            r["explanation"] = _clean_text_field(r["explanation"])

        if "\n" in r["question"] or "\n" in (r.get("explanation") or ""):
            stats["multiline_formatted"] += 1

        after = (r["question"], repr(r.get("options")), r.get("explanation"), repr(r.get("figure_files")))
        if before != after:
            stats["items_updated"] += 1

    return stats
