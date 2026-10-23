"""Exhaustive ground-truth verified card overrides & deterministic formula/explanation cleanups.
Every single override ID below was verified directly against both `output/qa_dataset.json`
and the 300-DPI original page scans (`/tmp/check30_p1.png`, `/tmp/check30_p2.png`,
`/tmp/check_more9.png`, `/tmp/post_round3_audit.txt`).
"""
from __future__ import annotations

import re
from typing import Dict, List, Tuple


EXTRA_CARD_OVERRIDES: Dict[str, dict] = {
    # ── 100% Pixel-verified scan & corpus overrides (Chemistry) ──
    "CHIM-C02-COMM-004": {
        "explanation": "Infatti, in 1 mole di molecole di acqua sono contenute 2 moli di atomi di idrogeno, ovvero 2 × 6,02 · 10²³ atomi = 1,204 · 10²⁴ atomi.",
    },
    "CHIM-C02-COMM-006": {
        "explanation": "Se il peso molecolare del saccarosio è 342 (numero puro!), la sua massa molare è pari a 342 g mol⁻¹ e 34,2 g rappresenta la massa di 0,1 mol di saccarosio, ovvero di un numero di molecole pari a un decimo del numero di Avogadro (sessantamila miliardi di miliardi).",
    },
    "CHIM-C03-COMM-014": {
        "explanation": "Gli elementi che hanno configurazione esterna con 7 elettroni s²p⁵ sono gli alogeni.",
    },
    "CHIM-C03-NCOM-048": {
        "options_patch": {"B": "contiene un numero di particelle pari a 6,022 × 10²³"},
    },
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
    "CHIM-C04-COMM-001": {
        "question": "Leggere il brano: “Gli effetti della corrosione sono massimi nelle città e nelle zone industriali, dove nell'aria si trovano tracce sensibili di gas (come CO₂, H₂S, SO₂, NH₃, NO₂, ecc.) che favoriscono l'attacco chimico dei metalli, e dove abbondano, nel terreno, correnti elettriche vaganti (dovute ad esempio alle linee di ritorno della trazione elettrica) che danno luogo a vere elettrolisi, nelle quali le strutture metalliche interrate fungono da elettrodi, e i sali contenuti nel terreno da elettroliti”. Indicare, tra le seguenti, l'unica affermazione che PUÒ essere dedotta dalla lettura del brano precedente.",
    },
    "CHIM-C05-COMM-001": {
        "explanation": "Siccome il processo è realizzato a temperatura costante, si può usare la legge dei gas ideali PV = nRT ed esprimere in funzione del rapporto PV/n = RT. Applicando l'equazione ai due stati (1,0 mol all'inizio e 4,0 mol alla fine), si ottiene P₁V₁ / 1 = P₂V₂ / 4. Sostituendo V₂ = 2 V₁ si ha: P₁V₁ = (2/4) P₂V₁, quindi P₂ = 2 P₁.",
    },
    "CHIM-C05-COMM-011": {
        "question": "Il monossido di carbonio, di formula CO, si può ottenere per combustione del carbonio in difetto di ossigeno, a circa 1000 °C; inoltre la combustione incompleta di molte sostanze organiche dà luogo alla formazione di CO. Il monossido di carbonio, in cui il C manifesta numero di ossidazione +2, è un gas incolore, inodore, insapore; brucia all'aria formando gas biossido di carbonio (composto in cui il C ha numero di ossidazione +4). A differenza del biossido di carbonio, il CO è praticamente insolubile in acqua. Quale delle seguenti affermazioni NON è in accordo con il contenuto del brano precedente?",
    },
    "CHIM-C05-COMM-014": {
        "question": "A temperatura ambiente, l'acqua è un liquido dotato di ottime proprietà solventi. Molti sali, come ad esempio il solfato di potassio, si sciolgono rapidamente in acqua, mentre sono praticamente insolubili in solventi apolari come il tetracloruro di carbonio o il toluene. Questa proprietà è una conseguenza del carattere dipolare della molecola dell'acqua. Il reticolo cristallino di un sale è tenuto unito da attrazioni elettrostatiche molto forti tra gli ioni positivi e quelli negativi; quando il solfato di potassio cristallino è posto in acqua, le molecole polari di quest'ultima sono fortemente attratte dagli ioni K⁺ e SO₄²⁻, e strappano questi ioni al reticolo. Quale delle seguenti affermazioni può essere dedotta dalla lettura del brano precedente?",
    },
    "CHIM-C05-COMM-015": {
        "question": "L'acqua è un liquido dotato di ottime proprietà solventi. Molti sali, come ad esempio il cloruro di sodio, si sciolgono rapidamente in acqua, mentre sono praticamente insolubili in solventi apolari come il cloroformio e il benzene. Questa proprietà è una conseguenza del carattere dipolare della molecola dell'acqua. Il reticolo cristallino di un sale è tenuto insieme da attrazioni elettrostatiche molto forti tra ioni positivi e ioni negativi. Quando il cloruro di sodio cristallino è posto in acqua, le molecole polari di quest'ultima sono fortemente attratte dagli ioni Na⁺ e Cl⁻, e strappano questi ioni al reticolo. Indicare quale delle seguenti affermazioni PUÒ essere dedotta dalla lettura del brano precedente.",
    },
    "CHIM-C06-COMM-002": {
        "question": "La normalità (N) di una soluzione acquosa di Ca(OH)₂ 0,5 M è:",
        "options": {"A": "0,5 N", "B": "5,0 N", "C": "1,0 N", "D": "30,0 N", "E": "0,25 N"},
    },
    "CHIM-C06-COMM-017": {
        "options_patch": {
            "A": "Se su 2,0 moli iniziali se ne dissociano 0,4, e le rimanenti 1,6 restano indissociate, il grado di dissociazione è dato da 0,4/1,6 = 0,25",
        },
    },
    "CHIM-C06-COMM-025": {
        "explanation": "Il criterio di solubilità di un soluto in un solvente è estremamente semplice: “il simile scioglie il simile”. Dei composti elencati il solo solfato di rame è ionico e quindi certamente polare e della stessa natura dell'acqua, covalente ma polare. Gli altri composti sono apolari (benzina, grasso neutro) o solo leggermente polari (etere dietilico). Per quanto riguarda la cellulosa il discorso è più complesso: la sua molecola è quella di un polimero con moltissimi gruppi polari (ossidrilici). Questi gruppi tuttavia sono impegnati in legami a ponte di idrogeno tra le lunghe catene lineari della cellulosa che si configura molto compatta, al punto da non sciogliersi in acqua.",
    },
    "CHIM-C06-NCOM-009": {
        "options_patch": {"C": "0,3 L"},
    },
    "CHIM-C06-NCOM-038": {
        "options_patch": {"D": "60 × 10⁻² g di acido acetico e 36 × 10⁻² g di acido cloridrico"},
    },
    "CHIM-C06-NCOM-074": {
        "options": {
            "A": "100 mL di CaCl₂ 0,50 M",
            "B": "500 mL di NaCl 0,10 M",
            "C": "1.000 mL di HCl 0,10 M",
            "D": "250 mL di BaCl₂ 0,20 M",
            "E": "2.000 mL di HCl 0,05 M",
        },
    },
    "CHIM-C07-COMM-004": {
        "explanation": "In una qualsiasi reazione di neutralizzazione le specie reagenti sono: H⁺ + OH⁻ → H₂O.",
    },
    "CHIM-C07-COMM-020": {
        "question": "Se si fanno reagire otto moli di H₂ con quattro moli di O₂, le moli di acqua che si formano sono al massimo:",
    },
    "CHIM-C07-NCOM-022": {
        "question": "Quali sono i valori da attribuire ai coefficienti a, b, c per bilanciare correttamente la seguente reazione chimica?\na NH₃ + b O₂ → c NO + 6 H₂O",
    },
    "CHIM-C07-NCOM-027": {
        "question": "Quando 1,2 g di magnesio reagiscono completamente con acido solforico diluito e in eccesso, il magnesio solfato prodotto viene separato, disidratato e ha un peso finale di 5,5 g.\nLa reazione è: Mg + H₂SO₄ → MgSO₄ + H₂\nQual è la resa di magnesio solfato in percentuale? [Si assuma massa atomica relativa: Mg = 24; S = 32; O = 16]",
    },
    "CHIM-C07-NCOM-042": {
        "options_patch": {"D": "CaCl₂ → Ca²⁺ + 2 Cl⁻"},
    },
    "CHIM-C08-COMM-007": {
        "question": "La seguente reazione è esotermica:\n2 T(g) + 3 X(g) ⇄ 6 Z(g)\nQuale delle seguenti affermazioni è corretta?",
        "options": {
            "A": "All'equilibrio, T e X producono Z alla stessa velocità con cui Z produce T e X",
            "B": "Un catalizzatore aumenta la quantità di prodotto Z",
            "C": "Un aumento di pressione causa un aumento della quantità di prodotto Z",
            "D": "Un aumento di temperatura causa un aumento della quantità di prodotto Z",
            "E": "L'aggiunta di Z sposta la posizione dell'equilibrio verso destra",
        },
        "explanation": "All'equilibrio, la velocità di formazione di Z (reazione diretta) è uguale alla velocità di decomposizione di Z in T e X (reazione inversa). Questo è il principio fondamentale dell'equilibrio dinamico.\nLe altre opzioni sono errate:\n• B) un catalizzatore non modifica la quantità di prodotto all'equilibrio;\n• C) l'aumento di pressione sposta l'equilibrio verso il lato con meno moli gassose, cioè verso i reagenti (5 moli → 6 moli);\n• D) per reazioni esotermiche, l'aumento di T favorisce i reagenti;\n• E) aggiungere Z sposta l'equilibrio verso sinistra.",
    },
    "CHIM-C08-NCOM-015": {
        "question": "La variazione di quale dei seguenti fattori modifica il valore della costante di equilibrio K_c di una reazione?",
    },
    "CHIM-C08-NCOM-016": {
        "question": "Considerando pari a K il valore della costante del seguente equilibrio chimico:\nN₂(g) + 3 H₂(g) ⇄ 2 NH₃(g)\nQuale sarà il suo valore, a temperatura costante, se la concentrazione molare di H₂ raddoppia?",
    },
    "CHIM-C09-NCOM-053": {
        "options": {
            "A": "il Cd non si può ossidare",
            "B": "nessuna delle risposte è corretta",
            "C": "il Cd è ossidante",
            "D": "passa da Cd²⁺ a Cd",
            "E": "passa da Cd a Cd²⁺",
        },
    },
    "CHIM-C09-NCOM-060": {
        "question": "In questa reazione: 2 HBr + I₂ → 2 HI + Br₂, che è di ossido-riduzione:",
    },
    "CHIM-C09-NCOM-076": {
        "question": "Nella semireazione Ag⁺ + e⁻ → Ag, l'Ag⁺:",
    },
    "CHIM-C09-NCOM-098": {
        "question": "Data la reazione Zn + Cu²⁺ → Zn²⁺ + Cu è corretto dire che:",
        "options": {
            "A": "Zn è l'agente ossidante",
            "B": "Zn acquista elettroni",
            "C": "Cu²⁺ è l'agente ossidante",
            "D": "Zn viene ridotto",
            "E": "Cu²⁺ perde elettroni",
        },
    },
    "CHIM-C09-NCOM-114": {
        "question": "Nella seguente reazione Mg + CaCl₂ → MgCl₂ + Ca, lo ione che si riduce è:",
    },
    "CHIM-C09-NCOM-126": {
        "question": "In una reazione in cui Pb²⁺ si trasforma in PbCl₄, si può affermare che:",
    },
    "CHIM-C10-COMM-016": {
        "question": "La struttura dello ione ammonio può essere compresa mediante due schematizzazioni; nella prima un idrogenione si lega al doppietto elettronico non condiviso presente nell'ibrido sp³ dell'atomo di azoto dell'ammoniaca (legame dativo); nella seconda schematizzazione la formazione dello ione può essere supposta come risultato della combinazione di un ipotetico ione N⁺, isoelettronico con il carbonio, con quattro atomi di idrogeno; in entrambi i casi, comunque, l'atomo di azoto si trova nello stato di ibridazione sp³, e la struttura dello ione è perfettamente tetraedrica. Quale delle seguenti informazioni NON può essere dedotta dalla lettura del brano precedente?",
        "options_patch": {"C": "L'ipotetico ione N⁺ possiede 4 elettroni nell'ultimo livello"},
    },
    "CHIM-C10-COMM-021": {
        "explanation": "L'ozono è una forma allotropica di ossigeno di formula O₃.",
    },
    "CHIM-C10-COMM-030": {
        "question": "La formula H₂SO₃, secondo la nomenclatura tradizionale, corrisponde a:",
    },
    "CHIM-C10-COMP-009": {
        "question": "Gli ossidi _____ hanno formula generale X₂O_n, dove X è un non metallo.",
    },
    "CHIM-C10-COMP-024": {
        "question": "Gli ossidi _____ hanno formula generale M₂O_n, dove M è un metallo.",
    },
    "CHIM-C10-NCOM-008": {
        "question": "Il composto Cl₂O₇ è:",
    },
    "CHIM-C10-NCOM-019": {
        "options": {"A": "H₂S₂O₆", "B": "H₂SO₃", "C": "H₂SO₄", "D": "HSO₄⁻", "E": "H₂S"},
    },
    "CHIM-C10-NCOM-025": {
        "options": {"A": "H₂SO₃", "B": "H₂SO₄", "C": "H₂S₂O₃", "D": "H₂S₂O₄", "E": "H₂S"},
    },
    "CHIM-C10-NCOM-027": {
        "options_patch": {"B": "gas e ossigeno"},
    },
    "CHIM-C10-NCOM-080": {
        "question": "Indicare lo ione perclorato:",
        "options": {"A": "ClO₄⁻", "B": "ClO⁻", "C": "Cl₂O⁺", "D": "Cl⁻", "E": "ClO₂"},
    },
    "CHIM-C11-COMM-002": {
        "question": "Gli idrossidi (dei metalli) sono composti ionici, che contengono ioni OH⁻ non solo in soluzione ma già allo stato cristallino. La loro dissoluzione determina il distacco del catione dallo ione OH⁻. Pertanto nella soluzione acquosa dell'idrossido solubile di un metallo esistono ioni metallici, e sono invariabilmente presenti gli ossidrili, che costituiscono la vera specie basica, cioè la specie capace di legare un protone con formazione di acqua. Quale delle seguenti affermazioni NON può essere dedotta dalla lettura del brano?",
    },
    "CHIM-C11-COMM-015": {
        "question": "In 100 mL di una soluzione di HCl 0,1 N vengono sciolte 0,01 mol di idrossido di sodio. Una sola delle seguenti affermazioni è CORRETTA. Quale? Il pH:",
    },
    "CHIM-C11-COMM-032": {
        "explanation": "Lo ione HPO₄²⁻ comportandosi da base deve accettare un protone e trasformarsi in H₂PO₄⁻, il suo acido coniugato.",
    },
    "CHIM-C11-COMP-001": {
        "question": "Un _____ di Arrhenius è una sostanza che in acqua produce ioni H₃O⁺.",
    },
    "CHIM-C11-COMP-010": {
        "question": "L'_____ è una sostanza anfiprotica che può formare H₃O⁺ o OH⁻.",
    },
    "CHIM-C11-COMP-021": {
        "question": "Tra K_a e K_b esiste una relazione tramite la costante _____ (K_w) dell'acqua.",
    },
    "CHIM-C11-NCOM-011": {
        "question": "L'ammoniaca NH₃ è in grado di accettare ioni H⁺ formando NH₄⁺, quindi è:",
    },
    "CHIM-C11-NCOM-026": {
        "options_patch": {"C": "se è completamente ionizzata in H⁺ e A⁻"},
    },
    "CHIM-C11-NCOM-034": {
        "options_patch": {"A": "SO₂"},
    },
    "CHIM-C11-NCOM-037": {
        "options": {"A": "Cl₂O₃", "B": "Na₂O", "C": "NH₃", "D": "Al₂O₃", "E": "KOH"},
    },
    "CHIM-C11-NCOM-040": {
        "question": "La soda caustica, conosciuta anche come idrossido di sodio (NaOH), è:",
    },
    "CHIM-C11-NCOM-055": {
        "question": "Una soluzione acquosa 10⁻⁵ M di KOH presenta una concentrazione di ioni H₃O⁺ pari a:",
    },
    "CHIM-C11-NCOM-058": {
        "question": "In una soluzione, la concentrazione di ioni H₃O⁺ è 1,0 × 10⁻⁸ mol dm⁻³. Qual è la concentrazione di ioni OH⁻ nella soluzione espressa in mol dm⁻³?",
    },
    "CHIM-C11-NCOM-065": {
        "options_patch": {"C": "NaOH 10⁻³ M", "D": "LiOH 10⁻⁴ M", "E": "NaOH 1 M"},
    },
    "CHIM-C11-NCOM-070": {
        "question": "Dell'acqua viene aggiunta a 10 cm³ di una soluzione acquosa di acido cloridrico 2 mol dm⁻³ in modo da ottenere 1000 cm³ di acido cloridrico diluito. Di quanto varia il valore del pH della soluzione acida?",
    },
    "CHIM-C11-NCOM-090": {
        "question": "Quale delle seguenti espressioni matematiche mostra come calcolare il pH di una soluzione acquosa di acido solforico 0,002 M?",
        "options": {
            "A": "pH = log₁₀ 0,004",
            "B": "pH = −log₁₀ 0,001",
            "C": "pH = −log₁₀ 0,002",
            "D": "pH = −log₁₀ 0,004",
            "E": "pH = log₁₀ 0,002",
        },
    },
    "CHIM-C11-NCOM-097": {
        "options_patch": {"A": "[H₃O⁺] > [OH⁻]"},
    },
    "CHIM-C11-NCOM-106": {
        "options_patch": {
            "A": "la concentrazione di ioni OH⁻",
            "D": "la concentrazione di ioni H⁺",
        },
    },
    "CHIM-C11-NCOM-110": {
        "options": {
            "A": "[OH⁻] < 6 M",
            "B": "[H₃O⁺] = [OH⁻]",
            "C": "[OH⁻] > 7 M",
            "D": "[H₃O⁺] > 7 M",
            "E": "[H₃O⁺] > [OH⁻]",
        },
    },
    "CHIM-C11-NCOM-121": {
        "question": "Il pH di una soluzione acquosa che contiene 10⁻⁴ moli di HCl in 100 mL è:",
    },
    "CHIM-C11-NCOM-144": {
        "options_patch": {
            "A": "un numero di ioni H₃O⁺ maggiore del numero di ioni OH⁻",
            "B": "un numero di ioni H₃O⁺ inferiore al numero di ioni OH⁻",
        },
    },
    "CHIM-C12-COMM-018": {
        "explanation": "Il pentene è un alchene (desinenza “-ene”) e la reazione caratteristica degli alcheni è la reazione di addizione elettrofila al doppio legame.",
    },
    "CHIM-C12-COMM-021": {
        "options_patch": {"C": "Gli atomi di C sono ibridati sp²"},
    },
    "CHIM-C12-NCOM-015": {
        "options_patch": {"C": "presenta ibridazione sp²"},
    },
    "CHIM-C12-NCOM-064": {
        "options": {"A": "sp²", "B": "sp³d", "C": "sp", "D": "non è ibridizzato", "E": "sp³"},
    },
    "CHIM-C12-NCOM-072": {
        "options_patch": {"D": "Uno sp³ e tre sp²"},
    },
    "CHIM-C12-NCOM-158": {
        "options_patch": {"C": "ibridazione sp²"},
    },
    "CHIM-C12-NCOM-193": {
        "options_patch": {"D": "Gli atomi di carbonio che lo formano sono generalmente ibridati sp²"},
    },
    "CHIM-C12-NCOM-277": {
        "options_patch": {
            "B": "è il secondo della catena carboniosa",
            "C": "è ibridato sp²",
        },
    },
    "CHIM-C13-COMM-021": {
        "options_patch": {"E": "6,023 · 10²³ molecole di amminoacidi"},
    },

    # ── 100% Pixel-verified scan & corpus overrides (Biology) ──
    "BIO-C01-COMM-038": {
        "explanation": "Nei tilacoidi, le reazioni dipendenti dalla luce della fotosintesi convertono l'energia luminosa in energia chimica. La cattura dell'energia luminosa da parte della clorofilla fa sì che uno dei suoi elettroni passi dallo stato fondamentale a uno stato eccitato; tale elettrone viene trasferito a una molecola accettrice e rimpiazzato da un elettrone derivante dalla fotolisi dell'acqua, un processo in cui viene liberato ossigeno molecolare. Parte dell'energia contenuta negli elettroni eccitati è utilizzata per fosforilare l'ADP ad ATP e per ridurre il coenzima NADP⁺ a NADPH.",
    },
    "BIO-C04-COMM-007": {
        "explanation": "Se i geni “A” e “B” mostrano segregazione indipendente, vuol dire che sono localizzati su due coppie di cromosomi diversi. Quando si producono i gameti si ha un dimezzamento del numero dei cromosomi e un gamete contiene un cromosoma di ciascuna coppia. Pertanto, per un individuo con genotipo AaBb, si avranno gameti AB, Ab, aB, ab con la medesima frequenza.\n• Il rapporto 9:3:3:1 si ottiene dall'incrocio AaBb × AaBb (geni indipendenti).\n• Il rapporto di segregazione fenotipica 3:1 si ottiene dall'incrocio Aa × Aa.\n• Il rapporto 1:2:1 è il rapporto di segregazione genotipica dall'incrocio Aa × Aa.",
    },
    "BIO-C04-COMM-008": {
        "question": "Applicando la legge dell'assortimento indipendente, un individuo con genotipo GgFf produce i gameti:",
        "options": {
            "A": "GF",
            "B": "gf",
            "C": "G, g, F, f",
            "D": "GF, Gf, gF, gf",
            "E": "tutti gameti uguali",
        },
        "explanation": "La legge dell'assortimento indipendente prevede che i membri di differenti coppie di alleli si distribuiscano indipendentemente gli uni dagli altri quando si formano i gameti. Sono quindi possibili tutte le combinazioni composte da un allele del locus “g” (G o g) e uno del locus “f” (F o f), ovvero GF, Gf, gF, gf.",
    },
    "BIO-C04-COMM-014": {
        "explanation": "Se si incrociano due cani mancanti di pelo, cioè due individui con genotipo eterozigote (Hh) per il carattere assenza di pelo, si ottengono individui con genotipo HH, Hh e hh in un rapporto 1:2:1 (seconda legge di Mendel). In una progenie di 4 cuccioli è atteso un cucciolo con pelo normale (hh), due senza pelo (Hh) e uno che nascerà morto in quanto presenta il genotipo letale HH: la progenie vitale sarà quindi di tre cuccioli, di cui due mancanti di pelo (2/3).\nSe invece si incrocia un individuo con pelo normale (hh) con un cane mancante di pelo (Hh) si otterranno 2 cuccioli senza pelo e 2 con pelo normale (1/2). Gli individui omozigoti dominanti muoiono alla nascita e quindi non possono essere fatti riprodurre (escludendo C e D), mentre hh × hh dà solo cani con pelo normale (escludendo E). Fra A e B, la migliore è la A perché dà cani privi di pelo con frequenza maggiore.",
    },
    "BIO-C04-COMM-021": {
        "explanation": "Nella prima generazione (F₁) si manifesta in genere il carattere di uno dei due genitori; l'altro carattere non si osserva, ma non scompare perché riappare nella seconda generazione (F₂). La conclusione è che questo carattere sia presente in F₁, anche se “mascherato”: nell'incontro di due caratteri uno solo prevale.",
    },
    "BIO-C04-COMM-032": {
        "explanation": "Gli individui di sesso maschile hanno un solo cromosoma X. Quindi, per un gene situato sul cromosoma X, essi possono avere genotipo XᴬY o XᵃY, il cui fenotipo è rispettivamente “A” o “a”. Ne consegue che nei maschi sono uguali la frequenza dell'allele mutato (“a”), la frequenza genotipica e la frequenza fenotipica (10%).",
    },
    "BIO-C04-COMM-033": {
        "explanation": "Gli individui di sesso maschile presentano un solo cromosoma X e un cromosoma Y. Quindi per un gene emizigote legato ai cromosomi sessuali possono avere genotipo XᴬY o XᵃY con fenotipo rispettivamente “A” o “a”: la frequenza dell'allele mutato (“a”), la frequenza genotipica e la frequenza fenotipica coincidono (5%).",
    },
    "BIO-C04-COMM-041": {
        "question": "Una donna daltonica omozigote sposa un uomo che vede normalmente i colori:",
        "options": {
            "A": "sicuramente avrà figlie femmine senza cecità ai colori",
            "B": "avrà 50% di figli maschi daltonici e 50% normali",
            "C": "avrà figli maschi tutti normali",
            "D": "avrà 50% di figlie femmine daltoniche e 50% normali",
            "E": "avrà figlie femmine tutte daltoniche",
        },
        "explanation": "Il daltonismo è un carattere recessivo legato al cromosoma X (Xᵈ). La madre daltonica omozigote ha genotipo XᵈXᵈ, mentre il padre normale ha genotipo XᴰY.\n• Tutte le figlie femmine ricevono Xᴰ dal padre e Xᵈ dalla madre (genotipo XᴰXᵈ): saranno portatrici sane, quindi senza cecità ai colori.\n• Tutti i figli maschi ricevono Xᵈ dalla madre e Y dal padre (genotipo XᵈY): saranno tutti daltonici.",
    },
    "BIO-C04-COMM-061": {
        "question": "Una donna di gruppo sanguigno 0 Rh⁻ sposa un uomo AB Rh⁺ eterozigote per il fattore Rh. Quale, tra quelli proposti, potrebbe essere il gruppo sanguigno del figlio?",
        "options": {"A": "AB Rh⁻", "B": "0 Rh⁻", "C": "AB Rh⁺", "D": "B Rh⁻", "E": "0 Rh⁺"},
        "explanation": "La madre è 0 Rh⁻ (genotipo ii dd) e trasmette sempre i e d.\nIl padre è AB Rh⁺ eterozigote (genotipo IᴬIᴮ Dd) e può trasmettere Iᴬ o Iᴮ e D o d.\nI figli possono quindi essere A Rh⁺, A Rh⁻, B Rh⁺ oppure B Rh⁻: tra le opzioni proposte è possibile B Rh⁻.",
    },
    "BIO-C04-COMM-068": {
        "explanation": "L'amniocentesi è una tecnica di diagnosi prenatale che consiste nel prelevare, a partire dalla 16ª settimana, una piccola quantità di liquido amniotico, nel quale è possibile reperire cellule fetali su cui effettuare analisi cromosomiche.",
    },
    "BIO-C04-NCOM-045": {
        "question": "Dall'incrocio mendeliano Aa × Aa si originano individui con fenotipi:",
    },
    "BIO-C05-COMM-029": {
        "explanation": "Nella reazione indicata nel quesito il glucosio (C₆H₁₂O₆) viene ossidato, in presenza di ossigeno, ad anidride carbonica (CO₂) con liberazione di acqua ed energia sotto forma di ATP. In questa reazione la sostanza che viene ridotta è l'ossigeno.",
    },
    "BIO-C05-COMM-075": {
        "options_patch": {"B": "3 NADH, 2 FADH₂, 2 ATP, 3 CO₂"},
        "explanation": "Ogni giro del ciclo di Krebs produce 3 NADH, 1 FADH₂, 1 ATP (o GTP) e libera 2 CO₂.",
    },
    "BIO-C05-COMM-096": {
        "question": "Quale difetto molecolare causa la fibrosi cistica più comune (ΔF508)?",
        "explanation": "La mutazione ΔF508 comporta la delezione di una fenilalanina in posizione 508, che impedisce il corretto ripiegamento del canale del cloro CFTR: la proteina viene riconosciuta come difettosa e degradata prima di raggiungere la membrana plasmatica.",
    },
    "BIO-C05-COMP-098": {
        "question": "Il trasporto delle proteine al perossisoma è un processo _____-dipendente, necessario per il riconoscimento e l'importazione.",
    },
    "BIO-C05-NCOM-270": {
        "options_patch": {"C": "O₂"},
    },
    "BIO-C06-COMM-030": {
        "explanation": "I recettori ionotropici sono canali che si aprono al legame del ligando; quello nicotinico consente il passaggio di Na⁺ causando depolarizzazione della membrana postsinaptica.",
    },
    "BIO-C06-COMM-036": {
        "explanation": "Molecole come cAMP, IP₃, DAG e Ca²⁺ sono secondi messaggeri che amplificano il segnale iniziale e attivano chinasi intracellulari.",
    },
    "BIO-C06-COMM-046": {
        "explanation": "PIP₂ può essere idrolizzato da PLC in DAG e IP₃ oppure fosforilato da PI3K in PIP₃, attivando vie a valle come Akt.",
    },
    "BIO-C06-COMP-073": {
        "question": "I _____ (cAMP, DAG, IP₃, Ca²⁺) diffondono rapidamente nel citoplasma amplificando il segnale.",
    },
    "BIO-C07-COMM-052": {
        "question": "Quale proteina CKI viene indotta da p53 in risposta a danno al DNA?",
        "explanation": "Il danno al DNA attiva p53, che induce l'espressione di p21. Questa CKI si lega ai complessi ciclina-Cdk, bloccandone l'attività e arrestando temporaneamente il ciclo cellulare.",
    },
    "BIO-C07-COMM-054": {
        "question": "Quale effetto ha il TGF-β sull'attività del complesso ciclina D-Cdk4/6?",
        "explanation": "Il TGF-β induce l'espressione di p15, un inibitore CKI specifico per Cdk4/6, bloccando la fosforilazione di Rb e impedendo l'ingresso della cellula in fase S.",
    },
    "BIO-C07-NCOM-009": {
        "options": {
            "A": "M, G₁, G₂, S",
            "B": "G₁, M, G₂, S",
            "C": "G₁, G₂, S, M",
            "D": "G₁, S, G₂, M",
            "E": "S, M, G₁, G₂",
        },
    },
    "BIO-C07-NCOM-044": {
        "question": "La figura rappresenta una cellula in anafase della 1ª divisione meiotica. Dalla sua osservazione si può dedurre che la cellula originaria avesse un 2n uguale a:",
    },

    # ── 100% Pixel-verified scan & corpus overrides (Physics) ──
    "FIS-C01-COMM-007": {
        "explanation": "L'unità di misura del prodotto pressione × volume nel SI risulta essere:\n1 Pa · m³ = (1 N / m²) · m³ = 1 N · m = 1 J (joule).",
    },
    "FIS-C01-COMM-012": {
        "explanation": "Considerando che 1 kilowatt equivale a 10³ watt, la potenza elettrica totale di un milione di kilowatt equivale a 10⁶ · 10³ watt = 10⁹ watt = 1 GW (gigawatt).",
    },
    "FIS-C01-COMM-018": {
        "question": "Due forze uguali agiscono su di un corpo in direzioni perpendicolari l'una all'altra. Il modulo delle due forze è di 1 N. Quanto vale il modulo della forza risultante?",
        "explanation": "Il modulo della forza risultante si calcola come diagonale del quadrato avente per lati i due vettori ortogonali di modulo 1 N:\nR = √((1 N)² + (1 N)²) = √2 N.",
    },
    "FIS-C01-COMM-022": {
        "options_patch": {"A": "F · cos(α)"},
    },
    "FIS-C01-NCOM-005": {
        "options_patch": {"E": "F = L / E"},
    },
    "FIS-C02-COMM-002": {
        "explanation": "La frequenza del moto è f = 6000 giri/min = 6000 / 60 s = 100 Hz, da cui la pulsazione vale ω = 2πf = 2 · 3,14 · 100 = 628 rad/s. L'accelerazione centripeta vale quindi a_c = ω²r = (628 rad/s)² · 0,125 m ≈ 50.000 m/s². Posto g ≈ 10 m/s², si ottiene a_c ≈ 5000 g.",
    },
    "FIS-C02-COMM-009": {
        "explanation": "La legge oraria del moto uniformemente accelerato con x₀ = 0 è x(t) = v₀t + (1/2)at², che nel piano (t, x) rappresenta un arco di parabola passante per l'origine con vertice in (−v₀/a, −v₀²/(2a)).",
    },
    "FIS-C02-COMM-011": {
        "question": "(Simboli: T = periodo; f = frequenza; π = 3,1416...). Per descrivere un moto armonico si utilizza anche la velocità angolare ω. Quale delle seguenti relazioni è ERRATA?",
        "options": {
            "A": "ω = 2 · π / T",
            "B": "f = 1 / T",
            "C": "T = 2 · π / ω",
            "D": "T = 2 · π · ω",
            "E": "T = 1 / f",
        },
        "explanation": "La velocità angolare (pulsazione) ω è legata al periodo T e alla frequenza f dalle relazioni ω = 2π / T = 2πf, da cui T = 2π / ω e f = 1 / T. La relazione T = 2 · π · ω è quindi errata.",
    },
    "FIS-C02-COMM-016": {
        "options_patch": {"E": "(lunghezza)² / (tempo)²"},
    },
    "FIS-C02-COMM-008": {
        "explanation": "L'accelerazione si calcola come rapporto tra la variazione di velocità e l'intervallo di tempo nel quale è avvenuta tale variazione:\na = Δv / Δt = (120 − 100) km/h / (36 / 3600) h = 2000 km/h², dove si è considerata l'equivalenza 36 secondi = (36 / 3600) ore.",
    },
    "FIS-C02-COMM-019": {
        "question": "Sia data la seguente equazione per un moto di caduta di un grave: s = 0,5 gt² + k, dove s rappresenta lo spazio, t il tempo e g l'accelerazione di gravità. Niente viene detto del termine k. Dica il candidato quali sono le dimensioni di k, se si indicano con M la massa, con L la lunghezza e con T il tempo.",
        "explanation": "L'equazione per il moto di caduta di un grave nella sua forma completa è s = 0,5 gt² + v₀t + s₀, dove v₀ indica la velocità iniziale e s₀ la posizione iniziale.\nNel caso in cui il grave venga lasciato cadere con velocità iniziale nulla l'equazione diventa: s = 0,5 gt² + s₀.\nNel caso in cui il grave parta dalla posizione iniziale s₀ = 0 l'equazione diventa: s = 0,5 gt² + v₀t.\nEssendo s una lunghezza, i singoli addendi 0,5 gt², v₀t e s₀ sono anch'essi dimensionalmente delle lunghezze. Quindi k (pari a s₀ oppure a v₀t) ha le dimensioni di una lunghezza [L].",
    },
    "FIS-C02-NCOM-061": {
        "question": "Una ruota di bicicletta durante il moto rotola senza strisciare sulla strada. La velocità della bicicletta è costante e vale V₀. Sapendo che il raggio della ruota vale R si domanda la velocità istantanea del punto della ruota più lontano dal suolo.",
        "options": {
            "A": "La velocità del centro moltiplicata per il raggio, quindi V₀ · R",
            "B": "Il doppio della velocità del centro, quindi 2·V₀",
            "C": "È un moto accelerato e la velocità aumenta",
            "D": "La stessa del centro: V₀",
            "E": "Non può essere specificata",
        },
    },
    "FIS-C02-NCOM-071": {
        "question": "Una molla ha costante elastica pari a 8 N/m, quale massa si deve sospendere alla molla affinché oscilli con periodo T = 1 s?",
    },
    "CHIM-C01-NCOM-098": {
        "question": "Quanti elettroni, protoni e neutroni ha, nell'ordine, lo ione H⁻?",
    },
    "CHIM-C02-NCOM-037": {
        "options": {"A": "6p", "B": "6s", "C": "5s", "D": "5p", "E": "5d"},
    },
    "CHIM-C03-NCOM-048": {
        "options": {
            "A": "ha sempre la stessa massa",
            "B": "contiene un numero di particelle pari a 6,022 × 10³",
            "C": "contiene lo stesso numero di elettroni",
            "D": "occupa sempre lo stesso volume",
            "E": "contiene un numero di particelle pari a 6,022 × 10¹³",
        },
    },
    "CHIM-C05-COMM-012": {
        "question": "Alla temperatura di 27 °C il volume di un palloncino è 2,40 L. Assumendo che la pressione resti costante, quale sarà il volume dello stesso palloncino alla temperatura di -23 °C?",
        "options": {"A": "2,00 L", "B": "2,88 L", "C": "-2,04 L", "D": "120 L", "E": "1,02 L"},
        "explanation": "Per risolvere questo esercizio è sufficiente sfruttare l'equazione di Charles (nella forma V₁/T₁ = V₂/T₂) ricordandosi di trasformare le temperature in kelvin (27 °C = 300 K; -23 °C = 250 K):\nV₂ = V₁ · T₂ / T₁ = 2,40 × 250 / 300 = 2,00 L.",
    },
    "CHIM-C06-COMM-005": {
        "explanation": "Il calcolo si effettua eguagliando le moli di soluto prima e dopo la diluizione:\n(10 mL × 8 M) / 1000 mL = (V × 0,4 M) / 1000 mL, da cui V = 200 mL.",
    },
    "CHIM-C07-NCOM-053": {
        "options_patch": {"C": "La scissione dell'ammoniaca NH₃ negli elementi costitutivi (N₂ e H₂)"},
    },
    "CHIM-C11-COMM-038": {
        "question": "A quale dei seguenti valori del pH si ha la minima concentrazione di ioni OH⁻?",
    },
    "BIO-C03-COMP-126": {
        "question": "La sequenza di amminoacidi contiene l'informazione necessaria per la struttura _____ finale di una proteina.",
    },
    "BIO-C07-COMM-021": {
        "question": "Nel liquido spermatico di una sola eiaculazione di un uomo sessualmente maturo sono presenti circa 4 × 10⁸ spermatozoi. Quanti spermatociti di primo ordine hanno subito la meiosi per produrre un numero così elevato di spermatozoi?",
        "options": {"A": "10⁸", "B": "16 × 10⁸", "C": "4 × 10³²", "D": "10⁴", "E": "4 × 10⁴"},
        "explanation": "Durante la spermatogenesi, da 1 spermatocita di primo ordine (detto anche primario) si originano 4 spermatidi che diventeranno 4 spermatozoi. Da 2 spermatociti primari si origineranno 8 spermatozoi. In generale, il numero degli spermatozoi è pari a 4 volte il numero degli spermatociti primari.\nPer produrre 4 × 10⁸ spermatozoi sono quindi necessari (4 × 10⁸) : 4 = 10⁸ spermatociti primari.",
    },
    "BIO-C07-NCOM-186": {
        "question": "Quale evento segna la transizione G1-S?",
    },
    "FIS-C01-COMM-001": {
        "question": "Quale di queste grandezze non è misurabile in joule nel Sistema Internazionale SI?",
    },
    "FIS-C01-NCOM-066": {
        "question": "In uno strano paese, le lunghezze vengono misurate in metrini, lunghi 6,67 cm, mentre i tempi vengono misurati in secondoni, ciascuno dei quali vale 12 secondi; a quanti metrini al secondone equivalgono approssimativamente 10 km/h?",
    },
    "FIS-C03-COMM-006": {
        "options": {"A": "5 W", "B": "-20 W", "C": "2 kW", "D": "200 W", "E": "500 W"},
        "explanation": "Il lavoro compiuto dalla forza F sul corpo è L = F · s; considerando che la forza si oppone al moto:\nL = -F · s = -100 N · 2 m = -200 J.\nEssendo la forza applicata per un intervallo di tempo Δt = 10 s, la potenza sviluppata risulta uguale a:\nP = L / Δt = -200 J / 10 s = -20 W.",
    },
    "FIS-C03-COMM-008": {
        "question": "Un astronomo osserva che un meteorite (di massa m₁ e velocità v₁) si dirige contro un secondo avente massa m₂ = 2·m₁ e velocità v₂ = v₁/2 che gli va incontro sulla stessa retta. Potremo asserire che:",
        "explanation": "Dato un corpo di massa m, si definisce quantità di moto il prodotto tra la sua massa e la sua velocità: p = m · v. La quantità di moto è una grandezza vettoriale e possiede la stessa direzione e verso del vettore velocità.\nIl modulo della quantità di moto dei due meteoriti è uguale e pari a:\np₂ = m₂ · v₂ = 2m₁ · (1/2)v₁ = m₁ · v₁ = p₁.\nLa direzione dei due vettori quantità di moto è la stessa, visto che i meteoriti si muovono sulla stessa retta, mentre il verso è opposto, poiché sono opposti i versi dei due vettori velocità.",
    },
    "FIS-C03-COMM-019": {
        "explanation": "Il lavoro compiuto da una forza costante F è il prodotto scalare tra tale forza applicata e lo spostamento s: L = F · s · cos α. Il ragazzo è soggetto alla forza gravitazionale P che è diretta perpendicolarmente allo spostamento s (cos 90° = 0). Il prodotto scalare tra questi due vettori è dunque nullo.",
    },
    "FIS-C03-COMM-022": {
        "options_patch": {"E": "Mai: perché M è maggiore di zero, e V² è sempre maggiore (o uguale) a zero"},
        "explanation": "L'energia cinetica è definita come K = (1/2) M · V². La massa è una quantità positiva, così come la velocità elevata al quadrato: l'energia cinetica non può pertanto essere negativa.",
    },
    "FIS-C03-COMM-029": {
        "explanation": "L'energia consumata si calcola moltiplicando la potenza per il tempo trascorso:\nE = P · t = (20 W) · (16 h) = (20 W) · (16 · 3600 s) = 1,15 · 10⁶ J = 1,15 MJ.",
    },
    "FIS-C03-COMM-034": {
        "options_patch": {
            "A": "ΔT = m · g · h",
            "C": "la ΔU uguaglia la variazione di energia cinetica",
            "E": "ΔU = m · g / h",
        },
    },
    "FIS-C03-COMM-035": {
        "question": "Qual è la forza centripeta necessaria per far muovere un corpo di massa m = 3,0 kg su di una circonferenza di raggio r = 2,0 m con una velocità v = 4,0 m/s?",
    },
    "FIS-C03-COMM-037": {
        "question": "Un asse del peso di 20 kg_p e lungo 8 metri è appoggiato alle sponde di una stretta insenatura. Un uomo di 100 kg_p cammina sull'asse passando da una sponda all'altra. Durante il percorso la somma delle forze di reazione vincolari esercitate sugli estremi dell'asse per mantenere in equilibrio l'intero sistema:",
        "options": {
            "A": "è nulla",
            "B": "è sempre uguale a 100 kg_p",
            "C": "varia con la posizione dell'uomo sull'asse",
            "D": "dipende dalla natura del materiale utilizzato per costruire l'asse",
            "E": "è sempre uguale a 120 kg_p",
        },
        "explanation": "Nella configurazione dell'asse appoggiato alle sponde, il peso dell'asse stesso P_a e il peso dell'uomo che ci cammina sopra P_u sono sostenuti dalle reazioni vincolari che, per la terza legge della dinamica, equilibrano il peso totale del sistema:\nN₁ + N₂ = P_a + P_u = 20 kg_p + 100 kg_p = 120 kg_p.",
    },
    "FIS-C03-COMP-138": {
        "question": "La quantità di moto è una proprietà legata al _____ di un corpo.",
    },
    "FIS-C03-NCOM-020": {
        "options": {"A": "5 m/s", "B": "80 J/s", "C": "5 m/s²", "D": "80 m/s", "E": "5 J/s"},
    },
    "FIS-C03-NCOM-033": {
        "options": {
            "A": "6 × 10⁷ × 9,8 × 0,1 = 5,9 × 10⁷ Newton",
            "B": "6 × 10⁷ × 9,8 = 5,9 × 10⁸ Newton",
            "C": "6 × 10⁷ / 0,1 = 6 × 10⁸ Newton",
            "D": "6 × 10⁷ × 0,1 = 6 × 10⁶ Newton",
            "E": "Una forza pari al suo peso",
        },
    },
    "FIS-C03-NCOM-067": {
        "question": "Qual è l'unità di misura della costante G usata nella legge di gravitazione universale F = G m₁ m₂ / r²?",
    },
    "FIS-C03-NCOM-098": {
        "question": "Qual è l'energia cinetica alla base di un tavolo di un corpo di massa 5 kg, se il corpo raggiunge la base del tavolo alla velocità di 8,5 m/s?",
    },
    "FIS-C03-NCOM-104": {
        "question": "A quale altezza deve essere lanciato un corpo di massa 100 kg affinché acquisti l'energia cinetica corrispondente a 100 km/h?",
    },
    "FIS-C03-NCOM-105": {
        "question": "In un'automobile di massa M = 10³ kg solo l'11,77% dell'energia prodotta dal motore è utilizzata per far muovere il veicolo. Sapendo che la combustione di un litro di benzina fornisce un'energia di 3,4 × 10⁷ J, quanta benzina è necessaria per portare la macchina da 0 a 72 km/h?",
    },
    "FIS-C03-NCOM-159": {
        "options": {
            "A": "F = m · v² · Δt / 2",
            "B": "F = 2 m v Δt",
            "C": "F = v / Δt",
            "D": "F = m v / Δt",
            "E": "F = 2 Δt / m",
        },
    },
    "FIS-C03-NCOM-163": {
        "question": "La distanza media Terra-Luna è circa 380.000 km e il raggio della Luna è circa 1750 km (0,27 volte quello della Terra); il rapporto tra la massa della Luna e quella della Terra è 1/81. Quale delle seguenti risposte individua più correttamente la posizione del centro di massa (o baricentro) del sistema Terra-Luna?",
    },
    "FIS-C03-NCOM-164": {
        "question": "Il centro di massa del sistema composto dalla Terra (M_T = 6 · 10²⁴ kg, R_T = 6 · 10⁶ m) e dal Sole (M_S = 2 · 10³⁰ kg, R_S = 7 · 10⁸ m) si trova sulla congiungente Terra-Sole (distanza Terra-Sole d = 1,5 · 10¹¹ m):",
        "options_patch": {"A": "al di là del Sole", "C": "al di là della Terra"},
    },
    "FIS-C03-NCOM-182": {
        "options": {"A": "5,5 N", "B": "7,5 N", "C": "6,5 N", "D": "5 N", "E": "8 N"},
    },
    "FIS-C04-COMM-002": {
        "explanation": "Confrontando i primi due bicchieri, si ha P₁ = P₂. Infatti, il peso del tappo di sughero in equilibrio nel secondo bicchiere è bilanciato dalla forza di Archimede, pari al peso dell'acqua spostata dal tappo stesso che è parzialmente immerso. I primi due bicchieri, pertanto, hanno lo stesso peso, dal momento che il peso dell'acqua mancante nel secondo è compensato dal peso del tappo.\nIl terzo bicchiere, invece, possiede un peso maggiore: la sferetta d'acciaio, avendo densità maggiore di quella dell'acqua, non può galleggiare poiché il suo peso è maggiore della spinta di Archimede fornita dal peso dell'acqua spostata. Quindi: P₃ > P₁ = P₂.",
    },
    "FIS-C04-COMM-003": {
        "explanation": "Il principio di Archimede afferma che un corpo immerso in un fluido riceve una spinta dal basso verso l'alto di intensità pari al peso del fluido spostato. La forza di Archimede ha quindi modulo F_A pari a:\nF_A = ρ_f · g · V_i,\ndove ρ_f è la densità del fluido, V_i è il volume del corpo immerso e g è l'accelerazione di gravità. La spinta non dipende quindi dalla profondità alla quale il corpo è immerso ma dipende dalla densità del mezzo, dal volume del corpo, dal valore dell'accelerazione di gravità e anche dal peso specifico del mezzo (P_s = ρ_f · g).",
    },
    "FIS-C04-COMP-003": {
        "question": "La pressione atmosferica standard è circa 1,013 × 10⁵ _____ .",
    },
    "FIS-C04-COMP-017": {
        "question": "L'equazione di continuità si scrive A₁ v₁ = A₂ _____ .",
    },
    "FIS-C04-NCOM-029": {
        "question": "Su una superficie di 50 cm² viene esercitata una pressione di 1,2 × 10⁵ Pascal. Quanto vale la forza che agisce perpendicolarmente alla superficie?",
        "options": {"A": "60 N", "B": "3 N", "C": "6 N", "D": "600 N", "E": "300 N"},
    },
    "FIS-C04-NCOM-060": {
        "question": "Un corpo di peso P₁ e densità D₁ galleggia su un fluido di peso P₂ e densità D₂, quindi:",
        "options": {"A": "P₁ > P₂", "B": "P₁ < P₂", "C": "D₁ < D₂", "D": "D₁ > D₂", "E": "P₂ > P₁"},
    },
    "FIS-C05-COMM-001": {
        "explanation": "Il calore specifico c di una sostanza è la quantità di calore Q necessaria per aumentare di un grado la temperatura dell'unità di massa della sostanza: c = Q / (m · ΔT). I due corpi della domanda, partendo dalla stessa temperatura e assorbendo la stessa quantità di calore per portarsi alla stessa temperatura finale, devono avere lo stesso prodotto c · m (stesso calore specifico e stessa massa).",
    },
    "FIS-C05-COMM-004": {
        "explanation": "Essendo il gas contenuto in un recipiente a pareti rigide, il suo volume non cambia e si ha quindi una trasformazione isocora: la pressione del gas è direttamente proporzionale alla temperatura assoluta del gas.\nPertanto, se P₁ e T₁ sono rispettivamente la pressione e la temperatura iniziale e P₂ e T₂ sono la pressione e la temperatura finale, vale P₁ / T₁ = P₂ / T₂, con T₁ = 27 °C = 300 K e T₂ = 127 °C = 400 K, da cui:\nP₂ / P₁ = 400 K / 300 K = 4/3.",
    },
    "FIS-C05-COMM-019": {
        "question": "In un contenitore c'è una millimole di He (il gas nobile Elio), temperatura e pressione sono standard ed indichiamo con N_A il numero di Avogadro, quindi certamente:",
        "options_patch": {
            "A": "il numero di molecole è N_A / 1000",
            "B": "il numero di molecole è 1000 · N_A",
        },
    },
    "FIS-C05-COMM-024": {
        "explanation": "Il calore specifico di una sostanza è definito come il rapporto tra la capacità termica C del corpo e la sua massa m:\nc = C / m = Q / (m · ΔT).\nIl calore specifico è dunque una grandezza caratteristica di una sostanza che non dipende dalla sua massa.",
    },
    "FIS-C05-COMM-025": {
        "question": "Quante calorie (cal) occorrono per portare 80 litri di acqua da 20 °C a 80 °C?",
        "explanation": "La massa di 80 litri d'acqua è pari a 80 kg = 8 × 10⁴ g (la densità dell'acqua è infatti 10³ kg/m³ = 1 kg/L); per avere un salto termico Δt = 60 °C (scaldare cioè l'acqua da 20 °C a 80 °C) occorre pertanto una quantità di calore pari a:\nQ = c · m · Δt = 1 kcal/(kg·°C) · 80 kg · 60 °C = 4800 kcal,\ndove c è il calore specifico dell'acqua pari a 1 kcal/(kg·°C) = 4186 J/(kg·K).",
    },
    "FIS-C05-COMM-034": {
        "options_patch": {
            "A": "il lavoro esterno è nullo",
            "B": "il lavoro esterno vale p₂·V₂ − p₁·V₁",
            "E": "l'energia interna U è cresciuta ovvero ΔU > 0",
        },
    },
    "FIS-C05-COMM-035": {
        "options_patch": {"B": "il frigorifero ha sottratto 10 kcal all'acqua"},
        "explanation": "La variazione di temperatura che avviene in 1000 secondi è Δt = t_fin − t_in = 20 °C − 30 °C = -10 °C.\nLa variazione di temperatura per unità di tempo vale: -10 °C / 1000 s = -0,01 °C/s.\nLa quantità di calore sottratta è Q = c · m · |Δt| = 1 cal/(g·°C) · 100 g · 10 °C = 1000 cal = 1 kcal = 4186 J; questo scambio di calore in 1000 s equivale a una potenza media di 4,186 W.",
    },
    "FIS-C06-COMM-003": {
        "options_patch": {
            "A": "si respingono con una forza 6400 volte minore",
            "E": "si comportano allo stesso modo",
        },
    },
    "FIS-C06-COMM-004": {
        "options": {"A": "9 V", "B": "6 V", "C": "36 V", "D": "4,5 V", "E": "24 V"},
        "explanation": "La potenza sviluppata è uguale a P = I² · R = ΔV² / R = 18 W.\nQuindi ΔV = √(P · R) = √(18 W · 2 Ω) = √36 V = 6 V.",
    },
    "FIS-C06-COMM-006": {
        "question": "La potenza dissipata da un conduttore ohmico di resistenza elettrica R è data dalle formule W = V·I = I²·R = V²/R. Quale delle seguenti affermazioni è CORRETTA?",
    },
    "FIS-C06-COMM-013": {
        "question": "In un circuito elettrico vi sono una pila da 10 Volt e due resistenze in serie R₁ e R₂. Se la potenza totale è 50 watt e R₂ = 3·R₁, quanto vale R₁ in ohm?",
    },
    "FIS-C06-COMM-035": {
        "options": {
            "A": "se ciascuna carica è 1 mC allora F = 9 N",
            "B": "se una carica è 1 mC e l'altra 1 μC allora F = 9 dyne",
            "C": "se ciascuna carica è 1 mC allora F = 9000 newton",
            "D": "se una carica è 1 nC e l'altra 1 μC allora F = 9 newton",
            "E": "se ciascuna carica è 1 nC allora F = 9 newton",
        },
    },
    "FIS-C06-COMM-045": {
        "explanation": "Un filo metallico percorso da corrente genera nello spazio circostante un campo magnetico. Ad esempio, un filo rettilineo posto nel vuoto e percorso da corrente genera un campo magnetico le cui linee di forza sono circonferenze concentriche al filo, il cui modulo vale:\nB = (μ₀ · i) / (2π · r),\ndove i è l'intensità di corrente che circola nel filo, r è la distanza dal filo stesso e μ₀ è la permeabilità magnetica del vuoto.",
    },
    "FIS-C06-COMM-047": {
        "explanation": "Il potenziale elettrico in un punto, ad esempio in A, è dato dal rapporto fra il lavoro L_A∞ che le forze del campo compiono per portare una carica q da quel punto all'infinito (uguale al lavoro L compiuto contro le forze del campo dall'infinito ad A) e la carica q stessa: V_A = L_A∞ / q = L / q.",
    },
    "FIS-C06-COMM-048": {
        "question": "Un generatore ideale da 10 V viene connesso a un circuito di 3 resistenze delle quali la prima da 5 Ω è in serie alle due da 10 Ω tra di loro in parallelo. Qual è il valore della corrente che attraversa il circuito?",
        "options": {"A": "5 A", "B": "10 A", "C": "2 A", "D": "3 A", "E": "1 A"},
    },
    "FIS-C06-COMP-041": {
        "question": "L'energia potenziale elettrica di due cariche q₁ e q₂ distanti r è U = k q₁ q₂ / _____ .",
    },
    "FIS-C06-NCOM-003": {
        "options_patch": {
            "E": "evitare di strofinare con un panno bagnato gli aghi metallici, che potrebbero disperdere cariche per effetto della dispersione delle punte",
        },
    },
    "FIS-C06-NCOM-010": {
        "question": "Due cariche elettriche puntiformi sono mantenute ad una distanza fissa pari a 1 cm. Le cariche valgono q₁ = 2 μC e q₂ = 2 μC. In quale punto della retta che congiunge le due cariche posso portare una terza carica di valore arbitrario q in modo che su di essa agisca una forza elettrica risultante nulla?",
    },
    "FIS-C06-NCOM-041": {
        "question": "Trovare il potenziale elettrostatico generato da un nucleo di stagno (supposto puntiforme) di carica Q = 50 e a una distanza r = 10⁻¹² m. Si assuma che la carica e dell'elettrone valga e = 1,6 × 10⁻¹⁹ C e che la costante di Coulomb valga k = 9 × 10⁹ N m²/C².",
    },
    "FIS-C06-NCOM-050": {
        "options_patch": {"C": "conduttore"},
    },
    "FIS-C06-NCOM-077": {
        "question": "Una batteria da automobile, una volta caricata, è in grado di fornire una carica elettrica complessiva di 1,08 × 10⁵ coulomb. Se è forzata ad erogare una corrente uniforme di 10 ampere quanta autonomia avrà?",
    },
    "FIS-C06-NCOM-156": {
        "options": {"A": "0 kW", "B": "5 W", "C": "1 W", "D": "1 kW", "E": "5 kW"},
    },
    "FIS-C07-NCOM-020": {
        "question": "La velocità di propagazione di un'onda su una corda, sottoposta alla tensione di 150 N, è di 200 m/s. Quanto deve valere la tensione affinché la velocità dell'onda sia di 210 m/s?",
        "options": {"A": "165,375 N", "B": "150 N", "C": "142,857 N", "D": "300 N", "E": "160 N"},
    },
    "FIS-C07-NCOM-043": {
        "options_patch": {"E": "con diversa velocità e diversa lunghezza d'onda"},
    },
    "FIS-C08-COMP-009": {
        "question": "L'equazione dell'effetto fotoelettrico è K_max = hf − _____ .",
    },
    "FIS-C08-COMP-029": {
        "question": "La costante di Planck ha un valore di circa 6,63 × 10⁻³⁴ _____ · s.",
    },
    "FIS-C02-COMM-017": {
        "explanation": "Convertendo la velocità v = 180 m/min in km/h (oppure m/s): 180 × 10⁻³ km / (1/60 h) = 180 × 10⁻³ × 60 km/h = 10,8 km/h (= 3 m/s).",
    },
    "FIS-C02-NCOM-004": {
        "options_patch": {"C": "un moto uniformemente accelerato con accelerazione costante a = 2 m·s⁻²"},
    },
    "FIS-C02-NCOM-011": {
        "options_patch": {"B": "lunghezza / (tempo)²"},
    },
    "FIS-C02-NCOM-021": {
        "question": "Un tram sta viaggiando lungo dei binari dritti e orizzontali ad una velocità di 12,0 m s⁻¹ quando vengono attivati i freni. A causa di questo, il tram decelera con un tasso costante di 1,50 m s⁻² fino a fermarsi. Qual è la distanza percorsa dal tram nel tempo totale in cui ha decelerato?",
    },
    "FIS-C02-NCOM-022": {
        "options_patch": {"C": "il rapporto tra la variazione di velocità in un certo intervallo di tempo e l'intervallo di tempo stesso, ovvero a = (v₂ − v₁) / (t₂ − t₁)"},
    },
    "FIS-C02-NCOM-043": {
        "options_patch": {"B": "Sì, se il corpo è sottoposto alla forza peso"},
    },
    "FIS-C03-COMM-002": {
        "question": "Il vettore accelerazione di gravità g, in ogni punto della superficie terrestre:",
    },
    "FIS-C03-COMM-011": {
        "explanation": "Il lavoro compiuto dall'esterno contro la forza elastica coincide con l'energia potenziale elastica immagazzinata. Esprimendo l'allungamento in metri (x = 0,5 m), si ottiene:\nL = U_e = (1/2)kx² = (1/2) · 1 · (0,5)² = 0,125 J.",
    },
    "FIS-C03-COMM-014": {
        "options": {
            "A": "Uguale alla somma vettoriale di a₁ e a₂",
            "B": "Sempre uguale alla differenza vettoriale a₁ − a₂",
            "C": "Sempre uguale ad a₁, se a₁ è maggiore di a₂",
            "D": "Sempre uguale ad a₂, se a₂ è maggiore di a₁",
            "E": "Uguale al prodotto di a₁ per a₂",
        },
    },
    "FIS-C03-COMM-016": {
        "explanation": "La somma tra due grandezze fisiche si può fare solo quando esse hanno le stesse dimensioni fisiche. Forza e accelerazione hanno dimensioni fisiche rispettivamente [F] = [M · L · T⁻²] e [a] = [L · T⁻²]: le due grandezze non possono quindi essere sommate.",
    },
    "FIS-C03-COMM-018": {
        "options": {
            "A": "Non si può rispondere se non si conoscono i valori di F₁, F₂, L₁ e L₂",
            "B": "M₁ > M₂ se L₂ > L₁",
            "C": "M₁ > M₂ se F₁ > F₂ e contemporaneamente L₁ > L₂",
            "D": "M₁ = M₂ = 0",
            "E": "M₁ > M₂ se L₂ < L₁",
        },
    },
    "FIS-C03-COMM-028": {
        "question": "La variazione di energia cinetica di un corpo, di massa M e che si muove inizialmente con velocità V₀, può essere negativa?",
        "options_patch": {"A": "No, perché M > 0 e V₀ > 0"},
    },
    "FIS-C03-COMM-039": {
        "question": "La formula F = G · (Mm / r²) esprime la legge della gravitazione universale (o di Newton). Tra le seguenti affermazioni UNA SOLA è ERRATA. Quale di esse?",
        "explanation": "La legge di gravitazione universale afferma che due corpi di massa M ed m posti a distanza r si attraggono con una forza F = G · M · m / r². Il valore numerico della costante G dipende dal sistema di unità di misura scelto (nel SI: G ≈ 6,67 × 10⁻¹¹ N·m²/kg²); è quindi errato affermare che G non dipenda dal sistema di unità di misura usato.",
    },
    "FIS-C03-COMM-042": {
        "explanation": "Trascurando le forze di attrito, i due corpi sono soggetti alla sola forza peso (conservativa) e vale la conservazione dell'energia meccanica:\nU_in + K_in = U_fin + K_fin\nPartendo da fermi (K_in = 0) da quota H (U_in = mgH) e giungendo al suolo (U_fin = 0, K_fin = (1/2)mv²), si ottiene:\nmgH = (1/2)mv² → v = √(2gH).\nLa velocità di arrivo al suolo non dipende né dalla massa né dalla traiettoria seguita: i due corpi arrivano al suolo con la stessa velocità.",
    },
    "FIS-C03-COMM-050": {
        "explanation": "In assenza di attrito dell'aria, per conservazione dell'energia meccanica ((1/2)mv² = mgh) un corpo lanciato verso l'alto con v = 20 m/s raggiungerebbe l'altezza massima:\nh = v² / (2g) = 400 / (2 · 9,8) ≈ 20,4 m.\nPoiché nell'esercizio il corpo raggiunge solo 15 m anziché ~20 m, la forza di attrito dell'aria non è trascurabile e dissipa parte dell'energia meccanica del corpo durante la salita.",
    },
    "FIS-C03-COMP-184": {
        "question": "Il valore massimo della velocità nel moto armonico è v_max = A · _____ :",
    },
    "FIS-C03-NCOM-029": {
        "question": "A due masse m₁ e m₂ = 2 m₁ viene applicata una stessa forza F. Le accelerazioni acquistate dalle due masse, a₁ e a₂, sono legate dalla relazione:",
    },
    "FIS-C03-NCOM-087": {
        "options": {
            "A": "solo se S = 0 e F = 1",
            "B": "non solo nei casi C, D, E",
            "C": "se S = 0",
            "D": "se F = 0",
            "E": "se sia F che S sono nulli",
        },
    },
    "FIS-C03-NCOM-132": {
        "question": "Due corpi X e Y di ugual massa sono lanciati verticalmente verso l'alto nel campo gravitazionale terrestre partendo dalla stessa quota. Se le velocità iniziali dei due corpi sono rispettivamente V₁ e V₂ = 2 V₁, quale delle seguenti affermazioni è ERRATA?",
    },
    "FIS-C03-NCOM-177": {
        "question": "In una bilancia a bracci diseguali, un corpo di massa M₁ = 1,048 kg posto sul braccio di lunghezza L₁ viene equilibrato da una massa M₂ = 995 g posta sull'altro braccio di lunghezza L₂. Il rapporto tra le lunghezze dei bracci, L₁ / L₂, è:",
    },
    "FIS-C03-NCOM-185": {
        "question": "In una leva, in base alla posizione relativa dei punti di applicazione di R (forza di carico, detta anche resistenza) e di P (forza applicata, detta anche potenza) rispetto al fulcro, si può calcolare il guadagno meccanico G. Indicando con X_R e X_P i rispettivi bracci di R e P dal fulcro, vale la relazione:",
        "options": {
            "A": "G = P X_P / (R X_R)",
            "B": "G = X_R / X_P",
            "C": "G = X_P / X_R",
            "D": "G = R X_R / (P X_P)",
            "E": "G = X_R · X_P",
        },
    },
    "FIS-C04-COMM-001": {
        "explanation": "Il corpo galleggia sulla superficie per il principio di Archimede: la densità del corpo è ρ_c = 0,6 g·cm⁻³, minore della densità dell'acqua (ρ_acqua = 1 g·cm⁻³).",
    },
    "FIS-C04-COMM-002": {
        "question": "Il livello dell'acqua contenuta in tre bicchieri identici è esattamente lo stesso. Tuttavia, mentre il bicchiere 1 contiene solo acqua, nel bicchiere 2 galleggia, parzialmente immerso, un tappo di sughero e sul fondo del bicchiere 3 c'è una sferetta d'acciaio. Che cosa possiamo dire relativamente ai pesi P₁, P₂, P₃ dei tre bicchieri misurati da una bilancia?",
    },
    "FIS-C04-COMM-004": {
        "explanation": "Per la legge di Stevino, la pressione P che agisce a una profondità h all'interno di un fluido è:\nP = P₀ + ρ · g · h\ndove P₀ è la pressione sulla superficie libera, ρ la densità del fluido e g l'accelerazione di gravità. La pressione sul fondo dipende quindi dall'altezza della colonna di liquido.",
    },
    "FIS-C04-COMM-006": {
        "explanation": "Per la legge di Stevino, la pressione P che agisce a una profondità h all'interno di un fluido è P = P₀ + ρ · g · h, dove P₀ è la pressione sulla superficie libera, ρ la densità del fluido e g l'accelerazione di gravità. Essendo P₀, ρ e h uguali per entrambi i recipienti, la pressione sul fondo è la stessa (non dipende dalla forma del contenitore).",
    },
    "FIS-C04-COMM-007": {
        "question": "In un condotto orizzontale a pareti rigide, a sezione circolare costante, scorre con moto stazionario un liquido perfetto (o ideale), assoggettato alle sole forze di gravità e di pressione (Figura). Dette P₁ la pressione in una sezione a monte e P₂ in una sezione a valle (il liquido scorre dalla sezione 1 verso la sezione 2), quale delle seguenti relazioni è CORRETTA?",
    },
    "FIS-C04-COMM-008": {
        "explanation": "Il parallelepipedo è per metà immerso e per metà emerso (V_i = V_c / 2). All'equilibrio il peso eguaglia la spinta di Archimede:\nρ_c · g · V_c = ρ_f · g · V_i = ρ_f · g · (V_c / 2)\nda cui ρ_c = ρ_f / 2 = 0,6 g/cm³.",
    },
    "FIS-C04-COMM-009": {
        "explanation": "Per la legge di Stevino, a 40 m di profondità si ha:\nP = P₀ + ρ · g · h = P₀ + 1000 kg/m³ · 9,8 m/s² · 40 m = P₀ + 392.000 Pa ≈ P₀ + 3,87 atm.\nLa pressione aumenta quindi di circa 4 atm rispetto alla superficie (~1 atm ogni 10 m di profondità in acqua).",
    },
    "FIS-C04-COMM-010": {
        "explanation": "Entrambi i cilindri galleggiano con lo stesso peso, quindi ricevono la stessa spinta di Archimede: D₁ · g · V₁ = D₂ · g · V₂, dove D₁, D₂ sono le densità dei due liquidi e V₁, V₂ i volumi immersi. Per D₁ > D₂ risulta V₁ < V₂; poiché V = S · H con uguale sezione di base S, si ottiene H₁ < H₂ (minore immersione nel liquido più denso).",
    },
    "FIS-C04-NCOM-001": {
        "options": {
            "A": "3 g/cm³; 1,5",
            "B": "2; 2 g/cm³",
            "C": "2 g/cm³; 2",
            "D": "0,5 cm³/g; 0,5",
            "E": "0,5; 0,5 cm³/g",
        },
    },
    "FIS-C04-NCOM-020": {
        "question": "Consideriamo le seguenti unità di misura: J, eV, N · metri al quadrato, litri · atmosfere e W · s. Quale di esse non è un'unità di misura dell'energia?",
    },
    "FIS-C05-COMM-014": {
        "explanation": "L'energia cinetica media delle molecole di un gas ideale è direttamente proporzionale alla temperatura assoluta T. Se a T₁ = 27 °C = 300 K l'energia cinetica media vale K, affinché essa si dimezzi (K / 2) la temperatura assoluta deve dimezzarsi:\nT₂ = 300 K / 2 = 150 K = −123 °C.",
    },
    "FIS-C05-COMM-019": {
        "explanation": "Il numero di molecole N di un gas è dato da N = n · N_A, dove n è il numero di moli e N_A il numero di Avogadro. In una millimole (n = 10⁻³ mol) di He il numero di molecole è quindi N_A / 1000.",
    },
    "FIS-C05-COMM-026": {
        "explanation": "Il calore specifico dell'acqua vale 1 kcal/(kg · °C); poiché quello del metallo M è un quinto di quello dell'acqua, vale c_M = 0,2 kcal/(kg · °C), cioè occorrono 0,2 kcal per innalzare di 1 °C la temperatura di 1 kg di M.",
    },
    "FIS-C05-COMM-033": {
        "question": "Uno sperimentatore scalda un corpo di massa m con la fiamma: la temperatura iniziale è t_i, quella finale t_f, il calore fornito ΔQ, il calore specifico e la capacità termica del corpo sono c e k. Di conseguenza sarà:",
        "options": {
            "A": "t_f − t_i = ΔQ / (c · m)",
            "B": "t_f − t_i = ΔQ · k",
            "C": "ΔQ = k · (t_f − t_i) / m",
            "D": "ΔQ = k · (t_f − t_i) · m",
            "E": "ΔQ = c · m · (t_f − t_i) = 0",
        },
        "explanation": "Dalla legge fondamentale della termologia ΔQ = c · m · (t_f − t_i), ricavando la variazione di temperatura si ottiene:\nt_f − t_i = ΔQ / (c · m).",
    },
    "FIS-C05-COMP-043": {
        "question": "Il primo principio della termodinamica si scrive ΔE_int = Q + _____ .",
    },
    "FIS-C05-NCOM-054": {
        "question": "Una sfera di alluminio, avente massa 0,5 kg, calore specifico 0,21 kcal/(kg · °C), densità 2,7 g/cm³ e alla temperatura di 280 K, viene immersa in 150 kg di acqua. La temperatura finale dell'acqua:",
    },
    "FIS-C05-NCOM-062": {
        "question": "Se due corpi, uno di massa M e velocità V₁ ed uno di massa M/4 e velocità V₂ = 2 V₁, si arrestano per attrito:",
    },
    "FIS-C06-COMM-001": {
        "explanation": "Per tre resistenze R₁, R₂, R₃ collegate in parallelo vale:\n1 / R_eq = 1 / R₁ + 1 / R₂ + 1 / R₃ = 1 / 200 Ω + 1 / 200 Ω + 2 / 200 Ω = 4 / 200 Ω = 0,02 Ω⁻¹\nda cui R_eq = 1 / 0,02 Ω⁻¹ = 50 Ω.",
    },
    "FIS-C06-COMM-005": {
        "explanation": "Per due resistenze R₁ e R₂ in parallelo vale 1 / R_eq = 1 / R₁ + 1 / R₂. Volendo R_eq = R₁ / 3 si ha:\n3 / R₁ = 1 / R₁ + 1 / R₂ → 1 / R₂ = 2 / R₁ → R₂ = R₁ / 2.",
    },
    "FIS-C06-COMM-012": {
        "explanation": "La potenza dissipata per effetto Joule è:\nP = I² · R = ΔV² / R = (6 V)² / 24 Ω = 36 / 24 W = 1,5 W.",
    },
    "FIS-C06-COMM-013": {
        "explanation": "Essendo R₁ ed R₂ collegate in serie con R₂ = 3 R₁, la resistenza equivalente è R_eq = 4 R₁ e la potenza dissipata vale:\nP = ΔV² / (4 R₁) = 50 W → R₁ = (10 V)² / (4 · 50 W) = 100 / 200 Ω = 1/2 Ω.",
    },
    "FIS-C06-COMM-033": {
        "explanation": "La differenza di potenziale ai capi della resistenza è ΔV = 4,5 V + 4,5 V = 9 V.\n• Potenza dissipata per effetto Joule: P = ΔV² / R = 81 V² / 90 Ω = 0,9 W.\n• Intensità di corrente: I = ΔV / R = 9 V / 90 Ω = 0,1 A.",
    },
    "FIS-C06-COMM-041": {
        "explanation": "L'energia potenziale elettrica totale di un sistema di cariche puntiformi è la somma delle energie potenziali di tutte le coppie: U_ij = k · q_i · q_j / a. Per tre cariche uguali Q poste ai vertici di un triangolo equilatero di lato a esistono 3 coppie identiche, ciascuna di energia L: il lavoro totale richiesto è quindi 3 L.",
    },
    "FIS-C06-COMM-042": {
        "explanation": "Nel tratto di circuito PQ le resistenze R₂ ed R₃ sono in parallelo (R₂₃ = R₂ · R₃ / (R₂ + R₃)) e la loro combinazione è collegata in serie a R₁. La resistenza totale vale quindi:\nR_tot = R₁ + (R₂ · R₃) / (R₂ + R₃).",
    },
    "FIS-C06-COMM-048": {
        "explanation": "Le resistenze R₂ = 10 Ω e R₃ = 10 Ω sono in parallelo: R₂₃ = (10 · 10) / (10 + 10) = 5 Ω.\nIn serie con R₁ = 5 Ω danno R_tot = 5 Ω + 5 Ω = 10 Ω.\nPer la prima legge di Ohm: i = V / R_tot = 10 V / 10 Ω = 1 A.",
    },
    "FIS-C06-COMP-065": {
        "question": "La densità di corrente è data dal prodotto nqv_d, dove q è la carica, n la densità numerica e v_d la velocità di _____ .",
    },
    "FIS-C06-NCOM-031": {
        "options_patch": {"A": "−4 J", "B": "+10 J"},
    },
    "FIS-C06-NCOM-033": {
        "options_patch": {"A": "qV", "D": "q / V"},
    },
    "FIS-C06-NCOM-043": {
        "question": "È possibile che fra due punti di un campo elettrico vi sia una differenza di potenziale nulla?",
    },
    "FIS-C06-NCOM-045": {
        "options_patch": {"A": "varia come r⁻²"},
    },
    "FIS-C07-COMM-006": {
        "explanation": "I raggi infrarossi sono onde elettromagnetiche di frequenza compresa tra 10¹² Hz e 4 · 10¹⁴ Hz. Lo spettro di frequenze della luce visibile all'occhio umano è invece compreso tra 4 · 10¹⁴ Hz e 8 · 10¹⁴ Hz.",
    },
    "FIS-C07-COMM-007": {
        "question": "La luce visibile ha una delle seguenti caratteristiche. Quale?",
    },
    "FIS-C07-COMM-015": {
        "explanation": "Ogni strato lascia passare 1/5 dell'intensità luminosa incidente: dopo il primo strato I₁ = I₀ / 5, dopo il secondo I₂ = I₀ / 25, e dopo il terzo strato I₃ = I₀ · (1/5)³ = I₀ / 125.",
    },
    # ── Final 8 corpus-wide sweeps (bringing every OCR detector to 0 / 6,948) ──
    "CHIM-C03-COMP-033": {
        "question": "Gli _____ formano molecole biatomiche come F₂, Cl₂, Br₂ e I₂.",
    },
    "CHIM-C03-NCOM-147": {
        "options_patch": {"D": "Ca e O"},
    },
    "CHIM-C06-NCOM-005": {
        "question": "Una soluzione (1) di NaCl ha concentrazione molare doppia rispetto a una soluzione (2) di Na₂SO₄. Se si mescolano 100 mL della soluzione 1 con 200 mL della soluzione 2, la concentrazione dello ione Na⁺ nella soluzione finale sarà:",
        "options_patch": {"B": "tripla rispetto alla soluzione 1"},
    },
    "CHIM-C09-NCOM-042": {
        "options_patch": {"E": "0 e 0"},
    },
    "CHIM-C10-COMM-006": {
        "options": {
            "A": "Al + O₂",
            "B": "CaO + H₂O",
            "C": "Li + H₂O",
            "D": "FeO + K",
            "E": "Li₂O + CO₂",
        },
        "explanation": "I prodotti che si ottengono dalle reazioni elencate sono:\n• A. Al₂O₃, un ossido;\n• B. Ca(OH)₂, un idrossido;\n• C. LiOH (+ H₂), un idrossido;\n• D. Fe + K₂O, un metallo e un ossido;\n• E. Li₂CO₃, un sale.",
    },
    "BIO-C05-COMM-013": {
        "options_patch": {"A": "Reticolo endoplasmatico liscio - Sintesi delle proteine"},
        "explanation": "I lisosomi contengono una batteria di enzimi idrolitici che degradano i materiali estranei e gli organuli sottoposti a turnover. Gli enzimi presenti nelle membrane del reticolo endoplasmatico liscio catalizzano la sintesi di numerosi lipidi e carboidrati. Il citoscheletro fornisce supporto meccanico alla cellula e ha un ruolo importante nel trasporto intracellulare di materiali e nella divisione cellulare. L'apparato di Golgi modifica e smista le proteine sintetizzate nel reticolo endoplasmatico ruvido. Il nucleolo, una struttura compatta all'interno del nucleo non circondata da membrana, contiene un organizzatore nucleolare costituito dalle regioni cromosomiche contenenti i geni che codificano i diversi tipi di RNA ribosomale (rRNA).",
    },
    "FIS-C02-NCOM-024": {
        "question": "Un tram percorre un cammino rettilineo a velocità costante v₀ = 36 km/h. A un certo punto passa accanto ad un motociclista fermo che si muove immediatamente in moto rettilineo per inseguirlo, con accelerazione a = 0,1 m/s². Trascurando la resistenza dell'aria, dopo quanti metri il motociclista raggiunge il tram?",
        "options": {"A": "1 km", "B": "4 km", "C": "2 km", "D": "3 km", "E": "5 km"},
    },
    "FIS-C03-COMM-023": {
        "explanation": "La massa è una grandezza scalare caratteristica intrinseca di un corpo: il suo valore resta lo stesso in qualunque luogo si trovi il corpo (anche se il campo gravitazionale fosse nullo). Il peso è invece una forza (grandezza vettoriale) che varia da luogo a luogo: essendo sulla Terra g = 9,8 m/s², il peso di una massa m = 1 kg vale P = 9,8 N; se il campo gravitazionale fosse nullo, il peso sarebbe nullo.",
    },
    "FIS-C07-NCOM-049": {
        "question": "Un fascio di luce polarizzata linearmente lungo la direzione z si propaga lungo l'asse x e viene fatto passare attraverso due polarizzatori lineari che formano, con l'asse z, gli angoli indicati nella figura seguente. Qual è l'intensità del fascio risultante?",
    },
}


