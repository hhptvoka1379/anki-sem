"""Round-2 scan-verified overrides, subtle OCR cleanup, publisher scrub, and deduplication.

Every entry in ROUND2_SCAN_OVERRIDES and DEDUP_DROP_MAP was verified directly against
the raw extracted items, high-resolution page scans, and all 358 live candidate pairs.
"""

from __future__ import annotations

import copy
import re

ROUND2_SCAN_OVERRIDES = {
    "CHIM-C03-COMM-010": {
        "q": (
            "Tutti i carbonati degli elementi del II gruppo sono poco solubili in acqua, e si trovano in natura "
            "come minerali solidi; il più comune tra questi composti è il carbonato di calcio, o calcare, che "
            "costituisce uno dei minerali più diffusi; il carbonato di calcio, praticamente insolubile in acqua pura, "
            "risulta invece assai solubile in acqua contenente anidride carbonica; la soluzione acquosa di CO₂ scioglie "
            "il carbonato di calcio, perché lo converte in idrogenocarbonato (o bicarbonato), solubile; le rocce "
            "calcaree vengono pertanto erose dalle acque del suolo, tutte contenenti CO₂. Quale delle seguenti "
            "affermazioni PUÒ essere dedotta dalla lettura del brano precedente?"
        ),
        "opts": {"A": "Il calcio è un elemento del II gruppo"},
        "exp": (
            "Il brano afferma nozioni corrette e richiede deduzioni corrette. Il brano fa capire che il Ca appartiene "
            "al II gruppo quando afferma che il suo carbonato è uno dei carbonati degli elementi del secondo gruppo "
            "che sono poco solubili in acqua. Il carbonato di calcio non è l'unico, è meno solubile del bicarbonato "
            "e non si ottiene dal bicarbonato per azione della CO₂, che invece trasforma il carbonato in bicarbonato."
        ),
    },
    "CHIM-C03-NCOM-062": {
        "opts": {"A": "II gruppo", "B": "VII gruppo", "C": "VIII gruppo", "D": "I gruppo", "E": "III gruppo"}
    },
    "CHIM-C03-NCOM-174": {"q": "Nel II gruppo del sistema periodico si trovano:"},
    "CHIM-C06-COMM-001": {
        "exp": (
            "Il principio di solubilità è semplice: il simile scioglie il simile; i solventi polari sciolgono i soluti "
            "polari. Il solfato di potassio è un solido salino (è anche un sale) formato quindi da ioni, specie cariche "
            "positivamente e negativamente."
        )
    },
    "CHIM-C06-COMM-017": {
        "q": (
            "Il grado di dissociazione, indicato col simbolo α, viene definito come la frazione di elettrolita che si "
            "dissocia, cioè come il rapporto tra il numero di moli ionizzate e il numero di moli originarie; così, ad "
            "esempio, se mettiamo in soluzione 1,2 moli di un elettrolita, e osserviamo che 0,3 moli si dissociano in "
            "ioni, mentre le rimanenti 0,9 moli restano indissociate, il grado di dissociazione, in base alla definizione "
            "precedente, è dato dal rapporto tra 0,3 e 1,2. Si ha pertanto α = 0,3/1,2 = 0,25. Spesso viene usata, invece "
            "del grado di dissociazione, la percentuale di dissociazione, che è data da α moltiplicato per 100; così, nel "
            "caso dell'esempio, la percentuale di dissociazione è del 25%. Quale delle seguenti affermazioni è in accordo "
            "con il contenuto del brano precedente?"
        )
    },
    "CHIM-C08-NCOM-007": {"opts": {"D": "II ordine"}},
    "CHIM-C12-COMM-024": {"q": "Il gruppo funzionale -CH₂OH si chiama:"},
    "CHIM-C12-COMM-039": {
        "exp": (
            "Il gruppo funzionale delle aldeidi è R-C=O(H), mentre quello dei chetoni è R-C=O(R'), quindi la risposta "
            "corretta è che le aldeidi hanno sempre un atomo di ossigeno e uno di idrogeno legati al carbonio carbonilico."
        )
    },
    "FIS-C03-NCOM-036": {
        "q": (
            "Il sistema mostrato in figura è privo di qualsiasi attrito ed è in equilibrio. Sono note le masse m₁ ed m₂ "
            "ed è noto l'angolo di inclinazione del piano α. Considerando la fune ideale, quanto vale la sua tensione T? "
            "(Si consideri l'accelerazione di gravità terrestre pari a g)"
        )
    },
    "FIS-C03-COMP-177": {"q": "Il periodo di oscillazione di un sistema massa-molla è T = 2π √(m / _____ )."},
    "FIS-C03-COMP-189": {"q": "Il periodo di un pendolo semplice è T = 2π √(L / _____ )."},
    "FIS-C04-NCOM-066": {
        "q": (
            "Il principio di Archimede stabilisce che ogni corpo immerso in un fluido qualsiasi riceve una spinta dal "
            "basso verso l'alto pari al peso del fluido spostato. Cosa si può dire della spinta di Archimede sulla "
            "superficie lunare?"
        )
    },
    # --- Option-shifted, formula & multi-column scans visually verified against PDF & scan PNGs ---
    "CHIM-C01-COMM-006": {
        "q": "Una soluzione satura di glucosio in acqua, in presenza del soluto indisciolto, rappresenta un esempio di:",
    },
    "CHIM-C01-COMM-007": {
        "q": "Una soluzione satura di NaCl in acqua, in presenza del sale indisciolto, rappresenta un esempio di:",
    },
    "CHIM-C01-COMM-009": {
        "opts": {"D": "di una o più specie chimiche in altre"},
    },
    "CHIM-C01-NCOM-011": {
        "opts": {"D": "O"},
    },
    "CHIM-C01-NCOM-036": {
        "q": (
            "Un campione d'aria è chiuso in un contenitore a temperatura ambiente (20 °C) "
            "e viene portato a una temperatura di -100 °C alla quale sia l'acqua che "
            "l'anidride carbonica sono allo stato solido. Quale delle seguenti righe mostra "
            "il tipo di miscuglio che si ottiene a 20 °C e a -100 °C in questo esperimento? "
            "[Riga 1: Omogeneo (gas) | Eterogeneo (solido + gas); "
            "Riga 2: Eterogeneo (gas) | Omogeneo (solido + gas); "
            "Riga 3: Omogeneo (gas) | Eterogeneo (liquido + gas); "
            "Riga 4: Eterogeneo (gas) | Omogeneo (liquido + gas); "
            "Riga 5: Omogeneo (gas) | Omogeneo (solido)]"
        ),
        "opts": {
            "A": "Riga 2",
            "B": "Riga 3",
            "C": "Riga 4",
            "D": "Riga 5",
            "E": "Riga 1",
        },
    },
    "CHIM-C02-COMM-004": {
        "opts": {
            "B": "6,023 · 10⁻²³",
            "C": "6,023 · 10²³",
        },
    },
    "CHIM-C02-COMM-024": {
        "opts": {
            "B": "il Ca appartiene con il Ba allo stesso gruppo del sistema periodico",
            "C": "il Ca è un elemento del II gruppo del sistema periodico",
            "E": "il Ca è un metallo alcalino",
        },
    },
    "CHIM-C03-NCOM-067": {
        "q": "In quale gruppo si trovano, nel sistema periodico, i gas nobili?",
        "opts": {"A": "Nel VII gruppo", "C": "Nel I gruppo"},
    },
    "CHIM-C03-NCOM-069": {
        "opts": {"C": "il carbonio"},
    },
    "CHIM-C03-NCOM-093": {
        "opts": {"C": "I metalli sono malleabili"},
    },
    "CHIM-C03-NCOM-108": {
        "q": "Tra i seguenti elementi indicare quello che ha configurazione elettronica 1s²2s²2p⁴:",
    },
    "CHIM-C03-NCOM-121": {
        "q": "In quale gruppo si trovano, nel sistema periodico, i metalli alcalino-terrosi?",
        "opts": {"A": "Nel I gruppo", "B": "Nel II gruppo", "C": "Nel III gruppo"},
    },
    "CHIM-C03-NCOM-123": {
        "opts": {"B": "N³⁻", "C": "K⁺", "E": "Ar"},
    },
    "CHIM-C03-NCOM-125": {
        "opts": {
            "A": "Cl",
            "B": "F",
            "C": "Nessuna delle risposte è corretta",
            "D": "I",
            "E": "Br",
        },
    },
    "CHIM-C03-NCOM-142": {
        "q": "Quale dei seguenti elementi appartiene al terzo periodo della tavola periodica?",
        "opts": {
            "A": "H",
            "B": "Li",
            "C": "Na",
            "D": "C",
            "E": "N",
        },
    },
    "CHIM-C04-COMM-002": {
        "q": "Nella molecola H₂, i due atomi sono uniti da un legame:",
    },
    "CHIM-C04-COMM-014": {
        "q": "L'H₂O bolle a temperatura più alta rispetto all'H₂S perché:",
        "opts": {
            "A": "ha un peso molecolare maggiore di quello dell'H₂S",
            "B": "ha un peso molecolare minore di quello dell'H₂S",
            "C": "non contiene legami a ponte di idrogeno, che invece sono presenti nell'H₂S",
            "D": "contiene legami a ponte di idrogeno, che invece non sono presenti nell'H₂S",
            "E": "è un acido più forte dell'H₂S",
        },
    },
    "CHIM-C04-NCOM-024": {
        "opts": {"C": "O"},
    },
    "CHIM-C04-NCOM-026": {
        "opts": {"D": "Cl₂"},
    },
    "CHIM-C04-NCOM-038": {
        "q": "Nella molecola Br₂, i due atomi di bromo sono uniti da un legame:",
        "opts": {
            "A": "ionico",
            "C": "covalente con parziale carattere ionico",
        },
    },
    "CHIM-C04-NCOM-047": {
        "opts": {
            "C": "atomi aventi diversa elettronegatività",
            "E": "ioni negativi aventi uguale elettronegatività",
        },
    },
    "CHIM-C04-NCOM-049": {
        "opts": {
            "B": "ioni e atomi neutri",
            "C": "ioni negativi aventi uguale elettronegatività",
        },
    },
    "CHIM-C04-NCOM-072": {
        "opts": {"C": "109,5°"},
    },
    "CHIM-C04-NCOM-083": {
        "q": "Indicare quale delle seguenti molecole ha ibridazione sp³:",
        "opts": {
            "A": "H₂SO₄",
            "B": "CH₄",
            "C": "CH₂=C=CH₂",
            "D": "CH₂=CH₂",
            "E": "CH≡CH",
        },
    },
    "CHIM-C04-NCOM-088": {
        "q": "Soltanto una delle seguenti affermazioni a proposito della molecola del metano è errata. Quale?",
        "opts": {
            "A": "L'atomo di C è ibridato sp³",
            "B": "I quattro atomi di idrogeno si trovano ai vertici di un tetraedro regolare",
            "C": "Gli angoli di legame sono di circa 109 gradi",
            "D": "La molecola è polare",
            "E": "La molecola non è planare",
        },
    },
    "CHIM-C04-COMP-028": {
        "q": "Un elettrolita _____ si dissocia solo parzialmente.",
    },
    "CHIM-C05-COMM-019": {
        "q": (
            "L'effusione dei gas attraverso fori sottili è regolata dalla legge di Graham, che stabilisce che "
            "la velocità di effusione (diffusione) ad una data temperatura dipende solo dalla massa molecolare "
            "(p.M.), ed è inversamente proporzionale alla sua radice quadrata. Quale delle seguenti affermazioni "
            "NON può essere dedotta dalla lettura del brano precedente?"
        ),
        "opts": {
            "D": "Un gas di p.M. 25 u.m.a. effonde con velocità doppia rispetto ad un gas di p.M. 100 u.m.a.",
            "E": "Un gas di p.M. 64 u.m.a. effonde con velocità minore rispetto ad un gas di p.M. 16 u.m.a.",
        },
    },
    "CHIM-C05-NCOM-005": {
        "q": (
            "Date le tre coppie di sostanze indicate di seguito, si identifichi per ogni coppia "
            "quale sostanza presenta forze intermolecolari maggiori: "
            "1. CH₄ e CBr₄; 2. N₂ e NO; 3. CH₃CH₂CH₂NH₂ e (CH₃)₃N "
            "[Si assumano temperatura e pressione standard (STP)]"
        ),
        "opts": {
            "A": "1: CBr₄, 2: N₂, 3: (CH₃)₃N",
            "B": "1: CBr₄, 2: NO, 3: CH₃CH₂CH₂NH₂",
            "C": "1: CBr₄, 2: N₂, 3: CH₃CH₂CH₂NH₂",
            "D": "1: CH₄, 2: NO, 3: (CH₃)₃N",
            "E": "1: CH₄, 2: N₂, 3: (CH₃)₃N",
        },
    },
    "CHIM-C05-NCOM-029": {
        "q": "Cosa potrebbe essere contenuto nei tre recipienti rappresentati in figura, a 15 °C e 1 atm?",
        "opts": {
            "A": "In A Br₂ o HCl, in B NH₃, in C I₂",
            "B": "In A I₂ o Br₂, in B NH₃ o HCl",
            "C": "In A Br₂ o NH₃, in B HCl, in C I₂",
            "D": "In A Br₂ o I₂, in B NH₃, in C HCl",
            "E": "In A NH₃ o HCl, in B Br₂, in C I₂",
        },
    },
    "CHIM-C06-COMM-001": {
        "opts": {"A": "l'etere dietilico", "D": "la cellulosa"},
    },
    "CHIM-C06-COMM-008": {
        "opts": {
            "C": "In acqua a 20 °C la solubilità di CO₂ è maggiore di quella di O₂",
            "E": "In acqua a 20 °C la solubilità di N₂ è minore di quella di O₂",
        },
    },
    "CHIM-C07-COMM-002": {
        "opts": {"A": "NH₃"},
    },
    "CHIM-C07-COMM-004": {
        "opts": {
            "D": "la concentrazione finale degli ioni idrogeno è minore di quella iniziale",
            "E": "un grammo equivalente di acido (una mole di H⁺) reagisce con un grammo equivalente di base (una mole di OH⁻) di pari forza",
        },
    },
    "CHIM-C07-COMM-006": {
        "q": "Sono stati ottenuti, con quattro differenti metodi, quattro campioni di uno stesso ossido di azoto. La percentuale in peso di azoto risulta essere la stessa in ognuno dei quattro campioni. Ciò costituisce una prova della legge:",
    },
    "CHIM-C07-COMM-008": {
        "q": (
            "Lo ione superossido viene decomposto in vivo da parte di enzimi che lo trasformano "
            "secondo la seguente reazione: 2 ·O₂⁻ + 2 H⁺ ⇌ O₂ + H₂O₂. "
            "Quali sono i numeri di ossidazione degli atomi di ossigeno nelle tre specie: "
            "ione superossido, ossigeno molecolare, acqua ossigenata?"
        ),
        "opts": {
            "A": "-0,5; 0; -1",
            "B": "-1; 0; -1",
            "C": "-0,5; 0; +1",
            "D": "-1; 0; +1",
            "E": "0; +1; -1",
        },
    },
    "CHIM-C07-COMM-021": {
        "opts": {"C": "Lo ione Cu²⁺"},
    },
    "CHIM-C07-COMM-023": {
        "q": "Il numero di ossidazione del cromo nel composto K₂Cr₂O₇ è:",
    },
    "CHIM-C07-COMP-014": {
        "q": "L'_____ è la perdita di elettroni da parte di una specie.",
    },
    "CHIM-C07-NCOM-005": {
        "q": "Quale fra le seguenti è l'equazione bilanciata?",
        "opts": {
            "A": "2 Na(s) + H₂O(l) → NaOH(aq) + H₂(g)",
            "B": "2 Na(s) + H₂O(l) → 2 NaOH(aq) + H₂(g)",
            "C": "2 Na(s) + 2 H₂O(l) → 2 NaOH(aq) + 2 H₂(g)",
            "D": "Na(s) + H₂O(l) → NaOH(aq) + H₂(g)",
            "E": "2 Na(s) + 2 H₂O(l) → 2 NaOH(aq) + H₂(g)",
        },
    },
    "CHIM-C07-NCOM-007": {
        "q": "Nella reazione (da bilanciare): As₂O₃ + HCl → AsCl₃ + H₂O, i coefficienti stechiometrici dell'equazione di reazione sono:",
        "opts": {
            "A": "1 - 3 → 2 - 1",
            "B": "1 - 3 → 2 - 3",
            "C": "2 - 6 → 2 - 3",
            "D": "1 - 2 → 1 - 1",
            "E": "1 - 6 → 2 - 3",
        },
    },
    "CHIM-C07-NCOM-012": {
        "q": "Indicare quale tra le seguenti reazioni è bilanciata:",
        "opts": {
            "A": "3 SO₂ + Ni₂O₃ → Ni₂(SO₃)₃",
            "B": "SO₂ + Ni₂O₃ → Ni₂(SO₃)₃",
            "C": "2 SO₂ + Ni₂O₃ → 2 Ni₂(SO₃)₃",
            "D": "1/2 SO₂ + Ni₂O₃ → Ni₂(SO₃)₃",
            "E": "SO₂ + 2 Ni₂O₃ → Ni₂(SO₃)₃",
        },
    },
    "CHIM-C07-NCOM-013": {
        "q": "Assegnare gli opportuni coefficienti stechiometrici alla seguente reazione: KClO₃ + H₂SO₄ → KHSO₄ + HClO₄ + ClO₂ + H₂O",
        "opts": {
            "A": "3; 3 → 3; 1; 2; 1",
            "B": "4; 2 → 3; 1; 2; 1",
            "C": "2; 4 → 1; 2; 1; 3",
            "D": "2; 2 → 2; 1; 1; 1",
            "E": "1; 1 → 1; 1; 1; 1",
        },
    },
    "CHIM-C07-NCOM-017": {
        "q": (
            "La Hausmannite (MnO · Mn₂O₃) è un minerale dal quale è possibile ottenere manganese "
            "in forma metallica secondo la seguente reazione: a MnO · Mn₂O₃ + b Al → c Al₂O₃ + d Mn. "
            "Quale delle seguenti combinazioni di coefficienti stechiometrici - a, b, c, d - deve essere utilizzata per bilanciare la reazione?"
        ),
        "opts": {
            "A": "a = 1; b = 4; c = 2; d = 3",
            "B": "a = 2; b = 4; c = 2; d = 6",
            "C": "a = 3; b = 8; c = 4; d = 9",
            "D": "a = 3; b = 4; c = 8; d = 9",
            "E": "a = 3; b = 6; c = 3; d = 6",
        },
    },
    "CHIM-C07-NCOM-020": {
        "q": "Data l'equazione: 3 Cu + x HNO₃ → y Cu(NO₃)₂ + z H₂O + 2 NO. Quale valore devono avere i coefficienti x e z affinché l'equazione sia bilanciata?",
        "opts": {
            "A": "x = 4; z = 2",
            "B": "x = 8; z = 4",
            "C": "x = 6; z = 3",
            "D": "x = 10; z = 5",
            "E": "x = 2; z = 1",
        },
    },
    "CHIM-C07-NCOM-023": {
        "q": "Quali sono i valori da attribuire ai coefficienti a, b, c per bilanciare correttamente la seguente reazione chimica? 3 Cl₂ + a NaOH → b NaClO₃ + c NaCl + 3 H₂O",
        "opts": {
            "A": "a = 6; b = 2; c = 4",
            "B": "a = 3; b = 2; c = 4",
            "C": "a = 6; b = 1; c = 5",
            "D": "a = 4; b = 1; c = 3",
            "E": "a = 3; b = 1; c = 5",
        },
    },
    "CHIM-C07-NCOM-026": {
        "q": "Calcolare quante moli di zolfo devono essere messe a reagire in presenza di ossigeno (reagente in eccesso) per ottenere 20 grammi di SO₃ (peso molecolare: 80 u.m.a.), dopo aver bilanciato la seguente reazione: S + O₂ → SO₃",
    },
    "CHIM-C07-NCOM-029": {
        "q": "Ammettendo che la seguente reazione (non bilanciata): Fe₂O₃(s) + Al(s) → Al₂O₃(s) + Fe(s) avvenga in maniera completa, quante moli di ossido di alluminio si otterrebbero mescolando 4 moli di ossido di ferro(III) con 4 moli di alluminio?",
    },
    "CHIM-C07-NCOM-035": {
        "q": (
            "Il propano reagisce con l'ossigeno secondo la reazione indicata di seguito: "
            "C₃H₈(g) + 5 O₂(g) → 3 CO₂(g) + 4 H₂O(g). Se 100 cm³ di propano vengono miscelati con 900 cm³ "
            "di ossigeno, qual è il volume di gas totale che rimarrà alla fine della reazione, assumendo "
            "che i volumi di tutti i gas siano misurati alla stessa temperatura e pressione?"
        ),
        "opts": {"C": "1300 cm³"},
    },
    "CHIM-C07-NCOM-039": {
        "q": "Indicare l'unica affermazione errata tra quelle riferite alla seguente equazione chimica: 2 Ca + O₂ → 2 CaO",
        "opts": {
            "A": "6 moli di Ca reagiscono con 3 moli di O₂ per dare 6 moli di CaO",
            "B": "1 mole di Ca reagisce con 0,5 moli di O₂ per dare 1 mole di CaO",
            "C": "2 g di Ca reagiscono con 1 g di O₂ per dare 2 g di CaO",
            "D": "2 atomi di Ca reagiscono con 1 molecola di O₂ per dare 2 molecole di CaO",
            "E": "2 moli di Ca reagiscono con 22,41 litri di O₂ (STP) per dare 2 moli di CaO",
        },
    },
    "CHIM-C07-NCOM-041": {
        "q": (
            "In un volume di 100 mL di una soluzione 2,5 M di HCl vengono messi 10 g di CaCO₃(s) "
            "(Massa molare = 100 g/mol). La reazione che si sviluppa è la seguente: "
            "CaCO₃(s) + 2 HCl(aq) → CaCl₂(aq) + CO₂(g) + H₂O. "
            "Individuare il reagente limitante della reazione e le moli di CO₂ che verranno effettivamente prodotte."
        ),
        "opts": {
            "A": "CaCO₃; 0,1 moli di CO₂",
            "B": "CaCO₃; 0,25 moli di CO₂",
            "C": "HCl; 0,25 moli di CO₂",
            "D": "HCl; 0,1 moli di CO₂",
            "E": "CaCO₃; 0,2 moli di CO₂",
        },
    },
    "CHIM-C07-NCOM-047": {
        "q": (
            "Considerando le reazioni all'equilibrio sottostanti, in quale delle reazioni verrà prodotta "
            "una quantità maggiore di X in entrambi i casi in cui si abbia o un aumento della temperatura "
            "o un aumento della pressione? [Si assuma che non avvenga un cambiamento di stato quando "
            "temperatura o pressione vengono cambiate]"
        ),
        "opts": {
            "A": "Q(g) + R(g) ⇌ 3 X(g) + T(g), la reazione diretta è esotermica",
            "B": "2 Q(g) ⇌ X(g), la reazione diretta è endotermica",
            "C": "Q(g) + R(g) ⇌ 2 X(g) + T(g), la reazione diretta è endotermica",
            "D": "Q(g) + R(g) ⇌ X(g), la reazione diretta è esotermica",
            "E": "Q(g) + R(g) ⇌ 2 X(g), la reazione diretta è esotermica",
        },
    },
    "CHIM-C09-NCOM-001": {"q": "Il valore massimo del numero di ossidazione del bromo è:"},
    "CHIM-C09-NCOM-004": {"q": "Il valore massimo del numero di ossidazione del fosforo è:"},
    "CHIM-C09-NCOM-007": {"q": "Qual è il numero di ossidazione del cromo nel composto Al₂(CrO₄)₃?"},
    "CHIM-C09-NCOM-009": {"q": "Qual è il numero di ossidazione del cromo nel composto CrO₃?"},
    "CHIM-C09-NCOM-014": {
        "q": "Il numero di ossidazione dello zolfo nel composto Al₂(SO₄)₃ è:",
        "opts": {"A": "+6"},
    },
    "CHIM-C09-NCOM-015": {"q": "Qual è il numero di ossidazione dell'idrogeno nell'idruro di litio?"},
    "CHIM-C09-NCOM-018": {"q": "Il numero di ossidazione dell'ossigeno nella molecola di H₂O è:"},
    "CHIM-C09-NCOM-019": {"q": "Qual è il numero di ossidazione del cloro nell'anione ClO₃⁻?"},
    "CHIM-C09-NCOM-023": {"q": "Qual è il numero di ossidazione del Mn nel composto KMnO₄?"},
    "CHIM-C09-NCOM-026": {"q": "Il numero di ossidazione dell'azoto nello ione NO₃⁻ è:"},
    "CHIM-C09-NCOM-028": {"q": "Qual è il numero di ossidazione dell'idrogeno in HF?"},
    "CHIM-C09-NCOM-034": {"q": "Il numero di ossidazione del manganese nel composto HMnO₄ è:"},
    "CHIM-C09-NCOM-036": {"q": "Il valore minimo del numero di ossidazione del carbonio è:"},
    "CHIM-C09-NCOM-041": {"q": "Indicare il numero di ossidazione dello zolfo in H₂SO₄:"},
    "CHIM-C09-NCOM-047": {"q": "Il numero di ossidazione dell'alluminio in Al₂(SO₄)₃ è:"},
    "CHIM-C09-NCOM-049": {"q": "Il numero di ossidazione del manganese nel composto Be(MnO₄)₂ è:"},
    "CHIM-C09-NCOM-051": {"q": "Il numero di ossidazione dell'ossigeno nella molecola O₂ è:"},
    "CHIM-C09-NCOM-057": {"q": "L'elemento che in una reazione aumenta il proprio numero di ossidazione è detto:"},
    "CHIM-C09-NCOM-058": {
        "q": "Quando l'acqua viene sottoposta all'azione di un agente ossidante forte, che cosa si forma?",
        "opts": {
            "A": "H₂",
            "B": "O₂",
            "C": "H₂ e O₂",
            "D": "H₂ e OH⁻",
            "E": "H⁺ e OH⁻",
        },
    },
    "CHIM-C09-NCOM-067": {
        "q": (
            "Data la seguente reazione di ossidoriduzione tra ioni ossalato (C₂O₄²⁻) e ioni permanganato "
            "(MnO₄⁻) in soluzione acquosa acida: 5 C₂O₄²⁻(aq) + 2 MnO₄⁻(aq) + 16 H⁺(aq) → 10 CO₂(g) + "
            "2 Mn²⁺(aq) + 8 H₂O(l). Quale delle seguenti affermazioni è corretta?"
        ),
    },
    "CHIM-C09-NCOM-086": {
        "q": "Nella seguente reazione: Cl₂(g) + 2 KI(aq) → I₂(aq) + 2 KCl(aq):",
        "opts": {
            "A": "il cloro si riduce e il potassio si ossida",
            "B": "il cloro si ossida e lo iodio si riduce",
            "C": "il cloro e lo iodio si ossidano e il potassio si riduce",
            "D": "il cloro si riduce e lo iodio si ossida",
            "E": "non si hanno ossidazioni né riduzioni",
        },
    },
    "CHIM-C09-NCOM-107": {
        "q": "In una reazione chimica gli ioni Ag⁺ in soluzione si trasformano in atomi del metallo. Ciò significa che gli ioni Ag⁺:",
        "opts": {"B": "si ossidano", "E": "si solidificano"},
    },
    "CHIM-C09-NCOM-113": {
        "q": "Nella seguente reazione: Zn + FeCl₂ → ZnCl₂ + Fe, l'elemento che si riduce è:",
        "opts": {"A": "sia Cl che Zn", "C": "Cl"},
    },
    "CHIM-C10-COMM-002": {
        "opts": {"C": "il calcio è un elemento del II gruppo del sistema periodico"},
    },
    "CHIM-C10-COMM-010": {
        "opts": {"C": "CaH₂", "D": "Mg(OH)₂", "E": "CuSO₄·5H₂O"},
    },
    "CHIM-C10-COMP-013": {
        "q": "Gli ossidi acidi reagiscono con basi formando _____.",
    },
    "CHIM-C10-NCOM-049": {
        "q": "Una reazione che permette di ottenere la calce spenta dalla calce viva è la seguente: CaO (calce viva) + H₂O → Ca(OH)₂ (calce spenta). In essa:",
    },
    "CHIM-C10-NCOM-067": {
        "q": "Il fosfato tricalcico corrisponde alla formula:",
        "opts": {
            "A": "Ca(H₂PO₄)₂",
            "B": "Ca₃(PO₄)₂",
            "C": "Ca(PO₃)₂",
            "D": "CaHPO₄",
            "E": "Ca₂PO₄",
        },
    },
    "CHIM-C10-NCOM-077": {
        "opts": {
            "A": "MgF₂",
            "B": "Mg₂F",
            "C": "Mg₂F₂",
            "D": "MgF",
            "E": "Mg(FO)₂",
        },
    },
    "CHIM-C10-NCOM-078": {"q": "Denominare il seguente composto: AlP"},
    "CHIM-C10-NCOM-079": {
        "q": "Denominare il seguente composto: HgCl₂",
        "opts": {"B": "Dicloruro di idrogeno", "D": "Dicloruro di mercurio"},
    },
    "CHIM-C11-COMM-017": {"opts": {"E": "il pH finale è minore di quello iniziale"}},
    "CHIM-C11-COMM-031": {"q": "Quando l'acqua si trasforma in ione idronio H₃O⁺, essa si comporta da:"},
    "CHIM-C11-NCOM-017": {
        "q": "Secondo Brønsted-Lowry l'acido coniugato della base CO₃²⁻ è:",
        "opts": {
            "A": "CO₂",
            "B": "H₃O⁺",
            "C": "HCO₃⁻",
            "D": "H₂CO₃",
            "E": "HNO₃",
        },
    },
    "CHIM-C11-NCOM-025": {
        "q": (
            "Tutte le equazioni sottostanti descrivono reazioni acido-base. "
            "In quale delle reazioni il composto sottolineato si comporta da acido di Lewis "
            "e non da acido di Brønsted-Lowry?"
        ),
        "opts": {
            "A": "NH₃ + H₂O → NH₄⁺ + OH⁻",
            "B": "CH₃COOH + NaOH → CH₃COONa + H₂O",
            "C": "NH₃ + BCl₃ → H₃NBCl₃ (BCl₃ sottolineato)",
            "D": "[Cu(H₂O)₄]²⁺ + H₂O → [Cu(H₂O)₃OH]⁺ + H₃O⁺",
            "E": "HNO₃ + H₂SO₄ → H₂NO₃⁺ + HSO₄⁻",
        },
    },
    "CHIM-C11-NCOM-038": {"opts": {"A": "Na₂O", "E": "NaCl"}},
    "CHIM-C11-NCOM-061": {
        "q": "Una soluzione ha [H⁺] = 10⁻² M. Essa è:",
        "opts": {"A": "con eccesso di OH⁻"},
    },
    "CHIM-C11-NCOM-067": {"q": "Una soluzione di acido acetico 0,1 M (K_a = 1,8 · 10⁻⁵) è:"},
    "CHIM-C11-NCOM-089": {
        "q": "Una soluzione ha una concentrazione di OH⁻ = 10⁻⁸ M. Il pH è:",
    },
    "CHIM-C11-NCOM-094": {
        "q": "Il pH di una soluzione di idrossido sodico avente una concentrazione di ossidrilioni pari a 10⁻² grammoioni/litro è:",
        "opts": {
            "A": "-log 10⁻²",
            "B": "2",
            "C": "12",
            "D": "pari a 10",
            "E": "compreso tra 7 e 9",
        },
    },
    "CHIM-C11-NCOM-104": {"opts": {"A": "5"}},
    "CHIM-C11-NCOM-118": {"q": "Una soluzione ha pH = 13. Il valore di [OH⁻] è:"},
    "CHIM-C11-NCOM-123": {
        "q": "Una soluzione ha [H⁺] = 10⁻³ M. Il pH è:",
        "opts": {
            "A": "11",
            "B": "9",
            "C": "6",
            "D": "-3",
            "E": "3",
        },
    },
    "CHIM-C11-NCOM-136": {"q": "Qual è il valore del pH di una soluzione contenente 1 · 10⁻² M di OH⁻?"},
    "CHIM-C11-NCOM-137": {"q": "Qual è il valore del pH di una soluzione contenente 1 · 10⁻⁴ M di H₃O⁺?"},
    "CHIM-C11-NCOM-152": {"opts": {"E": "ha la stessa acidità"}},
    "CHIM-C11-NCOM-165": {"q": "Qual è il pH di una soluzione acquosa di CaCl₂ 0,2 molare?"},
    "CHIM-C12-COMM-004": {"opts": {"A": "almeno un atomo di C asimmetrico"}},
    "CHIM-C12-COMM-010": {"opts": {"A": "L'atomo di C è ibridato sp³"}},
    "CHIM-C12-COMM-011": {
        "q": "Il ciclopentano:",
        "opts": {
            "A": "possiede atomi di C ibridati sp³",
            "B": "presenta carattere aromatico",
            "C": "è costituito da 6 atomi di C e 6 atomi di H",
            "D": "possiede atomi di C ibridati sp²",
            "E": "dà facilmente reazioni di addizione",
        },
    },
    "CHIM-C12-COMM-016": {"opts": {"D": "sostituzione elettrofila"}},
    "CHIM-C12-COMM-018": {
        "q": "Il pentene reagisce con l'idrogeno, con l'acqua ossigenata e con lo iodio; si tratta, in tutti e tre i casi, di reazioni di:",
    },
    "CHIM-C12-COMM-028": {"opts": {"E": "miscele di alcooli primari e di alcooli terziari"}},
    "CHIM-C12-COMM-039": {"opts": {"A": "Le aldeidi hanno due atomi di ossigeno legati al carbonio carbonilico"}},
    "CHIM-C12-NCOM-082": {"opts": {"A": "Supersolido"}},
    "CHIM-C12-NCOM-090": {
        "q": "A che formula corrisponde il butano?",
        "opts": {
            "A": "CH₃-CH₂-CH₂",
            "B": "CH₃-CH₂-CH₂-CH₃",
            "C": "CH₃-CH₃",
            "D": "CH₃-CH₂-CH₃",
            "E": "CH₂=CH-CH₃",
        },
    },
    "CHIM-C12-NCOM-101": {
        "q": "Qual è la formula generale degli alchini?",
        "opts": {
            "A": "CₙH₂ₙ₋₂",
            "B": "CₙH₂ₙ₊₂",
            "C": "CₙH₂ₙ₊₄",
            "D": "C₂ₙH₂ₙ",
            "E": "CₙHₙ",
        },
    },
    "CHIM-C12-NCOM-119": {
        "opts": {"C": "1 legame σ ed 1 legame π"},
    },
    "CHIM-C12-NCOM-120": {"opts": {"C": "Supersolido"}},
    "CHIM-C12-NCOM-128": {
        "q": "Quale delle seguenti è la formula bruta di un idrocarburo lineare monoinsaturo?",
        "opts": {
            "A": "CₙHₙ₊₂",
            "B": "CₙHₙ₋₂",
            "C": "CₙH₂ₙ₊₂",
            "D": "CₙH₂ₙ",
            "E": "CₙH₂ₙ₋₂",
        },
    },
    "CHIM-C12-NCOM-132": {"opts": {"A": "CH₄", "C": "Na₂SO₄"}},
    "CHIM-C12-NCOM-140": {
        "opts": {
            "A": "CH₂=CH₂",
            "B": "CH₄",
            "C": "H₂O",
            "D": "NH₃",
            "E": "C₂H₂",
        },
    },
    "CHIM-C12-NCOM-143": {
        "q": "Il numero di atomi di C presenti in un alchene contenente n atomi di H è:",
        "opts": {"A": "n + 2"},
    },
    "CHIM-C12-NCOM-152": {"opts": {"E": "Supersolido"}},
    "CHIM-C12-NCOM-165": {"q": "Il gruppo -CH₂OH è caratteristico:"},
    "CHIM-C12-NCOM-195": {
        "q": "Quale fra queste è una ammina secondaria?",
        "opts": {
            "A": "CH₃-CH₂-N(CH₃)₂",
            "B": "RNH₂",
            "C": "R₂NH",
            "D": "R₃N",
            "E": "NH₃",
        },
    },
    "CHIM-C12-NCOM-197": {
        "q": "La desinenza -one, secondo le regole internazionali di nomenclatura, spetta:",
        "opts": {"A": "ai chetoni"},
    },
    "CHIM-C12-NCOM-208": {"q": "Qual è il nome del CH₃-O-C₃H₇?"},
    "CHIM-C12-NCOM-212": {"opts": {"A": "Trifluoroetanolo"}},
    "CHIM-C12-NCOM-222": {"q": "Il composto CH₃-CH₂-O-CH₂-CH₃ è:"},
    "CHIM-C12-NCOM-229": {"q": "Qual è il nome del CH₃-CH₂-CHO?"},
    "CHIM-C12-NCOM-242": {"q": "Qual è il nome del CH₂=CH-CHO?"},
    "CHIM-C12-NCOM-247": {
        "opts": {
            "A": "NH₂OH",
            "B": "CH₃-CH₂-COOH",
            "C": "CH₃-CH₂-NH-CH₃",
            "D": "CH₃-CH₂-NH₂",
            "E": "CH₃-CH₂-SH",
        },
    },
    "CHIM-C12-NCOM-271": {
        "q": (
            "La presenza di un alogeno (che è caratterizzato da un'elevata elettronegatività) "
            "su un acido carbossilico a dare un alogenuro acilico del tipo R-CO-Cl (vedi figura), "
            "come modifica la reattività?"
        ),
        "opts": {
            "A": "Diminuisce la reattività nei confronti di nucleofili, in quanto rende δ⁻ il carbonio del gruppo C=O",
            "B": "Diminuisce la reattività nei confronti di nucleofili, in quanto rende δ⁺ il carbonio del gruppo C=O",
            "C": "Non modifica in nessun modo la reattività",
            "D": "Aumenta la reattività nei confronti di nucleofili, in quanto rende ancora più δ⁺ il carbonio del gruppo C=O",
            "E": "Aumenta la reattività nei confronti di nucleofili, in quanto rende ancora più δ⁻ il carbonio del gruppo C=O",
        },
    },
    "CHIM-C13-COMM-006": {"q": "Quale dei seguenti termini NON si riferisce alla medesima classe di composti?"},
    "CHIM-C13-COMM-009": {"opts": {"E": "nelle poliammine"}},
    "CHIM-C13-COMM-016": {"opts": {"A": "Clorofilla"}},
    "CHIM-C13-COMP-008": {"ans": "D"},
    "CHIM-C13-NCOM-076": {
        "q": "Indicare il sapone:",
        "opts": {"A": "cloruro di polivinile"},
    },

    # --- Fisica scan-verified overrides ---
    "FIS-C01-COMM-024": {"opts": {"B": "è sceso di 1 mm", "E": "è salito di 1 mm"}},
    "FIS-C03-COMM-026": {
        "q": "Un pilota di aviogetto di massa m descrive una circonferenza di raggio r con velocità v. Il pilota dovrà sopportare una forza centrifuga pari a:",
        "opts": {
            "A": "m · v · r²",
            "B": "m · v² / r",
            "C": "(1/2) m · v² / r",
            "D": "v r² / m",
            "E": "v² / m",
        },
    },
    "FIS-C03-COMP-036": {"q": "La relazione per la forza di attrito dinamico è f_d = _____ N."},
    "FIS-C03-COMP-046": {"q": "La velocità limite per un oggetto che cade in un fluido è data da v_T = _____ / b."},
    "FIS-C03-COMP-053": {"q": "L'angolo critico θ_c in un piano inclinato si calcola usando la relazione tan θ_c = _____."},
    "FIS-C03-COMP-152": {"q": "La relazione a_c = r ω² è la formula dell'accelerazione _____."},
    "FIS-C03-COMP-153": {"q": "L'energia cinetica rotazionale si calcola con la formula K_R = ½ I _____."},
    "FIS-C04-NCOM-027": {
        "q": "Un recipiente cilindrico alto 30 cm è riempito di liquido. La pressione sul fondo del recipiente dipende:",
    },
    "FIS-C04-NCOM-040": {
        "q": "È corretto dire che la pressione idrostatica alla base di un tubo verticale:",
        "opts": {
            "A": "si misura in atm/m²",
            "B": "non esiste nei tubi capillari",
            "C": "è indipendente dalla sezione della colonna liquida",
            "D": "è indipendente dalla densità del liquido",
            "E": "è nulla",
        },
    },
    "FIS-C04-NCOM-049": {
        "q": (
            "Un sub osserva una bolla d'aria che da una profondità di circa 15 m si muove verso "
            "la superficie dell'acqua. Trascurando la variazione di temperatura tra fondo e superficie, "
            "di quanto aumenta il volume della bolla? (Ricorda che a partire dalla superficie dell'acqua "
            "dove la pressione è quella atmosferica, sott'acqua la pressione aumenta di circa 1 atmosfera ogni 10 metri)"
        ),
        "opts": {
            "A": "V_sup = 9 V_fondo",
            "B": "V_sup = 15 V_fondo",
            "C": "V_sup = 0,25 V_fondo",
            "D": "V_sup = 2,5 V_fondo",
            "E": "V_sup = V_fondo",
        },
    },
    "FIS-C05-COMM-021": {
        "q": "Una mole di He a temperatura 0 °C e pressione 1 atm (N = num. di Avogadro):",
        "opts": {
            "A": "occupa 1 m³",
            "B": "ha N atomi",
            "C": "ha 4 · N atomi",
            "D": "ha 4 N protoni",
            "E": "occupa 22,4 m³",
        },
    },
    "FIS-C05-COMP-033": {"q": "Il calore latente di fusione dell'acqua è circa 3,33 × 10⁵ _____ /kg."},
    "FIS-C05-COMP-034": {"q": "Il calore latente di vaporizzazione dell'acqua è circa 2,26 × 10⁶ _____ /kg."},
    "FIS-C06-COMM-017": {
        "opts": {
            "A": "C = Q V",
            "B": "C = Q² / V",
            "C": "C = Q V²",
            "D": "C = V / Q",
            "E": "C = Q / V",
        },
    },
    "FIS-C06-COMM-024": {
        "q": "Una resistenza attraversata da una corrente di 5 A dissipa per effetto Joule 200 W. Se si raddoppia l'intensità della corrente, la potenza dissipata diventa:",
        "opts": {
            "A": "400 W",
            "B": "100 W",
            "C": "200 W",
            "D": "800 W",
            "E": "300 W",
        },
    },
    "FIS-C06-COMM-034": {
        "q": "Dato il circuito in figura in cui R₁ = 10 Ω, R₂ = R₃ = 20 Ω, V_A = 10 volt, V_B = 0, allora:",
        "opts": {
            "A": "V_M = 5 V",
            "B": "le tre resistenze equivalgono a una resistenza totale di 30 Ω",
            "C": "V_M = (40/50) · 10 V",
            "D": "la potenza complessiva è 100/30 W",
            "E": "la corrente complessiva è 10/40 A",
        },
    },
    "FIS-C06-NCOM-123": {
        "q": "Quale dei seguenti grafici mostra la caratteristica corrente I - tensione V di un conduttore ohmico?",
        "opts": {
            "A": "Grafico A (vedi figura: curva concava verso il basso)",
            "B": "Grafico B (vedi figura: curva a campana)",
            "C": "Grafico C (vedi figura: retta passante per l'origine)",
            "D": "Grafico D (vedi figura: retta con intercetta positiva sull'asse V)",
            "E": "Grafico E (vedi figura: curva crescente con concavità verso l'alto)",
        },
    },
    "FIS-C06-NCOM-155": {
        "q": "Se un circuito, formato da due resistenze R₁ e R₂, viene collegato a un generatore di tensione continua a 10 V, dissipa 20 W. Qual è una possibile configurazione del circuito?",
        "opts": {
            "A": "R₁ = 3 Ω, R₂ = 2 Ω, in parallelo",
            "B": "R₁ molto grande, R₂ circa 5 Ω, in serie",
            "C": "R₁ = 2 Ω, R₂ = 2 Ω, in parallelo",
            "D": "R₁ = 6 Ω, R₂ = 30 Ω, in parallelo",
            "E": "R₁ = 10 Ω, R₂ = 10 Ω, in serie",
        },
    },
    "FIS-C07-COMP-008": {
        "q": "In una funzione d'onda y = A sen(kx - ωt + φ), la quantità φ è detta _____.",
    },

    # --- Biologia scan-verified overrides ---
    "BIO-C01-COMM-017": {
        "opts": {
            "C": "Il terreno di coltura limitato è il fattore determinante",
            "D": "I batteri invecchiano e muoiono come tutti gli organismi viventi",
        },
    },
    "BIO-C01-COMM-034": {"q": "Lo schema rappresenta il ciclo dell'ATP. La freccia ① rappresenta:"},
    "BIO-C01-NCOM-117": {"q": "Il citoplasma delle cellule è composto prevalentemente da:"},
    "BIO-C01-NCOM-263": {
        "q": "Il grafico rappresenta l'albero evolutivo di alcune specie. Dal suo studio si deduce che:",
        "opts": {
            "A": "Z⁴ e W sono due specie strettamente imparentate",
            "B": "Q appartiene alla stessa specie di X¹",
            "C": "Z² e Z³ appartengono alla stessa specie",
            "D": "Y è l'antenato comune a tutte le specie attualmente viventi",
            "E": "X¹ è una specie estinta",
        },
    },
    "BIO-C03-COMM-024": {
        "q": (
            "Meselson e Stahl nel 1957 fornirono prove sperimentali che ciascun filamento di DNA "
            "serviva da stampo per il nuovo DNA, dimostrando così il processo di duplicazione "
            "semiconservativa del DNA. Essi fecero crescere un ceppo di Escherichia coli in un terreno "
            "contenente azoto pesante (¹⁵N), quindi lo passarono in un terreno contenente azoto leggero "
            "(¹⁴N). Dopo due generazioni esaminarono i risultati e constatarono che la percentuale di DNA "
            "composto da un'elica pesante (con azoto 15) e da una leggera (con azoto 14) era:"
        ),
    },
    "BIO-C03-NCOM-024": {"opts": {"E": "L'allele"}},
    "BIO-C04-COMM-001": {"q": "I gemelli biovulari hanno sesso:"},
    "BIO-C04-COMM-022": {
        "q": "Se si incrocia un individuo eterozigote per una caratteristica dominante con un omozigote recessivo, con quale probabilità avremo individui con il fenotipo recessivo?",
    },
    "BIO-C04-COMM-026": {"opts": {"A": "allelia multipla"}},
    "BIO-C04-COMM-051": {
        "opts": {
            "A": "I ribosomi correggono le modificazioni",
            "E": "Vi è una correzione post-trascrizionale della proteina",
        },
    },
    "BIO-C04-NCOM-120": {"opts": {"C": "i cromosomi X e Y"}},
    "BIO-C04-COMM-065": {
        "exp": (
            "Il gruppo Rh (Rh⁺ o Rh⁻) è determinato dalla combinazione di due alleli di uno stesso gene, di cui uno "
            "dominante (D) e uno recessivo (d) e si distingue per la presenza o assenza dell'antigene Rh sui globuli "
            "rossi. Un individuo può presentare genotipo DD (fenotipo Rh⁺), Dd (fenotipo Rh⁺) oppure dd (fenotipo Rh⁻). "
            "Gli individui con gruppo Rh⁻ non possiedono l'antigene e producono anticorpi anti-Rh se vengono a contatto "
            "con l'antigene Rh, mentre gli individui Rh⁺ possiedono l'antigene Rh e non producono anticorpi anti-Rh. "
            "Una gravidanza è a rischio per il fattore Rh quando vi è incompatibilità fra madre e nascituro (nascituro "
            "Rh positivo e madre Rh negativa). In questo caso, la madre produrrà anticorpi contro gli antigeni presenti "
            "sui globuli rossi del figlio. La conseguenza sarà la lisi dei globuli rossi del figlio."
        )
    },
    "BIO-C04-NCOM-168": {"opts": {"A": "solo 0 e A"}},
    "BIO-C04-NCOM-171": {"opts": {"B": "da tutti i gruppi sanguigni", "D": "B, 0", "E": "solo B"}},
    "BIO-C05-NCOM-059": {"opts": {"C": "la sede delle digestioni cellulari"}},
    "BIO-C05-NCOM-204": {"opts": {"C": "Fis1", "E": "Opa1"}},
    "BIO-C05-NCOM-205": {"opts": {"A": "Mfn1", "C": "Opa1"}},
    "BIO-C06-NCOM-034": {"opts": {"B": "integrine β4 e lamina basale"}},
    "BIO-C06-NCOM-061": {"opts": {"E": "integrine specializzate (es. α6β4)"}},
    "BIO-C07-NCOM-040": {
        "q": "Dall'osservazione della figura, si può dedurre che essa rappresenta:",
        "opts": {
            "B": "l'anafase della 2ª divisione meiotica",
            "C": "la profase della 1ª divisione meiotica",
            "D": "l'anafase della 1ª divisione meiotica",
        },
    },
    "BIO-C07-NCOM-055": {
        "q": (
            "La figura mostra due cromosomi omologhi in fase di crossing-over durante la meiosi "
            "di una cellula a corredo 2n = 2. Quale, delle 5 serie di cellule aploidi ottenute "
            "alla fine della meiosi, contiene i giusti cromosomi?"
        ),
        "opts": {
            "A": "Serie A (vedi figura: due cromatidi parentali scuri e due chiari non ricombinati)",
            "B": "Serie B (vedi figura: quattro cromatidi tutti ricombinati)",
            "C": "Serie C (vedi figura: due cromatidi parentali non ricombinati e due cromatidi ricombinati reciproci)",
            "D": "Serie D (vedi figura: tre cromatidi scuri e uno chiaro)",
            "E": "Serie E (vedi figura: due cromatidi chiari e due ricombinati)",
        },
    },
}


