"""Human-verified visual transcription overrides for 2D stacked fractions,
atomic/nuclear isotopes, orbital electron configurations, inline options, and
Greek/unit symbols inspected directly from canonical 300-DPI textbook renders.

Every entry below was read directly from the rendered page image (`bp_XXX.png`)
of `Eserciziario Unico per il Semestre Filtro`. Keys are `(subject_code, chapter_num, kind, qnum)`.
"""

from __future__ import annotations

VISUAL_MCQ_OVERRIDES: dict[tuple[str, int, str, int], dict] = {
    # ==================== CHIMICA CAP 1 ====================
    ("CHIM", 1, "commentati", 2): {
        "q": (
            "Quale/i fra le seguenti affermazioni è/sono vera/e? "
            "• A₁ l'idrogeno è l'unico elemento a cui si attribuiscono nomi differenti per alcuni suoi isotopi; "
            "• A₂ in chilogrammi, della massa di atomo è compresa fra 10⁻²¹ e 10⁻²⁹; "
            "• A₃ ad eccezione dell'idrogeno tutti gli atomi degli altri elementi chimici hanno in egual numero elettroni e neutroni."
        ),
        "opts": {"A": "A₂ e A₃", "B": "A₁ e A₂", "C": "Tutte", "D": "A₁ e A₃", "E": "Nessuna"},
    },
    ("CHIM", 1, "non_commentati", 33): {
        "opts": {"A": "Solo 3", "B": "Solo 1 e 2", "C": "Solo 2 e 3", "D": "Solo 1", "E": "Solo 2"},
    },
    ("CHIM", 1, "non_commentati", 36): {
        "opts": {"A": "Riga 2", "B": "Riga 3", "C": "Riga 4", "D": "Riga 5", "E": "Riga 1"},
    },
    ("CHIM", 1, "non_commentati", 44): {
        "q": "Un atomo ha la configurazione elettronica che termina in s². Qual è il suo numero atomico?",
    },
    ("CHIM", 1, "non_commentati", 56): {
        "q": "Qual è la massa atomica di ²³⁸₉₂U?",
    },
    ("CHIM", 1, "non_commentati", 70): {
        "opts": {
            "A": "³⁰₂₇Co; ³¹₂₇Co; ³³₂₇Co",
            "B": "⁵⁷₂₇Co; ⁵⁸₂₇Co; ⁶⁰₂₇Co",
            "C": "²⁷₃₀Co; ²⁷₃₁Co; ²⁷₃₃Co",
            "D": "²⁷₅₇Co; ²⁷₅₈Co; ²⁷₆₀Co",
            "E": "³⁰₂₇Co; ³¹₂₇Co; ⁶⁰₂₇Co",
        },
    },
    ("CHIM", 1, "non_commentati", 118): {
        "q": "Indicare cosa hanno in comune l'isotopo ⁵⁸Fe e l'isotopo ⁵⁹Co:",
    },

    # ==================== CHIMICA CAP 2 ====================
    ("CHIM", 2, "commentati", 6): {
        "q": "Il peso molecolare del saccarosio C₁₂H₂₂O₁₁ è 342 (u.m.a.), ciò implica che in 34,2 g di questa sostanza le molecole sono:",
    },
    ("CHIM", 2, "commentati", 8): {
        "opts": {
            "A": "appartengono al secondo gruppo della tavola periodica",
            "B": "possiedono lo stesso numero di protoni",
            "C": "appartengono allo stesso periodo della tavola periodica",
            "D": "sono dei non metalli",
            "E": "possiedono lo stesso numero di elettroni nei rispettivi livelli esterni",
        },
    },
    ("CHIM", 2, "commentati", 14): {
        "q": "Quanti elettroni, protoni e neutroni ha, nell'ordine, lo ione O²⁻? Tener presente che la massa atomica è 16 u.m.a., e il numero atomico è 8.",
        "opts": {"A": "17, 8, 8", "B": "16, 8, 8", "C": "10, 8, 8", "D": "17, 8, 9", "E": "18, 8, 8"},
    },
    ("CHIM", 2, "commentati", 22): {
        "q": "La struttura elettronica 1s² 2s² 2p⁶ 3s² 3p⁴ è caratteristica di:",
    },
    ("CHIM", 2, "commentati", 28): {
        "q": "A quale elemento neutro, non eccitato, appartiene la struttura elettronica esterna 2s² 2p²?",
        "opts": {"A": "Fe", "B": "O", "C": "C", "D": "N", "E": "F"},
    },
    ("CHIM", 2, "commentati", 29): {
        "q": "Qual è la struttura elettronica fondamentale dello ione F⁻?",
        "opts": {
            "A": "1s² 2s² 2p⁶ 3s¹",
            "B": "1s² 2s² 3s¹ 2p⁶",
            "C": "1s² 2s² 2p⁵ 3s²",
            "D": "1s² 2s² 2p⁶",
            "E": "1s² 2s² 2p⁶ 2d¹",
        },
    },
    ("CHIM", 2, "commentati", 33): {
        "q": "I gas nobili (ad eccezione dell'elio) hanno tutti configurazione elettronica esterna di tipo:",
        "opts": {"A": "sp⁶", "B": "sp⁸", "C": "s²p⁴", "D": "s²p⁶", "E": "s²p⁸"},
    },
    ("CHIM", 2, "commentati", 40): {
        "q": "La configurazione elettronica dello ione Li⁺ è rappresentata da:",
        "opts": {"A": "1s² 2s¹", "B": "1s¹ 2s²", "C": "1s²", "D": "1s¹", "E": "1s¹ 2s¹ 2p¹"},
    },
    ("CHIM", 2, "non_commentati", 25): {
        "q": "Lo ione O²⁻ ha la stessa configurazione elettronica:",
        "opts": {
            "A": "dello ione F⁻",
            "B": "dello ione Ca²⁺",
            "C": "dello ione S²⁻",
            "D": "dell'atomo di Na",
            "E": "dell'atomo di Mg",
        },
    },
    ("CHIM", 2, "non_commentati", 28): {
        "opts": {"A": "6", "B": "2", "C": "4", "D": "6", "E": "8"},  # Verbatim printed typo on bp.30: A. 6 and D. 6
    },
    ("CHIM", 2, "non_commentati", 31): {
        "q": "Qual è la configurazione elettronica dell'elemento X che ha numero atomico 16?",
        "opts": {
            "A": "[Ne] 3s² 3pₓ¹ 3pᵧ¹",
            "B": "[Ne] 3s² 3pₓ¹ 3pᵧ¹ 2p_z¹",
            "C": "[Ne] 3s² 3pₓ² 3pᵧ¹ 3p_z¹",
            "D": "[Ne] 3s² 3pₓ² 3pᵧ²",
            "E": "[Ne] 3s² 3pₓ² 3pᵧ² 3p_z¹",
        },
    },
    ("CHIM", 2, "non_commentati", 32): {
        "q": "La configurazione elettronica del Cloro (n° atomico 17) è rappresentata da:",
        "opts": {
            "A": "1s² 2s² 2p⁶ 3s²",
            "B": "1s² 2s² 2p⁶",
            "C": "1s² 2s² 2p³",
            "D": "1s² 2s² 2p⁶ 3s² 3p⁵",
            "E": "1s² 2s² 2p⁶ 3s³ 3p⁴",
        },
    },
    ("CHIM", 2, "non_commentati", 34): {
        "q": "Qual è la carica dello ione più stabile dell'elemento che ha configurazione elettronica 1s² 2s² 2p⁶ 3s² 3p¹?",
    },
    ("CHIM", 2, "non_commentati", 38): {
        "q": "Il Na ha numero atomico 11. La sua configurazione elettronica è:",
        "opts": {
            "A": "1s² 2s² 2p⁶ 3s¹",
            "B": "1s 2s 2p 3s 3p",
            "C": "1s² 2s² 2p⁶ 3d",
            "D": "1s² 1p⁶ 2s² 2p",
            "E": "1s 2p 3p² 3s³",
        },
    },
    ("CHIM", 2, "non_commentati", 39): {
        "opts": {
            "A": "1s²2s²2p⁶2d⁴",
            "B": "1s²2s²2p⁸3s²",
            "C": "1s²2s²2p⁶3s²3p⁷",
            "D": "1s²2s²2p⁶3s⁴3p²",
            "E": "1s²2s²2p⁶3s²3p⁶4s²",
        },
    },
    ("CHIM", 2, "non_commentati", 40): {
        "q": "Qual è la configurazione elettronica del catione Al³⁺, sapendo che il numero atomico di Al è 13?",
        "opts": {
            "A": "1s²2s²2p⁶",
            "B": "1s²2s²2p⁴3s²",
            "C": "1s²2s²2p⁶3s²3p¹",
            "D": "1s²2s²2p⁶3s²3p⁶",
            "E": "1s²2s²2p⁶3s²",
        },
    },
    ("CHIM", 2, "non_commentati", 41): {
        "q": "Una delle seguenti configurazioni elettroniche atomiche non è possibile. Quale?",
        "opts": {
            "A": "1s² 2s² 2p⁵",
            "B": "1s² 2s² 2p⁶",
            "C": "1s² 2s² 2d¹",
            "D": "1s² 2s² 2p⁶ 3s² 3p⁶ 4s² 3d⁵",
            "E": "1s¹",
        },
    },
    ("CHIM", 2, "non_commentati", 42): {
        "q": "Quale elemento presenta configurazione elettronica 1s² 2s¹?",
    },

    # ==================== CHIMICA CAP 3 ====================
    ("CHIM", 3, "commentati", 15): {
        "q": "Quale elemento corrisponde alla configurazione elettronica 1s² 2s² 2p⁴?",
    },
    ("CHIM", 3, "non_commentati", 3): {
        "opts": {
            "A": "g (grammo)",
            "B": "nessuna delle risposte è corretta",
            "C": "g/eV (grammo/elettronvolt)",
            "D": "μg (microgrammo)",
            "E": "g · cm⁻³",
        },
    },
    ("CHIM", 3, "non_commentati", 4): {
        "opts": {
            "A": "4,4 × 1,67 × 10⁻²⁷ kg",
            "B": "22 × 1,67 × 10⁻²⁷ kg",
            "C": "44 × 1,67 × 10⁻²⁷ kg",
            "D": "44 × 167 × 10⁻¹⁷ kg",
            "E": "44 × 0,167 × 10⁻³⁵ kg",
        },
    },
    ("CHIM", 3, "non_commentati", 10): {
        "opts": {"A": "Solo 1 e 2", "B": "Solo 1", "C": "Solo 2", "D": "Solo 3", "E": "Solo 1 e 3"},
    },
    ("CHIM", 3, "non_commentati", 23): {
        "q": "22,0 g di un gas occupano 5,60 dm³ a temperatura e pressione standard (STP). Qual è la massa molare del gas? [Volume molare del gas = 22,4 dm³ a STP]",
        "opts": {
            "A": "108 g mol⁻¹",
            "B": "44,0 g mol⁻¹",
            "C": "88,0 g mol⁻¹",
            "D": "5,50 g mol⁻¹",
            "E": "176 g mol⁻¹",
        },
    },
    ("CHIM", 3, "non_commentati", 24): {
        "q": "Il numero di Avogadro rappresenta il numero delle molecole contenute in:",
        "opts": {
            "A": "22,4 L di N₂ in condizioni standard",
            "B": "1 g di qualsiasi sostanza a 1 °C",
            "C": "1 kg di qualsiasi sostanza a 0 °C",
            "D": "1 dm³ di acqua a 4 °C",
            "E": "1 L di aria a 0 °C",
        },
    },
    ("CHIM", 3, "non_commentati", 25): {
        "q": "In una mole di idrogeno atomico ci sono circa:",
        "opts": {
            "A": "6 · 10⁻²³ elettroni e 6 · 10²³ protoni",
            "B": "6 · 10²³ elettroni e 6 · 10⁻²³ protoni",
            "C": "6 · 10³ elettroni e 6 · 10⁻²³ protoni",
            "D": "6 · 10⁻²³ elettroni e 6 · 10⁻²³ protoni",
            "E": "6 · 10²³ elettroni e 6 · 10²³ protoni",
        },
    },
    ("CHIM", 3, "non_commentati", 26): {
        "opts": {"A": "in un grammo", "B": "in una mole", "C": "in un dm³", "D": "in un m³", "E": "in un cm³"},
    },
    ("CHIM", 3, "non_commentati", 38): {
        "opts": {
            "A": "Una mole di acqua contiene una mole di atomi di idrogeno",
            "B": "Una mole di acqua contiene 6,022 · 10²³ atomi",
            "C": "Una mole di acqua contiene 6 · 10²³ atomi",
            "D": "La massa molare dell'acqua è 18,01 g",
            "E": "La massa di un atomo di ¹²C è esattamente 18,0000 g",
        },
    },
    ("CHIM", 3, "non_commentati", 39): {
        "opts": {"A": "10²³", "B": "6,02 · 10⁹", "C": "6,02 · 10²³", "D": "6,02 · 10⁻²³", "E": "6,02 · 10⁻³"},
    },
    ("CHIM", 3, "non_commentati", 40): {
        "q": "Il numero di atomi di Idrogeno contenuti in una mole di H₂O è:",
        "opts": {"A": "4", "B": "18,069 · 10²³", "C": "6,023 · 10²³", "D": "2", "E": "12,046 · 10²³"},
    },
    ("CHIM", 3, "non_commentati", 41): {
        "q": "La massa atomica relativa dell'uranio ²³⁸₉₂U è 238,0508. Qual è la massa in grammi di una mole di ²³⁸₉₂U?",
        "opts": {"A": "238,0508 g", "B": "233,99 g", "C": "6,022137 · 10²³ g", "D": "395,2229 · 10⁻²⁴ g", "E": "N g"},
    },
    ("CHIM", 3, "non_commentati", 46): {
        "opts": {
            "A": "contengono lo stesso numero di particelle",
            "B": "contengono sempre lo stesso numero di atomi",
            "C": "hanno la stessa massa",
            "D": "contengono sempre 6,02 × 10²³ particelle",
            "E": "contengono un numero di particelle proporzionale al numero atomico dei gas",
        },
    },
    ("CHIM", 3, "non_commentati", 47): {
        "opts": {
            "A": "100 mol di acqua",
            "B": "1,8 × 10⁻³ mol di acqua",
            "C": "1,8 × 10³ mol di acqua",
            "D": "22,4 mol di acqua",
            "E": "55,5 mol di acqua",
        },
    },
    ("CHIM", 3, "non_commentati", 49): {
        "opts": {
            "A": "Nessuna delle risposte è corretta",
            "B": "58 g di NaBr",
            "C": "58 g di Na₂O",
            "D": "58 g di NO",
            "E": "58 g di NaCl",
        },
    },
    ("CHIM", 3, "non_commentati", 58): {
        "q": "A quante moli corrispondono 4,0 ml di un composto avente massa molecolare pari a 50 u.m.a. e densità 1,25 g/ml?",
        "opts": {"A": "0,01", "B": "0,1", "C": "0,2", "D": "0,003", "E": "0,5"},
    },
    ("CHIM", 3, "non_commentati", 61): {
        "opts": {"A": "III", "B": "I", "C": "II", "D": "V", "E": "IV"},
    },
    ("CHIM", 3, "non_commentati", 65): {
        "q": "A quale gruppo appartiene l'elemento O?",
    },
    ("CHIM", 3, "non_commentati", 90): {
        "opts": {"A": "I", "B": "Br", "C": "Cl", "D": "B", "E": "F"},
    },
    ("CHIM", 3, "non_commentati", 99): {
        "opts": {"A": "Li⁺", "B": "Ca²⁺", "C": "La³⁺", "D": "Cl⁻", "E": "Mg²⁺"},
    },
    ("CHIM", 3, "non_commentati", 110): {
        "q": "Gli elementi del gruppo VIIA hanno configurazione elettronica esterna:",
        "opts": {"A": "s", "B": "s²p³", "C": "s²p", "D": "sp²", "E": "s²p⁵"},
    },
    ("CHIM", 3, "non_commentati", 116): {
        "q": "Il Na ha numero atomico 11. La sua configurazione elettronica è:",
        "opts": {
            "A": "1s²2s²2p⁶3s¹",
            "B": "1s²2s²2p⁶3d",
            "C": "1s²1p⁶2s²2p",
            "D": "1s2p⁴s²p³2d",
            "E": "1s2s2p3s3p",
        },
    },
    ("CHIM", 3, "non_commentati", 144): {
        "q": "Indicare la configurazione elettronica possibile per l'elemento M che dà facilmente lo ione M⁺:",
        "opts": {
            "A": "2s²",
            "B": "1s² 2s² 2p⁶ 3s²",
            "C": "1s² 2s² 2p⁶ 3s¹",
            "D": "1s² 2s² 2p⁶",
            "E": "1s² 2s² 2p⁵",
        },
    },
    ("CHIM", 3, "non_commentati", 153): {
        "q": "Qual è la configurazione elettronica esterna del Calcio?",
        "opts": {"A": "4s²", "B": "5s²", "C": "6s²", "D": "2s²", "E": "3s²"},
    },

    # ==================== CHIMICA CAP 4–13 ====================
    ("CHIM", 4, "commentati", 6): {"q": "Qual è la struttura spaziale di una molecola con ibridazione sp³?"},
    ("CHIM", 4, "non_commentati", 64): {
        "q": "Lo ione ammonio (NH₄⁺) e il metano (CH₄) hanno in comune:",
        "opts": {
            "A": "la struttura planare",
            "B": "la carica elettrica",
            "C": "l'ibridazione sp³",
            "D": "le spiccate proprietà acide",
            "E": "il carattere nettamente acido",
        },
    },
    ("CHIM", 4, "non_commentati", 69): {"q": "Gli orbitali ibridi sp³ sono in numero di:"},
    ("CHIM", 4, "non_commentati", 70): {"opts": {"A": "d²sp⁶", "B": "d²sp³", "C": "sp²", "D": "sp", "E": "sp³"}},
    ("CHIM", 4, "non_commentati", 71): {"opts": {"A": "sp²", "B": "sp", "C": "sp³", "D": "1s²2s²2p²", "E": "1s²2p³"}},
    ("CHIM", 4, "non_commentati", 73): {"q": "Nell'ibridazione sp²:"},
    ("CHIM", 4, "non_commentati", 78): {"q": "Qual è la struttura spaziale di una molecola con ibridazione sp²?"},
    ("CHIM", 4, "non_commentati", 82): {"opts": {"A": "sp - sp² - sp³", "B": "solo sp³", "C": "solo sp", "D": "solo sp²", "E": "d²sp³"}},
    ("CHIM", 4, "non_commentati", 86): {"q": "Quale delle seguenti sostanze presenta ibridazione sp³ e ha angoli diversi dal valore di 109,5°?"},
    ("CHIM", 5, "non_commentati", 19): {
        "q": "2 kg di ossigeno vengono introdotti in una bombola della capacità di 10 dm³. Il volume occupato dal gas è di:",
        "opts": {"A": "2 dm³", "B": "10 dm³", "C": "5 dm³", "D": "8 dm³", "E": "20 dm³"},
    },
    ("CHIM", 6, "commentati", 10): {
        "opts": {
            "A": "Δt_c = 1,86 × 10⁻⁴ × 5",
            "B": "Δt_c = 1,86 × 10⁻⁴ × 6",
            "C": "Δt_c = 1,86 × 10⁻⁴ × 7",
            "D": "Δt_c = 1,86 × 10⁻⁴ × 3",
            "E": "Δt_c = 1,86 × 10⁻⁴ × 2",
        },
    },
    ("CHIM", 6, "non_commentati", 45): {
        "opts": {"A": "5,0 × 10⁻³ M", "B": "1,5 × 10⁻³ M", "C": "1,0 × 10⁻³ M", "D": "2,0 × 10⁻³ M", "E": "0,5 · 10⁻³ M"},
    },
    ("CHIM", 6, "non_commentati", 50): {
        "opts": {"A": "4,2 · 10²²", "B": "1,6 · 10²³", "C": "9,8 · 10²⁴", "D": "6,0 · 10²³", "E": "8,8 · 10²²"},
    },
    ("CHIM", 7, "commentati", 17): {
        "q": "Nella reazione: Zn + FeCl₂ → ZnCl₂ + Fe, lo ione che si riduce è:",
        "opts": {"A": "Zn²⁺", "B": "Fe²⁺", "C": "Cl⁻", "D": "Fe³⁺", "E": "nessuno, si ha solo ossidazione"},
    },
    ("CHIM", 8, "commentati", 1): {
        "q": "Un catalizzatore è:",
        "opts": {
            "A": "un composto che accelera una reazione consumandosi",
            "B": "un composto che si aggiunge per impedire l'inquinamento",
            "C": "un composto che accelera una reazione senza consumarsi",
            "D": "un composto che inibisce una reazione consumandosi",
            "E": "un composto che inibisce una reazione senza consumarsi",
        },
    },
    ("CHIM", 8, "non_commentati", 1): {
        "q": (
            "Per la reazione R → P, il grafico riporta come varia la concentrazione del reagente R "
            "in funzione del tempo a partire dalla concentrazione iniziale [R]₀ = 1,0 M. "
            "Indicare a quale tempo la velocità di reazione assume il valore massimo."
        ),
        "opts": {
            "A": "al tempo t₃ = 3 min",
            "B": "mai: la velocità della reazione è costante",
            "C": "al tempo t₁ = 1 min",
            "D": "al tempo t₀ = 0 min",
            "E": "al tempo t₂ = 2 min",
        },
    },
    ("CHIM", 8, "non_commentati", 2): {
        "opts": {"A": "v = k[NO]²[O₂]", "B": "v = k[NO]²[O₂]²", "C": "v = k[NO]²", "D": "v = k[NO][O₂]/[NO₂]²", "E": "v = k[NO][O₂]"},
    },
    ("CHIM", 9, "commentati", 1): {
        "opts": {"A": "Nessuna delle risposte è corretta", "B": "HPO₃", "C": "H₃PO₄", "D": "P₂O₅", "E": "P₂O₃"},
    },
    ("CHIM", 9, "non_commentati", 78): {
        "q": "Nella reazione: Zn + FeCl₂ → ZnCl₂ + Fe, lo ione che si riduce è:",
        "opts": {"A": "Zn⁺⁺", "B": "Fe⁺⁺⁺", "C": "Cl⁻", "D": "Cl⁺", "E": "Fe⁺⁺"},
    },
    ("CHIM", 9, "non_commentati", 85): {
        "opts": {
            "A": "passa da Fe a Fe²⁺",
            "B": "passa da Fe³⁺ a Fe³⁺⁺",
            "C": "passa da Fe²⁺ a Fe³⁺",
            "D": "passa da Fe a Fe³⁺",
            "E": "passa da Fe³⁺ a Fe²⁺",
        },
    },
    ("CHIM", 9, "non_commentati", 114): {
        "opts": {"A": "nessuno, si ha solo ossidazione", "B": "Ca²⁺", "C": "Mg²⁺", "D": "Cl⁻", "E": "tutti"},
    },
    ("CHIM", 10, "commentati", 15): {
        "opts": {
            "A": "Può esistere un composto di formula F₂O₅",
            "B": "Tutti gli alogeni posseggono orbitali d vuoti",
            "C": "Esiste un composto di formula Br₂O₅",
            "D": "Esiste un composto di formula Cl₂O₇",
            "E": "Solo il fluoro possiede orbitali d vuoti",
        },
    },
    ("CHIM", 10, "non_commentati", 40): {"opts": {"A": "Li₂O₂", "B": "Li₄O", "C": "LiO₂", "D": "Li₂O", "E": "LiO"}},
    ("CHIM", 10, "non_commentati", 44): {"opts": {"A": "AlOH", "B": "Al(OH)₃", "C": "Al₃(OH)₃", "D": "Al₂HO₃", "E": "Al₂O₃"}},
    ("CHIM", 10, "non_commentati", 46): {"opts": {"A": "PbO", "B": "Pb(OH)₂", "C": "PbO₂", "D": "Pb(OH)₄", "E": "PbH₂O"}},
    ("CHIM", 10, "non_commentati", 64): {"opts": {"A": "C⁴⁻", "B": "CO²⁻", "C": "CO₃²⁻", "D": "CO₂", "E": "CO₂⁺"}},
    ("CHIM", 10, "non_commentati", 86): {"opts": {"A": "ZnCr₂O₇", "B": "Zn(ClO₄)₂", "C": "Zn(ClO₂)₂", "D": "Zn(OH)₂", "E": "Zn₂Cl₂"}},
    ("CHIM", 11, "commentati", 32): {
        "q": "Secondo Brönsted e Lowry, l'acido coniugato della base HPO₄²⁻ è:",
        "opts": {"A": "H₂PO₃", "B": "H₂PO₄⁻", "C": "HPO₄⁻", "D": "HPO₄²⁺", "E": "H₃PO₄"},
    },
    ("CHIM", 11, "non_commentati", 18): {"opts": {"A": "NO₃⁻", "B": "NO₂⁻", "C": "HCO₃⁻", "D": "SO₃⁻", "E": "NOH₂⁺"}},
    ("CHIM", 11, "non_commentati", 31): {"opts": {"A": "H₂O", "B": "HCO₃⁻", "C": "NH₃", "D": "H₂PO₄⁻", "E": "SO₄²⁻"}},
    ("CHIM", 11, "non_commentati", 49): {"opts": {"A": "10⁻⁷ M", "B": "10⁻³ M", "C": "7 M", "D": "10⁻⁵ M", "E": "10⁻¹¹ M"}},
    ("CHIM", 11, "non_commentati", 50): {"opts": {"A": "10¹⁴ M", "B": "10⁻⁷ M", "C": "10⁻¹⁴ M", "D": "10⁻² M", "E": "nessuna delle altre risposte è corretta"}},
    ("CHIM", 11, "non_commentati", 55): {"opts": {"A": "10⁻¹⁰ M", "B": "nessuna delle altre risposte è corretta", "C": "6 · 10⁻⁷ M", "D": "10⁻⁸ M", "E": "10⁻⁵ M"}},
    ("CHIM", 11, "non_commentati", 58): {"opts": {"A": "1,0 × 10⁻²", "B": "1,0 × 10⁻⁴", "C": "1,0 × 10⁻⁸", "D": "1,0 × 10⁻¹⁰", "E": "1,0 × 10⁻⁶"}},
    ("CHIM", 11, "non_commentati", 64): {"opts": {"A": "10⁻¹² M", "B": "10⁻¹⁴ M", "C": "10¹² M", "D": "10⁻² M", "E": "10⁻⁷ M"}},
    ("CHIM", 11, "non_commentati", 66): {"opts": {"A": "10⁻³", "B": "10⁻⁷", "C": "10⁻¹⁴", "D": "10⁻¹¹", "E": "10⁻¹²"}},
    ("CHIM", 11, "non_commentati", 91): {"opts": {"A": "10⁹ M", "B": "10⁻¹¹ M", "C": "10⁻⁹ M", "D": "10⁻³ M", "E": "10³ M"}},
    ("CHIM", 11, "non_commentati", 107): {"opts": {"A": "[H⁺] = 11 M", "B": "[H⁺] = 10⁻³ M", "C": "[H⁺] = 10⁻⁷ M", "D": "[H⁺] = 10⁻⁵ M", "E": "[H⁺] = 10⁻¹⁰ M"}},
    ("CHIM", 11, "non_commentati", 108): {"opts": {"A": "7,3 M", "B": "10⁻¹⁴ M", "C": "7,3¹⁰ M", "D": "10⁻⁷,³ M", "E": "10⁷ M"}},
    ("CHIM", 11, "non_commentati", 118): {"opts": {"A": "[OH⁻] = 10⁻⁸ M", "B": "[OH⁻] = 10⁻¹³ M", "C": "[OH⁻] = 1⁻¹³ M", "D": "[OH⁻] = 10⁻¹ M", "E": "[OH⁻] = 1 M"}},
    ("CHIM", 11, "non_commentati", 120): {"opts": {"A": "10⁻¹² M", "B": "10⁻² M", "C": "10¹² M", "D": "10⁻¹'² M", "E": "10² M"}},
    ("CHIM", 11, "non_commentati", 121): {"opts": {"A": "3", "B": "2", "C": "1", "D": "-4", "E": "4"}},
    ("CHIM", 11, "non_commentati", 137): {"opts": {"A": "10", "B": "4", "C": "0", "D": "0,4", "E": "-4"}},
    ("CHIM", 11, "non_commentati", 147): {"opts": {"A": "5 × 10³", "B": "5 × 10⁻²", "C": "10⁻³", "D": "5 × 10⁻⁴", "E": "10³"}},
    ("CHIM", 12, "non_commentati", 28): {"opts": {"A": "sp³d", "B": "d²sp³", "C": "sp", "D": "sp³", "E": "sp²"}},
    ("CHIM", 12, "non_commentati", 36): {"opts": {"A": "Tutti sp²", "B": "Uno sp³ e gli altri due sp²", "C": "Tutti sp³", "D": "Due sp e uno sp²", "E": "Uno sp² e gli altri due sp³"}},
    ("CHIM", 12, "non_commentati", 40): {"opts": {"A": "sp²", "B": "sp²d²", "C": "sp³", "D": "sp", "E": "sp²d"}},
    ("CHIM", 12, "non_commentati", 44): {
        "q": "Quando un composto è definito saturo?",
        "opts": {
            "A": "Quando contiene almeno un legame multiplo",
            "B": "Quando non contiene legami singoli C-C",
            "C": "Quando non contiene doppi e tripli legami",
            "D": "Quando contiene almeno un doppio legame",
            "E": "Quando contiene almeno un triplo legame",
        },
    },
    ("CHIM", 12, "non_commentati", 74): {"opts": {"A": "sp²d", "B": "sp³", "C": "s²p²", "D": "sp²", "E": "sp"}},
    ("CHIM", 12, "non_commentati", 103): {"opts": {"A": "C₂H₆", "B": "H₃-CH₂", "C": "C₂H₂", "D": "H₂C=CH₂", "E": "H₃C-CH₃"}},
    ("CHIM", 12, "non_commentati", 117): {"opts": {"A": "C₆H₆", "B": "C₃H₆", "C": "C₅H₁₂", "D": "C₁₀₀H₂₂₀", "E": "C₂H₂₀"}},
    ("CHIM", 12, "non_commentati", 161): {
        "q": "Date le rappresentazioni delle strutture molecolari riportate in figura si può affermare che:",
        "opts": {
            "A": "A è un alchene, B un alcano e C un alchino",
            "B": "A è un alchino, B un alcano e C un alchene",
            "C": "A è un alcano, B un alchino e C un alchene",
            "D": "A è un alchino, B un alchene e C un alcano",
            "E": "A è un alcano, B un alchene e C un alchino",
        },
    },
    ("CHIM", 12, "non_commentati", 163): {"opts": {"A": "C₆H₅COOH", "B": "CH₃CO₁₃OH", "C": "C₆H₁₃COOH", "D": "CH₃COOH", "E": "HCOOH"}},
    ("CHIM", 12, "non_commentati", 173): {"opts": {"A": "C₂H₂O", "B": "C₂H₆O", "C": "C₄H₄O₂", "D": "C₄HO₂", "E": "C₃H₄O"}},
    ("CHIM", 12, "non_commentati", 221): {"opts": {"A": "sp³d²", "B": "sp²", "C": "sp³", "D": "sp", "E": "spd"}},
    ("CHIM", 12, "non_commentati", 246): {
        "opts": {"A": "Dipropil estere", "B": "Difenil etere", "C": "Fenilpropil etere", "D": "Dipropil etere", "E": "Propenale"},
    },

    # ==================== BIOLOGIA ====================
    ("BIO", 1, "commentati", 3): {
        "q": "Lo schema mostra l'azione idrolitica di un enzima su di una molecola. Se A è il saccarosio, B e C saranno:",
    },
    ("BIO", 1, "commentati", 34): {
        "q": "Lo schema rappresenta il ciclo dell'ATP. La freccia 1) rappresenta:",
        "opts": {
            "A": "la condensazione dell'ATP",
            "B": "l'idrolisi dell'ATP",
            "C": "l'energia utile per compiere una reazione esoergonica",
            "D": "l'energia prodotta dalle reazioni endoergoniche",
            "E": "l'energia prodotta dalle reazioni esoergoniche",
        },
    },
    ("BIO", 4, "non_commentati", 130): {
        "q": (
            "L'albero genealogico riportato si riferisce ad una famiglia in cui compare il carattere "
            "“incapacità di distinguere alcuni colori” dovuto ad un allele recessivo che si trova sul cromosoma X. "
            "Dal suo esame si può dedurre che:"
        ),
        "opts": {
            "A": "la donna F₁-₃ è sicuramente portatrice del gene alterato",
            "B": "il figlio F₂-₁ diventerà malato",
            "C": "la donna P-₁ è sicuramente omozigote",
            "D": "la figlia F₂-₂ è sicuramente omozigote",
            "E": "la donna F₁-₂ è sicuramente eterozigote",
        },
    },
    ("BIO", 4, "non_commentati", 153): {
        "q": "Nell'albero genealogico di una famiglia si sono verificati casi di una malattia genetica recessiva, non legata al sesso. Si può escludere che nasca un bambino affetto da tale malattia:",
        "opts": {
            "A": "se il genitore è omozigote dominante",
            "B": "se i nonni del nascituro erano sani",
            "C": "se entrambi i genitori sono eterozigoti",
            "D": "se uno degli zii del nascituro è sano",
            "E": "se entrambi i genitori non manifestano la malattia",
        },
    },
    ("BIO", 7, "commentati", 22): {
        "q": "Lo schema rappresenta i successivi stadi della spermatogenesi. Se una delle cellule D ha 19 cromosomi, la cellula B avrà:",
    },
    ("BIO", 7, "non_commentati", 14): {
        "q": (
            "Alcune cellule prelevate dalla cute sono state coltivate su un substrato nutritivo. "
            "Tramite un'opportuna tecnica si è potuto misurare la quantità di DNA che una cellula di questa coltura "
            "presentava al passare del tempo, come riporta il grafico. Si può dedurre che la cellula dopo:"
        ),
        "opts": {
            "A": "4 ore è in anafase",
            "B": "6 ore ha iniziato la meiosi",
            "C": "14 ore muore",
            "D": "6 ore è morta",
            "E": "6 ore ha iniziato la mitosi",
        },
    },
    ("BIO", 3, "non_commentati", 87): {
        "q": (
            "La sequenza nucleotidica AUGCCAUUGGAAGAGA codifica per gli amminoacidi Met-Pro-Trp-Lys-Arg. "
            "Una mutazione che provocasse la sostituzione del nono nucleotide contenente guanina con un nucleotide "
            "contenente adenina (G → A) comporterebbe:"
        ),
        "opts": {
            "A": "la terminazione della catena proteica con l'amminoacido Pro perché la nuova tripletta che si verrebbe a formare è una tripletta di stop",
            "B": "la terminazione della catena proteica con l'amminoacido Met perché la tripletta che si verrebbe a formare è una tripletta di stop",
            "C": "nessuna modifica grazie alla ridondanza del codice genetico",
            "D": "la sostituzione dell'amminoacido Trp nella catena proteica",
            "E": "la perdita dell'amminoacido Lys",
        },
    },
    ("BIO", 5, "commentati", 99): {
        "opts": {"A": "COPII", "B": "Clatrina", "C": "Caveolina", "D": "Dinamina", "E": "COPI"},
    },
    ("BIO", 6, "commentati", 33): {
        "opts": {"A": "G_q", "B": "Ras", "C": "G_i", "D": "G_s", "E": "Gβγ"},
    },
    ("CHIM", 12, "non_commentati", 61): {
        "opts": {"A": "Benzene", "B": "Propilene", "C": "CH₄", "D": "C₂H₄", "E": "C₃H₆"},
    },
    ("CHIM", 12, "non_commentati", 176): {
        "opts": {
            "A": "R-COO⁻ + H₃O⁺",
            "B": "R-COO⁻ + H₃O⁻",
            "C": "R-CHO + H₃O₂",
            "D": "R-CHO + H₂O₂",
            "E": "R-COO₂ + H₂O₂",
        },
    },
    ("FIS", 1, "non_commentati", 56): {
        "opts": {"A": "10⁹ F", "B": "10¹⁰ F", "C": "10⁻¹² F", "D": "10⁻³ F", "E": "10⁻⁹ F"},
    },
    ("FIS", 6, "non_commentati", 83): {
        "q": (
            "Un elettrone possiede una carica di 1,6 · 10⁻¹⁹ coulomb. Se una corrente di 1,6 ampere attraversa "
            "un conduttore per 1 secondo, questo è attraversato da un numero di elettroni il cui logaritmo decimale è:"
        ),
        "opts": {"A": "-19", "B": "19", "C": "22", "D": "190", "E": "1,9"},
    },
    ("BIO", 6, "non_commentati", 180): {
        "opts": {"A": "PIP₂", "B": "PIP₃", "C": "DAG", "D": "IP₃", "E": "Ca²⁺"},
    },

    # ==================== FISICA ====================
    ("FIS", 1, "commentati", 13): {
        "opts": {"A": "1 watt = 10⁷ dine", "B": "1 watt = 10⁵ dine/s", "C": "1 watt = 1 J/min", "D": "1 watt = 10⁷ erg", "E": "1 watt = 10⁷ erg/s"},
    },
    ("FIS", 1, "commentati", 23): {
        "opts": {"A": "1,6 · 10⁻⁷ cm", "B": "6,4 · 10⁻⁷ m", "C": "1,6 · 10⁻³⁷ cm", "D": "28 · 10⁻⁴ cm", "E": "1,6 · 10⁷ cm"},
    },
    ("FIS", 1, "commentati", 25): {"opts": {"A": "1", "B": "2", "C": "3", "D": "4", "E": "5"}},
    ("FIS", 1, "non_commentati", 6): {"opts": {"A": "1 N/m²", "B": "10 N", "C": "1 atm", "D": "10 kg/cm²", "E": "1 N/m"}},
    ("FIS", 1, "non_commentati", 7): {"opts": {"A": "m²s", "B": "kg · m²/s²", "C": "m/s", "D": "kg · m/s²", "E": "kg · m · s"}},
    ("FIS", 1, "non_commentati", 10): {"opts": {"A": "m⁻¹", "B": "sec⁻²", "C": "hertz", "D": "volt", "E": "secondi"}},
    ("FIS", 1, "non_commentati", 34): {"opts": {"A": "cm²/s", "B": "m³/s", "C": "m/s", "D": "cm³/s", "E": "m²/s"}},
    ("FIS", 1, "non_commentati", 46): {"opts": {"A": "10⁻⁴ m", "B": "10⁴ m", "C": "10⁻⁶ m", "D": "10⁶ m", "E": "10⁶ m"}},  # Verbatim book typo: D & E both 10⁶ m
    ("FIS", 1, "non_commentati", 51): {"opts": {"A": "10⁻¹²", "B": "10⁻⁹", "C": "10⁻¹⁸", "D": "10⁻¹⁵", "E": "10⁻²⁴"}},
    ("FIS", 1, "non_commentati", 55): {"opts": {"A": "10⁻³ A", "B": "10⁻⁹ A", "C": "10⁻⁵ A", "D": "10⁻² A", "E": "10⁻⁶ A"}},
    ("FIS", 1, "non_commentati", 63): {"opts": {"A": "m/s", "B": "nessuna delle altre risposte è corretta", "C": "m²/s²", "D": "m² · s", "E": "m²/s"}},
    ("FIS", 2, "commentati", 4): {
        "q": "Un punto si muove nel piano xy, le sue proiezioni sugli assi cartesiani seguono le leggi: { x = 3t² ; y = 4t² }. Quale delle seguenti affermazioni relative al moto del punto è vera?",
    },
    ("FIS", 2, "commentati", 9): {
        "q": "Un'automobile si muove con velocità v = v₀ + at; in cui: v₀ = 6 m/s; a = 2 m/s²; t misurato in s. Il grafico dello spazio percorso in funzione del tempo, nel caso di spazio iniziale uguale a zero, rappresenta:",
    },
    ("FIS", 2, "commentati", 19): {"opts": {"A": "[T⁻¹]", "B": "[M L⁻¹]", "C": "[L² T⁻³]", "D": "[L]", "E": "[L⁻¹]"}},
    ("FIS", 2, "non_commentati", 69): {
        "q": "Quanto vale l'accelerazione in funzione di x di una particella che si muove di moto armonico con legge x = A sen ωt ?",
        "opts": {"A": "−ω²x", "B": "(−ω² / 2)x", "C": "ω²x", "D": "(−ω² / 4)x", "E": "(−ω / 4)x"},
    },
    ("FIS", 2, "non_commentati", 73): {
        "q": "Un quarzo compie 10⁷ oscillazioni al secondo. Qual è il periodo di oscillazione?",
        "opts": {"A": "10⁷ Hz", "B": "10⁻⁷ Hz", "C": "10⁻⁷ s", "D": "10 s", "E": "10⁷ s"},
    },
    ("FIS", 3, "commentati", 5): {"opts": {"A": "v", "B": "1.2 v", "C": "1.44 v", "D": "v / 1.2", "E": "v / 1.44"}},
    ("FIS", 3, "commentati", 35): {"opts": {"A": "2,4 N", "B": "12 N", "C": "5 N", "D": "24 N", "E": "6 N"}},
    ("FIS", 3, "non_commentati", 23): {"opts": {"A": "5 m/s²", "B": "0,1 m/s²", "C": "0,5 m/s²", "D": "5 m/s²", "E": "1 m/s²"}},  # Verbatim book typo on bp.712
    ("FIS", 3, "non_commentati", 36): {
        "opts": {
            "A": "T = (m₁ sin α + m₂)g",
            "B": "T = m₂g sin α",
            "C": "T = m₁g",
            "D": "T = m₁g sin α",
            "E": "T = m₂g cos α",
        },
    },
    ("FIS", 3, "non_commentati", 67): {"opts": {"A": "N m² kg⁻²", "B": "kg m⁻²", "C": "m² kg⁻¹", "D": "N m⁻² kg²", "E": "kg³ m⁻²"}},
    ("FIS", 3, "non_commentati", 74): {"opts": {"A": "M · L² · T³", "B": "M⁻² · L²", "C": "M · L · T⁻²", "D": "M² · L⁻²", "E": "M⁻¹ · L³ · T⁻²"}},
    ("FIS", 4, "commentati", 2): {"opts": {"A": "P₁ = P₂ = P₃", "B": "P₃ > P₂ > P₁", "C": "P₃ > P₁ > P₂", "D": "P₂ > P₁ > P₃", "E": "P₃ > P₁ = P₂"}},
    ("FIS", 4, "non_commentati", 73): {"opts": {"A": "1,96 · 10² N", "B": "1,96 · 10³ N", "C": "1,96 · 10⁴ N", "D": "1,96 · 10⁶ N", "E": "1,96 · 10⁵ N"}},
    ("FIS", 6, "commentati", 20): {"opts": {"A": "5 V/m", "B": "è necessario precisare il verso dei vettori componenti", "C": "2 V/m", "D": "3/4 V", "E": "7 V/m"}},
    ("FIS", 6, "commentati", 42): {
        "q": (
            "Tre resistenze R₁, R₂ e R₃ sono inserite in un circuito, tra i punti P e Q, come indicato nel grafico. "
            "Qual è la resistenza totale del tratto di circuito PQ, supponendo trascurabile la resistenza dei tratti di filo "
            "conduttore che connettono le resistenze con i punti P e Q e le resistenze tra loro?"
        ),
        "opts": {
            "A": "R = R₁ + (R₂ · R₃)/(R₂ + R₃)",
            "B": "R = R₁ + 1/R₂ + 1/R₃",
            "C": "R = R₁ + R₂ + R₃",
            "D": "R = 1/R₁ + 1/R₂ + 1/R₃",
            "E": "R = 1/R₁ + (R₂ + R₃)/(R₂ · R₃)",
        },
    },
    ("FIS", 6, "commentati", 50): {
        "opts": {"A": "W = iV²/t", "B": "W = i²Rt", "C": "W = i²t/R", "D": "W = iVt/R", "E": "W = tV²/R"},
    },
    ("FIS", 6, "non_commentati", 30): {"opts": {"A": "1,66 · 10⁶ V", "B": "1,403 · 10⁶ V", "C": "1,5 · 10⁶ V", "D": "10,88 · 10⁶ V", "E": "10,57 · 10⁶ V"}},
    ("FIS", 6, "non_commentati", 41): {
        "opts": {
            "A": "Il potenziale elettrostatico vale 7,2 V",
            "B": "Il potenziale elettrostatico vale 7,2 · 10⁹ V",
            "C": "Il potenziale elettrostatico vale 7,2 × 10³ V",
            "D": "Il potenziale elettrostatico vale 7,2 × 10⁵ V",
            "E": "Il potenziale elettrostatico vale 7,2 × 10⁴ V",
        },
    },
    ("FIS", 6, "non_commentati", 47): {
        "q": (
            "Si consideri un conduttore cavo, di forma sferica e raggio R, sulla cui superficie è presente una carica elettrica +Q. "
            "All'interno del conduttore è praticato il vuoto, pertanto la costante dielettrica vale ε₀. "
            "Detta r la distanza dal centro della superficie sferica del conduttore, quanto vale il campo elettrico per r < R?"
        ),
        "opts": {"A": "0", "B": "Q / (4πε₀r)", "C": "Q / (4πε₀r²)", "D": "Q / (4πε₀R²)", "E": "Q / (4πε₀R)"},
    },
    ("FIS", 6, "non_commentati", 53): {"opts": {"A": "C = Q · V", "B": "C = Q", "C": "C = V/Q", "D": "C = 1/2 · Q · V²", "E": "C = Q/V"}},
    ("FIS", 6, "non_commentati", 74): {"opts": {"A": "16 μF", "B": "0,33 μF", "C": "8 μF", "D": "3 μF", "E": "4 μF"}},
    ("FIS", 6, "non_commentati", 80): {"opts": {"A": "10³ J", "B": "10⁻¹ J", "C": "10⁻³ J", "D": "10⁻³ kJ", "E": "10³ kJ"}},
    ("FIS", 6, "non_commentati", 87): {"opts": {"A": "V", "B": "R", "C": "V²⁰", "D": "V²", "E": "R²"}},
    ("FIS", 6, "non_commentati", 90): {
        "q": "Una corrente elettrica I passa, per un tempo t, in un conduttore ai cui estremi esiste una differenza di potenziale V. L'energia dissipata è:",
        "opts": {"A": "V/I", "B": "V/It", "C": "VIt", "D": "VI", "E": "It"},
    },
    ("FIS", 6, "non_commentati", 93): {
        "q": "Indicando con R la resistenza elettrica di un conduttore, con V la differenza di potenziale applicata agli estremi e con I la corrente che lo percorre, la potenza dissipata per effetto Joule è:",
        "opts": {"A": "P = V / I", "B": "P = V · R · I", "C": "P = V · I", "D": "P = V · R", "E": "P = I · R²"},
    },
    ("FIS", 6, "non_commentati", 95): {
        "opts": {"A": "V · I²", "B": "V²/R", "C": "V · R²", "D": "I⁴/V", "E": "I²/V"},
    },
    ("FIS", 6, "non_commentati", 101): {"opts": {"A": "4P", "B": "P", "C": "P²", "D": "2P", "E": "P/2"}},
    ("FIS", 6, "non_commentati", 106): {
        "q": "Un ferro da stiro elettrico ha una resistenza R = 20 Ω e assorbe una corrente I = 5 A. Calcolare il calore sviluppato nel tempo Δt = 1 minuto.",
    },
    ("FIS", 6, "non_commentati", 111): {
        "q": "Un filo di alluminio ha una sezione di 1,0 × 10⁻⁶ m². Il filo è lungo 16,0 cm ed ha una resistenza pari a 4,0 × 10⁻³ Ω. Qual è la resistività dell'alluminio di cui è fatto questo filo?",
        "opts": {"A": "2,5 × 10⁻⁶ Ω·m", "B": "2,5 × 10⁻⁸ Ω·m", "C": "2,5 × 10⁻⁵ Ω·m", "D": "6,4 × 10⁴ Ω·m", "E": "6,4 × 10⁶ Ω·m"},
    },
    ("FIS", 6, "non_commentati", 128): {
        "q": (
            "Quando due resistenze elettriche (rispettivamente uguali a R e 4R) sono collegate in serie, "
            "la resistenza equivalente della combinazione è pari a 50 Ω. Se le medesime resistenze fossero "
            "collegate in parallelo, quale sarebbe la resistenza equivalente?"
        ),
        "opts": {"A": "12 Ω", "B": "10 Ω", "C": "32 Ω", "D": "50 Ω", "E": "8 Ω"},
    },
    ("FIS", 6, "non_commentati", 141): {
        "q": (
            "Due resistori, di resistenza R e 4R, sono connessi in serie in modo da ottenere una resistenza totale di 100 Ω. "
            "Questi due resistori vengono ora connessi tra di loro in parallelo in un circuito a corrente continua. "
            "Qual è ora la resistenza risultante?"
        ),
        "opts": {"A": "20 Ω", "B": "25 Ω", "C": "400 Ω", "D": "16 Ω", "E": "625 Ω"},
    },
    ("FIS", 6, "non_commentati", 144): {
        "q": "Due resistori sono posti in parallelo in un circuito alimentato da un generatore che eroga una differenza di potenziale V_g. Indicare QUALE di queste affermazioni è certamente SBAGLIATA.",
        "opts": {
            "A": "La corrente nei resistori è proporzionale alla differenza di potenziale erogata dal generatore",
            "B": "Il rapporto tra le correnti nei due resistori è I₁/I₂ = R₁/R₂",
            "C": "Il rapporto tra le correnti nei due resistori è I₁/I₂ = R₂/R₁",
            "D": "La corrente è maggiore nel resistore che presenta resistenza minore",
            "E": "La differenza di potenziale è la stessa ai capi dei due resistori [refuso di stampa p.814: doppia riga E con R = R₁ + R₂ + R₃]",
        },
    },
    ("FIS", 6, "non_commentati", 150): {
        "q": "La resistenza elettrica di un filo conduttore di lunghezza l e sezione S:",
        "opts": {
            "A": "aumenta al diminuire di l",
            "B": "diminuisce all'aumentare di l",
            "C": "aumenta all'aumentare di S",
            "D": "resta costante all'aumentare di l",
            "E": "diminuisce all'aumentare di S",
        },
    },
    ("FIS", 6, "non_commentati", 154): {
        "q": "Una resistenza R₁ = 5 Ω e una seconda resistenza R₂ ignota, collegate in serie, dissipano 10 W se collegate a un generatore di tensione continua da 20 V. Quanto vale R₂?",
        "opts": {"A": "Circa 5,7 Ω", "B": "1 Ω", "C": "15 Ω", "D": "35 Ω", "E": "Circa 3,3 Ω"},
    },
    ("FIS", 6, "non_commentati", 156): {
        "q": (
            "Un circuito è composto da un generatore di corrente continua, che fornisce una d.d.p. pari a 1 V, "
            "e da 5 resistori identici posti in parallelo fra di loro, di resistenza pari a 5 Ω ciascuno: "
            "qual è la potenza istantanea assorbita in totale dai resistori?"
        ),
    },
    ("FIS", 6, "non_commentati", 158): {
        "q": (
            "Due batterie di forza elettromotrice ε₁ = 20 V ed ε₂ = 8 V e resistenza interna r₁ = 0,5 Ω e r₂ = 0,2 Ω "
            "sono poste in serie e connesse fra loro tramite i morsetti negativi. In serie con loro è posta una resistenza "
            "R = 5,3 Ω. Si vuole conoscere il valore della corrente nel circuito."
        ),
    },
    ("FIS", 6, "non_commentati", 180): {
        "opts": {"A": "D", "B": "D²", "C": "D¹/²", "D": "D⁻¹", "E": "D⁴"},
    },
    ("FIS", 6, "non_commentati", 186): {
        "q": "La forza per unità di lunghezza che si esercita tra i due fili rappresentati in figura è di 8 · 10⁻⁶ N/m. Quanto vale la corrente I₂?",
        "opts": {"A": "4,2 A", "B": "4 A", "C": "6,4 A", "D": "5,5 A", "E": "6,25 A"},
    },
    ("FIS", 6, "non_commentati", 188): {
        "q": "Una spira circolare piana di area S uguale a 1 dm² poggia su una superficie orizzontale. Un campo magnetico, diretto orizzontalmente, ha intensità che cresce ogni secondo di 0,1 tesla. La f.e.m. indotta ai capi della spira vale:",
        "opts": {"A": "0,001 V", "B": "0 V", "C": "10 V", "D": "0,1 V", "E": "0,01 V"},
    },
    ("FIS", 7, "commentati", 3): {
        "q": "Un fotone è caratterizzabile con la frequenza f o con la lunghezza d'onda λ. Detta h la costante di Planck:",
        "opts": {
            "A": "h · f è l'energia del fotone",
            "B": "λ è direttamente proporzionale a f",
            "C": "h dipende dalla frequenza",
            "D": "la velocità di propagazione nel vuoto è funzione di f",
            "E": "se f supera il centimetro abbiamo a che fare con raggi gamma",
        },
    },
    ("FIS", 7, "commentati", 15): {
        "opts": {"A": "Nessuna", "B": "3/5", "C": "1/15", "D": "(1/5)³", "E": "(4/5)³"},
    },
    ("FIS", 7, "non_commentati", 27): {
        "opts": {"A": "P_m = 0,25 mW", "B": "P_m = 250 mW", "C": "P_m = 2,5 mW", "D": "P_m = 25 mW", "E": "P_m = 2,5 W"},
    },
    ("FIS", 7, "non_commentati", 49): {
        "opts": {
            "A": "Il 50% di quella iniziale",
            "B": "Il 70% di quella iniziale",
            "C": "Zero",
            "D": "Il 100% di quella iniziale",
            "E": "Il 25% di quella iniziale",
        },
    },
    ("FIS", 7, "non_commentati", 51): {
        "q": (
            "Un fascio di luce monocromatica incide su una fenditura sottile. Nella figura di diffrazione "
            "il primo minimo si trova ad un angolo θ rispetto alla posizione centrale. Quali delle seguenti "
            "affermazioni sono vere? 1) Riducendo la larghezza della fenditura, si riduce l'angolo θ. "
            "2) Aumentando la lunghezza d'onda della luce, aumenta l'angolo θ. "
            "3) Aumentando la frequenza della luce, aumenta l'angolo θ. "
            "4) Si vedono zone di luce anche ad angoli maggiori di θ."
        ),
    },
    ("FIS", 8, "non_commentati", 17): {
        "q": "Perché ⁷₃Li e ⁷₄Be sono detti “isobari”?",
    },
    # --- Realigned & formula-verified Completamento & MCQ stems ---
    ("CHIM", 2, "completamento", 1): {"q": "Gli _____ sono costituiti da particelle subatomiche: protoni, neutroni ed elettroni."},
    ("CHIM", 2, "completamento", 4): {"q": "Il _____ è una particella priva di carica elettrica situata nel nucleo."},
    ("CHIM", 2, "completamento", 5): {"q": "Il _____ contiene protoni e neutroni ed è la parte centrale e massiva dell'atomo."},
    ("CHIM", 2, "completamento", 6): {"q": "La massa atomica è concentrata quasi interamente nel _____ ."},
    ("CHIM", 2, "completamento", 7): {"q": "Il _____ è il numero di protoni presenti nel nucleo di un atomo."},
    ("CHIM", 2, "completamento", 8): {"q": "Il _____ corrisponde alla somma di protoni e neutroni."},
    ("CHIM", 2, "completamento", 9): {"q": "Un _____ è un atomo dello stesso elemento con diverso numero di neutroni."},
    ("CHIM", 2, "completamento", 10): {"q": "Il peso atomico è la _____ ponderata delle masse degli isotopi naturali di un elemento."},
    ("CHIM", 2, "completamento", 11): {"q": "Gli _____ occupano regioni dello spazio dette orbitali."},
    ("CHIM", 2, "completamento", 12): {"q": "Un _____ è una regione in cui la probabilità di trovare un elettrone è elevata."},
    ("CHIM", 2, "completamento", 13): {"q": "Gli _____ si raggruppano in sottogusci indicati con le lettere s, p, d, f."},
    ("CHIM", 2, "completamento", 14): {"q": "I gusci elettronici sono livelli energetici principali numerati dall'interno verso l'_____ ."},
    ("CHIM", 2, "completamento", 15): {"q": "Gli elettroni di valenza sono quelli presenti nel guscio più _____ e determinano le proprietà chimiche."},
    ("CHIM", 2, "completamento", 16): {"q": "L'energia degli elettroni è _____, ossia assume solo valori discreti."},
    ("CHIM", 2, "completamento", 17): {"q": "Un _____ è una particella di luce emessa o assorbita durante le transizioni elettroniche."},
    ("CHIM", 2, "completamento", 21): {"q": "Il _____ stabilisce che in un orbitale possono stare al massimo due elettroni con spin opposto."},
    ("CHIM", 3, "non_commentati", 10): {
        "q": (
            "Il cloro ha due isotopi con masse atomiche relative di 35 u e 37 u. Un campione di CH₂Cl₂ ha una massa "
            "molecolare relativa di 86 u. Quale/i tra questi di seguito potrebbe/ro essere il campione? "
            "1. Una miscela 50% di CH₂(³⁵Cl)₂ e 50% di CH₂(³⁷Cl)₂ "
            "2. 100% di CH₂³⁵Cl³⁷Cl "
            "3. Una miscela 25% di CH₂(³⁵Cl)₂ e 75% di CH₂³⁵Cl³⁷Cl "
            "[Massa atomica relativa: H = 1 u, C = 12 u]"
        ),
    },
    ("CHIM", 4, "completamento", 16): {"q": "Gli ossidi metallici sono composti ionici tra un _____ e l'ossigeno."},
    ("CHIM", 4, "completamento", 17): {"q": "I _____ binari sono composti ionici privi di idrogeno e ossigeno."},
    ("CHIM", 4, "completamento", 18): {"q": "Gli _____ metallici si formano dal legame tra un metallo e lo ione H⁻."},
    ("CHIM", 9, "non_commentati", 91): {
        "q": (
            "Quale/i delle seguenti reazioni è/sono delle ossidoriduzioni? "
            "1. Cl₂(aq) + 2 Br⁻(aq) → Br₂(aq) + 2 Cl⁻(aq) "
            "2. Cl₂(aq) + H₂O(l) → H⁺(aq) + HOCl(aq) + Cl⁻(aq) "
            "3. HCl(aq) + H₂O(l) → H₃O⁺(aq) + Cl⁻(aq)"
        ),
    },
    ("CHIM", 10, "completamento", 10): {"q": "L'_____ (CO₂) è un tipico ossido acido."},
    ("CHIM", 10, "completamento", 25): {"q": "L'_____ (Na₂O) è un tipico ossido basico."},
    ("CHIM", 10, "completamento", 26): {"q": "L'_____ (CaO) è noto come calce viva."},
    ("CHIM", 10, "completamento", 31): {"q": "La formula generale di un _____ è M(OH)ₙ."},
    ("CHIM", 11, "completamento", 15): {"q": "L'_____ (HCl) è un tipico acido forte."},
    ("CHIM", 11, "completamento", 20): {"q": "Il _____ è il logaritmo negativo di K_b."},
    ("CHIM", 11, "completamento", 23): {"q": "Il _____ dell'acqua K_w è pari a 1,0 × 10⁻¹⁴ a 25 °C."},
    ("CHIM", 11, "completamento", 25): {"q": "Una soluzione è _____ se [H₃O⁺] = [OH⁻]."},
    ("CHIM", 11, "completamento", 26): {"q": "Una soluzione è _____ se [H₃O⁺] > [OH⁻]."},
    ("CHIM", 11, "completamento", 27): {"q": "Una soluzione è _____ se [H₃O⁺] < [OH⁻]."},
    ("CHIM", 12, "non_commentati", 144): {
        "q": (
            "Quale/i delle seguenti affermazioni è/sono corretta/e relativamente ai legami carbonio-carbonio? "
            "1. L'energia di legame cresce nell'ordine C–C, C=C, C≡C "
            "2. La lunghezza del legame C–C è doppia rispetto a quella del legame C=C "
            "3. Nel legame C=C gli atomi di carbonio condividono quattro elettroni"
        ),
    },
    ("CHIM", 12, "completamento", 22): {"q": "Il _____ (CH₄) è il più semplice alcano."},
    ("CHIM", 12, "completamento", 24): {"q": "Il _____ (C₃H₈) è un combustibile comune."},
    ("CHIM", 12, "completamento", 50): {"q": "Il _____ è un benzene con gruppo –OH."},
    ("CHIM", 12, "completamento", 79): {"q": "Le _____ contengono il gruppo –CONH₂."},
    ("BIO", 3, "completamento", 82): {"q": "I recettori steroidei possono interagire con altri fattori, come _____, per modulare finemente la trascrizione."},
    ("BIO", 4, "non_commentati", 146): {
        "q": (
            "In un incrocio diibrido, alcuni dei discendenti hanno un fenotipo diverso rispetto a quello dei genitori. "
            "Quale delle seguenti affermazioni può spiegare il manifestarsi di questo fenotipo? "
            "1. È avvenuta una mutazione. "
            "2. I genitori sono entrambi eterozigoti per entrambi i geni. "
            "3. Un genitore è eterozigote per entrambi i geni e l'altro genitore è omozigote recessivo per entrambi i geni."
        ),
    },
    ("BIO", 4, "completamento", 17): {"q": "In un albero genealogico la femmina è rappresentata con un _____ e il maschio con un _____ ."},
    ("BIO", 6, "completamento", 48): {"q": "Le _____ regolative prevedono l'attivazione sequenziale di chinasi e fosfatasi che modulano proteine bersaglio."},
    ("BIO", 6, "completamento", 85): {"q": "L'attivazione dei RTK recluta proteine adattatrici che attivano _____, una piccola GTPasi."},
    ("BIO", 6, "completamento", 86): {"q": "Ras attiva la cascata delle _____, che comprende Raf (MAPKKK), Mek (MAPKK) ed Erk (MAPK)."},
    ("BIO", 6, "completamento", 87): {"q": "La proteina _____ fosforila proteine nucleari e citoplasmatiche, modulando l'espressione genica."},
    ("BIO", 6, "completamento", 88): {"q": "La via Ras-MAP chinasi è un tipico esempio di cascata di _____ con effetto amplificatorio."},
    ("BIO", 6, "completamento", 89): {"q": "Mutazioni costitutivamente attive di _____ contribuiscono alla trasformazione neoplastica."},
    ("BIO", 6, "completamento", 90): {"q": "Un _____ è un gene la cui mutazione porta a proliferazione incontrollata."},
    ("BIO", 6, "completamento", 91): {"q": "Ras mutato è uno degli _____ più comuni nei tumori umani."},
    ("BIO", 6, "completamento", 92): {"q": "Il recettore dell'_____ è un RTK che, una volta attivato, stimola vie legate al metabolismo e alla crescita."},
    ("BIO", 6, "completamento", 93): {"q": "Il recettore per _____ attiva Ras e la cascata MAPK, promuovendo proliferazione e differenziamento."},
    ("BIO", 6, "completamento", 94): {"q": "Mutazioni o iperespressione del recettore EGF sono associate a numerosi tumori _____ ."},
    ("BIO", 6, "completamento", 95): {"q": "La via _____ converte PIP₂ in PIP₃, attivando Akt/PKB, cruciale per sopravvivenza cellulare e proliferazione."},
    ("BIO", 7, "completamento", 81): {"q": "I _____ sono la manifestazione citologica del crossing over."},
    ("FIS", 2, "completamento", 8): {"q": "Quando la velocità di un corpo varia, si dice che il corpo è soggetto a _____ ."},
    ("FIS", 2, "completamento", 29): {"q": "Se la velocità scalare è costante, il grafico velocità-tempo è una linea _____ ."},
    ("FIS", 3, "non_commentati", 182): {
        "q": (
            "Un'asta uniforme e rettilinea di estremi A e B ha lunghezza pari a 6 metri e si trova in posizione "
            "verticale, incernierata nell'estremo A ad un punto fisso. A metà dell'asta viene applicata una forza "
            "orizzontale di intensità pari a 5 N (Newton). Quale deve essere l'intensità di una forza di verso "
            "opposto da applicare in un punto P a distanza di 2 metri da A affinché sia soddisfatta la condizione di equilibrio?"
        ),
    },
    ("FIS", 3, "completamento", 76): {"q": "Quando θ = 0°, il lavoro è _____ ."},
    ("FIS", 4, "non_commentati", 72): {
        "q": (
            "Un cilindro di un materiale omogeneo (di densità costante), di sezione S = 20 cm² e altezza h = 60 cm, "
            "galleggia in acqua (densità = 1 g/cm³) in posizione perfettamente verticale. Sapendo che il corpo è "
            "sommerso per i 2/3, determinare il valore approssimato della densità del materiale."
        ),
    },
    ("FIS", 5, "non_commentati", 80): {
        "q": (
            "La pressione all'interno di un recipiente di volume V = 20 l in cui sono contenute 0,5 moli di azoto "
            "(peso molecolare 28) a una temperatura di 27 °C è:"
        ),
    },
    ("FIS", 6, "completamento", 105): {"q": "Il momento massimo è dato da τ = I A _____ ."},
    ("FIS", 6, "completamento", 122): {"q": "1 henry equivale a 1 V·s per _____ ."},
}