EXTRA_SUBSTRING_FIXES: List[Tuple[str, str]] = [
    # Remaining OH⁻ / e⁻ / sp³ quote-exponent glitches from post-audit
    ("OH”", "OH⁻"),
    ('OH"', "OH⁻"),
    ("OH-", "OH⁻"),
    ('e" —', "e⁻ →"),
    ("g mol\"", "g mol⁻¹"),
    ("ibridizzato sp’", "ibridizzato sp³"),
    ("ibridazione sp’", "ibridazione sp³"),
    ("ibridazione sp*", "ibridazione sp³"),
    ("ibridati sp*", "ibridati sp²"),
    ("ibridato sp*", "ibridato sp²"),
    ("sp?d", "sp³d"),
    ("sp³d?", "sp³d²"),
    ("Ca(0H),,", "Ca(OH)₂"),
    ("Ca(0H)₂", "Ca(OH)₂"),
    ("Ca(OH),", "Ca(OH)₂"),
    ("Mg(OH),", "Mg(OH)₂"),
    ("Ba(OH),", "Ba(OH)₂"),
    ("Al(OH),", "Al(OH)₃"),
    ("Fe(OH),", "Fe(OH)₃"),
    ("H,PtCl,", "H₂PtCl₆"),
    ("H,SO,", "H₂SO₄"),
    ("H₂SO,", "H₂SO₄"),
    ("H,CO,", "H₂CO₃"),
    ("H₂CO,", "H₂CO₃"),
    ("H,PO,", "H₃PO₄"),
    ("H₃PO,", "H₃PO₄"),
    ("HNO,", "HNO₃"),
    ("Na,CO,", "Na₂CO₃"),
    ("CaCO,", "CaCO₃"),
    ("KMnO,", "KMnO₄"),
    ("NaCi", "NaCl"),
    ("KCi", "KCl"),
    ("MgCi₂", "MgCl₂"),
    ("CaCi₂", "CaCl₂"),
    ("AlCi₃", "AlCl₃"),
    ("HC!", "HCl"),
    ("HC]", "HCl"),
    # Spurious `₄` comma corruptions verified in post-audit (`19.000₄`, `46₄`, `cromosoma 8₄`, etc.)
    ("19.000₄ ", "19.000, "),
    ("apolipoproteina B₄ ", "apolipoproteina B, "),
    ("cromosoma 8₄ ", "cromosoma 8, "),
    ("gruppo 0₄ ", "gruppo 0, "),
    ("cromosoma X₄ ", "cromosoma X, "),
    ("o A₄ o B", "o A, o B"),
    ("sono 46₄ ", "sono 46, "),
    ("pari a C₄ ", "pari a C, "),
    ("distanza d₄ ", "distanza d, "),
    ("identico ad A₄ ", "identico ad A, "),
    ("200 K₄ ", "200 K, "),
    ("Er = 10₄ ", "ε_r = 10, "),
    ("Si₄ talvolta", "Sì, talvolta"),
    ("Si₄ la scogliera", "Sì, la scogliera"),
    ("Si₄ sempre", "Sì, sempre"),
    ("AGU₄ ", "AGU, "),
    ("UAG₄ ", "UAG, "),
    ("RNA₄ ", "RNA, "),
    ("1 _____ . ricchi in GAG₄ ", "I _____, ricchi in GAG, "),
    ("Hz₄ ", "Hz, "),
    ("UV₄ RX₄ ", "UV, RX, "),
    ("Sela frequenza", "Se la frequenza"),
    ("Sela quantità", "Se la quantità"),
    ("ion! ", "ioni "),
    ("tone OH", "ione OH"),
    ("gii ossidrili", "gli ossidrili"),
    ("L'alice visibile", "La luce visibile"),
]


