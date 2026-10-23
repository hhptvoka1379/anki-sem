#!/usr/bin/env python3
"""Exact remediation & Italian scientific explanations for all 189 CHIM items in chim_434.txt."""
from __future__ import annotations

CHIM_189: dict[str, dict] = {
    "CHIM-C01-NCOM-008": {
        "question": "Quale dei seguenti elementi forma molecole biatomiche?",
        "options": {"D": "N⁺"},
        "explanation": "Allo stato elementare l'azoto (N) forma molecole biatomiche N₂ unite da un triplo legame covalente, mentre Mg, Fe e K sono metalli monoatomici reticolari e N⁺ è uno ione.",
    },
    "CHIM-C01-NCOM-060": {
        "question": "L'elemento radioattivo tecnezio si utilizza in campo medico. Indicare il numero di elettroni, protoni e neutroni in un atomo di ⁹⁹₄₃Tc:",
        "options": {"A": "43, 56, 59", "B": "43, 43, 43", "E": "43, 43, 56"},
        "answer_text": "43, 43, 56",
        "explanation": "Nell'atomo neutro di ⁹⁹₄₃Tc il numero atomico Z = 43 fornisce il numero di protoni (43) e di elettroni (43), mentre i neutroni sono A − Z = 99 − 43 = 56.",
    },
    "CHIM-C01-NCOM-092": {
        "options": {"A": "hanno lo stesso numero di massa"},
        "explanation": "Prozio (¹H), deuterio (²H) e trizio (³H) sono i tre isotopi dell'idrogeno: possiedono tutti lo stesso numero atomico Z = 1 (un solo protone) ma differiscono per il numero di neutroni (0, 1 e 2) e quindi per il numero di massa.",
        "errata_note": "Nota: avendo lo stesso numero atomico Z = 1, i tre isotopi occupano anche la medesima casella nella tavola periodica (opzione D); la chiave ufficiale seleziona B perché la definizione primaria di isotopi si fonda sull'identità di Z.",
    },
    "CHIM-C01-NCOM-097": {
        "explanation": "Gli isotopi dello stesso elemento hanno uguale numero atomico (Z = 53 per lo iodio, quindi stessi protoni ed elettroni) e differiscono per i neutroni: ¹²⁷I ne possiede 127 − 53 = 74 mentre ¹³¹I ne possiede 131 − 53 = 78, ossia il primo ha 4 neutroni in meno.",
    },
    "CHIM-C01-NCOM-101": {
        "question": "Il ⁴₃Li è un isotopo instabile del litio che decade emettendo un protone. Quale sarà il prodotto di decadimento?",
        "options": {"A": "³₂He", "B": "³₃Li", "C": "³₁H", "D": "⁴₂He", "E": "²₁H"},
        "answer": "A",
        "answer_text": "³₂He",
        "explanation": "Nell'emissione protonica ⁴₃Li → ¹₁p + ³₂He si conservano sia il numero di massa A (4 − 1 = 3) sia il numero atomico Z (3 − 1 = 2, elio): il nuclide figlio è quindi ³₂He.",
    },
    "CHIM-C01-NCOM-110": {
        "question": "Una sola delle seguenti affermazioni concernenti lo ione potassio K⁺ (Z = 19, P.A. = 39) è errata. Quale?",
        "options": {"C": "Nel nucleo è presente un numero di neutroni inferiore a 39"},
        "explanation": "Nel nuclide ³⁹₁₉K il numero di massa A = 39 è la somma di protoni (19) e neutroni: i neutroni nel nucleo sono quindi 39 − 19 = 20 (inferiore a 39), e non 39 come affermato erroneamente in E.",
    },
    "CHIM-C02-NCOM-021": {
        "options": {
            "A": "Il numero quantico angolare l può assumere tutti i valori interi tra 0 e (n − 1)",
            "B": "Il numero di orbitali possibili per ogni valore di n è n³",
            "D": "Il numero quantico di spin mₛ può assumere solo due valori",
        },
        "answer_text": "Il numero di orbitali possibili per ogni valore di n è n³",
        "explanation": "Per un dato livello principale n il numero complessivo di orbitali è pari a n² (somma dei 2l + 1 orbitali per l = 0, …, n − 1), e non n³; tutte le altre affermazioni sui numeri quantici sono corrette.",
    },
    "CHIM-C02-NCOM-035": {
        "question": "L'ordine di riempimento degli orbitali atomici per gli elementi del terzo periodo è:",
        "options": {"A": "3s, 3p"},
        "answer_text": "3s, 3p",
        "explanation": "Lungo il terzo periodo (da Na ad Ar) si riempiono in sequenza il sottolivello 3s e poi il 3p secondo la regola della diagonale (n + l); il sottolivello 3d ha energia superiore anche al 4s e si popola solo nel quarto periodo.",
    },
    "CHIM-C02-NCOM-037": {
        "explanation": "Secondo il principio di Aufbau e la regola (n + l), i valori sono: 5s (5+0=5), 5p (5+1=6), 6s (6+0=6), 5d (5+2=7), 6p (6+1=7); l'orbitale 5s ha quindi l'energia più bassa del gruppo ed è occupato per primo.",
    },
    "CHIM-C03-NCOM-029": {
        "options": {"E": "4 moli"},
        "answer_text": "4 moli",
        "explanation": "Il numero di moli di rame si ottiene dividendo la massa del campione per la massa molare: n = 254,184 g / 63,546 g·mol⁻¹ = 4 moli.",
        "errata_note": "Refuso editoriale EdiSES: nella stampa originale sia l'opzione C sia l'opzione E riportano «4 moli» (chiave ufficiale E).",
    },
    "CHIM-C03-NCOM-031": {
        "options": {"B": "180 × 24"},
        "explanation": "Poiché il peso molecolare del glucosio è 180 u, 180 g corrispondono a 1 mole di glucosio e contengono quindi un numero di Avogadro di molecole (≈ 6 × 10²³).",
        "errata_note": "Refuso tipografico EdiSES nell'opzione E: la stampa riporta l'esponente «10²⁴» invece di «10²³», ma E resta l'unica risposta compatibile con la costante di Avogadro.",
    },
    "CHIM-C03-NCOM-033": {
        "explanation": "Per il principio di Avogadro, volumi uguali di gas diversi nelle stesse condizioni di T e P contengono lo stesso numero di moli e di molecole; avendo però masse molari diverse (SO₂ = 64 g/mol vs NH₃ = 17 g/mol), la massa in grammi nei due palloni è differente.",
        "errata_note": "Nota: anche il numero totale di atomi differisce tra i due palloni (SO₂ è triatomica, 3 atomi/molecola; NH₃ è tetratomica, 4 atomi/molecola, opzione B); la chiave ufficiale seleziona D (massa in grammi).",
    },
    "CHIM-C03-NCOM-037": {
        "options": {"E": "contengono lo stesso numero di atomi"},
        "explanation": "Una mole di qualsiasi sostanza molecolare contiene sempre lo stesso numero di molecole, pari alla costante di Avogadro N_A = 6,022 × 10²³ (mentre peso molecolare e numero totale di atomi differiscono tra H₂SO₄ e HCl).",
    },
    "CHIM-C03-NCOM-042": {
        "question": "Una mole di acido solforico (H₂SO₄) pesa:",
        "options": {"C": "98 g", "D": "12 g", "E": "40 g"},
        "answer_text": "98 g",
        "explanation": "La massa molare dell'acido solforico H₂SO₄ vale 2·(1) + 32 + 4·(16) = 98 g/mol, quindi una mole pesa 98 g.",
    },
    "CHIM-C03-NCOM-048": {
        "explanation": "Per la legge dei gas ideali (V = nRT/P), una mole (n = 1 mol) di qualunque gas ideale alle medesime pressione e temperatura occupa sempre lo stesso volume molare (le opzioni B ed E sono errate perché riportano esponenti 10³ e 10¹³ anziché 10²³).",
    },
    "CHIM-C03-NCOM-049": {
        "question": "In quale delle seguenti masse sono contenute 6,022 × 10²³ molecole? (Massa atomica: Na: 23 uma, Cl: 35 uma, Br: 80 uma, O: 16 uma, F: 16 uma).",
        "explanation": "6,022 × 10²³ entità elementari corrispondono a 1 mole di sostanza: per NaCl la massa molare è 23 + 35 = 58 g/mol, quindi 58 g di NaCl equivalgono a 1 mole (mentre 1 mol di NaBr pesa 103 g, di Na₂O 62 g e di NO 30 g).",
        "errata_note": "Nota: rigorosamente NaCl è un composto ionico formato da unità formula Na⁺Cl⁻ e non da molecole discrete (e la stampa riporta «F: 16 uma» come refuso irrilevante); nei quesiti EdiSES «molecole» è inteso come unità stechiometriche.",
    },
    "CHIM-C03-NCOM-071": {
        "explanation": "Lo zinco (Zn, Z = 30) è un elemento metallico del blocco d; idrogeno e fosforo sono non metalli, mentre ottone (Cu + Zn) e bronzo (Cu + Sn) sono leghe metalliche e non singoli elementi.",
    },
    "CHIM-C03-NCOM-074": {
        "options": {"A": "I", "C": "nessuna delle sigle indica un alogeno"},
        "answer_text": "I",
        "explanation": "Il simbolo chimico I identifica lo iodio (Z = 53), elemento del Gruppo 17 (VIIA, alogeni); Fe è un metallo di transizione, Xe un gas nobile e Ca un metallo alcalino-terroso.",
    },
    "CHIM-C03-NCOM-086": {
        "options": {"B": "hanno la tendenza a formare ioni positivi"},
        "explanation": "Gli alogeni (Gruppo 17, configurazione esterna ns² np⁵) possiedono sette elettroni di valenza ed elevata affinità elettronica: tendono quindi ad acquistare un singolo elettrone per raggiungere l'ottetto stabile del gas nobile successivo, formando anioni mononegativi X⁻.",
        "errata_note": "Nota: acquistare un elettrone (E) comporta la formazione di ioni negativi monovalenti X⁻ (D); la chiave ufficiale seleziona E perché specifica esattamente il numero di elettroni acquistati (uno).",
    },
    "CHIM-C03-NCOM-088": {
        "question": "L'isotopo di un elemento è ²⁷₁₃X. Qual è la posizione dell'elemento X nella Tavola Periodica?",
        "options": {"B": "Periodo: 3; Gruppo: 13"},
        "answer_text": "Periodo: 3; Gruppo: 13",
        "explanation": "Il numero atomico Z = 13 corrisponde all'alluminio, con configurazione elettronica 1s² 2s² 2p⁶ 3s² 3p¹: il livello principale più esterno n = 3 indica il Periodo 3, mentre i 3 elettroni di valenza indicano il Gruppo 13 (IIIA).",
    },
    "CHIM-C03-NCOM-101": {
        "options": {"A": "Perché hanno lo stesso numero di elettroni totali", "E": "Perché hanno lo stesso numero di isotopi"},
        "explanation": "Gli elementi appartenenti allo stesso gruppo verticale della tavola periodica presentano la medesima configurazione elettronica del guscio di valenza (stesso numero di elettroni esterni), da cui dipendono il comportamento chimico e la stechiometria dei legami.",
    },
    "CHIM-C03-NCOM-133": {
        "options": {"B": "Solo 1 e 3", "D": "Solo 1 e 2"},
        "answer": "D",
        "answer_text": "Solo 1 e 2",
        "explanation": "Il grande salto energetico tra la 2ª (1450 kJ/mol) e la 3ª energia di ionizzazione (7730 kJ/mol) indica 2 elettroni di valenza, quindi Gruppo 2 (affermazione 1 vera; i dati sono quelli del magnesio, Periodo 3, perciò la 3 è falsa). Per definizione la 3ª energia di ionizzazione (7730 kJ/mol) corrisponde esattamente al processo X²⁺(g) → X³⁺(g) + e⁻ (affermazione 2 vera): sono quindi corrette 1 e 2.",
        "errata_note": "Errata corrige chiave EdiSES: il testo originale indicava E («Solo 1»), trascurando che 7730 kJ/mol è il terzo valore dell'elenco e definisce per l'appunto la terza ionizzazione X²⁺(g) → X³⁺(g) + e⁻ (risposta corretta D).",
    },
    "CHIM-C03-NCOM-136": {
        "question": (
            "La seguente tabella riporta le energie di ionizzazione successive (in kJ mol⁻¹) di un elemento del Periodo 3 della Tavola Periodica degli Elementi: "
            "1ª = 790; 2ª = 1600; 3ª = 3200; 4ª = 4400; 5ª = 16000; 6ª = 20000. "
            "A quale gruppo della Tavola Periodica appartiene questo elemento?"
        ),
        "crop_figure": True,
        "explanation": "Si osserva un brusco aumento (quasi quadruplicazione) passando dalla 4ª (4400 kJ/mol) alla 5ª energia di ionizzazione (16000 kJ/mol), segno che il quinto elettrone proviene dal core interno 2s²2p⁶: l'atomo ha quindi 4 elettroni di valenza e appartiene al Gruppo 14 (silicio).",
    },
    "CHIM-C03-NCOM-137": {
        "question": (
            "Nella tabella sottostante sono riportati i valori delle prime otto energie di ionizzazione (in kJ mol⁻¹) di un elemento con Z < 20: "
            "I = 578; II = 1817; III = 2745; IV = 11577; V = 14842; VI = 18379; VII = 23326; VIII = 27465. "
            "A quale Gruppo della Tavola Periodica appartiene l'elemento?"
        ),
        "crop_figure": True,
        "explanation": "Il salto netto avviene tra la III (2745 kJ/mol) e la IV energia di ionizzazione (11577 kJ/mol): una volta rimossi i 3 elettroni di valenza si intacca un livello interno completo. L'elemento possiede pertanto 3 elettroni esterni e appartiene al Gruppo 13 (alluminio, Z = 13).",
    },
    "CHIM-C03-NCOM-149": {
        "explanation": "I gas nobili (He, Ne, Ar, Kr, Xe, Rn) presentano il guscio di valenza completo (ns² np⁶, duet 1s² per He) e occupano l'ultima colonna a destra della tavola periodica (Gruppo 18 o VIIIA).",
    },
    "CHIM-C03-NCOM-179": {
        "explanation": "Tra gli elementi elencati appartengono al Gruppo 17 (alogeni) esclusivamente fluoro (F), cloro (Cl), bromo (Br) e iodio (I); Li e Na sono metalli alcalini, Mg e Ca alcalino-terrosi, B un semimetallo del gruppo 13, Ti un metallo di transizione e U un attinide.",
    },
    "CHIM-C03-COMP-014": {
        "cloze_stem": "La {{c1::mole}} è la quantità di sostanza che contiene 6,022 × 10²³ particelle.",
        "accepted_synonyms": ["mole", "mol"],
        "explanation": "Nel Sistema Internazionale la mole (simbolo mol) è l'unità di misura della quantità di sostanza ed è definita come la quantità che contiene esattamente 6,02214076 × 10²³ entità elementari (costante di Avogadro).",
    },
    "CHIM-C03-COMP-022": {
        "cloze_stem": "I {{c1::metalli di transizione}} appartengono ai gruppi dal 3B all'8B.",
        "answer": "metalli di transizione",
        "answer_text": "metalli di transizione",
        "accepted_synonyms": ["metalli di transizione", "elementi di transizione"],
        "explanation": "Nella notazione tradizionale americana/CAS i gruppi B (dal 3B all'8B più 1B e 2B, corrispondenti ai gruppi 3–12 IUPAC) identificano i metalli di transizione del blocco d.",
    },
    "CHIM-C03-COMP-024": {
        "cloze_stem": "Gli elementi rappresentativi appartengono ai gruppi principali 1A–{{c1::8A}}.",
        "answer": "8A",
        "answer_text": "8A",
        "accepted_synonyms": ["8A", "VIIIA"],
        "explanation": "Gli elementi rappresentativi (blocchi s e p della tavola periodica) occupano gli otto gruppi principali indicati nella nomenclatura tradizionale con 1A–8A (gruppi 1, 2 e 13–18 IUPAC).",
    },
    "CHIM-C03-COMP-033": {
        "cloze_stem": "Gli {{c1::alogeni}} formano molecole biatomiche come F₂, Cl₂, Br₂ e I₂.",
        "accepted_synonyms": ["alogeni"],
        "explanation": "Gli elementi del Gruppo 17 (alogeni: fluoro, cloro, bromo, iodio) hanno configurazione esterna ns² np⁵ e allo stato elementare condividono un elettrone ciascuno formando molecole biatomiche omonucleari X₂.",
    },
    "CHIM-C04-NCOM-003": {
        "options": {
            "A": "coppie di ioni nei liquidi e un reticolo cristallino nei solidi",
            "D": "composti solidi, liquidi o gassosi, a seconda dei casi",
            "E": "un reticolo cristallino di ioni che può estendersi nelle tre direzioni dello spazio",
        },
        "answer_text": "un reticolo cristallino di ioni che può estendersi nelle tre direzioni dello spazio",
        "explanation": "L'interazione elettrostatica coulombiana tra cationi e anioni è adirezionale: non genera molecole discrete, bensì un reticolo cristallino ionico tridimensionale esteso nello spazio.",
    },
    "CHIM-C04-NCOM-009": {
        "explanation": "Nel cloruro di idrogeno allo stato gassoso (HCl) idrogeno e cloro condividono una coppia di elettroni formando una molecola tenuta insieme da un legame covalente polare (Δχ ≈ 0,96).",
    },
    "CHIM-C04-NCOM-012": {
        "options": {
            "A": "Da due legami σ e uno π",
            "B": "Da tre legami σ",
            "C": "Da un legame σ e da due legami π",
            "E": "Da tre legami π",
        },
        "answer_text": "Da un legame σ e da due legami π",
        "explanation": "Un legame triplo tra due atomi (come in N≡N o HC≡CH) è sempre costituito da un solo legame σ di sovrapposizione assiale e da due legami π di sovrapposizione laterale su piani perpendicolari.",
    },
    "CHIM-C04-NCOM-029": {
        "options": {
            "B": "C e Cl hanno uguali valori di elettronegatività",
            "D": "CCl₄ è una molecola tetraedrica",
            "E": "Le dimensioni dell'atomo di C sono inferiori rispetto a quelle dell'atomo di Cl",
        },
        "answer_text": "CCl₄ è una molecola tetraedrica",
        "explanation": "Nel tetracloruro di carbonio (CCl₄) ciascun legame C–Cl è polare, ma la disposizione simmetrica dei quattro atomi di cloro ai vertici di un tetraedro regolare fa sì che la somma vettoriale dei quattro momenti di dipolo sia esattamente nulla (μ = 0).",
    },
    "CHIM-C04-NCOM-040": {
        "answer": "C",
        "answer_text": "legami multipli",
        "explanation": "Ciascun atomo di azoto ha 5 elettroni di valenza (2s² 2p³) e completa l'ottetto condividendo tre coppie elettroniche con l'altro atomo di N in un legame triplo N≡N (legame multiplo covalente omopolare).",
        "errata_note": "Nota: il legame N≡N è al tempo stesso covalente (opzione A) e multiplo (opzione C); nelle chiavi di consenso e nella tassonomia del capitolo la risposta specifica attesa è C («legami multipli»), pur essendo anche A chimicamente vera.",
    },
    "CHIM-C04-NCOM-051": {
        "options": {"D": "Dei due elementi che lo costituiscono uno appartiene al gruppo I e l'altro al gruppo VII"},
        "answer_text": "Dei due elementi che lo costituiscono uno appartiene al gruppo I e l'altro al gruppo VII",
        "explanation": "Un metallo alcalino del gruppo I (bassissima energia di ionizzazione ed elettronegatività) combinato con un alogeno del gruppo VII (alta affinità elettronica ed elettronegatività) presenta massima differenza di elettronegatività e forma un tipico solido ionico (es. NaCl, KBr).",
    },
    "CHIM-C04-NCOM-056": {
        "question": "Tra quali delle seguenti coppie di elementi si stabilisce un legame prevalentemente ionico?",
        "options": {"A": "Fe e Fe", "B": "S e O", "C": "K e Cl", "D": "Si e I", "E": "H e C"},
        "answer_text": "K e Cl",
        "explanation": "Tra il potassio (metallo alcalino, χ = 0,8) e il cloro (alogeno, χ = 3,2) la differenza di elettronegatività è Δχ = 2,4 > 1,9, dando luogo al composto ionico K⁺Cl⁻; Fe–Fe è metallico, mentre S–O, Si–I e H–C sono legami covalenti.",
    },
    "CHIM-C04-NCOM-063": {
        "explanation": "Nello ione ammonio NH₄⁺ l'azoto centrale forma quattro legami equivalenti N–H senza coppie solitarie residue (ibridazione sp³), assumendo geometria tetraedrica regolare con angoli di 109,5° (isoelettronico e isostrutturale con CH₄).",
    },
    "CHIM-C04-COMP-012": {
        "cloze_stem": "Il {{c1::cloruro di sodio}} è un tipico composto ionico formato da Na⁺ e Cl⁻.",
        "accepted_synonyms": ["cloruro di sodio", "NaCl"],
        "explanation": "Il cloruro di sodio (NaCl, salgemma) è il prototipo dei solidi cristallini ionici, costituito da un reticolo cubico a facce centrate di cationi Na⁺ e anioni Cl⁻.",
    },
    "CHIM-C05-NCOM-008": {
        "options": {"A": "CHF₃", "B": "CHCl₃", "C": "CHBr₃", "D": "CHI₃", "E": "CH₄"},
        "explanation": "L'intensità delle forze di dispersione di London cresce all'aumentare del numero totale di elettroni e della polarizzabilità della nube elettronica: lo iodoformio CHI₃, contenente tre grandi atomi di iodio (Z = 53), ha la massima polarizzabilità ed è infatti solido a temperatura ambiente.",
    },
    "CHIM-C05-NCOM-016": {
        "explanation": "Nello stato liquido le forze attrattive intermolecolari sono più deboli rispetto a quelle che vincolano rigidamente le particelle nel reticolo solido (consentendo lo scorrimento fluido), ma restano molto più intense di quelle quasi nulle dello stato gassoso.",
        "errata_note": "Nota: anche l'opzione C («maggiori di quelle presenti nello stato gassoso») è fisicamente vera poiché F_solido > F_liquido > F_gas; la chiave ufficiale EdiSES riporta E.",
    },
    "CHIM-C05-NCOM-017": {
        "options": {"C": "H₂S", "D": "CH₄"},
        "explanation": "Tra i gas elencati solo l'ammoniaca (NH₃, T_eb = −33 °C) è in grado di formare legami a idrogeno intermolecolari grazie agli atomi di H legati all'azoto fortemente elettronegativo, presentando perciò il punto di ebollizione più elevato.",
    },
    "CHIM-C05-NCOM-024": {
        "options": {"E": "Distillazione"},
        "answer_text": "Distillazione",
        "explanation": "La distillazione separa i componenti di una miscela sfruttandone la diversa volatilità mediante un doppio passaggio di stato: evaporazione (ebollizione) del componente più volatile seguita dalla sua condensazione per raffreddamento.",
    },
    "CHIM-C05-NCOM-025": {
        "question": "L'ammoniaca (NH₃) ha un punto di ebollizione pari a −33 °C. La fosfina (PH₃) ha invece un punto di ebollizione pari a −88 °C. Quale delle seguenti affermazioni spiega perché hanno punti di ebollizione così differenti?",
        "options": {
            "B": "La NH₃ è un composto ionico. La PH₃ è un composto molecolare",
            "C": "La NH₃ ha una massa inferiore alla PH₃",
            "D": "La NH₃ forma ponti idrogeno intermolecolari più facilmente della PH₃",
            "E": "La NH₃ ha una struttura molto grande. La PH₃ ha una struttura molecolare semplice",
        },
        "answer_text": "La NH₃ forma ponti idrogeno intermolecolari più facilmente della PH₃",
        "explanation": "Pur avendo massa molecolare inferiore a PH₃, l'ammoniaca NH₃ possiede legami N–H fortemente polarizzati (χ_N = 3,0 contro χ_P = 2,1) che danno luogo a legami a idrogeno intermolecolari, richiedendo molta più energia termica per l'ebollizione.",
    },
    "CHIM-C05-NCOM-029": {
        "crop_figure": True,
        "explanation": "A 15 °C e 1 atm NH₃ e HCl sono gas (contenuti nella bombola chiusa A per gas), il bromo Br₂ è un liquido denso e volatile (nel flacone chiuso B per liquidi), mentre lo iodio I₂ è un solido cristallino (nel contenitore aperto C per solidi).",
    },
    "CHIM-C05-NCOM-040": {
        "question": "Quali interazioni spiegano la solubilità in acqua dell'acido cloridrico (HCl)?",
        "options": {"D": "Formazione di legami ionici"},
        "explanation": "Secondo l'impostazione didattica del quesito, le molecole fortemente polari di HCl interagiscono inizialmente con i dipoli dell'acqua tramite legami a idrogeno / trasferimento protonico (H–Cl···OH₂ → Cl⁻ + H₃O⁺), favorendone l'elevatissima solubilità.",
        "errata_note": "Nota chimica: in acqua HCl è un acido forte che si ionizza completamente formando un legame covalente dativo in H₃O⁺ e idratando gli ioni H₃O⁺ e Cl⁻ mediante intense interazioni ione-dipolo; tra le alternative proposte la chiave EdiSES seleziona E.",
    },
    "CHIM-C06-NCOM-003": {
        "options": {"A": "1 M", "C": "0,4 M", "E": "2 M"},
        "answer_text": "0,4 M",
        "explanation": "Le moli di glucosio disciolte sono n = 36 g / 180 g·mol⁻¹ = 0,20 mol; dividendo per il volume V = 500 mL = 0,500 L si ottiene la molarità M = 0,20 mol / 0,500 L = 0,4 M.",
    },
    "CHIM-C06-NCOM-015": {
        "question": "Un grammo-equivalente di NH₄Cl (P.M. = 53,45) è:",
        "options": {"A": "26,73 g", "B": "13,36 g", "C": "53,45 g", "D": "17,82 g", "E": "106,9 g"},
        "explanation": "Il cloruro d'ammonio NH₄Cl si dissocia scambiando una sola carica positiva/negativa per unità formula (NH₄⁺ + Cl⁻, valenza operativa z = 1): il peso equivalente coincide quindi con il peso molecolare, pari a 53,45 g/eq.",
    },
    "CHIM-C06-NCOM-023": {
        "options": {
            "A": "0,001 moli di soluto in 100 mL di soluzione",
            "B": "0,1 moli di soluto in 100 mL di soluzione",
            "C": "0,1 moli di soluto in un mL di soluzione",
            "D": "0,0001 moli di soluto in un mL di soluzione",
            "E": "0,001 moli di soluto in 1 L di soluzione",
        },
        "answer_text": "0,0001 moli di soluto in un mL di soluzione",
        "explanation": "Una soluzione 0,1 M contiene 0,1 moli di soluto in 1 L (1000 mL) di soluzione; in 1 mL (10⁻³ L) sono quindi presenti n = 0,1 mol/L × 10⁻³ L = 10⁻⁴ mol = 0,0001 moli di soluto.",
    },
    "CHIM-C06-NCOM-029": {
        "question": "2 g di idrossido di sodio sono sciolti in 200 mL di acqua. Qual è la molarità dell'idrossido di sodio nella soluzione risultante? [masse atomiche relative: H = 1 u; O = 16 u; Na = 23 u]",
        "explanation": "La massa molare di NaOH è 23 + 16 + 1 = 40 g/mol, quindi 2 g corrispondono a n = 2 / 40 = 0,05 mol; in V = 0,200 L la molarità vale M = 0,05 mol / 0,200 L = 0,25 M.",
    },
    "CHIM-C06-NCOM-038": {
        "options": {
            "A": "12 g di acido acetico e 3,6 g di acido cloridrico",
            "B": "12 g di acido acetico e 12 g di acido cloridrico",
            "C": "12 mg di acido acetico e 36 mg di acido cloridrico",
        },
        "explanation": "Per ottenere soluzioni di uguale volume e uguale molarità occorre sciogliere lo stesso numero di moli dei due soluti: 60 × 10⁻² g (0,60 g) di CH₃COOH equivalgono a 0,60 / 60 = 0,01 mol, esattamente come 36 × 10⁻² g (0,36 g) di HCl (0,36 / 36 = 0,01 mol).",
    },
    "CHIM-C06-NCOM-042": {
        "options": {"A": "49 g", "D": "13 g", "E": "24,5 g"},
        "answer_text": "49 g",
        "explanation": "In V = 250 mL = 0,250 L di soluzione 2 M sono contenute n = M · V = 2 mol/L × 0,250 L = 0,50 moli di H₂SO₄, la cui massa è m = 0,50 mol × 98 g/mol = 49 g.",
    },
    "CHIM-C06-NCOM-050": {
        "explanation": "In 50 g di cioccolato al 47% di zuccheri vi sono m = 50 × 0,47 = 23,5 g di saccarosio, pari a n = 23,5 / 342,31 ≈ 0,06865 mol; moltiplicando per il numero di Avogadro si ottengono 0,06865 × 6,022 × 10²³ ≈ 4,1–4,2 · 10²² molecole.",
    },
    "CHIM-C06-NCOM-070": {
        "question": "NaCl posto in acqua dà:",
        "options": {"C": "NaH, ClOH", "E": "Na⁺, Cl⁻"},
        "answer_text": "Na⁺, Cl⁻",
        "explanation": "Il cloruro di sodio è un elettrolita forte ionico: in acqua subisce dissociazione elettrolitica liberando cationi Na⁺(aq) e anioni Cl⁻(aq) solvatati senza dare idrolisi acido-base.",
    },
    "CHIM-C06-NCOM-071": {
        "options": {"D": "protico"},
        "explanation": "La dissociazione dei solidi ionici avviene nei solventi polari ad alta costante dielettrica, capaci di attenuare l'attrazione elettrostatica tra gli ioni; poiché tale dicitura non compare tra B–E, la chiave seleziona A («nessuna delle risposte è corretta»).",
        "errata_note": "Nota: l'acqua è al contempo un solvente polare e protico (opzione D), ma non tutti i solventi protici hanno costante dielettrica sufficiente a dissociare i sali (es. acido acetico anidro); la risposta attesa dal testo è A.",
    },
    "CHIM-C06-NCOM-074": {
        "explanation": "Calcolando le moli di ioni Cl⁻ (n_Cl⁻ = M · V · ν_Cl): A dà 0,100 × 0,50 × 2 = 0,10 mol; C dà 1,00 × 0,10 × 1 = 0,10 mol; D dà 0,250 × 0,20 × 2 = 0,10 mol; E dà 2,00 × 0,05 × 1 = 0,10 mol; solo B (0,500 L × 0,10 M × 1) contiene 0,05 mol di Cl⁻.",
    },
    "CHIM-C06-NCOM-088": {
        "options": {"C": "O"},
        "answer": "E",
        "answer_text": "Nessuna delle risposte è corretta",
        "explanation": "La pressione osmotica è convenzionalmente indicata con la lettera greca π (legge di van 't Hoff: π = M·R·T·i), simbolo assente tra le alternative A–D (nella scansione originale l'opzione C riporta O, non π).",
    },
    "CHIM-C06-NCOM-099": {
        "options": {
            "A": "La soluzione contiene ioni Na⁺ e ioni Cl⁻",
            "B": "La temperatura di ebollizione è maggiore di 100 °C",
            "D": "La temperatura di solidificazione è minore di 0 °C",
            "E": "La temperatura di ebollizione è minore di 100 °C",
        },
        "answer_text": "La temperatura di ebollizione è minore di 100 °C",
        "explanation": "L'aggiunta di un soluto non volatile come NaCl abbassa la tensione di vapore dell'acqua provocando innalzamento ebullioscopico (T_eb > 100 °C a 1 atm) e abbassamento crioscopico (T_cong < 0 °C); è quindi falsa l'affermazione E.",
    },
    "CHIM-C07-NCOM-011": {
        "question": "La reazione Ca(OH)₂ + H₂SO₄ → CaSO₄ + H₂O:",
        "explanation": "A sinistra compaiono complessivamente 4 atomi di idrogeno e 6 di ossigeno (2 O in Ca(OH)₂ + 4 O in H₂SO₄), mentre a destra compaiono solo 2 H e 5 O: occorre quindi porre il coefficiente 2 davanti a H₂O nei prodotti (Ca(OH)₂ + H₂SO₄ → CaSO₄ + 2 H₂O).",
    },
    "CHIM-C07-NCOM-019": {
        "question": "Data l'equazione: a NH₃ + b O₂ → 4 NO + c H₂O, quale valore deve avere il coefficiente b affinché l'equazione sia bilanciata?",
        "explanation": "I 4 atomi di azoto in 4 NO impongono a = 4 (4 NH₃), da cui 12 atomi di idrogeno che richiedono c = 6 (6 H₂O); a destra vi sono allora 4 + 6 = 10 atomi di ossigeno, bilanciati a sinistra da b = 5 molecole di O₂ (4 NH₃ + 5 O₂ → 4 NO + 6 H₂O).",
    },
    "CHIM-C07-NCOM-022": {
        "options": {
            "A": "a = 4; b = 4; c = 5",
            "B": "a = 4; b = 5; c = 4",
            "C": "a = 3; b = 2; c = 4",
            "D": "a = 4; b = 1; c = 3",
            "E": "a = 3; b = 1; c = 3",
        },
        "answer_text": "a = 4; b = 5; c = 4",
        "explanation": "Dalle 6 molecole di H₂O (12 atomi di H) si ricava a = 4 per NH₃; per conservare i 4 atomi di azoto deve essere c = 4 per NO; infine i 4 + 6 = 10 atomi di ossigeno nei prodotti richiedono b = 5 molecole di O₂.",
    },
    "CHIM-C07-NCOM-027": {
        "explanation": "Le moli iniziali di Mg sono n = 1,2 g / 24 g·mol⁻¹ = 0,050 mol; per rapporto 1:1 si attendono 0,050 mol di MgSO₄ (MM = 24 + 32 + 64 = 120 g/mol), pari a una resa teorica di 0,050 × 120 = 6,0 g. La resa percentuale è quindi (5,5 g / 6,0 g) × 100 ≈ 91,7% ≈ 92%.",
    },
    "CHIM-C07-NCOM-042": {
        "options": {
            "A": "HCl + H₂O → H₃O⁺ + Cl⁻",
            "B": "H₂ + Br₂ → 2 HBr",
            "C": "Ni + 2 HCl → NiCl₂ + H₂",
            "D": "CaCl₂ → Ca²⁺ + 2 Cl⁻",
            "E": "CaCO₃ → CaO + CO₂",
        },
        "answer_text": "CaCO₃ → CaO + CO₂",
        "explanation": "La calcinazione termica del carbonato di calcio CaCO₃ → CaO + CO₂ scinde un unico composto chimico in due composti più semplici ed è una classica reazione di decomposizione (A è protolisi acido-base, B sintesi, C scambio semplice redox, D dissociazione ionica).",
    },
    "CHIM-C07-NCOM-043": {
        "question": "La reazione 2 KI + Br₂ → 2 KBr + I₂ è una reazione di:",
        "explanation": "Il bromo passa da numero di ossidazione 0 (in Br₂) a −1 (in KBr) riducendosi, mentre lo iodio passa da −1 (in KI) a 0 (in I₂) ossidandosi: si tratta quindi di una reazione di ossidoriduzione (spostamento di alogeno).",
    },
    "CHIM-C07-NCOM-044": {
        "options": {
            "B": "Ox: 2; Red: 1; Redox: 1",
            "C": "Ox: 1; Red: 1; Redox: 2",
            "D": "Ox: 2; Red: 1; Redox: 2",
            "E": "Ox: 2; Red: 2; Redox: 1",
        },
        "answer_text": "Ox: 2; Red: 1; Redox: 1",
        "explanation": "Analizzando i cinque processi: (1) 2H⁺ + 2e⁻ → H₂ è una semireazione di sola riduzione (Red = 1); (2) Ag⁺ + Cl⁻ → AgCl è precipitazione non redox; (3) Cu⁺ → Cu²⁺ + e⁻ e (5) Mg → Mg²⁺ + 2e⁻ sono due semireazioni di sola ossidazione (Ox = 2); (4) 2Cu⁺ → Cu + Cu²⁺ è una dismutazione completa di ossidoriduzione (Redox = 1).",
    },
    "CHIM-C07-NCOM-050": {
        "question": "Nella formazione di una mole di CO₂ a partire da carbonio ed ossigeno, C + O₂ → CO₂, si produce una quantità di calore pari a 93,6 chilocalorie. La reazione può essere definita:",
        "explanation": "Lo sviluppo di calore (ΔH < 0) definisce specificamente una reazione esotermica; poiché «esotermica» non figura tra le alternative proposte, la risposta corretta è D («nessuna delle risposte è corretta»).",
    },
    "CHIM-C07-COMP-004": {
        "cloze_stem": "I simboli di stato (s, l, g, aq) specificano la {{c1::fase}} fisica delle sostanze coinvolte.",
        "accepted_synonyms": ["fase", "stato di aggregazione"],
        "explanation": "Nelle equazioni chimiche i pedici tra parentesi (s = solido, l = liquido, g = gas/aeriforme, aq = soluzione acquosa) indicano la fase o stato fisico di ciascun reagente e prodotto.",
    },
    "CHIM-C07-COMP-035": {
        "cloze_stem": "Le {{c1::basi}} liberano OH⁻ in soluzione e reagiscono con acidi neutralizzandoli.",
        "accepted_synonyms": ["basi"],
        "explanation": "Secondo la definizione di Arrhenius, le basi sono sostanze che in soluzione acquosa rilasciano ioni idrossido OH⁻ e reagiscono con gli acidi (donatori di H⁺) dando sali e acqua (neutralizzazione).",
    },
    "CHIM-C08-NCOM-001": {
        "crop_figure": True,
        "explanation": "Per la legge cinetica v = −d[R]/dt = k[R]ⁿ (con ordine positivo), la velocità istantanea è massima quando la concentrazione del reagente [R] è massima, ovvero all'istante iniziale t₀ = 0 min (dove la pendenza della tangente alla curva [R](t) è più ripida).",
    },
    "CHIM-C08-NCOM-016": {
        "options": {"C": "K²"},
        "explanation": "La costante di equilibrio K dipende esclusivamente dalla temperatura: raddoppiando la concentrazione di H₂ a temperatura costante il sistema si sposta verso destra per ristabilire l'equilibrio, ma il valore numerico di K rimane invariato.",
    },
    "CHIM-C09-NCOM-031": {
        "options": {"A": "6 e 4", "B": "1 e −1", "C": "5 e 3", "D": "4 e 2", "E": "3 e 1"},
        "answer_text": "5 e 3",
        "explanation": "Il fosforo appartiene al V gruppo principale (Gruppo 15, configurazione 3s² 3p³): il suo numero di ossidazione massimo positivo è +5 e quello inferiore di due unità è +3.",
    },
    "CHIM-C09-NCOM-038": {
        "question": "La somma algebrica dei numeri di ossidazione degli atomi di NH₄⁺ è:",
        "explanation": "Per regola generale, in qualunque ione poliatomico la somma algebrica dei numeri di ossidazione di tutti gli atomi costituenti è uguale alla carica elettrica complessiva dello ione: per NH₄⁺ vale (−3) + 4·(+1) = +1.",
    },
    "CHIM-C09-NCOM-042": {
        "question": "I perossidi sono composti contenenti legami tra:",
        "options": {"A": "H e O", "B": "C e H", "C": "H e H", "D": "C e O", "E": "O e O"},
        "answer_text": "O e O",
        "explanation": "I perossidi sono caratterizzati dal ponte perossidico –O–O–, cioè da un legame covalente singolo diretto tra due atomi di ossigeno, ciascuno con numero di ossidazione −1.",
    },
    "CHIM-C09-NCOM-052": {
        "question": "Nella reazione 2 NaCl + Br₂ → Cl₂ + 2 NaBr:",
        "options": {
            "C": "il cloro si ossida e il bromo si riduce",
            "E": "il bromo e il cloro si ossidano e il sodio si riduce",
        },
        "answer_text": "il cloro si ossida e il bromo si riduce",
        "explanation": "Nell'equazione scritta il cloro passa da −1 (in NaCl) a 0 (in Cl₂) perdendo elettroni e quindi si ossida, mentre il bromo passa da 0 (in Br₂) a −1 (in NaBr) acquistando elettroni e quindi si riduce (Na⁺ resta a +1).",
    },
    "CHIM-C09-NCOM-053": {
        "explanation": "L'ossidazione consiste nella cessione di elettroni con aumento del numero di ossidazione: il cadmio metallico Cd (n.o. 0) perde i due elettroni di valenza 5s² trasformandosi nel catione Cd²⁺ (n.o. +2).",
    },
    "CHIM-C09-NCOM-054": {
        "question": "Nella semireazione Pb²⁺ + 2 e⁻ → Pb, il piombo:",
        "options": {"E": "si ossida"},
        "explanation": "Lo ione Pb²⁺ acquista due elettroni abbassando il proprio numero di ossidazione da +2 a 0 (piombo metallico): subisce quindi una riduzione.",
    },
    "CHIM-C09-NCOM-060": {
        "options": {
            "B": "il bromo si ossida e lo iodio si riduce",
            "C": "il bromo e lo iodio si ossidano e il potassio si riduce",
            "E": "il potassio e il bromo si riducono e lo iodio si ossida",
        },
        "answer_text": "il bromo si ossida e lo iodio si riduce",
        "explanation": "Nella reazione scritta il bromo passa da n.o. −1 (in HBr) a 0 (in Br₂) ossidandosi, mentre lo iodio passa da n.o. 0 (in I₂) a −1 (in HI) riducendosi.",
    },
    "CHIM-C09-NCOM-061": {
        "question": "Nella semireazione Zn → Zn²⁺ + 2 e⁻, lo Zn:",
        "explanation": "Lo zinco metallico (n.o. 0) cede due elettroni trasformandosi nello ione Zn²⁺ (n.o. +2): la perdita di elettroni definisce un processo di ossidazione.",
    },
    "CHIM-C09-NCOM-062": {
        "question": "Il passaggio da Fe³⁺ a Fe²⁺ è una reazione di:",
        "explanation": "Passando da Fe³⁺ a Fe²⁺ il ferro acquista un elettrone (Fe³⁺ + e⁻ → Fe²⁺) e il suo numero di ossidazione diminuisce da +3 a +2: si tratta quindi di una riduzione.",
    },
    "CHIM-C09-NCOM-083": {
        "question": "Nella semireazione Co → Co²⁺ + 2 e⁻, il cobalto:",
        "explanation": "Il cobalto metallico perde due elettroni passando da numero di ossidazione 0 a +2: subisce pertanto un'ossidazione.",
    },
    "CHIM-C09-NCOM-087": {
        "question": "Nella reazione 2 Zn + O₂ → 2 ZnO:",
        "explanation": "Nell'ossidazione dello zinco con ossigeno molecolare, lo zinco passa da 0 a +2 (si ossida) mentre l'ossigeno passa da 0 (in O₂) a −2 (in ZnO), acquistando elettroni e quindi riducendosi.",
    },
    "CHIM-C09-NCOM-088": {
        "question": "In Cu²⁺ + 2 e⁻ → Cu, il rame:",
        "options": {"C": "non si riduce né si ossida"},
        "explanation": "Lo ione rameico Cu²⁺ acquista due elettroni passando da numero di ossidazione +2 a 0 (rame metallico): poiché acquista elettroni, si riduce.",
    },
    "CHIM-C09-NCOM-096": {
        "question": "La reazione Cu⁺ − 1 e⁻ → Cu²⁺ è una:",
        "explanation": "Lo ione rameoso Cu⁺ perde un elettrone trasformandosi nello ione rameico Cu²⁺ (aumento del numero di ossidazione da +1 a +2): è quindi una semireazione di ossidazione.",
    },
    "CHIM-C09-NCOM-098": {
        "explanation": "Nella reazione Zn + Cu²⁺ → Zn²⁺ + Cu lo ione Cu²⁺ acquista due elettroni dallo zinco riducendosi a Cu metallico: poiché provoca l'ossidazione di Zn (da 0 a +2), Cu²⁺ è l'agente ossidante.",
    },
    "CHIM-C09-NCOM-109": {
        "options": {
            "B": "gli elementi non variano il loro stato di ossidazione",
            "D": "il Fe è l'agente ossidante",
            "E": "lo ione Cu²⁺ è l'agente riducente",
        },
        "explanation": "Il ferro metallico cede due elettroni ossidandosi a Fe²⁺ (agente riducente), mentre lo ione Cu²⁺ acquista i due elettroni riducendosi a Cu metallico e agisce perciò da agente ossidante.",
    },
    "CHIM-C09-NCOM-115": {
        "question": "Nella seguente reazione: 3 Cu + 8 HNO₃ → 3 Cu(NO₃)₂ + 2 NO + 4 H₂O",
        "options": {
            "A": "il Cu si ossida",
            "B": "l'N cede elettroni",
            "C": "il Cu si riduce",
            "E": "l'N si ossida",
        },
        "answer_text": "il Cu si ossida",
        "explanation": "Il rame passa da stato di ossidazione 0 (in Cu) a +2 (in Cu(NO₃)₂), cedendo due elettroni per atomo e quindi ossidandosi, mentre parte dell'azoto nitrico si riduce da +5 a +2 (in NO).",
    },
    "CHIM-C09-NCOM-117": {
        "question": "Nell'equazione di ossido-riduzione di seguito: 4 Fe³⁺ + N₂H₄ → 4 Fe²⁺ + N₂ + 4 H⁺",
        "options": {"B": "l'azoto si ossida"},
        "answer_text": "l'azoto si ossida",
        "explanation": "Nell'idrazina N₂H₄ l'azoto ha numero di ossidazione −2 e passa a 0 in N₂ cedendo elettroni: pertanto l'azoto si ossida (mentre Fe³⁺ si riduce a Fe²⁺).",
    },
    "CHIM-C09-NCOM-119": {
        "question": "Nella reazione seguente: 2 NaBr + Cl₂ → Br₂ + 2 NaCl",
        "options": {
            "A": "il cloro si riduce e il bromo si ossida",
            "D": "il bromo ed il cloro si ossidano e il sodio si riduce",
        },
        "answer_text": "il cloro si riduce e il bromo si ossida",
        "explanation": "Il cloro molecolare Cl₂ (n.o. 0) acquista elettroni trasformandosi in Cl⁻ (n.o. −1) e si riduce, mentre lo ione bromuro Br⁻ (n.o. −1) cede elettroni formando Br₂ (n.o. 0) e si ossida.",
    },
    "CHIM-C09-NCOM-126": {
        "question": "In una reazione in cui PbCl₂ si trasforma in PbCl₄, si può affermare che:",
        "options": {"D": "il cloro si è ossidato"},
        "explanation": "Nel cloruro piomboso PbCl₂ il piombo ha numero di ossidazione +2, mentre nel tetracloruro di piombo PbCl₄ ha numero di ossidazione +4 (il cloro resta a −1): aumentando il proprio stato di ossidazione, il piombo si è ossidato.",
    },
    "CHIM-C09-NCOM-128": {
        "question": "Nella seguente reazione di ossido-riduzione: Zn + 2 HCl → ZnCl₂ + H₂",
        "options": {
            "C": "lo zinco si ossida e si riducono sia idrogeno che cloro",
            "E": "lo zinco si riduce e il cloro si ossida",
        },
        "explanation": "Lo zinco metallico passa da n.o. 0 a +2 in ZnCl₂ (si ossida), l'idrogeno passa da +1 in HCl a 0 in H₂ (si riduce), mentre lo ione Cl⁻ rimane spettatore a n.o. −1.",
    },
    "CHIM-C09-COMP-013": {
        "cloze_stem": "Una reazione redox in ambiente acido può richiedere l'aggiunta di {{c1::H⁺}} e H₂O per bilanciare gli atomi.",
        "accepted_synonyms": ["H+", "H⁺", "H3O+", "H₃O⁺", "ioni H+"],
        "explanation": "Nel metodo delle semireazioni in ambiente acido si bilanciano gli atomi di ossigeno con molecole di H₂O e gli atomi di idrogeno aggiungendo ioni H⁺ (o coppie H₃O⁺/H₂O).",
    },
    "CHIM-C09-COMP-014": {
        "cloze_stem": "Una reazione redox in ambiente basico si bilancia aggiungendo {{c1::OH⁻}} e H₂O.",
        "accepted_synonyms": ["OH-", "OH⁻", "ioni OH-", "ioni ossidrile"],
        "explanation": "In ambiente alcalino (basico) il bilancio di carica e degli atomi di idrogeno e ossigeno nelle semireazioni redox si effettua mediante ioni idrossido OH⁻ e molecole di acqua H₂O.",
    },
    "CHIM-C10-NCOM-005": {
        "explanation": "Quando un singolo atomo neutro di ossigeno (configurazione esterna 2s² 2p⁴) acquista due elettroni completa l'ottetto formando l'anione monoatomico ossido O²⁻ (n.o. −2).",
    },
    "CHIM-C10-NCOM-008": {
        "explanation": "In Cl₂O₇ l'ossigeno è a −2 e il cloro raggiunge il suo massimo numero di ossidazione +7 (2x − 14 = 0 ⇒ x = +7): nella nomenclatura tradizionale degli ossidi acidi del cloro prende quindi il prefisso per- e il suffisso -ica, ossia anidride perclorica.",
    },
    "CHIM-C10-NCOM-016": {
        "options": {
            "A": "NH₄B = ammonio bromuro",
            "B": "H₂SO₃ = acido solforoso",
            "C": "SO₂ = anidride solforosa",
            "D": "HNO₂ = acido nitroso",
            "E": "H₃PO₄ = acido ortofosforico",
        },
        "explanation": "Il bromo ha simbolo chimico Br (B è il boro), per cui il bromuro d'ammonio ha formula NH₄Br e non NH₄B; le altre quattro associazioni formula-nome nella scansione originale sono tutte esatte.",
    },
    "CHIM-C10-NCOM-017": {
        "options": {"A": "H₂NO₄", "B": "HNO₂", "C": "N(OH)₃", "D": "HNO₃", "E": "NO₂"},
        "answer_text": "HNO₂",
        "explanation": "L'acido nitroso è l'ossiacido dell'azoto trivalente (n.o. +3) e ha formula HNO₂, mentre HNO₃ è l'acido nitrico (n.o. +5).",
    },
    "CHIM-C10-NCOM-018": {
        "options": {"A": "CO₃²⁻", "B": "HCOOH", "C": "CO", "D": "H₂CO₂", "E": "CO₂"},
        "answer_text": "CO₂",
        "explanation": "L'anidride corrispondente all'acido carbonico H₂CO₃ (carbonio con n.o. +4) è il diossido di carbonio CO₂ (anidride carbonica), poiché CO₂ + H₂O ⇌ H₂CO₃ (nella scansione originale l'opzione A riporta lo ione CO₃²⁻).",
    },
    "CHIM-C10-NCOM-037": {
        "question": "Il nome ufficiale (IUPAC) del composto Al₂O₃ è:",
        "options": {"A": "triossido di dialluminio"},
        "answer_text": "triossido di dialluminio",
        "explanation": "Nella nomenclatura sistematica IUPAC si specificano gli indici stechiometrici con prefissi greci: Al₂O₃ contiene 3 atomi di ossigeno e 2 di alluminio e si denomina triossido di dialluminio (ossido di alluminio nella tradizionale).",
    },
    "CHIM-C10-NCOM-053": {
        "options": {"A": "NO₂⁻"},
        "answer_text": "NO₂⁻",
        "explanation": "Lo ione nitrito deriva dalla dissociazione dell'acido nitroso HNO₂ (azoto con n.o. +3) e ha formula NO₂⁻, mentre NO₃⁻ è lo ione nitrato e N₃⁻ lo ione azoturo.",
    },
    "CHIM-C10-NCOM-054": {
        "question": "Il composto Na₂SO₄ corrisponde a:",
        "explanation": "Il solfato di sodio Na₂SO₄ è un composto ionico formato dal catione metallico Na⁺ e dall'ossianione SO₄²⁻ (derivato dall'acido solforico), ed è pertanto un sale neutro ternario.",
    },
    "CHIM-C10-NCOM-080": {
        "options": {"E": "ClO₂⁻"},
        "answer_text": "ClO₄⁻",
        "explanation": "Lo ione perclorato ha formula ClO₄⁻, in cui il cloro presenta il massimo numero di ossidazione (+7), e deriva dall'acido perclorico HClO₄ (ClO⁻ è ipoclorito, ClO₂⁻ clorito, Cl⁻ cloruro).",
    },
    "CHIM-C10-NCOM-096": {
        "options": {"C": "(NH₄)₂SO₄", "E": "(NH₄)₂SO₃"},
        "answer_text": "(NH₄)₂SO₃",
        "explanation": "Combinando il catione monovalente ammonio NH₄⁺ con l'anione bivalente solfito SO₃²⁻ (derivato da H₂SO₃) in rapporto 2:1 per la neutralità elettrica si ottiene (NH₄)₂SO₃.",
    },
    "CHIM-C10-NCOM-099": {
        "options": {"A": "ClO₂⁻", "B": "ClO₃⁻", "C": "Cl⁻", "D": "ClO₄⁻", "E": "ClO⁻"},
        "answer_text": "ClO₃⁻",
        "explanation": "Lo ione clorato deriva dall'acido clorico HClO₃ (cloro con n.o. +5) ed è rappresentato dalla formula ClO₃⁻.",
    },
    "CHIM-C10-COMP-002": {
        "cloze_stem": "Gli {{c1::idracidi}} si scrivono con la formula generale HₙX dove X è un alogeno o lo zolfo.",
        "accepted_synonyms": ["idracidi"],
        "explanation": "Gli idracidi sono acidi binari non ossigenati di formula generale HₙX formati dall'idrogeno con gli alogeni (HF, HCl, HBr, HI, con n = 1), con lo zolfo (H₂S, n = 2) o col gruppo cianuro (HCN).",
    },
    "CHIM-C10-COMP-009": {
        "cloze_stem": "Gli ossidi {{c1::acidi}} hanno formula generale X₂Oₙ, dove X è un non metallo.",
        "accepted_synonyms": ["acidi", "anidridi"],
        "explanation": "Gli ossidi dei non metalli (detti ossidi acidi o anidridi, di stechiometria formale X₂Oₙ prima dell'eventuale semplificazione degli indici) reagiscono con l'acqua generando ossiacidi.",
    },
    "CHIM-C10-COMP-016": {
        "cloze_stem": "La formula di un {{c1::ossiacido}} è generalmente HₙXOₘ.",
        "accepted_synonyms": ["ossiacido", "ossoacido"],
        "explanation": "Un ossiacido (acido ternario ossigenato) presenta formula generale HₙXOₘ, con idrogeno acido legato ad atomi di ossigeno a loro volta legati a un non metallo (o metallo ad alto stato di ossidazione) X.",
    },
    "CHIM-C10-COMP-017": {
        "cloze_stem": "L'acido {{c1::solforico}} (H₂SO₄) è un tipico ossiacido.",
        "accepted_synonyms": ["solforico"],
        "explanation": "H₂SO₄ contiene zolfo esavalente (n.o. +6, suffisso -ico) ed è l'acido solforico, ossiacido biprotico forte.",
    },
    "CHIM-C10-COMP-024": {
        "cloze_stem": "Gli ossidi {{c1::basici}} hanno formula generale M₂Oₙ, dove M è un metallo.",
        "accepted_synonyms": ["basici"],
        "explanation": "La combinazione di un metallo M (a basso/medio stato di ossidazione +n) con l'ossigeno (−2) forma gli ossidi basici M₂Oₙ, che reagendo con l'acqua danno idrossidi M(OH)ₙ.",
    },
    "CHIM-C10-COMP-033": {
        "cloze_stem": "La nomenclatura tradizionale degli idrossidi usa la parola «{{c1::idrossido}}» seguita dal nome del metallo.",
        "accepted_synonyms": ["idrossido"],
        "explanation": "Per i composti ternari M(OH)ₙ la nomenclatura tradizionale premette il termine «idrossido» seguito da «di + metallo» (se a unica valenza) o dall'aggettivo in -oso/-ico (se a doppia valenza).",
    },
    "CHIM-C10-COMP-035": {
        "cloze_stem": "L'{{c1::idrossido}} di ferro(II), Fe(OH)₂, contiene ferro allo stato di ossidazione +2.",
        "accepted_synonyms": ["idrossido"],
        "explanation": "Nel composto Fe(OH)₂ (idrossido ferroso o diidrossido di ferro) due gruppi ossidrilici OH⁻ (−1 ciascuno) bilanciano il catione Fe²⁺ (stato di ossidazione +2).",
    },
    "CHIM-C11-NCOM-006": {
        "options": {
            "A": "Acido acetico > acido nitroso > acido permanganico",
            "B": "Acido solforico > acido solforoso > acido cianidrico",
            "C": "Acido solforoso > acido citrico > acido nitrico",
            "D": "Acido acetico > acido nitroso > acido nitrico",
            "E": "Acido solforico > acido nitrico > acido perclorico",
        },
        "answer_text": "Acido solforico > acido solforoso > acido cianidrico",
        "explanation": "L'acido solforico H₂SO₄ è un acido forte (pK_a1 < 0), l'acido solforoso H₂SO₃ è un acido debole-medio (K_a1 ≈ 1,5 × 10⁻²) e l'acido cianidrico HCN è un acido debolissimo (K_a ≈ 6 × 10⁻¹⁰): l'ordine decrescente di forza acida è quindi H₂SO₄ > H₂SO₃ > HCN.",
    },
    "CHIM-C11-NCOM-007": {
        "options": {"C": "cede ioni H⁺"},
        "answer_text": "cede ioni H⁺",
        "explanation": "Secondo le definizioni di Arrhenius e di Brønsted-Lowry, un acido è una specie chimica in grado di cedere ioni idrogeno H⁺ (protoni); la sola presenza di atomi di H nella molecola (es. CH₄) non è sufficiente.",
    },
    "CHIM-C11-NCOM-009": {
        "options": {"C": "un acido monoprotico"},
        "answer_text": "un acido monoprotico",
        "explanation": "L'acido nitrico HNO₃ contiene un solo atomo di idrogeno ionizzabile e in acqua libera un solo protone H⁺ per molecola (HNO₃ → H⁺ + NO₃⁻): è perciò un acido monoprotico.",
    },
    "CHIM-C11-NCOM-014": {
        "question": "Quale delle seguenti formule corrisponde a un acido debole?",
        "explanation": "L'acido cianidrico HCN si dissocia in acqua in misura minima (K_a ≈ 6,2 × 10⁻¹⁰) ed è quindi un acido molto debole, mentre HCl e HNO₃ sono acidi forti e NaOH è una base forte.",
    },
    "CHIM-C11-NCOM-015": {
        "question": "Quale/i dei seguenti acidi è/sono monoprotico/i in soluzione acquosa? 1. CH₃COOH  2. HNO₃  3. H₃PO₄",
        "options": {"A": "Solo 1 e 2", "E": "Solo 2 e 3"},
        "answer_text": "Solo 1 e 2",
        "explanation": "L'acido acetico CH₃COOH possiede un solo idrogeno acido carbossilico (i tre H del metile non si dissociano in acqua) ed è monoprotico così come l'acido nitrico HNO₃, mentre H₃PO₄ è un acido triprotico.",
    },
    "CHIM-C11-NCOM-016": {
        "options": {"C": "ioni negativi H⁻"},
        "explanation": "Secondo Arrhenius un acido in soluzione acquosa si dissocia liberando ioni positivi idrogeno H⁺ (che si idratano a ioni idronio H₃O⁺).",
        "errata_note": "Nota: un catione H⁺ privo dell'unico elettrone coincide fisicamente con un protone (opzione A, terminologia di Brønsted-Lowry); la chiave EdiSES seleziona D perché esplicita la carica ionica positiva («ioni positivi H⁺») in contrapposizione a «ioni negativi H⁻».",
    },
    "CHIM-C11-NCOM-019": {
        "question": "Una base è una sostanza che:",
        "options": {
            "A": "ha un gusto amarognolo",
            "B": "nessuna delle altre risposte è corretta",
            "C": "è capace di accettare elettroni",
            "D": "acquista una coppia di elettroni",
            "E": "ha disponibile un orbitale vuoto",
        },
        "answer": "B",
        "answer_text": "nessuna delle altre risposte è corretta",
        "explanation": "Chimicamente una base rilascia OH⁻ in acqua (Arrhenius), accetta protoni H⁺ (Brønsted-Lowry) oppure dona un doppietto elettronico (Lewis). Le opzioni C, D ed E descrivono invece un acido di Lewis (accettore di coppie elettroniche con orbitale vuoto), mentre il sapore amarognolo (A) è un carattere empirico-organolettico non definitorio: la chiave corretta è quindi B.",
        "errata_note": "Nota sul tie-break: la chiave ufficiale EdiSES (p. 293) conferma B («nessuna delle altre risposte è corretta»), poiché l'opzione A non costituisce una definizione chimica valida di base.",
    },
    "CHIM-C11-NCOM-021": {
        "question": "L'acido H₂CO₃ (acido carbonico) è:",
        "explanation": "L'acido carbonico H₂CO₃ (O=C(OH)₂) possiede due gruppi ossidrilici acidi capaci di cedere due protoni in due equilibri successivi (verso HCO₃⁻ e CO₃²⁻), ed è quindi un acido biprotico (diprotico).",
    },
    "CHIM-C11-NCOM-034": {
        "options": {"A": "SO₄²⁻", "B": "HPO₃²⁻", "C": "OH⁻", "D": "HSO₄⁻", "E": "NH₄⁺"},
        "answer_text": "NH₄⁺",
        "explanation": "Secondo Brønsted-Lowry lo ione ammonio NH₄⁺ può solo cedere un protone formando NH₃, ma non può accettarne altri perché l'azoto non ha doppietti elettronici liberi: si comporta quindi unicamente da acido (HSO₄⁻ è invece anfotero; SO₄²⁻, OH⁻ e HPO₃²⁻ — derivato dall'acido fosforoso diprotico H₃PO₃ — agiscono da basi).",
    },
    "CHIM-C11-NCOM-037": {
        "explanation": "L'anidride clorosa Cl₂O₃ è un ossido acido (ossido di un non metallo) che reagendo con l'acqua forma un ossiacido (Cl₂O₃ + H₂O → 2 HClO₂, acido cloroso); Na₂O, NH₃ e KOH danno soluzioni basiche, mentre Al₂O₃ è un ossido anfotero insolubile in acqua.",
    },
    "CHIM-C11-NCOM-042": {
        "options": {"A": "NH₄Cl", "B": "CH₃COONa"},
        "answer_text": "CH₃COONa",
        "explanation": "L'acetato di sodio CH₃COONa è il sale di una base forte (NaOH) e di un acido debole (CH₃COOH): in acqua lo ione acetato subisce idrolisi basica (CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻) portando il pH sopra 7 (NH₄Cl dà idrolisi acida; NaBr, NaCl e KCl sono sali neutri).",
    },
    "CHIM-C11-NCOM-048": {
        "options": {"C": "7"},
        "explanation": "A 25 °C la costante del prodotto ionico dell'acqua vale K_w = [H⁺]·[OH⁻] = 1,0 × 10⁻¹⁴ M².",
    },
    "CHIM-C11-NCOM-051": {
        "question": "Se in una soluzione acquosa la concentrazione degli ioni ossidrile è 10⁻³ moli/litro, la concentrazione degli ioni idrogeno deve essere:",
        "options": {
            "A": "10⁴ moli/litro",
            "B": "10⁻⁴ moli/litro",
            "C": "10⁻³ moli/litro",
            "D": "10⁻⁵ moli/litro",
            "E": "10⁻¹¹ moli/litro",
        },
        "answer_text": "10⁻¹¹ moli/litro",
        "explanation": "Applicando il prodotto ionico dell'acqua a 25 °C ([H⁺]·[OH⁻] = 10⁻¹⁴), da [OH⁻] = 10⁻³ mol/L si ottiene [H⁺] = 10⁻¹⁴ / 10⁻³ = 10⁻¹¹ mol/L.",
    },
    "CHIM-C11-NCOM-054": {
        "explanation": "20 g di NaOH (MM = 40 g/mol) sono 0,50 mol in 0,500 L, quindi la soluzione di NaOH è 1,0 M. Le moli di H₂SO₄ in 25 mL 1,0 M sono 0,025 mol; poiché H₂SO₄ è biprotico (H₂SO₄ + 2 NaOH → Na₂SO₄ + 2 H₂O), servono 2 × 0,025 = 0,050 mol di NaOH, pari a V = 0,050 mol / 1,0 M = 0,050 L = 50 mL.",
    },
    "CHIM-C11-NCOM-055": {
        "explanation": "KOH è una base forte monoprotica: a concentrazione 10⁻⁵ M fornisce [OH⁻] = 10⁻⁵ M, da cui a 25 °C [H₃O⁺] = K_w / [OH⁻] = 10⁻¹⁴ / 10⁻⁵ = 10⁻⁹ M. Poiché 10⁻⁹ M non compare tra le opzioni A, C, D, E, è corretta B («nessuna delle altre risposte è corretta»).",
    },
    "CHIM-C11-NCOM-058": {
        "explanation": "Dalla relazione K_w = [H₃O⁺][OH⁻] = 1,0 × 10⁻¹⁴ mol² dm⁻⁶ a 25 °C, con [H₃O⁺] = 1,0 × 10⁻⁸ mol dm⁻³ si ricava [OH⁻] = 1,0 × 10⁻¹⁴ / 1,0 × 10⁻⁸ = 1,0 × 10⁻⁶ mol dm⁻³.",
    },
    "CHIM-C11-NCOM-063": {
        "options": {
            "A": "[H⁺] > 10⁻⁷ M",
            "C": "[H⁺] < 10⁻⁷ M",
            "D": "[H⁺] = 10⁻⁷ M",
        },
        "answer_text": "[H⁺] > 10⁻⁷ M",
        "explanation": "A 25 °C una soluzione acquosa è definita in generale acida quando la concentrazione di ioni idrogeno supera quella dell'acqua pura, cioè [H⁺] > 10⁻⁷ M (ossia pH < 7; l'opzione E indica solo un singolo valore particolare).",
    },
    "CHIM-C11-NCOM-065": {
        "explanation": "Tutte le specie elencate (LiOH, NaOH, KOH) sono idrossidi alcalini forti completamente dissociati in acqua: la soluzione più basica è quindi quella con maggiore concentrazione molare di ioni OH⁻, ossia NaOH 1 M (pH = 14).",
    },
    "CHIM-C11-NCOM-070": {
        "options": {"E": "Il valore del pH aumenta di 2"},
        "answer_text": "Il valore del pH aumenta di 2",
        "explanation": "Portando il volume di un acido forte come HCl da 10 cm³ a 1000 cm³ la soluzione viene diluita di un fattore 100 (10²): la concentrazione [H⁺] diventa 1/100 di quella iniziale e pertanto pH_fin = −log₁₀([H⁺]₀ / 10²) = pH_iniz + 2.",
    },
    "CHIM-C11-NCOM-082": {
        "question": "Volendo preparare 10 L di soluzione di NaOH (massa molare: 40 g/mol) a pH 12, in quale di questi modi si può procedere?",
        "options": {"E": "Prelevare 10 mL da una soluzione di NaOH 1 M e diluire fino a 10 L"},
        "explanation": "A 25 °C pH = 12 corrisponde a pOH = 2, cioè [OH⁻] = 10⁻² M = 0,01 mol/L. In V = 10 L occorrono n = 0,01 mol/L × 10 L = 0,10 mol di NaOH, la cui massa vale m = 0,10 mol × 40 g/mol = 4 g.",
    },
    "CHIM-C11-NCOM-087": {
        "options": {"C": "5", "D": "10⁻⁷"},
        "explanation": "Nell'acqua pura a 25 °C [H₃O⁺] = [OH⁻] = 10⁻⁷ M, perciò il valore del pH è −log₁₀(10⁻⁷) = 7.",
    },
    "CHIM-C11-NCOM-090": {
        "explanation": "Trattando l'acido solforico H₂SO₄ in soluzione molto diluita (0,002 M) come completamente dissociato in entrambi gli stadi (H₂SO₄ → 2 H⁺ + SO₄²⁻), la concentrazione idrogenionica è [H⁺] = 2 × 0,002 = 0,004 M, da cui pH = −log₁₀(0,004).",
    },
    "CHIM-C11-NCOM-097": {
        "options": {"B": "[OH⁻] > [H₃O⁺]", "D": "[H⁺] > [OH⁻]"},
        "explanation": "A 25 °C una soluzione con pH > 7 è basica: in essa [H⁺] < 10⁻⁷ M e conseguentemente [OH⁻] > 10⁻⁷ M, per cui vale la disuguaglianza [H⁺] < [OH⁻].",
        "errata_note": "Nota: in soluzione acquosa H⁺ e H₃O⁺ indicano la medesima specie idratata, per cui anche l'opzione B ([OH⁻] > [H₃O⁺]) esprime matematicamente la stessa relazione vera di E ([H⁺] < [OH⁻]); la chiave ufficiale EdiSES riporta E.",
    },
    "CHIM-C11-NCOM-099": {
        "question": "Quando la [OH⁻] è minore della [H⁺]?",
        "options": {
            "A": "A pH = 8",
            "B": "A pH = 5",
            "C": "A pH = 10",
            "D": "A pH = 2",
            "E": "A pH = 7",
        },
        "answer_text": "A pH = 2",
        "explanation": "A 25 °C si ha [OH⁻] < [H⁺] in ambiente acido (pH < 7): a pH = 2 vale [H⁺] = 10⁻² M e [OH⁻] = 10⁻¹² M, con marcata prevalenza di [H⁺].",
        "errata_note": "Nota: a 25 °C la disuguaglianza [OH⁻] < [H⁺] è soddisfatta per qualunque pH < 7, quindi anche a pH = 5 (opzione B: [H⁺] = 10⁻⁵ M > [OH⁻] = 10⁻⁹ M); la chiave EdiSES seleziona D (pH = 2).",
    },
    "CHIM-C11-NCOM-100": {
        "options": {"C": "4, 3, 1, 2", "D": "3, 1, 2, 4"},
        "answer_text": "3, 1, 2, 4",
        "explanation": "Il pH cresce al diminuire di [H⁺]: (3) H₂SO₄ 0,2 M è diprotico e fornisce la massima [H⁺] (> 0,2 M, pH minimo); seguono gli acidi forti monoprotici (1) HCl 0,2 M ([H⁺] = 0,2 M, pH = 0,7) e (2) HNO₃ 0,1 M ([H⁺] = 0,1 M, pH = 1,0); infine l'acido debole parzialmente dissociato (4) CH₃COOH 0,1 M ha la minima [H⁺] e il pH più alto (~2,9). L'ordine crescente di pH è 3, 1, 2, 4.",
    },
    "CHIM-C11-NCOM-106": {
        "explanation": "Per definizione di Sørensen il pH = −log₁₀[H⁺] misura l'acidità di una soluzione acquosa esprimendo su scala logaritmica la concentrazione molare degli ioni idrogeno H⁺ (idronio H₃O⁺).",
    },
    "CHIM-C11-NCOM-110": {
        "explanation": "A 25 °C un pH = 6 (< 7) indica una soluzione debolmente acida nella quale [H₃O⁺] = 10⁻⁶ M e [OH⁻] = 10⁻⁸ M: vale pertanto [H₃O⁺] > [OH⁻].",
    },
    "CHIM-C11-NCOM-121": {
        "explanation": "Sciogliendo n = 10⁻⁴ mol dell'acido forte HCl in V = 100 mL = 0,10 L si ottiene [H⁺] = 10⁻⁴ mol / 10⁻¹ L = 10⁻³ M, da cui pH = −log₁₀(10⁻³) = 3.",
    },
    "CHIM-C11-NCOM-127": {
        "question": "Una soluzione acquosa a 25 °C in cui la concentrazione di H⁺ è uguale a 10⁻⁵ M e la concentrazione di OH⁻ è pari a 10⁻⁸ M:",
        "explanation": "In ogni soluzione acquosa all'equilibrio a 25 °C il prodotto [H⁺]·[OH⁻] deve eguagliare K_w = 10⁻¹⁴ M²; poiché sulla scansione originale i dati sono 10⁻⁵ M e 10⁻⁸ M (il cui prodotto è 10⁻¹³ ≠ 10⁻¹⁴), tale soluzione non può esistere.",
    },
    "CHIM-C11-NCOM-129": {
        "explanation": "Una soluzione 0,001 M (10⁻³ M) di un acido monoprotico HA presenta pH = 3, ossia [H⁺] = 10⁻³ M = C_a: il grado di dissociazione è α = 1 (dissociazione completa al 100%), proprietà distintiva di un acido forte.",
    },
    "CHIM-C11-NCOM-144": {
        "explanation": "A 25 °C un pH = 8 corrisponde a [H₃O⁺] = 10⁻⁸ M e [OH⁻] = 10⁻⁶ M: a prescindere dal soluto con cui la soluzione è stata preparata (base forte diluita, base debole o sale ad idrolisi basica), è certamente vero che il numero di ioni H₃O⁺ è inferiore al numero di ioni OH⁻.",
    },
    "CHIM-C11-NCOM-148": {
        "explanation": "Il bromuro di potassio KBr deriva dalla neutralizzazione tra una base forte (KOH) e un acido forte (HBr): né K⁺ né Br⁻ danno idrolisi in acqua, per cui dal punto di vista acido-base la soluzione è neutra (pH = 7 a 25 °C).",
        "errata_note": "Nota: dal punto di vista osmotico rispetto al plasma umano (~300 mOsm/L), KBr all'1% m/V (~0,084 M, i ≈ 2 ⇒ ~168 mOsm/L) risulterebbe anche ipotonica (B); collocato nel capitolo sugli equilibri acido-base, il quesito valuta la reazione di idrolisi del sale (D: neutra).",
    },
    "CHIM-C11-NCOM-156": {
        "explanation": "Il cloruro di sodio NaCl è un sale formato da catione di base forte (NaOH) e anione di acido forte (HCl): non subisce idrolisi acido-base e la soluzione acquosa resta neutra con pH = 7,0 (a 25 °C).",
    },
    "CHIM-C11-NCOM-162": {
        "question": "Il bicarbonato di sodio sciolto in acqua dà una soluzione:",
        "options": {"A": "acida in quanto il sale è formato da uno ione a carattere acido e uno a carattere neutro (Na⁺)"},
        "explanation": "In NaHCO₃ lo ione Na⁺ è acido-base neutro, mentre lo ione idrogenocarbonato HCO₃⁻ è anfiprotico ma con costante di idrolisi basica K_b = K_w/K_a1 ≈ 2,3 × 10⁻⁸ maggiore della seconda dissociazione acida K_a2 ≈ 4,7 × 10⁻¹¹: prevale quindi il carattere basico (pH ≈ 8,3).",
    },
    "CHIM-C11-NCOM-170": {
        "question": "Se si aggiunge NH₄Cl ad una soluzione di ammoniaca:",
        "explanation": "L'aggiunta del sale NH₄Cl fornisce in soluzione lo ione ammonio NH₄⁺, acido coniugato della base debole NH₃: la coppia coniugata NH₃ / NH₄⁺ in concentrazioni comparabili costituisce un classico sistema tampone basico.",
        "errata_note": "Nota: per effetto dello ione comune NH₄⁺ l'equilibrio NH₃ + H₂O ⇌ NH₄⁺ + OH⁻ retrocede riducendo [OH⁻], quindi anche il pH diminuisce rispetto all'ammoniaca pura (opzione D vera); la chiave ufficiale EdiSES è E (formazione di soluzione tampone).",
    },
    "CHIM-C11-COMP-011": {
        "cloze_stem": "Un acido {{c1::forte}} si dissocia completamente in acqua per produrre H₃O⁺.",
        "accepted_synonyms": ["forte"],
        "explanation": "Un acido forte (es. HCl, HBr, HI, HNO₃, HClO₄) trasferisce quantitativamente i propri protoni all'acqua (grado di dissociazione α ≈ 1) generando ioni idronio H₃O⁺.",
    },
    "CHIM-C11-COMP-021": {
        "cloze_stem": "Tra Kₐ e K_b esiste una relazione tramite la costante {{c1::ionica}} (K_w) dell'acqua.",
        "accepted_synonyms": ["ionica", "del prodotto ionico", "di autoprotolisi"],
        "explanation": "Per qualsiasi coppia coniugata acido-base in soluzione acquosa il prodotto della costante acida per la costante basica eguaglia il prodotto ionico dell'acqua: Kₐ · K_b = K_w (= 1,0 × 10⁻¹⁴ a 25 °C).",
    },
    "CHIM-C11-COMP-022": {
        "cloze_stem": "L'autoprotolisi dell'acqua genera spontaneamente piccolissime quantità di {{c1::H₃O⁺}} e OH⁻.",
        "answer": "H₃O⁺",
        "answer_text": "H₃O⁺",
        "accepted_synonyms": ["H3O+", "H₃O⁺", "H+", "H⁺", "ioni idronio"],
        "explanation": "Nell'equilibrio di autoprotolisi 2 H₂O ⇌ H₃O⁺ + OH⁻ si formano concentrazioni equimolari pari a 10⁻⁷ M (a 25 °C) di ioni idronio H₃O⁺ e ioni idrossido OH⁻.",
    },
    "CHIM-C12-NCOM-021": {
        "question": "La formula di struttura CH₂=CH–CH=CH₂ corrisponde a:",
        "options": {"B": "1-butene"},
        "explanation": "La catena lineare a quattro atomi di carbonio contenente due doppi legami coniugati in posizione 1 e 3 è l'1,3-butadiene (comunemente butadiene).",
    },
    "CHIM-C12-NCOM-038": {
        "options": {"A": "gli alcoli", "B": "gli alcani"},
        "answer_text": "gli alcoli",
        "explanation": "L'addizione elettrofila acido-catalizzata di acqua (idratazione) al doppio legame C=C di un alchene segue la regola di Markovnikov e produce un alcol (R–CH=CH₂ + H₂O → R–CH(OH)–CH₃).",
    },
    "CHIM-C12-NCOM-059": {
        "question": "Il legame fra gli atomi di carbonio nel propano di che tipo è?",
        "options": {"D": "σ", "E": "Multiplo"},
        "answer_text": "σ",
        "explanation": "Il propano (CH₃–CH₂–CH₃) è un alcano saturo in cui tutti gli atomi di carbonio sono ibridati sp³ e uniti tra loro esclusivamente da legami covalenti singoli di tipo σ.",
    },
    "CHIM-C12-NCOM-068": {
        "options": {
            "B": "contenga elettroni π delocalizzati",
            "C": "i suoi atomi siano ibridizzati sp³",
            "D": "non sia ciclico",
        },
        "answer_text": "contenga elettroni π delocalizzati",
        "explanation": "Secondo i criteri di aromaticità di Hückel, un composto aromatico deve essere ciclico, planare, completamente coniugato (atomi sp²) e possedere una nube continua di (4n + 2) elettroni π delocalizzati sull'anello.",
    },
    "CHIM-C12-NCOM-071": {
        "explanation": "Gli alcani di formula generale C_nH_{2n+2} formano una serie omologa perché ciascun termine differisce dal precedente e dal successivo per un gruppo metilenico costante –CH₂– (14 u).",
        "errata_note": "Refuso tipografico EdiSES nell'opzione C: la stampa riporta «gruppo -CH₃» invece del gruppo metilenico «-CH₂-» (omologo successivo: C_nH_{2n+2} + CH₂ → C_{n+1}H_{2n+4}); la chiave ufficiale EdiSES è C, sebbene preso alla lettera il refuso renderebbe difendibile A.",
    },
    "CHIM-C12-NCOM-078": {
        "options": {"A": "Sì, talvolta"},
        "explanation": "Un idrogeno prende il grado (primario, secondario, terziario) del carbonio a cui è legato; poiché un carbonio quaternario è già legato a quattro altri atomi di carbonio e non può legare alcun atomo di idrogeno, in un alcano non possono mai esservi idrogeni quaternari.",
        "errata_note": "Nota: proprio per la tetravalenza del carbonio gli idrogeni quaternari non esistono affatto (opzione E anch'essa vera); la chiave ufficiale EdiSES risponde direttamente alla domanda «Si possono avere...?» con D («No, mai»).",
    },
    "CHIM-C12-NCOM-081": {
        "question": "Il composto CH₃–CH₂–CH₃ presenta:",
        "options": {"E": "un atomo di carbonio terziario e due primari"},
        "explanation": "Nel propano (CH₃–CH₂–CH₃) i due carboni terminali –CH₃ sono legati ciascuno a un solo altro carbonio (primari), mentre il carbonio centrale –CH₂– è legato a due atomi di carbonio (secondario).",
    },
    "CHIM-C12-NCOM-085": {
        "explanation": "Nel metano CH₄ i quattro atomi di idrogeno sono legati all'unico atomo di carbonio (gruppo metilico) e vengono classificati in chimica organica come idrogeni metilici (distinti da primari, secondari e terziari).",
        "errata_note": "Nota: per la simmetria tetraedrica T_d del metano i quattro atomi di H sono anche chimicamente e magneticamente equivalenti tra loro (opzione E); nel contesto della classificazione C/H degli alcani la chiave EdiSES è A («metilici»).",
    },
    "CHIM-C12-NCOM-108": {
        "question": "I legami fra gli atomi di carbonio negli alcani di che tipo sono?",
        "options": {
            "A": "A volte σ e a volte π",
            "B": "Tutti π",
            "C": "Tutti σ",
            "D": "A volte dativi e a volte π",
        },
        "answer_text": "Tutti σ",
        "explanation": "Gli alcani sono idrocarburi saturi privi di legami multipli: ogni legame C–C (così come ogni C–H) nasce dalla sovrapposizione frontale di orbitali ed è esclusivamente di tipo σ.",
    },
    "CHIM-C12-NCOM-121": {
        "options": {"A": "σ", "C": "σ e π", "E": "π"},
        "answer_text": "σ",
        "explanation": "Nell'etano (H₃C–CH₃) i due atomi di carbonio ibridati sp³ sono uniti da un legame covalente semplice generato da sovrapposizione assiale sp³–sp³, cioè un legame σ.",
    },
    "CHIM-C12-NCOM-129": {
        "question": "Qual è lo stato di ibridazione degli orbitali del carbonio nel cicloesano (C₆H₁₂)?",
        "explanation": "Nel cicloesano (cicloalcano saturo C₆H₁₂) ciascuno dei sei atomi di carbonio forma quattro legami singoli σ (due C–C e due C–H) ed è pertanto ibridato sp³ (adottando la conformazione a sedia priva di tensione angolare).",
    },
    "CHIM-C12-NCOM-134": {
        "options": {
            "B": "due legami π",
            "C": "un legame σ e un legame π",
            "E": "due legami σ",
        },
        "answer_text": "un legame σ e un legame π",
        "explanation": "Nell'etilene (etene, H₂C=CH₂) i due carboni sono ibridati sp²: il doppio legame C=C comprende un legame σ frontale (sp²–sp²) e un legame π laterale tra i due orbitali p non ibridati.",
    },
    "CHIM-C12-NCOM-135": {
        "question": "Il triplo legame dell'acetilene è costituito da:",
        "options": {
            "B": "tre legami π",
            "C": "due legami σ e un legame π",
            "D": "tre legami σ",
            "E": "un legame σ e due legami π",
        },
        "answer_text": "un legame σ e due legami π",
        "explanation": "Nell'acetilene (etino, HC≡CH) i carboni sono ibridati sp: il triplo legame C≡C è formato da un legame σ assiale (sp–sp) e da due legami π perpendicolari ottenuti dalla sovrapposizione laterale delle due coppie di orbitali p puri.",
    },
    "CHIM-C12-NCOM-141": {
        "options": {
            "A": "CH₂=C=CH₂",
            "B": "CH₂=CH₂",
            "C": "HC≡CH",
            "D": "CH₃–C≡CH",
            "E": "CH₃–CH=CH₂",
        },
        "answer_text": "CH₃–C≡CH",
        "explanation": "Il propino è l'alchino a tre atomi di carbonio (C₃H₄, formula C_nH_{2n−2} con n = 3) caratterizzato da un triplo legame C≡C: la sua formula di struttura condensata è CH₃–C≡CH.",
    },
    "CHIM-C12-NCOM-159": {
        "options": {"B": "CO₂ e H₂O"},
        "answer_text": "CO₂ e H₂O",
        "explanation": "La combustione completa degli idrocarburi della benzina o del gasolio in presenza di ossigeno sufficiente produce come prodotti stechiometrici principali diossido di carbonio (CO₂) e vapore acqueo (H₂O).",
    },
    "CHIM-C12-NCOM-161": {
        "crop_figure": True,
        "explanation": "Osservando le formule scheletriche in figura: la molecola A contiene un doppio legame C=C (alchene), la molecola B presenta solo legami singoli C–C (alcano) e la molecola C presenta un triplo legame C≡C con geometria lineare sul gruppo C≡C (alchino).",
    },
    "CHIM-C12-NCOM-164": {
        "question": "La struttura R–NH₂ caratterizza:",
        "explanation": "La sostituzione di un solo atomo di idrogeno dell'ammoniaca NH₃ con un radicale organico alchilico o arilico R dà un'ammina primaria di formula generale R–NH₂.",
    },
    "CHIM-C12-NCOM-172": {
        "explanation": "Gli acidi grassi insaturi naturali sono acidi monocarbossilici a catena lineare che presentano nella coda alifatica sia legami semplici C–C sia uno o più doppi legami C=C.",
        "errata_note": "Refuso tipografico EdiSES nell'opzione E: la stampa riporta «contengono doppi legami semplici» per caduta di «e legami» («contengono doppi legami [e legami] semplici»); B («solo legami doppi») e C («solo legami semplici») sono certamente errate.",
    },
    "CHIM-C12-NCOM-178": {
        "question": "Qual è la struttura della benzaldeide?",
        "options": {"B": "C₆H₁₁CH=O", "C": "C₆H₅CH=O"},
        "answer_text": "C₆H₅CH=O",
        "explanation": "La benzaldeide è la più semplice aldeide aromatica, costituita da un anello fenilico C₆H₅– legato direttamente al gruppo formilico –CH=O: la formula è quindi C₆H₅CH=O.",
    },
    "CHIM-C12-NCOM-207": {
        "question": "Il composto CH₂O prende il nome di:",
        "explanation": "CH₂O (ossia H–CH=O, metanale nella nomenclatura IUPAC) è il primo termine della serie delle aldeidi ed è universalmente noto col nome tradizionale di formaldeide (o aldeide formica).",
    },
    "CHIM-C12-NCOM-217": {
        "question": "Il composto CH₃–CH₂–NH–CH₃ prende il nome di:",
        "options": {"A": "metil-etil ammina", "C": "ammoniaca etanoata"},
        "answer_text": "metil-etil ammina",
        "explanation": "CH₃–CH₂–NH–CH₃ è un'ammina secondaria asimmetrica in cui l'atomo di azoto lega un gruppo metile (–CH₃) e un gruppo etile (–CH₂CH₃): nella nomenclatura radicofunzionale si chiama etilmetilammina (o metil-etil ammina; IUPAC: N-metiletanammina).",
    },
    "CHIM-C12-NCOM-223": {
        "question": "CH₃–CH(OH)–CH₂–CH₂–CH₃ rappresenta:",
        "explanation": "La presenza del gruppo funzionale ossidrilico –OH legato a un atomo di carbonio saturo sp³ (in posizione 2 di una catena a cinque carboni: pentan-2-olo) identifica un alcol secondario.",
    },
    "CHIM-C12-NCOM-230": {
        "options": {"B": "R–CO–NH₂"},
        "answer_text": "R–CO–NH₂",
        "explanation": "Le ammidi primarie derivano formalmente dagli acidi carbossilici per sostituzione dell'ossidrile –OH del carbossile con il gruppo –NH₂ e hanno formula generale R–CO–NH₂ (R–COOH è acido carbossilico, R–O–R etere, R–CO–R chetone).",
    },
    "CHIM-C12-NCOM-238": {
        "explanation": "Nella molecola Cl–CH₂–CH₂–OH il gruppo principale a priorità maggiore è l'ossidrile alcolico –OH, che assegna il numero 1 al carbonio a cui è legato (etanolo); l'atomo di cloro si trova quindi sul carbonio 2, dando il 2-cloroetanolo.",
    },
    "CHIM-C12-NCOM-245": {
        "question": "Il composto CH₃–CH₂–CO–NH–CH₃ rappresenta:",
        "explanation": "Il concatenamento funzionale –CO–NH– tra un gruppo acilico (propanoile) e un azoto sostituito caratterizza il legame ammidico: si tratta di un'ammide secondaria N-sostituita (N-metilpropanammide).",
    },
    "CHIM-C12-NCOM-253": {
        "options": {"A": "C₆H₅NO₂", "B": "C₆H₅NH₂"},
        "answer_text": "C₆H₅NH₂",
        "explanation": "L'anilina (fenilammina o benzenammina) è la più semplice ammina primaria aromatica, formata da un anello benzenico legato a un gruppo amminico –NH₂: la sua formula è C₆H₅NH₂.",
    },
    "CHIM-C12-NCOM-254": {
        "question": "Quale composto è rappresentato dalla formula CH₃–CO–CH₃?",
        "options": {"D": "Un'aldeide"},
        "explanation": "CH₃–CO–CH₃ (propanone o acetone) contiene il gruppo carbonilico >C=O legato a due atomi di carbonio ed è pertanto il più semplice rappresentante della classe dei chetoni.",
    },
    "CHIM-C12-NCOM-271": {
        "crop_figure": True,
        "explanation": "Negli alogenuri acilici R–CO–Cl il cloro fortemente elettronegativo esercita un intenso effetto induttivo elettron-attrattore (−I) superiore alla debole retrodonazione mesomera (+M) e costituisce inoltre un ottimo gruppo uscente (Cl⁻): ciò accentua la carica parziale positiva δ⁺ sul carbonio carbonilico, esaltandone la reattività verso l'attacco dei nucleofili.",
    },
    "CHIM-C12-NCOM-276": {
        "question": "I composti CH₃–CH₂–O–CH₂–CH₃ e CH₃–CO–CH₃ sono, nell'ordine:",
        "options": {"E": "un chetone e un estere"},
        "explanation": "Il primo composto presenta un atomo di ossigeno a ponte tra due gruppi etilici (R–O–R', etere dietilico, cioè un etere), mentre il secondo contiene un gruppo carbonilico interno >C=O tra due metili (acetone, cioè un chetone).",
    },
    "CHIM-C12-COMP-029": {
        "cloze_stem": "La combustione degli {{c1::alcani}} produce CO₂ e H₂O liberando energia.",
        "accepted_synonyms": ["alcani", "idrocarburi"],
        "explanation": "La combustione completa degli alcani (e in generale degli idrocarburi) con eccesso di O₂ è una reazione redox fortemente esotermica che trasforma tutto il carbonio in CO₂ e tutto l'idrogeno in H₂O.",
    },
    "CHIM-C12-COMP-032": {
        "cloze_stem": "Il {{c1::butano}} (C₄H₁₀) ha due isomeri: lineare e isobutano.",
        "accepted_synonyms": ["butano"],
        "explanation": "C₄H₁₀ è il primo alcano a presentare isomeria costituzionale di catena, esistendo come n-butano lineare (CH₃CH₂CH₂CH₃) e come isobutano ramificato (2-metilpropano, CH(CH₃)₃).",
    },
    "CHIM-C12-COMP-036": {
        "cloze_stem": "Un {{c1::alchino}} è un idrocarburo insaturo con uno o più tripli legami C≡C.",
        "accepted_synonyms": ["alchino"],
        "explanation": "Gli alchini sono idrocarburi insaturi caratterizzati dalla presenza di almeno un triplo legame carbonio-carbonio C≡C (formula generale C_nH_{2n−2} per gli alchini aciclici con un solo triplo legame).",
    },
    "CHIM-C12-COMP-049": {
        "cloze_stem": "L'anilina è un derivato {{c1::aromatico}} contenente un gruppo –NH₂.",
        "accepted_synonyms": ["aromatico", "benzenico"],
        "explanation": "L'anilina (C₆H₅–NH₂) è un'ammina aromatica primaria ottenuta per sostituzione di un idrogeno dell'anello benzenico con il gruppo amminico –NH₂.",
    },
    "CHIM-C12-COMP-055": {
        "cloze_stem": "Una solfonazione introduce un gruppo {{c1::solfonico}} (–SO₃H) sul benzene.",
        "accepted_synonyms": ["solfonico"],
        "explanation": "La solfonazione aromatica è una sostituzione elettrofila (condotta con H₂SO₄ fumante / SO₃) che lega all'anello benzenico il gruppo solfonico –SO₃H formando l'acido benzensolfonico.",
    },
    "CHIM-C12-COMP-067": {
        "cloze_stem": "Un'{{c1::aldeide}} contiene il gruppo funzionale –CHO.",
        "accepted_synonyms": ["aldeide"],
        "explanation": "Le aldeidi sono caratterizzate dal gruppo formilico terminale –CHO (un carbonile >C=O legato ad almeno un atomo di idrogeno).",
    },
    "CHIM-C13-NCOM-028": {
        "explanation": "Tra le alternative proposte dal quesito, l'unica riferibile a monosaccaridi comuni (gli esosi come glucosio, fruttosio e galattosio) è la formula bruta C₆H₁₂O₆ (glicogeno è un polisaccaride, i polimeri di amminoacidi sono proteine e il gruppo carbossilico caratterizza gli acidi organici).",
        "errata_note": "Nota biochimica: in senso rigoroso i monosaccaridi hanno formula generale (CH₂O)ₙ con 3 ≤ n ≤ 7 (comprendendo triosi C₃H₆O₃, pentosi come ribosio C₅H₁₀O₅, ecc., non solo gli esosi C₆H₁₂O₆), motivo per cui l'opzione C sarebbe formalmente difendibile; la chiave EdiSES seleziona E intendendo gli esosi rappresentativi.",
    },
    "CHIM-C13-NCOM-035": {
        "options": {"A": "hanno sei atomi di C nella molecola"},
        "answer_text": "hanno sei atomi di C nella molecola",
        "explanation": "I monosaccaridi si classificano in base al numero di atomi di carbonio della catena: triosi (3 C), tetrosi (4 C), pentosi (5 C) ed esosi (6 atomi di carbonio, formula C₆H₁₂O₆, come glucosio, galattosio e fruttosio).",
    },
    "CHIM-C13-NCOM-104": {
        "options": {
            "A": "A, B e D",
            "B": "A, C ed E",
            "C": "B e D",
            "D": "B e A",
            "E": "solo di tipo B",
        },
        "answer": "C",
        "answer_text": "B e D",
        "explanation": "Secondo la definizione ufficiale IUPAC (convenzione di Sanger), la struttura primaria di una proteina specifica l'intera connettività dei legami covalenti, comprendendo sia la sequenza dei legami peptidici (B) sia la posizione dei ponti disolfuro covalenti –S–S– tra residui di cisteina (D); pertanto la chiave ufficiale EdiSES è C («B e D»).",
        "errata_note": "Nota importante (tie-break): molti testi didattici di biochimica (es. Lehninger) restringono la definizione di struttura primaria ai soli legami peptidici («E: solo di tipo B») collocando i ponti disolfuro nella stabilizzazione della struttura terziaria, mentre la IUPAC e la chiave stampata EdiSES (p. 305) includono tutti i legami covalenti (C: «B e D»).",
    },
    "CHIM-C13-NCOM-109": {
        "options": {"B": "amminoacido naturale"},
        "answer_text": "amminoacido naturale",
        "explanation": "L'acido L-glutammico (glutammato) è uno dei 20 α-amminoacidi naturali proteinogenici, caratterizzato da una catena laterale acida contenente un secondo gruppo carbossilico (–CH₂–CH₂–COOH).",
    },
    "CHIM-C13-NCOM-126": {
        "explanation": "La struttura terziaria descrive l'avvolgimento spaziale tridimensionale globale dell'intera catena polipeptidica nativa guidato dalle interazioni tra i gruppi R.",
        "errata_note": "Nota terminologica: in stereochimica rigorosa il ripiegamento tridimensionale per rotazione attorno a legami singoli si definisce «conformazione» nativa (opzione E), mentre «configurazione» indica la disposizione stereochimica fissata dai legami covalenti (es. serie L); la chiave EdiSES riporta impropriamente B («la configurazione che può assumere la proteina»).",
    },
    "CHIM-C13-NCOM-156": {
        "explanation": "L'adenina (6-amminopurina) è una base azotata purinica biciclica eteroaromatica (costituente di DNA, RNA, ATP, NAD⁺ e FAD), classificata nel quesito come derivato amminico aromatico per esclusione di fosfolipidi, ormoni e amminoacidi.",
        "errata_note": "Nota chimica: strutturalmente l'adenina possiede un gruppo amminico esociclico primario (–NH₂ in C-6) unito a un anello eterociclico purinico (contenente un gruppo –NH– endociclico imidazolico), per cui definirla «ammina aromatica secondaria» (opzione E, chiave EdiSES) è impreciso.",
    },
    "CHIM-C13-COMP-019": {
        "cloze_stem": "Gli acidi grassi {{c1::saturi}} hanno solo legami semplici C–C.",
        "answer": "saturi",
        "answer_text": "saturi",
        "accepted_synonyms": ["saturi"],
        "explanation": "Gli acidi grassi privi di doppi legami nella catena idrocarburica (contenenti unicamente legami semplici C–C) si definiscono acidi grassi saturi.",
    },
}