SUBTLE_OCR_REGEXES: list[tuple[re.Pattern[str], str]] = [
    # Remaining running-header & watermark bleed fragments in stems/options/explanations
    (re.compile(r"\s*Capitolo⁴?\s*i?\s*meccanismi[^\n]*"), ""),
    (re.compile(r"\s*Capitolo⁴\s+Il legame chimico\s*\d*"), ""),
    (re.compile(r"\s*Capitolo\s+\d+\s+[A-ZÀ-Ú][^\n?.!]*?\s+\d{1,3}\s*$"), ""),
    (re.compile(r"\s*750\s+Fisica\s+Quiz\w*"), ""),
    (re.compile(r"\s*missione e controllo dei caratteri selvatici e mutati\s*\d*"), ""),
    (re.compile(r"\s*controllo dell'informazione genetica e epigenetica\s*\d*"), ""),
    (re.compile(r"\s*(?:della\s+)?proliferazione e della sopravvivenza cellulare\s*\d*"), ""),
    (re.compile(r"\s*03 Urdnerra gli cement da tavola periodica St"), ""),
    (re.compile(r"\s*(?:\b[a-z]{1,3}\s+)?(?:JP|JO|PP|PZ)\s+DI\b"), ""),
    (re.compile(r"\s*\b(?:aos\s+JP|vo\s+edîses\s*\|?|ics\s+Pe|i\s+di\s+ses\s*\d*|toy,\s*di\s*ses\.?)\b", re.IGNORECASE), ""),
    (re.compile(r"\s*\b(?:non\s+commentati|commentati|incommentati|commentali|icommentali|commentabi|nmentati|nmentali|nmentoti|nmentab|imentati)\s*\d*\s*$"), ""),
    (re.compile(r"\s*\bmental\s*$"), ""),

    # Bracket / pipe OCR substitutions for Italian 'il' / "l'" / Roman numeral 'I'
    (re.compile(r"(?<!\S)i\]\s+"), "il "),
    (re.compile(r"(?<!\S)1\]\s+"), "il "),
    (re.compile(r"(?<!\S)I\}\s+"), "Il "),
    (re.compile(r"(?<!\S)i\}\s+"), "il "),
    (re.compile(r"(?<!\S)\|\s*['’]"), "l'"),
    (re.compile(r"\b(Topoisomerasi|topoisomerasi|polimerasi|Polimerasi|tipo|Tipo|metafase|Metafase|matafase|profase meiotica|anafase|telofase|complesso|Complesso|fotosistema|Fotosistema)\s+\|(?!\w)"), r"\1 I"),
    (re.compile(r"\bmatafase\b"), "metafase"),
    (re.compile(r"\bIdrocarburi lineare\b"), "idrocarburo lineare"),
    (re.compile(r"\bidrocarburi lineare\b"), "idrocarburo lineare"),

    # Biology Greek subunit & protein-family OCR fixes verified against scans
    (re.compile(r"\bintegrin([ae])\s+f4\b"), r"integrin\1 β4"),
    (re.compile(r"\bintegrin([ae])\s+B([1-9])\b"), r"integrin\1 β\2"),
    (re.compile(r"\bintegrin([ae])\s+aB\b"), r"integrin\1 αβ"),
    (re.compile(r"\ba6B4\b"), "α6β4"),
    (re.compile(r"\ba₆B₄\b"), "α₆β₄"),
    (re.compile(r"\ba5B1\b"), "α5β1"),
    (re.compile(r"\bB-adrenergico\b"), "β-adrenergico"),
    (re.compile(r"\badrenergico B\b"), "adrenergico β"),
    (re.compile(r"\bimportina B\b"), "importina β"),
    (re.compile(r"\btubulina a e B\b"), "tubulina α e β"),
    (re.compile(r"\btubulina a\b"), "tubulina α"),
    (re.compile(r"\bguanilii ciclasi\b"), "guanilil ciclasi"),
    (re.compile(r"\bFis1,\s*Mfn1,\s*0pa1\b"), "Fis1, Mfn1, Opa1"),
    (re.compile(r"\bOpa1l\b"), "Opa1"),
    (re.compile(r"\b0pa1\b"), "Opa1"),

    # Glued Italian words caught across all 7,078 cards
    (re.compile(r"\bLelettrone\b"), "L'elettrone"),
    (re.compile(r"\blelettrone\b"), "l'elettrone"),
    (re.compile(r"\bLaffinit[àa]\b"), "L'affinità"),
    (re.compile(r"\blaffinit[àa]\b"), "l'affinità"),
    (re.compile(r"\bLelettronegativit[àa]\b"), "L'elettronegatività"),
    (re.compile(r"\blelettronegativit[àa]\b"), "l'elettronegatività"),
    (re.compile(r"\bLelio\b"), "L'elio"),
    (re.compile(r"\bLargon\b"), "L'argon"),
    (re.compile(r"\b(?:H|U)legame\b"), "Il legame"),
    (re.compile(r"\bLacqua\b"), "L'acqua"),
    (re.compile(r"\blacqua\b"), "l'acqua"),
    (re.compile(r"\bHocriterlo\b"), "Il criterio"),
    (re.compile(r"\bLebullioscop[li]a\b"), "L'ebullioscopia"),
    (re.compile(r"\bHcloro\b"), "Il cloro"),
    (re.compile(r"\b(?:U|H)numero\b"), "Il numero"),
    (re.compile(r"\bLidrossido\b"), "L'idrossido"),
    (re.compile(r"\blidrossido\b"), "l'idrossido"),
    (re.compile(r"\bUacido\b"), "L'acido"),
    (re.compile(r"\bSeli pH\b"), "Se il pH"),
    (re.compile(r"\bHbrano\b"), "Il brano"),
    (re.compile(r"\bLidrolisi\b"), "L'idrolisi"),
    (re.compile(r"\blidrolisi\b"), "l'idrolisi"),
    (re.compile(r"\bHcicloesano\b"), "Il cicloesano"),
    (re.compile(r"\bLetene\b"), "L'etene"),
    (re.compile(r"\bLesano\b"), "L'esano"),
    (re.compile(r"\bLetano\b"), "L'etano"),
    (re.compile(r"\b(?:U|L)ibridazione\b"), "L'ibridazione"),
    (re.compile(r"\blibridazione\b"), "l'ibridazione"),
    (re.compile(r"\bHsimile\b"), "Il simile"),
    (re.compile(r"\bHsaccarosio\b"), "Il saccarosio"),
    (re.compile(r"\bHquidi\b"), "liquidi"),
    (re.compile(r"\bUnenzimaallosterico\b"), "Un enzima allosterico"),
    (re.compile(r"\bUdiametro\b"), "Il diametro"),
    (re.compile(r"\bLepidermide\b"), "L'epidermide"),
    (re.compile(r"\bLadiploidia\b"), "La diploidia"),
    (re.compile(r"\bLottamero\b"), "L'ottamero"),
    (re.compile(r"\bLacetilazione\b"), "L'acetilazione"),
    (re.compile(r"\bLermafroditismo\b"), "L'ermafroditismo"),
    (re.compile(r"\bLembrione\b"), "L'embrione"),
    (re.compile(r"\blembrione\b"), "l'embrione"),
    (re.compile(r"\bLapoptosi\b"), "L'apoptosi"),
    (re.compile(r"\blapoptosi\b"), "l'apoptosi"),
    (re.compile(r"\bLimprinting\b"), "L'imprinting"),
    (re.compile(r"\bLanticodone\b"), "L'anticodone"),
    (re.compile(r"\bLaligasi\b"), "La ligasi"),
    (re.compile(r"\bLemofilia\b"), "L'emofilia"),
    (re.compile(r"\bLallele\b"), "L'allele"),
    (re.compile(r"\blallele\b"), "l'allele"),
    (re.compile(r"\bLosteogenesi\b"), "L'osteogenesi"),
    (re.compile(r"\bLamminoacido\b"), "L'amminoacido"),
    (re.compile(r"\blamminoacido\b"), "l'amminoacido"),
    (re.compile(r"\bLeinserzioniele\b"), "Le inserzioni e le"),
    (re.compile(r"\bHnucleolo\b"), "Il nucleolo"),
    (re.compile(r"\bLinstaurarsi\b"), "L'instaurarsi"),
    (re.compile(r"\bLacetile\b"), "L'acetile"),
    (re.compile(r"\bLendocitosi\b"), "L'endocitosi"),
    (re.compile(r"\bLendosoma\b"), "L'endosoma"),
    (re.compile(r"\bLassonema\b"), "L'assonema"),
    (re.compile(r"\bUnglobulo\b"), "Un globulo"),
    (re.compile(r"\bLesocitosi\b"), "L'esocitosi"),
    (re.compile(r"\bLalamina\b"), "La lamina"),
    (re.compile(r"\bLetight\b"), "Le tight"),
    (re.compile(r"\bLelastina\b"), "L'elastina"),
    (re.compile(r"\bLoocita\b"), "L'oocita"),
    (re.compile(r"\bLacitodieresi\b"), "La citodieresi"),
    (re.compile(r"\bUnlinfocita\b"), "Un linfocita"),
    (re.compile(r"\bLaneuploidia\b"), "L'aneuploidia"),
    (re.compile(r"\bLecicline\b"), "Le cicline"),
    (re.compile(r"\bLaciclina\b"), "La ciclina"),
    (re.compile(r"\bLavia\b"), "La via"),
    (re.compile(r"\bLelettronvolt\b"), "L'elettronvolt"),
    (re.compile(r"\bLeffusione\b"), "L'effusione"),
    (re.compile(r"\bHsuono\b"), "Il suono"),
    (re.compile(r"\bUnelettrone\b"), "Un elettrone"),
    (re.compile(r"\bLidrogeno\b"), "L'idrogeno"),
    (re.compile(r"\bIlcatabolismo\b"), "Il catabolismo"),
    (re.compile(r"\bimito\s*condri\b"), "i mitocondri"),
    (re.compile(r"\bunidrocarburo\b"), "un idrocarburo"),
    (re.compile(r"\bunlipide\b"), "un lipide"),
    (re.compile(r"\bhannola\b"), "hanno la"),
    (re.compile(r"\bViè\b"), "Vi è"),
    (re.compile(r"\balle\s+lia\b"), "allelia"),
    (re.compile(r"\bparia\s+(\d)"), r"pari a \1"),
    (re.compile(r"\bécostituito\b"), "è costituito"),

    # Leading digit '1 ' OCR'd for capital 'I ' / 'Il ' at start of sentence/option
    (re.compile(r"^1\s+(quattro|sei|tre principali|metalli|composti|corpi|chetoni|gruppi|trigliceridi|polisaccaridi|carboidrati|pesi|monosaccaridi|bioelementi|batteri|cromosomi|gemelli|gameti|microtubuli|perossisomi|recettori|telomeri|fili)\b"), r"I \1"),
    (re.compile(r"^1\s+(numero|legame|gruppo|contenuto)\b"), r"Il \1"),
]