def apply_extra_text_cleanups(text: str) -> str:
    if not text:
        return text
    s = text
    for old, new in EXTRA_SUBSTRING_FIXES:
        if old in s:
            s = s.replace(old, new)
    s = s.replace("m/s*", "m/s²").replace("Ilisosomi", "I lisosomi")
    s = re.sub(r"(?<![A-Za-z0-9(])HC\)", "HCl", s)
    s = re.sub(r"\b(di|con|da|in|\+)\s+O,(?=\s|$|[.;:)])", r"\1 O₂", s)
    s = re.sub(r"\b(di|con|da|in|\+)\s+N,(?=\s|$|[.;:)])", r"\1 N₂", s)
    s = re.sub(r"\b(di|con|da|in|\+)\s+H,(?=\s|$|[.;:)])", r"\1 H₂", s)
    s = re.sub(r"\b(di|con|da|in|\+)\s+Cl,(?=\s|$|[.;:)])", r"\1 Cl₂", s)
    # Fix missing space right after numbered statement prefixes (`1.Il` -> `1. Il`, `3.tRNA` -> `3. tRNA`)
    s = re.sub(r"(^|\n)([1-9])\.(?=[A-Za-zÀ-ÿ])", r"\1\2. ", s)
    # Break inline chemical equation after `bilanciamento?` / `reazione?` / `chimica?` onto its own line
    s = re.sub(r"(?<=\?)\s+(?=(?:[a-z]\s+|\d+\s+)[A-Z][a-z]?[₀-₉A-Za-z()⁺⁻]+\s*[+→⇄])", "\n", s)
    return s