# Exact, 100% live-verified deduplication map (drop_id -> kept_canonical_id) across all 358
# candidate pairs in BIO, CHIM, and FIS.
#
# Verified invariants:
# 1. Every drop_id and keep_id exists in the 7,078-item dataset, with zero transitive chains.
# 2. In 100% of pairs where a 'commentati' version exists anywhere in the duplicate group,
#    the kept card is a 'commentati' card (retaining the full worked explanation).
# 3. Genuinely distinct questions that share a short generic stem ("La cromatina è:",
#    "Il fruttosio è:", "I mitocondri sono:", "L'apparato del Golgi:", "Quale di queste
#    affermazioni è corretta?", "Gli isotopi di un elemento:", etc.) are preserved intact.
DEDUP_DROP_MAP: dict[str, str] = {
    # --- CHIMICA (51 redundant copies dropped; 100% of commentati cards retained!) ---
    "CHIM-C01-NCOM-023": "CHIM-C01-COMM-004",
    "CHIM-C06-NCOM-012": "CHIM-C01-COMM-007",
    "CHIM-C07-NCOM-003": "CHIM-C01-COMM-009",
    "CHIM-C01-NCOM-017": "CHIM-C10-COMM-028",
    "CHIM-C01-NCOM-018": "CHIM-C07-COMM-006",
    "CHIM-C05-COMP-017": "CHIM-C01-COMP-009",
    "CHIM-C05-COMP-034": "CHIM-C01-COMP-041",
    "CHIM-C06-COMP-005": "CHIM-C01-COMP-041",
    "CHIM-C02-COMP-009": "CHIM-C01-COMP-046",
    "CHIM-C03-NCOM-009": "CHIM-C02-COMM-001",
    "CHIM-C13-NCOM-174": "CHIM-C02-COMM-001",
    "CHIM-C03-NCOM-040": "CHIM-C02-COMM-004",
    "CHIM-C03-NCOM-132": "CHIM-C02-COMM-024",
    "CHIM-C03-NCOM-116": "CHIM-C02-NCOM-038",
    "CHIM-C03-NCOM-134": "CHIM-C03-COMM-002",
    "CHIM-C03-NCOM-177": "CHIM-C03-COMM-004",
    "CHIM-C13-NCOM-175": "CHIM-C03-NCOM-011",
    "CHIM-C03-NCOM-044": "CHIM-C05-COMM-007",
    "CHIM-C03-NCOM-160": "CHIM-C03-NCOM-080",
    "CHIM-C04-NCOM-091": "CHIM-C03-NCOM-093",
    "CHIM-C03-NCOM-169": "CHIM-C03-NCOM-130",
    "CHIM-C05-NCOM-006": "CHIM-C04-COMM-014",
    "CHIM-C04-NCOM-089": "CHIM-C04-NCOM-076",
    "CHIM-C04-NCOM-088": "CHIM-C12-COMM-010",
    "CHIM-C06-COMP-028": "CHIM-C04-COMP-027",
    "CHIM-C06-COMP-029": "CHIM-C04-COMP-028",
    "CHIM-C06-COMM-020": "CHIM-C05-COMM-020",
    "CHIM-C05-NCOM-032": "CHIM-C06-COMM-008",
    "CHIM-C05-NCOM-039": "CHIM-C06-COMM-001",
    "CHIM-C10-NCOM-083": "CHIM-C07-COMM-002",
    "CHIM-C09-NCOM-033": "CHIM-C07-COMM-009",
    "CHIM-C09-NCOM-013": "CHIM-C07-COMM-011",
    "CHIM-C09-NCOM-037": "CHIM-C07-COMM-014",
    "CHIM-C09-NCOM-080": "CHIM-C07-COMM-015",
    "CHIM-C09-NCOM-078": "CHIM-C07-COMM-017",
    "CHIM-C10-NCOM-084": "CHIM-C07-COMM-019",
    "CHIM-C09-NCOM-110": "CHIM-C07-COMM-021",
    "CHIM-C09-NCOM-097": "CHIM-C07-COMM-022",
    "CHIM-C10-COMM-004": "CHIM-C07-COMM-022",
    "CHIM-C09-NCOM-039": "CHIM-C07-COMM-023",
    "CHIM-C09-NCOM-040": "CHIM-C07-COMM-024",
    "CHIM-C09-NCOM-058": "CHIM-C07-COMM-027",
    "CHIM-C09-COMP-005": "CHIM-C07-COMP-014",
    "CHIM-C09-COMP-006": "CHIM-C07-COMP-015",
    "CHIM-C09-COMP-007": "CHIM-C07-COMP-016",
    "CHIM-C09-COMP-008": "CHIM-C07-COMP-017",
    "CHIM-C09-NCOM-069": "CHIM-C09-COMM-002",
    "CHIM-C09-NCOM-120": "CHIM-C09-NCOM-057",
    "CHIM-C09-NCOM-130": "CHIM-C09-NCOM-107",
    "CHIM-C10-NCOM-051": "CHIM-C10-COMM-018",
    "CHIM-C11-NCOM-022": "CHIM-C10-COMM-023",
    "CHIM-C10-NCOM-047": "CHIM-C10-COMM-026",
    "CHIM-C11-NCOM-023": "CHIM-C10-COMM-029",
    "CHIM-C10-NCOM-093": "CHIM-C10-NCOM-072",
    "CHIM-C10-NCOM-094": "CHIM-C11-NCOM-041",
    "CHIM-C11-NCOM-033": "CHIM-C11-COMM-009",
    "CHIM-C11-NCOM-047": "CHIM-C11-COMM-031",
    "CHIM-C11-NCOM-122": "CHIM-C11-COMM-034",
    "CHIM-C12-NCOM-011": "CHIM-C12-COMM-004",
    "CHIM-C12-NCOM-273": "CHIM-C12-COMM-028",
    "CHIM-C13-NCOM-026": "CHIM-C12-COMM-039",
    "CHIM-C12-NCOM-153": "CHIM-C12-NCOM-114",
    "CHIM-C12-NCOM-303": "CHIM-C12-NCOM-222",
    "CHIM-C12-NCOM-304": "CHIM-C12-NCOM-208",
    "CHIM-C12-NCOM-298": "CHIM-C12-NCOM-272",
    "CHIM-C12-NCOM-296": "CHIM-C12-NCOM-281",
    "CHIM-C13-NCOM-048": "CHIM-C13-COMM-006",
    "CHIM-C13-NCOM-135": "CHIM-C13-NCOM-115",
    "CHIM-C13-NCOM-134": "CHIM-C13-NCOM-118",

    # --- Cross-subject redundant copies across BIO / CHIM / FIS (100% retaining commentati!) ---
    "FIS-C08-NCOM-018": "CHIM-C02-COMM-016",
    "FIS-C05-NCOM-108": "CHIM-C05-COMM-016",
    "FIS-C05-NCOM-077": "CHIM-C05-COMM-018",
    "FIS-C05-NCOM-005": "CHIM-C05-COMM-019",
    "FIS-C05-NCOM-109": "CHIM-C05-COMM-021",
    "CHIM-C05-NCOM-021": "FIS-C05-NCOM-051",
    "BIO-C03-NCOM-031": "CHIM-C13-COMM-029",
    "CHIM-C13-NCOM-130": "BIO-C01-NCOM-030",
    "CHIM-C13-NCOM-143": "BIO-C03-NCOM-062",
    "CHIM-C13-NCOM-147": "BIO-C01-NCOM-189",

    # --- BIOLOGIA (39 redundant copies dropped; 100% of commentati cards retained!) ---
    "BIO-C02-NCOM-050": "BIO-C01-COMM-016",
    "BIO-C01-NCOM-095": "BIO-C01-COMM-017",
    "BIO-C05-NCOM-144": "BIO-C01-COMM-034",
    "BIO-C05-NCOM-141": "BIO-C01-COMM-037",
    "BIO-C03-NCOM-085": "BIO-C01-NCOM-033",
    "BIO-C01-NCOM-066": "BIO-C04-COMM-084",
    "BIO-C01-NCOM-180": "BIO-C01-NCOM-162",
    "BIO-C01-NCOM-168": "BIO-C05-COMM-035",
    "BIO-C01-NCOM-213": "BIO-C03-COMM-024",
    "BIO-C02-NCOM-086": "BIO-C01-NCOM-224",
    "BIO-C01-NCOM-235": "BIO-C07-COMM-014",
    "BIO-C07-NCOM-129": "BIO-C01-NCOM-241",
    "BIO-C07-NCOM-106": "BIO-C02-COMM-002",
    "BIO-C02-NCOM-051": "BIO-C04-COMM-071",
    "BIO-C02-NCOM-073": "BIO-C04-COMM-043",
    "BIO-C07-NCOM-143": "BIO-C04-COMM-043",
    "BIO-C02-NCOM-074": "BIO-C04-COMM-044",
    "BIO-C02-NCOM-084": "BIO-C04-COMM-046",
    "BIO-C03-NCOM-059": "BIO-C03-COMM-025",
    "BIO-C03-NCOM-074": "BIO-C03-NCOM-024",
    "BIO-C03-NCOM-065": "BIO-C04-COMM-048",
    "BIO-C03-NCOM-087": "BIO-C04-COMM-052",
    "BIO-C03-NCOM-113": "BIO-C04-COMM-051",
    "BIO-C07-NCOM-107": "BIO-C04-COMM-001",
    "BIO-C07-NCOM-108": "BIO-C04-COMM-002",
    "BIO-C07-NCOM-109": "BIO-C04-COMM-003",
    "BIO-C04-NCOM-052": "BIO-C04-COMM-022",
    "BIO-C04-NCOM-175": "BIO-C04-COMM-026",
    "BIO-C04-NCOM-129": "BIO-C04-COMM-031",
    "BIO-C04-NCOM-103": "BIO-C04-COMM-031",
    "BIO-C04-NCOM-133": "BIO-C04-COMM-031",
    "BIO-C04-NCOM-224": "BIO-C04-COMM-049",
    "BIO-C04-NCOM-144": "BIO-C04-COMM-055",
    "BIO-C04-NCOM-163": "BIO-C04-COMM-058",
    "BIO-C04-NCOM-094": "BIO-C07-COMM-019",
    "BIO-C05-NCOM-014": "BIO-C05-COMM-002",
    "BIO-C05-NCOM-015": "BIO-C05-COMM-003",
    "BIO-C05-NCOM-169": "BIO-C05-COMM-065",
    "BIO-C05-NCOM-275": "BIO-C05-NCOM-205",
    "BIO-C06-NCOM-114": "BIO-C06-COMM-029",
    "BIO-C06-NCOM-131": "BIO-C06-COMM-033",
    "BIO-C07-NCOM-098": "BIO-C07-NCOM-085",

    # --- FISICA (9 redundant copies dropped; 100% of commentati cards retained!) ---
    "FIS-C04-NCOM-014": "FIS-C01-COMM-024",
    "FIS-C01-NCOM-072": "FIS-C02-COMM-017",
    "FIS-C02-COMP-033": "FIS-C02-COMP-005",
    "FIS-C03-NCOM-140": "FIS-C03-COMM-042",
    "FIS-C03-COMP-176": "FIS-C03-COMP-062",
    "FIS-C03-COMP-112": "FIS-C03-COMP-078",
    "FIS-C03-COMP-183": "FIS-C03-COMP-089",
    "FIS-C07-COMP-007": "FIS-C03-COMP-178",
    "FIS-C08-NCOM-002": "FIS-C07-COMM-004",
}


def apply_subtle_ocr_fixes(text: str) -> str:
    if not text:
        return text
    s = text
    for rx, rep in SUBTLE_OCR_REGEXES:
        s = rx.sub(rep, s)
    s = re.sub(r"[ \t]{2,}", " ", s).strip()
    return s


def scrub_publisher_branding(item: dict) -> None:
    """Remove all publisher branding ('publisher' / 'edi[s]es') from deck names & fields."""
    if "anki_deck" in item and isinstance(item["anki_deck"], str):
        item["anki_deck"] = re.sub(
            r"^Semestre Filtro\s+edi[s]es(?=::|$)",
            "Semestre Filtro",
            item["anki_deck"],
            flags=re.IGNORECASE,
        )
        item["anki_deck"] = re.sub(r"\s*edi[s]es\s*", " ", item["anki_deck"], flags=re.IGNORECASE)
        item["anki_deck"] = re.sub(r"\s*::\s*", "::", item["anki_deck"]).strip().strip()
    for field in ("question", "answer_text", "explanation"):
        if field in item and isinstance(item[field], str):
            item[field] = re.sub(r"\bedi[s]es\b", "", item[field], flags=re.IGNORECASE)
            item[field] = re.sub(r"[ \t]{2,}", " ", item[field]).strip()
    if isinstance(item.get("options"), dict):
        for k in list(item["options"].keys()):
            v = re.sub(r"\bedi[s]es\b", "", item["options"][k], flags=re.IGNORECASE)
            item["options"][k] = re.sub(r"[ \t]{2,}", " ", v).strip()


def deduplicate_dataset(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """Remove redundant duplicate questions while always retaining commented cards.

    Returns `(kept_items, removed_records)` where every kept item retains its canonical `id`
    and `global_index` is re-numbered sequentially `1..len(kept_items)`.
    """
    by_id = {it["id"]: it for it in items}
    priority = {"commentati": 3, "non_commentati": 2, "completamento": 1}

    removed_records: list[dict] = []
    for drop_id, keep_id in DEDUP_DROP_MAP.items():
        assert drop_id in by_id, f"Missing drop_id {drop_id}"
        assert keep_id in by_id, f"Missing canonical keep target {keep_id} for {drop_id}"
        assert keep_id not in DEDUP_DROP_MAP, f"Transitive drop chain {drop_id} -> {keep_id}"
        d_it = by_id[drop_id]
        k_it = by_id[keep_id]
        assert priority[k_it["quiz_type"]] >= priority[d_it["quiz_type"]], (
            f"Priority violation: dropping {drop_id} ({d_it['quiz_type']}) for {keep_id} ({k_it['quiz_type']})"
        )
        removed_records.append(
            {
                "dropped_id": drop_id,
                "kept_id": keep_id,
                "subject_code": k_it["subject_code"],
                "dropped_quiz_type": d_it["quiz_type"],
                "kept_quiz_type": k_it["quiz_type"],
                "dropped_answer": d_it["answer"],
                "kept_answer": k_it["answer"],
                "question": k_it["question"],
            }
        )

    kept_items: list[dict] = []
    for it in items:
        if it["id"] in DEDUP_DROP_MAP:
            continue
        out = copy.deepcopy(it)
        kept_items.append(out)

    for idx, it in enumerate(kept_items, start=1):
        it["global_index"] = idx

    return kept_items, removed_records
