"""Visually verified scan overrides across Chimica, Biologia e Genetica, and Fisica.

Every override in this module was verified directly against the original 300-DPI
textbook bitmap scan to eliminate OCR subscript/superscript/charge/symbol misreads,
running-header bleeds, watermark fragments, and glued/corrupted Italian words.
"""

from __future__ import annotations

from typing import Any, Dict

EXTRA_SCAN_VERIFIED_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "BIO-C06-COMM-023": {
        "options": {
            "A": "Usa la circolazione sanguigna",
            "B": "Agisce su cellule vicine",
            "C": "Avviene solo nelle cellule nervose",
            "D": "Richiede integrine",
            "E": "Implica canali ionici voltaggio-dipendenti",
        },
    },
    "BIO-C01-NCOM-053": {"options": {"E": "millimetro"}},
    "BIO-C01-NCOM-199": {"options": {"D": "accoppiamento complementare fra timina (T) e guanina (G)"}},
    "BIO-C03-COMM-024": {
        "explanation": "La duplicazione del DNA è semiconservativa, ovvero da una elica di DNA se ne ottengono due, ciascuna formata da un filamento di origine parentale e uno neosintetizzato. Il batterio E. coli cresciuto in terreno con ¹⁵N avrà DNA composto da due filamenti contenenti entrambi solo ¹⁵N. Se questo batterio viene messo in un terreno contenente solo ¹⁴N, alla prima generazione (ovvero dopo una duplicazione del DNA) il DNA sarà composto da un filamento parentale contenente ¹⁵N e uno neosintetizzato contenente ¹⁴N, quindi avremo 50% ¹⁵N e 50% ¹⁴N. Nel passaggio alla seconda generazione queste molecole di DNA ibride andranno incontro a duplicazione: si formeranno di nuovo due molecole di DNA a partire da una; una molecola sarà costituita dal filamento parentale con ¹⁵N e da uno neosintetizzato con ¹⁴N, l'altra sarà invece formata da due filamenti entrambi con ¹⁴N. La percentuale di DNA composto da un'elica pesante e una leggera dopo due generazioni sarà quindi 50%.",
    },
    "BIO-C03-COMM-029": {
        "explanation": "In E. coli la proteina DnaA riconosce l'oriC e destabilizza la doppia elica, favorendo l'apertura della zona ricca in basi A-T.",
    },
    "BIO-C03-COMM-035": {
        "explanation": "L'operone lac è un classico esempio di regolazione inducibile in E. coli: in presenza di lattosio e bassa concentrazione di glucosio, il repressore viene inattivato e CAP attiva la trascrizione.",
    },
    "BIO-C03-NCOM-138": {"options": {"B": "DNA polimerasi ε"}},
    "BIO-C03-NCOM-141": {"options": {"A": "DNA polimerasi ε"}},
    "BIO-C03-COMP-003": {
        "question": "La proteina _____ riconosce la sequenza oriC in E. coli, destabilizza la doppia elica e permette l'apertura iniziale.",
    },
    "BIO-C04-COMM-061": {
        "explanation": "I gruppi sanguigni ABO sono controllati da tre alleli di un singolo locus, che mostrano codominanza. Gli individui con genotipo IᴬIᴬ o Iᴬi hanno il gruppo sanguigno A, quelli con genotipo IᴮIᴮ o Iᴮi il gruppo B, quelli con genotipo IᴬIᴮ il gruppo AB e quelli con genotipo ii il gruppo 0. Il fattore Rh è codificato da un gene che presenta due alleli con dominanza completa (Rh dominante e rh recessivo). Il genotipo della donna è ii rhrh e quello dell'uomo è IᴬIᴮ Rhrh. Per quanto riguarda il gruppo sanguigno, la loro progenie può avere genotipo Iᴬi (gruppo A) oppure Iᴮi (gruppo B); in merito al fattore Rh, la progenie può avere genotipo Rhrh (fenotipo Rh⁺) oppure rhrh (fenotipo Rh⁻).",
    },
    "BIO-C04-COMM-062": {
        "explanation": "Gli individui con antigene A (2527/6000) possono avere genotipo IᴬIᴬ, Iᴬi oppure IᴬIᴮ. Analogamente, gli individui che presentano l'antigene B (2234/6000) possono avere genotipo IᴮIᴮ, Iᴮi oppure IᴬIᴮ. Infine, gli individui che non hanno nessun antigene (1846/6000) hanno genotipo ii. Se sommiamo 2527 + 2234 + 1846 si ottiene 6607, valore superiore al numero di individui oggetto di studio (6000), poiché gli individui con genotipo IᴬIᴮ vengono contati due volte (sia fra gli individui con antigene A sia fra quelli con antigene B). Pertanto la differenza 6607 - 6000 = 607 corrisponde agli individui con genotipo IᴬIᴮ.",
    },
    "BIO-C04-COMM-063": {
        "explanation": "Gli individui di gruppo sanguigno 0 presentano genotipo omozigote recessivo ii. Gli individui di gruppo A possono presentare genotipo omozigote IᴬIᴬ oppure eterozigote Iᴬi; analogamente, gli individui di gruppo B possono presentare genotipo omozigote IᴮIᴮ oppure eterozigote Iᴮi. Nell'albero genealogico, i genitori con gruppo sanguigno A e B della seconda generazione sono entrambi eterozigoti, in quanto ciascuno eredita un allele recessivo i dal genitore di prima generazione di gruppo 0 (genotipo ii). L'incrocio della seconda generazione è quindi Iᴬi × Iᴮi, da cui possono nascere individui con genotipo Iᴬi, Iᴮi, IᴬIᴮ, ii e fenotipo A, B, AB, 0.",
    },
    "BIO-C04-COMM-064": {
        "explanation": "I gruppi sanguigni del sistema ABO sono determinati dalla presenza di specifici antigeni sulla superficie degli eritrociti: l'allele Iᴬ codifica l'antigene A, l'allele Iᴮ l'antigene B e l'allele i nessun antigene. Gli alleli Iᴬ e Iᴮ sono codominanti e l'allele i è recessivo; pertanto, gli individui con genotipo IᴬIᴬ o Iᴬi sono di gruppo A, quelli con genotipo IᴮIᴮ o Iᴮi di gruppo B, quelli con genotipo IᴬIᴮ di gruppo AB e quelli con genotipo ii di gruppo 0. Un bambino di gruppo AB deve aver ricevuto l'allele Iᴬ da un genitore e l'allele Iᴮ dall'altro, per cui sua madre non può avere gruppo sanguigno 0 (genotipo ii).",
    },
    "BIO-C04-COMM-074": {
        "explanation": "Un individuo con gruppo sanguigno A può avere genotipo IᴬIᴬ o Iᴬi (dove i è l'allele recessivo), mentre un individuo con gruppo sanguigno 0 ha genotipo ii. Nel caso in esame, la donna trasmetterà sempre ai figli un allele i, mentre l'uomo trasmetterà con uguale probabilità (50%) l'allele Iᴬ o l'allele i. I figli avranno quindi come genotipi possibili Iᴬi o ii e come fenotipi gruppo A o gruppo 0. La risposta D non è corretta poiché ogni singolo concepimento è un evento indipendente e non è detto che i figli siano necessariamente metà di gruppo A e metà di gruppo 0.",
    },
    "BIO-C05-COMM-021": {
        "question": "Il grafico riportato nella figura rappresenta le variazioni del potenziale di membrana di un neurone all'arrivo di uno stimolo. Il periodo refrattario è rappresentato dal segmento:",
    },
    "BIO-C05-NCOM-012": {"options": {"C": "è corretta solo la (1)"}},
    "BIO-C06-NCOM-122": {"options": {"E": "recettore del TGF-β"}},
    "BIO-C07-COMM-058": {"options": {"C": "Durante l'anafase II"}},
    "BIO-C07-NCOM-038": {"options": {"B": "Profase"}},
    "BIO-C07-NCOM-130": {"options": {"E": "Riproduzione asessuata"}},
    "CHIM-C01-NCOM-013": {"question": "Nella molecola H₄P₂O₇ sono presenti:"},
    "CHIM-C01-NCOM-016": {
        "question": "Quale delle seguenti molecole biatomiche NON si può formare?",
        "options": {"A": "CO", "B": "HS", "C": "F₂", "D": "CaO", "E": "HCl"},
    },
    "CHIM-C02-COMM-009": {
        "question": "Una molecola di ossigeno (massa atomica 16 u.m.a.) pesa:",
        "options": {"A": "2 × 16 g", "B": "16 u.m.a.", "C": "16 × 6,02 × 10²³ u.m.a.", "D": "16 g", "E": "2 × 16 u.m.a."},
        "explanation": "La molecola di ossigeno è biatomica (O₂), perciò la sua massa è il doppio di quella dell'atomo: 2 × 16 u (o u.m.a.).",
    },
    "CHIM-C02-COMM-022": {
        "explanation": "L'elemento ha 6 elettroni nello strato esterno (con n = 3), appartiene quindi al III periodo e al VI gruppo. Esso cade nella zona dei non metalli.",
    },
    "CHIM-C02-COMM-031": {
        "explanation": "BF₃: la configurazione elettronica dell'atomo di boro è 1s²2s²2p¹. A seguito della promozione di un elettrone dall'orbitale 2s a quello 2p, si ottengono tre orbitali ibridi sp² e resta un orbitale 2p vuoto. Ciascun atomo di fluoro (1s²2s²2p⁵) forma un legame semplice con i tre orbitali sp² del boro; l'atomo di boro non rispetta la regola dell'ottetto perché è circondato solo da tre coppie di elettroni. PF₅: la configurazione elettronica del fosforo è [Ne] 3s²3p³; promuovendo un elettrone 3s a 3d si ottengono cinque orbitali ibridi sp³d e il fosforo espande l'ottetto con cinque coppie di elettroni. NO: l'azoto (1s²2s²2p³) si trova con soli sette elettroni intorno a sé (specie radicalica). BrO₂: il bromo ([Ar] 3d¹⁰4s²4p⁵) espande l'ottetto trovandosi con undici elettroni intorno a sé. NF₃: l'azoto (ibridizzato sp³) forma tre legami semplici con i tre atomi di fluoro e conserva un doppietto solitario: nella molecola NF₃ sia l'atomo di azoto sia ciascun atomo di fluoro sono circondati da otto elettroni.",
    },
    "CHIM-C02-COMM-036": {
        "explanation": "I numeri quantici definiscono la probabilità di trovare un elettrone in una regione dello spazio (orbitale). Il numero quantico principale (n) può assumere valori interi positivi (1, 2, 3, ...). Il numero quantico secondario o angolare (l) definisce la forma dell'orbitale e può assumere valori interi da 0 a n - 1 (pertanto le opzioni con n = 2, l = 3 sono errate). Il numero quantico magnetico (m) definisce l'orientamento nello spazio dell'orbitale e assume valori interi compresi tra -l e +l (pertanto le opzioni con m = 4 o valori frazionari sono errate). Il numero quantico di spin (m_s) assume solo i valori -1/2 e +1/2 (pertanto m_s = 0 è errato).",
    },
    "CHIM-C02-NCOM-002": {"question": "Cosa si intende con il termine orbitale?"},
    "CHIM-C02-NCOM-013": {"options": {"D": "i numeri quantici principale e secondario"}},
    "CHIM-C02-NCOM-014": {"options": {"A": "o frazionari da 0 fino a 8", "D": "o frazionari da 0 fino a infinito"}},
    "CHIM-C02-NCOM-015": {
        "options": {
            "A": "n = 2; l = 5; m_l = 1",
            "B": "n = 2; l = 3; m_l = 1",
            "C": "n = 3; l = 3; m_l = 3",
            "D": "n = 3; l = 2; m_l = 1",
            "E": "n = 3; l = 2; m_l = 3",
        },
    },
    "CHIM-C02-NCOM-022": {"options": {"E": "può essere positivo o negativo"}},
    "CHIM-C02-NCOM-036": {"question": "Il numero massimo di elettroni che può essere contenuto in totale nei primi 3 livelli elettronici è:"},
    "CHIM-C02-COMP-036": {"question": "Il modello di _____ fu il primo a descrivere la materia come composta da atomi indivisibili."},
    "CHIM-C03-COMM-001": {"question": "Una sola delle seguenti affermazioni è ERRATA. Quale? Gli elementi F, Cl, Br e I:"},
    "CHIM-C03-COMM-019": {
        "options": {"A": "F, O, N, C", "B": "O, N, C, F", "C": "C, N, O, F", "D": "C, O, N, F", "E": "F, O, C, N"},
        "explanation": "Il potenziale di prima ionizzazione cresce, nell'ambito di uno stesso periodo, in linea di massima da sinistra a destra al diminuire del raggio atomico. Tuttavia si hanno anomalie per gli elementi con sottolivello s completo (Be e Mg) o con sottolivello p riempito a metà (N e P), che presentano un massimo relativo di energia di ionizzazione rispetto all'elemento successivo (quindi E_i(N) > E_i(O), dando l'ordine C < O < N < F).",
    },
    "CHIM-C03-COMM-024": {
        "options": {"B": "l'affinità elettronica di H (-73 kJ/mol) è più negativa di quella di Li (-60 kJ/mol), la quale a sua volta è più negativa di quella di Na (-53 kJ/mol)"},
    },
    "CHIM-C03-COMM-025": {
        "explanation": "L'argon è un gas nobile, si trova quindi sempre allo stato elementare. L'azoto si trova facilmente allo stato elementare come molecola biatomica (N₂). L'argento è un metallo nobile ed è possibile trovarlo anche allo stato elementare. Il carbonio in natura si trova come diamante o come grafite. Il sodio, invece, è un metallo alcalino così reattivo che non è possibile trovarlo in natura allo stato elementare.",
    },
    "CHIM-C03-NCOM-009": {
        "question": "I pesi atomici degli elementi H, P e O sono rispettivamente 1, 31 e 16 (u.m.a.). Il peso molecolare (espresso in u.m.a.) dell'acido ortofosforico (H₃PO₄) è:",
    },
    "CHIM-C03-NCOM-011": {
        "question": "Poiché i pesi atomici di H, S e O sono rispettivamente 1, 32 e 16 u.m.a., il peso molecolare espresso in u.m.a. dell'acido solforico vale:",
    },
    "CHIM-C03-NCOM-015": {
        "options": {
            "A": "Un numero di Avogadro di ⁶⁴Zn pesa 80,062 u.m.a.",
            "B": "Una mole di ⁶⁴Zn pesa 80,062 u.m.a.",
            "C": "Nessuna delle risposte è corretta",
            "D": "La massa molecolare di ⁶⁴Zn è 80,062 u.m.a.",
            "E": "La massa molare di ⁶⁴Zn è 80,062 u.m.a.",
        },
    },
    "CHIM-C03-NCOM-021": {
        "question": "In quale dei seguenti campioni sono contenute 3 · 6,02 · 10²³ molecole?",
        "options": {
            "A": "17 g di H₂S (MM = 34 u)",
            "B": "36 g di H₂O (MM = 18 u)",
            "C": "253 g di CHBr₃ (MM = 253 u)",
            "D": "234 g di AsH₃ (MM = 78 u)",
            "E": "66 g di CO₂ (MM = 44 u)",
        },
    },
    "CHIM-C03-NCOM-033": {
        "question": "Due palloni da 3 L, alla stessa temperatura e alla stessa pressione, contengono, rispettivamente, SO₂(g) e NH₃(g). Che cosa non è uguale nei due palloni?",
        "options": {"C": "Il numero delle moli"},
    },
    "CHIM-C03-NCOM-064": {
        "options": {
            "A": "Be, Mg, Ca, Sr, Ba",
            "B": "Fe, Co, Ni, Cr, Mn",
            "C": "Li, Na, K, Rb, Cs, Fr",
            "D": "Cu, Ag, Au, Zn, Pb",
            "E": "Cu, Al, Ni, Zn, Pb",
        },
    },
    "CHIM-C03-NCOM-068": {"options": {"D": "B = Bromo, C = Carbonio, Au = Oro"}},
    "CHIM-C03-NCOM-094": {
        "question": "La tabella sottostante mostra a quale gruppo della Tavola Periodica appartengono i singoli elementi [B: 13; H: 1; Br: 17; N: 15; C: 14; O: 16; F: 17; P: 15]. Quale delle seguenti molecole o ioni ha la stessa forma della fosfina (PH₃)?",
        "options": {"A": "BrF₅", "B": "CO₃²⁻", "C": "BF₃", "D": "H₃O⁺", "E": "NO₃⁻"},
    },
    "CHIM-C03-NCOM-133": {
        "question": "Si assuma che i valori delle prime sei energie di ionizzazione (espresse in kJ mol⁻¹) di un elemento siano: 738, 1450, 7730, 10500, 13600 e 18000. Quale/i delle seguenti affermazioni è/sono corretta/e? 1. L'elemento appartiene al Gruppo 2 della Tavola Periodica; 2. Il valore 7730 kJ mol⁻¹ corrisponde al processo: X²⁺(g) → X³⁺(g) + e⁻; 3. L'elemento appartiene al Periodo 2 della Tavola Periodica",
    },
    "CHIM-C03-NCOM-135": {
        "question": "L'elemento idrogeno ha tre diversi isotopi: ¹H, ²H e ³H. Il numero atomico dell'idrogeno è 1. Considerando un singolo atomo per ciascun isotopo, quale delle seguenti affermazioni è corretta?",
        "options": {
            "A": "³H ha il triplo dei protoni di ¹H",
            "B": "²H ha il doppio dei neutroni di ¹H",
            "C": "¹H ha la metà degli elettroni di ²H",
            "D": "³H ha un protone, un neutrone e un elettrone",
            "E": "³H ha il doppio dei neutroni di ²H",
        },
    },
    "CHIM-C03-NCOM-173": {
        "question": "Quale dei seguenti elementi, dei quali è indicato il numero atomico Z, è un elemento di transizione?",
        "options": {"A": "Ca (Z = 20)", "B": "Cu (Z = 29)", "C": "Cl (Z = 17)", "D": "Cs (Z = 55)", "E": "C (Z = 6)"},
    },
    "CHIM-C04-COMM-005": {
        "options": {"A": "AlCl₃, NH₃", "B": "NH₃, BH₃", "C": "NH₃, PH₃", "D": "Nessuna delle coppie elencate", "E": "BF₃, AlCl₃"},
        "explanation": "Sia il trifluoruro di boro (BF₃) che il tricloruro di alluminio (AlCl₃) presentano geometria trigonale planare secondo la teoria VSEPR, poiché i 3 legami formati dai 3 elettroni di valenza del boro e dell'alluminio con gli atomi di fluoro e di cloro si dispongono alla massima distanza possibile, con angoli di legame di 120°. L'azoto (N) e il fosforo (P) possiedono entrambi 5 elettroni di valenza; tuttavia NH₃ e PH₃ hanno geometria piramidale trigonale (derivata dalla tetraedrica) a causa della presenza di un doppietto elettronico solitario sull'atomo centrale.",
    },
    "CHIM-C04-COMM-016": {
        "explanation": "Nel brano si afferma che in soluzione acquosa tra lo ione Co³⁺ e 6 molecole d'acqua si formano legami più forti delle comuni interazioni ione-dipolo, simili a legami covalenti dativi. Il quesito richiede di individuare l'affermazione NON deducibile dal testo.",
    },
    "CHIM-C04-NCOM-005": {"question": "Il legame ionico è un legame:"},
    "CHIM-C04-NCOM-029": {"options": {"A": "C forma quattro legami e Cl solo due", "C": "Cl è più elettronegativo di C"}},
    "CHIM-C04-NCOM-055": {
        "options": {
            "A": "NH₃, H₂O, Ne",
            "B": "CO₂, CH₄, F₂",
            "C": "NO, HBr, LiOH",
            "D": "CO₂, BaCl₂, N₂",
            "E": "NaF, CCl₄, Al(OH)₃",
        },
    },
    "CHIM-C04-NCOM-060": {
        "question": "Individuare il solvente polare:",
        "options": {"A": "Etano", "B": "Olio", "C": "C₆H₆", "D": "Benzene", "E": "H₂O"},
    },
    "CHIM-C04-NCOM-062": {"options": {"A": "NF₃", "B": "BeF₂", "C": "CCl₄", "D": "PF₅", "E": "SF₆"}},
    "CHIM-C04-COMP-031": {"question": "Il _____ ha formula AlPO₄, risultante dall'unione di Al³⁺ e PO₄³⁻."},
    "CHIM-C05-COMM-004": {
        "explanation": "Il comportamento di un gas a temperatura costante (T = costante) è regolato dalla legge di Boyle: P·V = costante (ovvero V = cost./P). Il volume di un gas a temperatura costante è quindi inversamente proporzionale alla pressione: se si triplica il volume, la pressione diventa un terzo di quella iniziale.",
    },
    "CHIM-C05-COMM-005": {
        "options": {"C": "La temperatura critica rappresenta la temperatura al di sotto della quale il vapore non può essere mai portato allo stato liquido"},
        "explanation": "In un diagramma di stato pressione-temperatura, le curve rappresentano le condizioni di temperatura e pressione alle quali due fasi coesistono all'equilibrio. Dal diagramma di stato della CO₂ si deduce che l'equilibrio solido-aeriforme è possibile solo al di sotto del punto triplo (dove tutte e tre le fasi coesistono all'equilibrio). La temperatura critica è la temperatura al di sopra della quale il gas non può essere liquefatto per semplice compressione (~31 °C per la CO₂).",
    },
    "CHIM-C05-COMM-016": {"options": {"C": "dal volume occupato dal gas"}},
    "CHIM-C05-COMM-018": {
        "options": {"A": "16 atm", "B": "4 atm", "C": "1 atm", "D": "0,25 atm", "E": "0,64 atm"},
        "explanation": "Poiché la temperatura è costante (legge isoterma di Boyle), si applica la relazione P₁V₁ = P₂V₂, da cui: P₂ = (1 atm × 4 L) / 16 L = 0,25 atm.",
    },
    "CHIM-C05-COMM-020": {"options": {"A": "Una soluzione concentrata, in presenza del solvente puro, tende a diluirsi"}},
    "CHIM-C05-COMM-021": {
        "question": "Gli urti, che nei gas ideali vengono supposti come perfettamente elastici, determinano un continuo trasferimento di energia cinetica da una molecola all'altra; ne consegue che, in un determinato istante, le molecole non posseggono tutte lo stesso valore di energia cinetica. Mediante calcoli statistici è possibile dimostrare che i valori dell'energia cinetica in un sistema contenente un gran numero di molecole sono distribuiti intorno ad un valore medio E_m, dipendente esclusivamente dalla temperatura assoluta, a cui è direttamente proporzionale; la statistica dimostra che, se il numero di molecole del sistema è sufficientemente elevato, è del tutto lecito sostituire alla popolazione reale delle molecole con valori individuali dell'energia cinetica, una popolazione ideale in cui tutte le molecole posseggono il valore E_m. Quale delle seguenti informazioni NON può essere dedotta dalla lettura del brano precedente?",
        "options": {
            "A": "Il valore dell'energia cinetica media dipende dal numero delle molecole del sistema",
            "D": "Se la temperatura assoluta si raddoppia, si raddoppia anche il valore di E_m",
            "E": "Il valore dell'energia cinetica media non dipende dal volume del recipiente in cui è contenuto il gas",
        },
    },
    "CHIM-C05-COMM-025": {
        "explanation": "Come conseguenza del principio di Avogadro, nelle stesse condizioni di T e di P, una mole di qualsiasi gas ideale occupa lo stesso volume (22,4 L a 0 °C e 1 atm). Poiché la massa molare di CH₄ è 16 g/mol, 1 mole occupa 22,4 L e quindi 11,2 L (0,5 mol) hanno una massa di 8 g.",
    },
    "CHIM-C05-NCOM-002": {
        "options": {"A": "CO₂, CO₂", "B": "CO, CH₄", "C": "CCl₄, SO₂", "D": "I₂, I₂", "E": "SO₂, SO₂"},
    },
    "CHIM-C05-NCOM-005": {
        "question": "Date le tre coppie di sostanze indicate di seguito, si identifichi per ogni coppia quale sostanza presenta forze intermolecolari maggiori: 1. CH₄ e CBr₄; 2. N₂ e NO; 3. CH₃CH₂CH₂NH₂ e (CH₃)₃N [Si assumano temperatura e pressione standard (STP)]",
        "options": {
            "A": "1: CBr₄, 2: N₂, 3: (CH₃)₃N",
            "B": "1: CBr₄, 2: NO, 3: CH₃CH₂CH₂NH₂",
            "C": "1: CBr₄, 2: N₂, 3: CH₃CH₂CH₂NH₂",
            "D": "1: CH₄, 2: NO, 3: (CH₃)₃N",
            "E": "1: CH₄, 2: N₂, 3: (CH₃)₃N",
        },
    },
    "CHIM-C05-NCOM-009": {
        "options": {"A": "O₂, H₂", "B": "HCl, CHCl₃", "C": "H₂, H₂O", "D": "H₂Se, F₂", "E": "F₂, Cl₂"},
    },
    "CHIM-C05-NCOM-029": {
        "question": "Cosa potrebbe essere contenuto nei tre recipienti rappresentati in figura, a 15 °C e 1 atm?",
        "options": {
            "A": "In A Br₂ o HCl, in B NH₃, in C I₂",
            "B": "In A I₂ o Br₂, in B NH₃ o HCl",
            "C": "In A Br₂ o NH₃, in B HCl, in C I₂",
            "D": "In A Br₂ o I₂, in B NH₃, in C HCl",
            "E": "In A NH₃ o HCl, in B Br₂, in C I₂",
        },
    },
    "CHIM-C05-NCOM-032": {
        "options": {
            "C": "In acqua a 20 °C la solubilità di CO₂ è maggiore di quella di O₂",
            "E": "In acqua a 20 °C la solubilità di N₂ è minore di quella di O₂",
        },
    },
    "CHIM-C05-NCOM-044": {
        "question": "Quale delle seguenti sostanze si scioglie in acqua con notevole sviluppo di calore?",
        "options": {"A": "NaCl", "B": "HCN", "C": "KNO₃", "D": "H₂SO₄", "E": "SO₂"},
    },
    "CHIM-C06-COMM-004": {
        "question": "In 500 mL di una soluzione acquosa sono presenti 2 g di NaOH (p.m. = 40 u.m.a.); la concentrazione della soluzione è:",
        "options": {"A": "1 M", "B": "0,1 M", "C": "1 m", "D": "0,1 m", "E": "0,05 M"},
        "explanation": "La molarità di una soluzione è data dal numero di moli per litro di soluzione. Qui in 0,5 L di soluzione sono contenute 2 g / 40 g·mol⁻¹ (massa molare di NaOH) = 0,05 mol. Perciò in 1 L di soluzione sono contenute 0,05 mol / 0,5 L = 0,1 mol/L (0,1 M).",
    },
    "CHIM-C06-COMM-006": {
        "options": {
            "B": "dissolvendo 0,2 moli di glucosio in 2 L di acqua distillata",
            "D": "miscelando 0,4 moli di glucosio con 1 L di acqua distillata in un matraccio da 2 L, e portando successivamente a volume con acqua distillata",
        },
        "explanation": "0,4 moli di glucosio portate a un volume finale di 2 L di soluzione corrispondono a [glucosio] = 0,4 mol / 2 L = 0,2 M.",
    },
    "CHIM-C06-COMM-010": {
        "question": "Per elettroliti forti, in soluzione sufficientemente diluita (molalità: m < 10⁻²), la concentrazione attiva ai fini delle proprietà colligative è data dal prodotto della concentrazione analitica dell'elettrolita per l'indice di dissociazione ν, definito come il numero di ioni in cui una formula di elettrolita si dissocia (ad esempio, per NaCl si ha ν = 2). L'abbassamento crioscopico Δt_c di una soluzione acquosa 0,002 m di NaCl può essere calcolato dall'espressione Δt_c = K_c · 0,002 · 2, dove K_c = 1,86 °C·kg/mol è la costante crioscopica dell'acqua. Quindi l'abbassamento crioscopico di una soluzione acquosa 0,0001 m di solfato di alluminio Al₂(SO₄)₃ è dato da:",
        "explanation": "Al₂(SO₄)₃ si dissocia in 2 Al³⁺ + 3 SO₄²⁻ (ν = 5 ioni); applicando la formula si ottiene: Δt_c = 1,86 × 0,0001 × 5 = 1,86 × 10⁻⁴ × 5.",
    },
    "CHIM-C06-COMM-014": {
        "options": {
            "A": "BaCO₃ è meno solubile di Ba(HCO₃)₂",
            "B": "Na₂CO₃ è più solubile di K₂CO₃",
            "C": "Li₂CO₃ è più solubile di LiHCO₃",
            "D": "Mg(HCO₃)₂ è più solubile di MgCO₃",
            "E": "KHCO₃ è meno solubile di K₂CO₃",
        },
        "explanation": "Ba e Mg sono metalli alcalino-terrosi; Na, Li e K sono metalli alcalini. Le opzioni A, C, D ed E sono quindi deducibili dal brano, mentre nulla si dice sul confronto di solubilità tra i carbonati di due diversi metalli alcalini (Na₂CO₃ e K₂CO₃).",
    },
    "CHIM-C06-COMM-016": {
        "question": "Una soluzione è stata ottenuta mescolando 30 g di alcol etilico (CH₃CH₂OH: MM = 46 g/mol) con 70 g di acqua (H₂O: MM = 18 g/mol). Quale delle seguenti affermazioni è falsa?",
        "explanation": "L'acqua e l'alcol etilico sono miscibili in tutte le proporzioni e formano una miscela azeotropica che non può essere completamente separata per distillazione frazionata. Essendo la massa totale della soluzione pari a 100 g, l'alcol etilico ha una concentrazione del 30% m/m (e non 30 g in 100 mL, poiché la densità della miscela è inferiore a 1 g/mL). Le frazioni molari valgono: mol(CH₃CH₂OH) = 30 / 46 = 0,65 mol; mol(H₂O) = 70 / 18 = 3,89 mol; X(CH₃CH₂OH) = 0,65 / 4,54 = 0,14; X(H₂O) = 3,89 / 4,54 = 0,86.",
    },
    "CHIM-C06-COMM-018": {
        "explanation": "Calcoliamo la massa di MgCl₂ (MM = 95 g/mol) in ciascuna soluzione: A: 1 M × 1 L = 1 mol → 95 g; B: 1 mol/kg in meno di 1 kg di solvente → < 95 g; C: 10% m/m in 0,5 L (~500 g) → ~50 g; D: 2 M × 0,5 L = 1 mol → 95 g; E: 10% m/V in 1000 mL → (10 g / 100 mL) × 1000 mL = 100 g di MgCl₂. La soluzione con la massa maggiore di MgCl₂ è quindi la E.",
    },
    "CHIM-C06-COMM-019": {
        "options": {"C": "Il contributo dei sali al totale della pressione osmotica del sangue è maggiore del 90%"},
    },
    "CHIM-C06-COMM-021": {
        "question": "Quale delle seguenti azioni produce una soluzione acquosa di NaNO₃ (M = 85 g/mol) con concentrazione 0,20 M?",
        "options": {
            "A": "Diluire 50 mL di una soluzione 2 M di NaNO₃ fino a 200 mL",
            "B": "Sciogliere 17,0 g di NaNO₃ in 250 mL di H₂O",
            "C": "Aggiungere acqua a 8,5 g di NaNO₃ per ottenere 250 mL di soluzione",
            "D": "Diluire 250 mL di una soluzione di NaNO₃ 0,8 M fino a 1,0 L",
            "E": "Mescolare 150 mL di una soluzione di NaNO₃ 0,15 M con 50 mL di una soluzione di NaNO₃ 0,05 M",
        },
        "explanation": "Calcoliamo le concentrazioni finali: A. (2 M × 50 mL) / 200 mL = 0,50 M; B. (17,0 g / 85 g/mol) / 0,250 L ≈ 0,8 M; C. (8,5 g / 85 g/mol) / 0,250 L = 0,40 M; D. (0,8 M × 0,25 L) / 1,0 L = 0,20 M; E. (0,15 M × 150 mL + 0,05 M × 50 mL) / 200 mL = 0,125 M.",
    },
    "CHIM-C06-NCOM-049": {
        "options": {
            "A": "1,5 grammoequivalenti di H₂SO₄ in 1 litro di soluzione",
            "B": "98 g di H₂SO₄ in 1 litro di soluzione",
            "C": "3 moli di H⁺ in 1 litro di soluzione",
            "D": "3 moli di SO₄²⁻ in 1 litro di soluzione",
            "E": "49 g di H₂SO₄ in 3 litri di soluzione",
        },
    },
    "CHIM-C06-NCOM-084": {
        "question": "La soluzione S₂ è ipertonica rispetto alla soluzione S₁, pertanto:",
        "options": {
            "A": "nelle stesse condizioni di temperatura la tensione di vapore di S₁ è maggiore della tensione di vapore di S₂",
            "B": "S₁ esercita una pressione osmotica maggiore rispetto a S₂",
            "C": "la temperatura di ebollizione di S₂ è minore della temperatura di ebollizione di S₁",
            "D": "S₂ congela a temperatura più elevata rispetto a S₁",
            "E": "S₁ è maggiormente concentrata",
        },
    },
    "CHIM-C06-NCOM-089": {
        "question": "Affermare che la salinità del mare si aggira intorno al 3,5%, equivale a dire che:",
        "options": {"A": "su 1.000 g di acqua di mare, 3,5 g sono di sali"},
    },
    "CHIM-C06-NCOM-098": {
        "options": {
            "C": "La soluzione (a) ha una pressione osmotica maggiore di quella della soluzione (b)",
            "D": "Il solvente si sposta dalla soluzione più diluita alla più concentrata",
        },
    },
    "CHIM-C07-COMM-003": {
        "question": "La reazione di combustione del propano C₃H₈ con ossigeno O₂ avviene con formazione di CO₂ e H₂O. Perciò, per bruciare una mole di propano, è necessaria una quantità di ossigeno costituita da un numero di moli di gas pari a:",
        "explanation": "La reazione bilanciata è C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O e il rapporto stechiometrico tra propano e ossigeno è di 1 : 5.",
    },
    "CHIM-C07-COMM-005": {
        "question": "Quale dei seguenti metodi può funzionare, nell'equilibrio tra sostanze gassose: A + B ⇄ C + D, per ridurre la quantità del prodotto C?",
    },
    "CHIM-C07-COMM-007": {
        "question": "20 mL di CH₄(g) vengono bruciati insieme con 80 mL di O₂(g), misurati nelle stesse condizioni di temperatura e pressione. Al termine della reazione CH₄(g) + 2 O₂(g) → CO₂(g) + 2 H₂O(g), qual è la composizione percentuale in volume della miscela gassosa?",
        "options": {
            "A": "40% O₂, 20% CO₂, 40% H₂O",
            "B": "33% CO₂, 66% H₂O",
            "C": "40% CH₄, 20% CO₂, 40% H₂O",
            "D": "25% CH₄, 25% O₂, 25% CO₂, 25% H₂O",
            "E": "25% CH₄, 50% O₂, 25% CO₂",
        },
        "explanation": "Nelle stesse condizioni di T e P i volumi dei gas sono proporzionali alle moli: 20 mL di CH₄ reagiscono completamente con 40 mL di O₂, lasciando 40 mL di O₂ in eccesso e formando 20 mL di CO₂ e 40 mL di H₂O(g), per un volume finale complessivo di 100 mL (40% O₂, 20% CO₂, 40% H₂O).",
    },
    "CHIM-C07-COMM-010": {
        "options": {"A": "MnO₄²⁻", "B": "MnO₄⁻", "C": "MnO", "D": "Mn₂O₃", "E": "MnO₂"},
        "explanation": "I numeri di ossidazione del manganese nelle diverse specie sono: MnO₄²⁻ (+6, VI); MnO₄⁻ (+7, VII); MnO (+2, II); Mn₂O₃ (+3, III); MnO₂ (+4, IV).",
    },
    "CHIM-C07-COMM-012": {
        "question": "Sulla base delle reazioni rappresentate nella figura seguente (CH₃CH₂OH → CH₃CHO → CH₃COOH), determinare se, nel corso della reazione complessiva, l'atomo di carbonio 1 va incontro ad una ossidazione o a una riduzione; indicare, inoltre, il numero di ossidazione che il carbonio 1 assume nelle tre specie rappresentate:",
        "explanation": "La prima reazione rappresenta l'ossidazione dell'etanolo ad acetaldeide e la seconda l'ossidazione dell'acetaldeide ad acido acetico: il carbonio 1 va incontro a due ossidazioni successive, passando da n.o. = -1 (nell'etanolo) a n.o. = +1 (nell'acetaldeide) fino a n.o. = +3 (nell'acido acetico).",
    },
    "CHIM-C07-COMM-013": {
        "question": "Nella reazione As₂O₃ + 4 HNO₃ + H₂O → 2 H₃AsO₄ + 4 NO₂, gli elementi che subiscono una variazione del numero di ossidazione sono:",
        "options": {"A": "As e N", "B": "O e As", "C": "N e H", "D": "As e H", "E": "nessuno"},
        "explanation": "È una reazione redox in cui l'arsenico (As) passa da n.o. +3 a +5 ossidandosi, mentre l'azoto (N) passa da +5 a +4 riducendosi.",
    },
    "CHIM-C07-COMM-018": {
        "options": {"A": "CO", "B": "CCl₄", "C": "C₂H₆", "D": "C₆H₁₂O₆", "E": "CHCl₃"},
        "explanation": "I numeri di ossidazione del carbonio nei composti elencati sono rispettivamente: +2 (CO), +4 (CCl₄), -3 (C₂H₆), 0 (C₆H₁₂O₆), +2 (CHCl₃).",
    },
    "CHIM-C07-COMM-025": {
        "question": "Quale affermazione riferita alla seguente equazione chimica, che deve essere bilanciata, è corretta? MnO₂ + HCl → MnCl₂ + Cl₂ + H₂O",
        "options": {
            "A": "Si formano 2 moli di Cl₂ per ogni mole di MnO₂",
            "B": "Il cloro si riduce",
            "C": "Sono necessarie 4 moli di HCl per ogni mole di MnO₂",
            "D": "Il manganese è l'agente riducente",
            "E": "È una reazione di dismutazione",
        },
        "explanation": "Si tratta di una reazione redox in cui il cloro si ossida (da -1 a 0) e il manganese si riduce (da +4 a +2, fungendo da agente ossidante). Bilanciando: MnO₂ + 4 HCl → MnCl₂ + Cl₂ + 2 H₂O; occorrono quindi 4 moli di HCl per ogni mole di MnO₂.",
    },
    "CHIM-C07-COMM-026": {
        "question": "L'ossigeno molecolare (O₂) e l'idrogeno molecolare (H₂) reagiscono per formare acqua (H₂O); nelle condizioni in cui si fa avvenire la reazione (alta temperatura), tutte e tre le sostanze si trovano allo stato gassoso; dal punto di vista stechiometrico, la reazione si svolge tra UNA mole di O₂ e DUE moli di H₂, e si formano DUE moli di H₂O. Se la reazione non decorre a completezza, si raggiunge una situazione di equilibrio dinamico, caratterizzato dall'uguaglianza delle velocità della reazione diretta (sintesi dell'acqua) e di quella inversa (scissione dell'acqua in ossigeno e idrogeno); le condizioni dell'equilibrio dipendono essenzialmente dalla temperatura e dalla pressione; se si lavora a temperatura costante, l'equilibrio è tanto più favorevole alla sintesi dell'acqua quanto più alta è la pressione a cui si opera, in quanto, in conformità del principio dell'equilibrio mobile di Le Chatelier-Braun, nella sintesi si passa da tre a due moli di gas, che esercitano una pressione minore rispetto a tre moli. Quale delle seguenti affermazioni NON può essere dedotta dalla lettura del brano precedente?",
        "options": {"E": "A temperatura costante, la scissione dell'acqua in ossigeno e idrogeno produce un aumento della pressione"},
        "explanation": "La reazione di equilibrio è: 2 H₂(g) + O₂(g) ⇄ 2 H₂O(g). Nel brano non si specifica se la reazione sia endotermica o esotermica, quindi non è possibile dedurre dal solo testo l'effetto della temperatura sull'equilibrio (risposta A).",
    },
    "CHIM-C07-COMM-027": {
        "options": {"A": "H₂", "B": "O₂", "C": "H₂ e O₂", "D": "H⁺ e OH⁻", "E": "H⁺ e e⁻"},
        "explanation": "Un ossidante forte può ossidare solo l'ossigeno dell'acqua (poiché l'idrogeno si trova già al numero di ossidazione massimo +1), secondo la semireazione 2 H₂O → O₂ + 4 H⁺ + 4 e⁻, liberando O₂.",
    },
    "CHIM-C07-COMM-028": {
        "question": "I coefficienti stechiometrici della reazione a Fe²⁺ + b H⁺ + c MnO₄⁻ → d Fe³⁺ + e Mn²⁺ + f H₂O sono:",
        "options": {
            "A": "a = 6; b = 24; c = 1; d = 6; e = 1; f = 12",
            "B": "a = 5; b = 8; c = 3; d = 5; e = 3; f = 4",
            "C": "a = 2; b = 8; c = 1; d = 2; e = 1; f = 4",
            "D": "a = 5; b = 8; c = 1; d = 5; e = 1; f = 4",
            "E": "a = 4; b = 5; c = 3; d = 3; e = 1; f = 4",
        },
        "explanation": "Semireazione di riduzione: MnO₄⁻ + 8 H⁺ + 5 e⁻ → Mn²⁺ + 4 H₂O; semireazione di ossidazione: 5 × (Fe²⁺ → Fe³⁺ + e⁻). Sommando membro a membro: 5 Fe²⁺ + 8 H⁺ + MnO₄⁻ → 5 Fe³⁺ + Mn²⁺ + 4 H₂O (17 cariche positive per lato).",
    },
    "CHIM-C07-COMM-030": {
        "question": "Quale delle seguenti combinazioni di coefficienti stechiometrici - a, b, c, d, e - deve essere utilizzata per bilanciare la reazione a Cu + b HNO₃ → c Cu(NO₃)₂ + d NO + e H₂O?",
        "options": {
            "A": "a = 3; b = 6; c = 3; d = 2; e = 4",
            "B": "a = 2; b = 8; c = 2; d = 4; e = 4",
            "C": "a = 1; b = 3; c = 1; d = 1; e = 2",
            "D": "a = 3; b = 8; c = 3; d = 2; e = 4",
            "E": "a = 4; b = 6; c = 2; d = 2; e = 3",
        },
        "explanation": "Semireazione di ossidazione: 3 × (Cu → Cu²⁺ + 2 e⁻); semireazione di riduzione: 2 × (NO₃⁻ + 4 H⁺ + 3 e⁻ → NO + 2 H₂O). Forma ionica: 3 Cu + 2 NO₃⁻ + 8 H⁺ → 3 Cu²⁺ + 2 NO + 4 H₂O; forma molecolare: 3 Cu + 8 HNO₃ → 3 Cu(NO₃)₂ + 2 NO + 4 H₂O.",
    },
    "CHIM-C07-NCOM-004": {
        "options": {
            "A": "N₂ + 3 H₂ → 3 NH₃",
            "B": "3 KOH + 2 H₃PO₄ → K₃PO₄ + 3 H₂O",
            "C": "2 O₃ → 2 O₂ + O",
            "D": "2 CaO → Ca + O₂",
            "E": "4 NH₃ + 5 O₂ → 4 NO + 6 H₂O",
        },
    },
    "CHIM-C07-NCOM-006": {
        "question": "Quale delle seguenti sequenze di numeri esprime, in ordine, i coefficienti stechiometrici dei reagenti e dei prodotti nella reazione di combustione del propano C₃H₈? C₃H₈(g) + O₂(g) → CO₂(g) + H₂O(g)",
        "options": {"A": "1, 3, 3, 4", "B": "2, 2, 1, 4", "C": "1, 5, 3, 4", "D": "1, 1, 1, 2", "E": "1, 2, 1, 2"},
    },
    "CHIM-C07-NCOM-008": {
        "options": {
            "A": "2 Na₂SO₃ + 2 AgNO₃ → Ag₂SO₃ + 2 NaNO₃",
            "B": "2 Na₂SO₃ + 2 AgNO₃ → 2 Ag₂SO₃ + 2 NaNO₃",
            "C": "Na₂SO₃ + AgNO₃ → Ag₂SO₃ + NaNO₃",
            "D": "Na₂SO₃ + 2 AgNO₃ → 2 Ag₂SO₃ + 2 NaNO₃",
            "E": "Na₂SO₃ + 2 AgNO₃ → Ag₂SO₃ + 2 NaNO₃",
        },
    },
    "CHIM-C07-NCOM-014": {
        "options": {
            "A": "NH₃ + H₂SO₄ → NH₄SO₄",
            "B": "NH₃ + HCl → NH₄Cl",
            "C": "K₂CO₃ + H₂SO₄ → K₂SO₄ + H₂O + CO₂",
            "D": "NH₄HCO₃ + HCl → NH₄Cl + CO₂ + H₂O",
            "E": "CaO + 2 HCl → CaCl₂ + H₂O",
        },
    },
    "CHIM-C07-NCOM-015": {
        "question": "La seguente reazione non è bilanciata. Quali coefficienti è necessario usare per un corretto bilanciamento? a KClO₃ → b KCl + c O₂",
        "options": {
            "A": "a = 1; b = 2; c = 2",
            "B": "a = 2; b = 3; c = 2",
            "C": "a = 2; b = 2; c = 3",
            "D": "a = 1; b = 2; c = 3",
            "E": "a = 1; b = 1; c = 1",
        },
    },
    "CHIM-C07-NCOM-021": {
        "question": "Quale delle seguenti combinazioni di coefficienti stechiometrici - a, b, c, d, e, f - deve essere utilizzata per bilanciare la reazione? a H₃AsO₃ + b HIO₃ + c Cl⁻ → d ICl₂⁻ + e H₃AsO₄ + f OH⁻",
        "options": {
            "A": "a = 1; b = 1; c = 1; d = 1; e = 1; f = 1",
            "B": "a = 1; b = 1; c = 2; d = 1; e = 1; f = 1",
            "C": "a = 2; b = 1; c = 2; d = 1; e = 2; f = 1",
            "D": "a = 2; b = 2; c = 2; d = 1; e = 2; f = 2",
            "E": "a = 2; b = 2; c = 2; d = 2; e = 2; f = 2",
        },
    },
    "CHIM-C07-NCOM-024": {
        "question": "A una soluzione acquosa acida di KBrO₃ (100 mL, 0,1 mol/L) vengono aggiunti 100 mL di una soluzione acquosa contenente 0,006 moli di K₂S₂O₃ e 0,09 moli di KI. Avvengono le seguenti reazioni quantitative: (1) 9 I⁻(aq) + BrO₃⁻(aq) + 6 H⁺(aq) → 3 I₃⁻(aq) + Br⁻(aq) + 3 H₂O(l); (2) I₃⁻(aq) + 2 S₂O₃²⁻(aq) → 3 I⁻(aq) + S₄O₆²⁻(aq). La reazione (2) è istantanea, mentre la reazione (1) è relativamente lenta. Nel momento in cui tutto l'anione S₂O₃²⁻ presente in soluzione avrà reagito, quante moli di BrO₃⁻ saranno state consumate?",
        "options": {"B": "0,001 mol"},
    },
    "CHIM-C07-NCOM-031": {
        "question": "Indicare la massa di ossido di calcio (calce viva) che si ottiene da 1 kg di CaCO₃, se la reazione è: CaCO₃ → CaO + CO₂ (p.at. Ca = 40, p.at. C = 12, p.at. O = 16 u.m.a.)",
    },
    "CHIM-C07-NCOM-032": {
        "question": "Indicare le moli di ossigeno molecolare necessarie per bruciare una mole di propano ammettendo che la reazione del C₃H₈ con O₂ (combustione) avvenga in modo completo:",
    },
    "CHIM-C07-NCOM-036": {
        "question": "Se nella reazione 3 NO₂ + H₂O → 2 HNO₃ + NO si formano 1,80 mol di NO, allora nella stessa reazione:",
        "options": {
            "A": "si consumano 3,60 mol di HNO₃",
            "B": "si consumano 3,60 mol di H₂O",
            "C": "si formano anche 5,40 mol di NO₂",
            "D": "si formano anche 3,60 mol di HNO₃",
            "E": "si formano anche 1,80 mol di HNO₃",
        },
    },
    "CHIM-C07-NCOM-038": {
        "question": "Il benzene, C₆H₆, può reagire con il fluoro, F₂, secondo la reazione bilanciata C₆H₆ + 9 F₂ → C₆F₁₂ + 6 HF. Quante sono le moli di F₂ che reagiscono con 3 moli di benzene?",
    },
    "CHIM-C07-NCOM-044": {"options": {"A": "Ox: 1; Red: 2; Redox: 3"}},
    "CHIM-C07-NCOM-045": {
        "options": {
            "A": "12 HNO₃ + 16 NH₃ → 24 H₂O + 14 N₂ + 6 H₂",
            "B": "Am(NO₃)₃ → Am³⁺ + 3 NO₃⁻",
            "C": "NH₄NO₃ → N₂ + 2 H₂O",
            "D": "[Ni(NH₃)₆]²⁺ → Ni²⁺ + 6 NH₃",
            "E": "4 NH₄NO₃ → 2 NH₃ + 3 NO₂ + NO + N₂ + 5 H₂O",
        },
    },
    "CHIM-C07-NCOM-047": {"options": {"D": "Q(g) + R(g) ⇄ X(g) la reazione diretta è esotermica"}},
    "CHIM-C07-COMP-024": {"question": "La _____ è la quantità di sostanza contenente 6,022 × 10²³ unità formula."},
    "CHIM-C08-COMM-004": {
        "question": "Indicare la corretta K_eq relativa alla reazione Ca(OH)₂ + H₂SO₄ ⇄ CaSO₄ + 2 H₂O:",
        "options": {
            "A": "[CaSO₄]·[H₂O] / ([Ca(OH)₂]·[H₂SO₄])",
            "B": "nessuna delle risposte è corretta",
            "C": "[CaSO₄]·[H₂O]² / ([Ca(OH)₂]·[H₂SO₄])",
            "D": "[Ca(OH)₂]·[H₂SO₄] / ([CaSO₄]·[H₂O]²)",
            "E": "[Ca(OH)₂]·[H₂SO₄] / [CaSO₄]",
        },
        "explanation": "La costante di equilibrio K_eq si esprime ponendo al numeratore il prodotto delle concentrazioni molari dei prodotti e al denominatore quello dei reagenti, ciascuna elevata al proprio coefficiente stechiometrico: K_eq = [CaSO₄]·[H₂O]² / ([Ca(OH)₂]·[H₂SO₄]).",
    },
    "CHIM-C08-NCOM-002": {
        "question": "Raddoppiando la sola concentrazione di NO nella reazione 2 NO(g) + O₂(g) → 2 NO₂(g) la velocità di reazione aumenta di 4 volte; raddoppiando la concentrazione sia di NO sia di O₂, la velocità di reazione aumenta di 8 volte. Qual è la legge cinetica della reazione?",
    },
    "CHIM-C09-COMM-002": {
        "question": "L'anione dicromato Cr₂O₇²⁻ si trasforma nel catione Cr³⁺ e in questa reazione l'atomo di Cr:",
        "options": {"C": "passa da numero di ossidazione -2 a +3 e si ossida", "D": "passa da numero di ossidazione -2 a +3 e si riduce"},
        "explanation": "Nell'anione dicromato Cr₂O₇²⁻ il cromo ha numero di ossidazione +6 (2x + 7(-2) = -2 → x = +6). Nel catione Cr³⁺ il cromo ha numero di ossidazione +3. Diminuendo il numero di ossidazione da +6 a +3, il cromo acquista elettroni e quindi si riduce.",
    },
    "CHIM-C09-NCOM-008": {"question": "Qual è il numero di ossidazione del cromo nel composto Cr(OH)₃?"},
    "CHIM-C09-NCOM-016": {"question": "Qual è il numero di ossidazione dello zolfo nell'anione S₂O₃²⁻?"},
    "CHIM-C09-NCOM-020": {"question": "Nell'anione PO₄³⁻, qual è il numero di ossidazione del fosforo?"},
    "CHIM-C09-NCOM-021": {
        "options": {"A": "CCl₄", "B": "C₆H₁₂O₆", "C": "C₂H₆", "D": "CO", "E": "CHCl₃"},
    },
    "CHIM-C09-NCOM-025": {
        "question": "Indicare il composto in cui l'azoto ha il più alto numero di ossidazione:",
        "options": {"A": "NO₂", "B": "nessuna delle risposte è corretta", "C": "HNO₃", "D": "NO", "E": "N₂O₃"},
    },
    "CHIM-C09-NCOM-029": {"question": "Qual è il numero di ossidazione dello zolfo nell'anione S₄O₆²⁻?"},
    "CHIM-C09-NCOM-030": {
        "question": "Le molecole e gli ioni nell'elenco di seguito contengono azoto: N₂, NH₄⁺, NO, NO₂⁻, N₂O₄, N₂H₄. Quale delle seguenti opzioni riporta correttamente la sequenza di molecole e ioni in ordine crescente di ossidazione dell'azoto dal più negativo al più positivo?",
        "options": {
            "A": "NO₂⁻, N₂H₄, N₂, NO, N₂O₄, NH₄⁺",
            "B": "NO₂⁻, N₂O₄, NH₄⁺, NO, N₂H₄, N₂",
            "C": "NH₄⁺, N₂H₄, N₂, NO, NO₂⁻, N₂O₄",
            "D": "N₂, NO, N₂H₄, NO₂⁻, NH₄⁺, N₂O₄",
            "E": "N₂H₄, NH₄⁺, N₂, NO, NO₂⁻, N₂O₄",
        },
    },
    "CHIM-C09-NCOM-032": {
        "options": {
            "A": "N₂O₄, HNO₃, HNO₂",
            "B": "NO, N₂O₄, HNO₂",
            "C": "N₂H₄, NO, HNO₂",
            "D": "HNO₃, N₂O₄, HNO₂",
            "E": "HNO₃, HNO₂, N₂O₄",
        },
    },
    "CHIM-C09-NCOM-121": {"question": "Nella reazione seguente: 2 Ca₃(PO₄)₂ + 10 C + 6 SiO₂ → P₄ + 6 CaSiO₃ + 10 CO"},
    "CHIM-C09-NCOM-122": {
        "question": "Nella seguente reazione 3 Cu + 8 HNO₃ → 3 Cu(NO₃)₂ + 2 NO + 4 H₂O, gli elementi che cambiano numero di ossidazione sono:",
        "options": {"A": "Cu e H", "B": "N e O", "C": "tutti", "D": "Cu e N", "E": "H e O"},
    },
    "CHIM-C10-COMM-012": {
        "question": 'I composti inorganici costituiti da due soli elementi (composti binari) vengono in genere denominati utilizzando la radice del secondo elemento della formula, seguita dalla congiunzione "di" e dal nome del primo elemento; il numero di atomi di ciascun elemento nella formula è indicato con un prefisso (mono-, di-, tri-, tetra-, penta-, esa-, epta-); il prefisso mono- viene in genere omesso. Ad esempio, Fe₂O₃ viene chiamato triossido di diferro, ICl viene denominato cloruro di iodio. Sulla base delle regole indicate nel testo, quali sono i nomi dei composti P₄O₆ e N₂O₅?',
        "options": {
            "A": "Esaossido di tetrafosforo, e diossido di pentaazoto",
            "B": "Tetraossido di esafosforo e pentaossido di azoto",
            "C": "Esaossido di fosforo e diossido di pentaazoto",
            "D": "Esaossido di tetrafosforo e pentaossido di diazoto",
            "E": "Tetraossido di esafosforo e diossido di pentaazoto",
        },
        "explanation": "Il brano riporta la nomenclatura tradizionale/IUPAC dei composti binari: P₄O₆ è l'esaossido di tetrafosforo e N₂O₅ è il pentaossido di diazoto. (Fe₂O₃, essendo ionico, nella nomenclatura di Stock si denomina ossido di ferro(III)).",
    },
    "CHIM-C10-COMM-013": {
        "question": "LiF, KOH, FeO e HCl sono, rispettivamente:",
        "options": {"A": "un sale, un idrossido, chetone, un acido"},
        "explanation": "LiF (fluoruro di litio) è un sale binario; KOH (idrossido di potassio) è un idrossido; FeO (ossido ferroso) è un ossido basico; HCl (acido cloridrico) è un acido.",
    },
    "CHIM-C10-COMM-014": {
        "question": 'I composti costituiti da due elementi vengono in genere denominati utilizzando la radice del nome del secondo elemento nella formula, seguita da "di" e dal nome del primo elemento; il numero di atomi di ciascun elemento nella formula è indicato da un prefisso (mono, di, tri, tetra, penta, ecc.; il prefisso mono viene in genere omesso). Così, ad esempio, il composto Al₂O₃ viene chiamato triossido di dialluminio, e il composto ICl prende il nome di cloruro di iodio. Sulla base delle regole indicate nel testo, quali sono le formule del tetrossido di diazoto e del pentacloruro di fosforo?',
        "options": {"A": "Na₂O₄; PCl₅", "B": "N₂O₄; FCl₅", "C": "N₄O₂; PCl₃", "D": "N₂O₄; PCl₃", "E": "N₂O₄; PCl₅"},
    },
    "CHIM-C10-NCOM-003": {"options": {"A": "AsO₃", "B": "AsO", "C": "As₂O₃", "D": "A₂O₃", "E": "Ar₂O₃"}},
    "CHIM-C10-NCOM-013": {"options": {"A": "P₂O₅", "B": "F₂O₅", "C": "CaH₂", "D": "PI₃", "E": "SF₆"}},
    "CHIM-C10-NCOM-021": {"options": {"A": "SO₃", "B": "H₂SO", "C": "S₂O₃", "D": "H₂SO₄", "E": "SO₂"}},
    "CHIM-C10-NCOM-023": {"options": {"A": "SO₃", "B": "SO", "C": "SO₂", "D": "H₂S", "E": "H₂SO₄"}},
    "CHIM-C10-NCOM-029": {"options": {"A": "Fe(OH)₃", "B": "Fe(OH)₂", "C": "Fe₂O₃", "D": "Fe₂HO", "E": "FeO"}},
    "CHIM-C10-NCOM-030": {"options": {"A": "Na₂O₂", "B": "NaO₂", "C": "NaO", "D": "Na₂O", "E": "Na₃O₂"}},
    "CHIM-C10-NCOM-031": {"options": {"A": "MgO₂", "B": "MgO", "C": "Mg₂HO₂", "D": "Mg₂O₂", "E": "Mg(OH)₂"}},
    "CHIM-C10-NCOM-032": {"options": {"A": "Cu₂O", "B": "CuO", "C": "CuO₂", "D": "Cu₂O₂", "E": "CuOH"}},
    "CHIM-C10-NCOM-034": {"options": {"A": "Rb₂O₂", "B": "Rb₄O", "C": "RbO", "D": "RbO₃", "E": "Rb₂O"}},
    "CHIM-C10-NCOM-050": {"options": {"A": "CaSO₃", "B": "Ca₂SO₄", "C": "CaSO", "D": "non esiste", "E": "CaSO₄"}},
    "CHIM-C10-NCOM-052": {"options": {"A": "(NH₄)S", "B": "(NH₄)₂S", "C": "(NH₄)S₂", "D": "(NH₄)HS", "E": "NH₄S"}},
    "CHIM-C10-NCOM-058": {
        "question": "Il solfito acido di sodio corrisponde a:",
        "options": {"A": "NaSO₃", "B": "NaHSO₃", "C": "Na₂SO₃", "D": "NaHSO", "E": "NaHSO₄"},
    },
    "CHIM-C10-NCOM-059": {"options": {"A": "CuCO", "B": "Cu₂(ClO)₃", "C": "Cu(ClO)₂", "D": "Cu₂ClO", "E": "CuClO"}},
    "CHIM-C10-NCOM-060": {
        "question": "Il perclorato di manganese corrisponde alla formula:",
        "options": {"A": "MnClO₄", "B": "Mn(ClO₄)₄", "C": "Mn(ClO₄)₂", "D": "MnCl", "E": "Mn₂(ClO)"},
    },
    "CHIM-C10-NCOM-066": {"options": {"A": "NaClO", "B": "NaClO₂", "C": "NaClO₄", "D": "Na₂Cl₄O", "E": "Na₂ClO"}},
    "CHIM-C10-NCOM-068": {"question": "Il composto K₂S è:"},
    "CHIM-C10-NCOM-071": {"options": {"A": "SO₃²⁻", "B": "IS²⁻", "C": "S²⁻", "D": "PO₄³⁻", "E": "SO₄²⁻"}},
    "CHIM-C10-NCOM-073": {"options": {"A": "Cd(NO₃)₂", "B": "CdNO₂", "C": "Cd(NO₂)₂", "D": "Ca(NO₂)", "E": "Ca(NO₂)₂"}},
    "CHIM-C10-NCOM-075": {"question": "Il composto ioduro rameico ha formula:"},
    "CHIM-C10-NCOM-081": {
        "question": "La formula del bicarbonato di calcio è:",
        "options": {"A": "Ca₂HCO", "B": "Ca(HCO₃)₂", "C": "CaHCO₃", "D": "Ca₂(CO₃)₂", "E": "CaCO₃"},
    },
    "CHIM-C10-NCOM-082": {
        "question": "Il cloruro mercuroso ha formula:",
        "options": {"A": "Hg₂Cl", "B": "HgCl₂", "C": "Hg₂Cl₂", "D": "MeCl", "E": "Me₂Cl₂"},
    },
    "CHIM-C10-NCOM-087": {"options": {"A": "CaO", "B": "BaCl₂", "C": "RbBr", "D": "Al₂F₃", "E": "KMnO₄"}},
    "CHIM-C10-NCOM-088": {"options": {"A": "HCl", "B": "NaOH", "C": "CH₃OH", "D": "CH₄", "E": "Na₂SO₄"}},
    "CHIM-C10-NCOM-098": {"options": {"A": "KCO₃", "B": "KHSO₃", "C": "KHCO₃", "D": "K₂CO₃", "E": "KHCO₄"}},
    "CHIM-C11-COMM-005": {
        "options": {
            "A": "a pH = 8 si ha la stessa concentrazione degli ioni H⁺ e OH⁻",
            "B": "a pH = 8 la concentrazione degli ioni H⁺ è maggiore di quella degli ioni OH⁻",
            "C": "a pH = 8 la concentrazione degli ioni OH⁻ è maggiore di quella degli ioni H⁺",
            "D": "il pH non dipende dalla concentrazione degli ioni OH⁻",
            "E": "a pH = 8 non vi sono ioni H⁺ e OH⁻",
        },
        "explanation": "Per definizione, pH = -log[H₃O⁺]. Se il pH è 8, [H₃O⁺] = 10⁻⁸ M; poiché a 25 °C [H₃O⁺][OH⁻] = 10⁻¹⁴, risulta [OH⁻] = 10⁻¹⁴ / 10⁻⁸ = 10⁻⁶ M > 10⁻⁸ M.",
    },
    "CHIM-C11-COMM-006": {
        "explanation": "L'acido formico è un acido debole (HCOOH + H₂O ⇄ H₃O⁺ + HCOO⁻) e il formiato di sodio si dissocia completamente (HCOONa → Na⁺ + HCOO⁻). L'acido formico e lo ione formiato costituiscono una coppia acido/base coniugata con rapporto [HCOOH]/[HCOO⁻] = 0,4 M / 1,0 M = 0,4, formando una soluzione tampone. Per l'equazione di Henderson-Hasselbalch, pH = pK_a + log([HCOO⁻]/[HCOOH]) = pK_a + log((mol_HCOO⁻ / V) / (mol_HCOOH / V)): poiché il volume V si semplifica, una moderata diluizione non altera il pH.",
    },
    "CHIM-C11-COMM-009": {
        "options": {"C": "Lo ione solfato (SO₄²⁻) è la base coniugata dell'acido solforico"},
        "explanation": "L'affermazione errata è quella riguardante l'acido solforico (H₂SO₄): la sua base coniugata diretta (perdita di un solo protone) è lo ione idrogenosolfato HSO₄⁻, mentre lo ione solfato SO₄²⁻ è la base coniugata di HSO₄⁻.",
    },
    "CHIM-C11-COMM-013": {
        "question": "L'idrolisi salina è il fenomeno:",
        "options": {
            "A": "per il quale alcuni sali sciolti in acqua ne provocano la scissione in H₂ e O₂",
            "B": "per il quale alcuni sali reagiscono con l'acqua dando luogo, a seconda dei casi, a soluzioni acquose acide o basiche",
            "D": "per il quale alcuni sali sciolti in acqua si dissociano in ioni",
        },
        "explanation": "L'idrolisi salina spiega perché molti sali derivanti da acido debole o base debole non danno soluzioni neutre: il pH dipende dal comportamento acido-base dei loro ioni in acqua, che possono mostrare carattere neutro (Li⁺, Na⁺, K⁺, Cl⁻, I⁻, NO₃⁻, ClO₄⁻), basico (S²⁻, CO₃²⁻, HCOO⁻, CH₃COO⁻) o acido (NH₄⁺, RNH₃⁺).",
    },
    "CHIM-C11-COMM-026": {
        "question": "Una soluzione di acido formico 0,1 M (K_a = 4,8 × 10⁻⁵) è:",
    },
    "CHIM-C11-COMM-034": {
        "explanation": "pH = -log[H₃O⁺] = -log(10⁻¹) = 1.",
    },
    "CHIM-C11-NCOM-002": {
        "question": "Tra i composti elencati qui sotto: CO₂, MgO, HCl, Na₂O, HNO₃, NO₂, H₂SO₄, SO₃, K₂O, KOH — quanti sono acidi e quanti basici in soluzione acquosa?",
    },
    "CHIM-C11-NCOM-025": {
        "question": "Tutte le equazioni sottostanti descrivono reazioni acido-base. In quale delle reazioni il composto sottolineato si comporta da acido di Lewis e non da acido di Brønsted-Lowry?",
        "options": {
            "A": "NH₃ + H₂O → NH₄⁺ + OH⁻",
            "B": "CH₃COOH + NaOH → CH₃COONa + H₂O",
            "C": "NH₃ + BCl₃ → H₃NBCl₃",
            "D": "[Cu(H₂O)₄]²⁺ + H₂O → [Cu(H₂O)₃OH]⁺ + H₃O⁺",
            "E": "HNO₃ + H₂SO₄ → H₂NO₃⁺ + HSO₄⁻",
        },
    },
    "CHIM-C11-NCOM-030": {
        "question": "Indicare una coppia coniugata acido-base nella seguente reazione: CN⁻ + H₂O ⇄ HCN + OH⁻",
        "options": {"A": "H₂O, HCN", "B": "CN⁻, H₂O", "C": "CN⁻, OH⁻", "D": "H₂O, OH⁻", "E": "HCN, OH⁻"},
    },
    "CHIM-C11-NCOM-033": {
        "options": {
            "A": "Lo ione solfato (SO₄²⁻) è la base coniugata dell'acido solforico",
            "C": "Lo ione fluoruro è la base coniugata di HF",
            "E": "L'acqua è la base coniugata dello ione idronio",
        },
    },
    "CHIM-C11-NCOM-035": {
        "options": {
            "A": "l'acido coniugato di PO₄³⁻ è H₃PO₄",
            "B": "la base coniugata di H₃O⁺ è H₂O",
            "C": "nella reazione tra HCl e acqua si formano ioni idruro e ioni cloruro",
            "D": "nella reazione tra NH₃ e H₂O si formano ioni idronio e ioni ammonio",
            "E": "la base coniugata di H₂SO₄ è SO₄²⁻",
        },
    },
    "CHIM-C11-NCOM-041": {"options": {"A": "K₂O", "B": "SO₃", "C": "HCl", "D": "NO₂", "E": "LiCl"}},
    "CHIM-C11-NCOM-044": {
        "options": {"A": "7 · 10⁻⁷ M", "B": "10⁻¹⁴ M", "C": "7 M", "D": "10⁻³ M", "E": "10⁻⁷ M"},
    },
    "CHIM-C11-NCOM-046": {
        "options": {"D": "0,2 moli di ossidrilioni", "E": "0,002 moli di ossidrilioni"},
    },
    "CHIM-C11-NCOM-048": {"question": "Il prodotto ionico dell'acqua [H⁺] · [OH⁻] è uguale a:"},
    "CHIM-C11-NCOM-056": {
        "question": "Qual è il volume minimo di una soluzione acquosa di idrossido di potassio 0,150 mol/L necessario per neutralizzare completamente una soluzione acquosa contenente 5 × 10⁻³ mol di acido succinico (HOOCCH₂CH₂COOH)?",
        "options": {"C": "167 mL"},
    },
    "CHIM-C11-NCOM-059": {"options": {"E": "[OH⁻] > [O²⁻]"}},
    "CHIM-C11-NCOM-060": {"question": "Una soluzione ha [OH⁻] = 10⁻¹² M. Essa:"},
    "CHIM-C11-NCOM-063": {"options": {"E": "[H⁺] = 10⁻⁵ M"}},
    "CHIM-C11-NCOM-066": {
        "question": "In una soluzione diluita di un acido forte monoprotico, tipo HCl, abbiamo [H⁺] = 0,001 mol/L. Qual è la concentrazione degli ioni [OH⁻] espressa in mol/L?",
    },
    "CHIM-C11-NCOM-069": {
        "options": {
            "A": "Il logaritmo dell'inverso della concentrazione di ioni H⁺",
            "B": "Il logaritmo del reciproco della concentrazione ossidrilionica",
            "C": "Nessuna delle altre risposte è corretta",
            "D": "L'esponente della potenza in base 10 che esprime la concentrazione di ioni H⁺",
            "E": "Il logaritmo dell'inverso della concentrazione di ioni H⁺ e OH⁻",
        },
    },
    "CHIM-C11-NCOM-074": {
        "question": "Quale delle seguenti coppie di sostanze reagendo dà una soluzione con pH inferiore a 7?",
        "options": {
            "A": "CaO(s) + H₂O(l)",
            "B": "K₂CO₃(s) + H₂O(l)",
            "C": "Mg(s) + H₂O(l)",
            "D": "NH₃(g) + H₂O(l)",
            "E": "CO₂(g) + H₂O(l)",
        },
    },
    "CHIM-C11-NCOM-080": {
        "question": "In una soluzione che ha pH = 7, la concentrazione di ioni OH⁻ è:",
        "options": {"A": "10⁷ M", "B": "14 M", "C": "10⁻¹⁴ M", "D": "10⁻⁷ M", "E": "7 M"},
    },
    "CHIM-C11-NCOM-096": {
        "question": "Il pH:",
        "options": {"A": "aumenta se la concentrazione ossidrilionica diminuisce"},
    },
    "CHIM-C11-NCOM-097": {"options": {"C": "[H⁺] = [OH⁻]", "E": "[H⁺] < [OH⁻]"}},
    "CHIM-C11-NCOM-101": {"question": "Quando la [H⁺] è minore della [OH⁻]?"},
    "CHIM-C11-NCOM-110": {"options": {"B": "[H₃O⁺] = [OH⁻]"}},
    "CHIM-C11-NCOM-120": {
        "question": "Una soluzione ha pH = 2. La concentrazione molare di H⁺ è:",
        "options": {"A": "10⁻¹² M", "B": "10⁻² M", "C": "10¹² M", "D": "10⁻¹·² M", "E": "10² M"},
    },
    "CHIM-C11-NCOM-146": {
        "question": "Individuare la successione corretta che ordina, in base al pH crescente, le seguenti soluzioni acquose: a) NH₃ 0,1 M; b) HNO₃ 0,1 M; c) KOH 0,1 M; d) HNO₃ 0,001 M; e) HCl 1 M",
        "options": {
            "A": "e, b, a, c, d",
            "B": "c, a, d, e, b",
            "C": "e, b, d, c, a",
            "D": "e, b, d, a, c",
            "E": "a, c, d, b, e",
        },
    },
    "CHIM-C12-COMM-005": {
        "explanation": "Due isomeri costituzionali sono composti con la stessa formula bruta ma diversa connettività. Il pentano ha formula C₅H₁₂ (alcano, CₙH₂ₙ₊₂); ciclopentano e 2-pentene hanno formula C₅H₁₀; il 2-pentanone ha formula C₅H₁₀O. Solo il 2-metilbutano (C₅H₁₂) è un isomero del pentano.",
    },
    "CHIM-C12-COMM-007": {
        "options": {
            "A": "CH₃CH₂CH(OH)CH₂CH₃",
            "B": "(CH₃)₂CHCH₂CH₂OH",
            "C": "CH₃CH₂CH₂CH₂CH₂OH",
            "D": "CH₃CH₂CH(CH₃)CH₂OH",
            "E": "(CH₃)₂CH-O-CH₂CH₃",
        },
        "explanation": "I nomi dei composti elencati sono: A, 3-pentanolo; B, 3-metil-1-butanolo; C, 1-pentanolo; D, 2-metil-1-butanolo; E, etil isopropil etere.",
    },
    "CHIM-C12-COMM-008": {
        "options": {"B": "2-clorofenolo e o-clorofenolo"},
        "explanation": "L'acetone e la propionaldeide hanno entrambi formula molecolare C₃H₆O e sono quindi isomeri strutturali. Butano e ciclobutano hanno formula C₄H₁₀ e C₄H₈; 2-clorofenolo e o-clorofenolo sono due nomi dello stesso composto (C₆H₅ClO); benzene e cicloesano hanno formula C₆H₆ e C₆H₁₂; propano e propino hanno formula C₃H₈ e C₃H₄.",
    },
    "CHIM-C12-COMM-012": {
        "explanation": "Il cicloesano è un cicloalcano a 6 atomi di carbonio (C₆H₁₂) in cui ogni atomo di carbonio è ibridizzato sp³ (angoli tetraedrici di ~109,5°) e lega due atomi di idrogeno; non è quindi planare (adotta conformazione a sedia).",
    },
    "CHIM-C12-COMM-015": {
        "question": "Il numero di atomi di H presenti in un alchene contenente n atomi di C è:",
        "explanation": "Un alchene aciclico (con un doppio legame C=C, desinenza -ene) ha formula generale CₙH₂ₙ; perciò gli atomi di idrogeno per n atomi di carbonio sono 2n.",
    },
    "CHIM-C12-COMM-031": {
        "options": {
            "B": "fra le molecole dei due composti si stabiliscono legami apolari deboli",
            "C": "a temperatura ambiente e pressione normale l'isoottano è gassoso e l'etanolo è liquido",
            "E": "l'etanolo non è solubile in isoottano",
        },
        "explanation": "L'etanolo (CH₃CH₂OH) possiede una catena etilica idrofobica (CH₃CH₂-) apolare in grado di instaurare interazioni di dispersione (forze di London) con le molecole apolari dell'isoottano.",
    },
    "CHIM-C12-COMM-035": {
        "question": "Il composto (CH₃CH₂CH₂)₃N è:",
        "options": {"D": "una nitrosammina"},
        "explanation": "È un'ammina terziaria (formula generale R₃N) con R = -CH₂CH₂CH₃ (tripropilammina).",
    },
    "CHIM-C12-COMM-039": {"options": {"D": "I chetoni hanno sempre un atomo di idrogeno legato al carbonio carbonilico"}},
    "CHIM-C12-COMP-017": {"question": "I _____ sono molecole organiche con formula generale Cₙ(H₂O)ₘ."},
    "CHIM-C12-COMP-023": {"question": "L'_____ (C₂H₆) ha geometria tetraedrica attorno al carbonio."},
    "CHIM-C12-COMP-046": {"question": "Il _____ è l'aromatico più semplice con formula C₆H₆."},
    "CHIM-C12-COMP-049": {"answer": "aromatico", "answer_text": "aromatico"},
    "CHIM-C12-COMP-053": {
        "question": "Una _____ introduce un gruppo -NO₂ sull'anello aromatico.",
        "answer": "nitrazione",
        "answer_text": "nitrazione",
        "explanation": "La reazione di sostituzione elettrofila aromatica che introduce un gruppo nitro (-NO₂) sull'anello benzenico è la nitrazione (nel testo originale riportata per refuso editoriale come 'nitrificazione').",
    },
    "CHIM-C12-NCOM-012": {"question": "Quanti isomeri costituzionali sono possibili nella molecola C₃H₈O?"},
    "CHIM-C12-NCOM-013": {"options": {"C": "la presenza di almeno tre atomi di carbonio asimmetrici"}},
    "CHIM-C12-NCOM-019": {
        "question": "Quali delle sostanze di formule: A. CH₃-CH₂Cl; B. CH₃-CHCl₂; C. CH₃-CCl₃; D. CH₂Cl-CH₂Cl sono isomere tra loro?",
        "options": {"A": "A e B", "B": "B e D", "C": "B e C", "D": "A e C", "E": "A e D"},
    },
    "CHIM-C12-NCOM-023": {"options": {"A": "C₃H₁₀", "B": "C₄H₁₀", "C": "CH₄CH₁₀", "D": "C₄H₈", "E": "C₄H₆"}},
    "CHIM-C12-NCOM-031": {
        "question": "Qual è il nome del C₂H₆?",
        "options": {"C": "Acetilene"},
    },
    "CHIM-C12-NCOM-034": {
        "options": {"A": "CₙH₂ₙ₋₂", "B": "C₂ₙH₂ₙ₊₂", "C": "CₙH₂ₙ₊₄", "D": "CₙH₂ₙ", "E": "CₙH₂ₙ₊₂"},
    },
    "CHIM-C12-NCOM-037": {"question": "Qual è il nome del C₂H₂?"},
    "CHIM-C12-NCOM-046": {
        "question": "Qual è il nome sistematico IUPAC del composto organico con formula CH₃CBr₂CH(OH)(CH₂)₄CH₃?",
        "options": {
            "A": "7,7-dibromo-ottan-1-olo",
            "B": "2,2-dibromo-ottan-3-olo",
            "C": "7,7-dibromo-eptan-6-olo",
            "D": "2,2-dibromo-eptan-3-olo",
            "E": "2,2-dibromo-ottan-2-olo",
        },
    },
    "CHIM-C12-NCOM-049": {
        "options": {"A": "CₙH₂ₙ", "B": "CH₂H₂ₙ", "C": "CₙH₂ₙ₋₂", "D": "CₙHₙ", "E": "CₙH₂ₙ₊₂"},
    },
    "CHIM-C12-NCOM-054": {
        "options": {"A": "C₁₄H₃₀", "B": "C₂₀H₂₂", "C": "C₁₀H₂₀", "D": "C₁₀H₂₂", "E": "C₂₀H₄₂"},
    },
    "CHIM-C12-NCOM-057": {
        "options": {"A": "CO₂ e H₂", "B": "Anidride carbonica e O₂", "C": "O₂ e H₂O", "D": "H₂O e CO", "E": "CO₂ e H₂O"},
    },
    "CHIM-C12-NCOM-069": {
        "options": {"A": "C₆H₁₄", "B": "C₆H₁₀", "C": "C₆H₄", "D": "C₆H₁₂", "E": "C₆H₈"},
    },
    "CHIM-C12-NCOM-076": {
        "options": {"A": "H₂O e O₂", "B": "CO₂ e H₂", "C": "CO₂ e H₂O", "D": "CO₂ e O₂", "E": "O₂ e H₂"},
    },
    "CHIM-C12-NCOM-091": {
        "question": "Il 2-pentene ha struttura:",
        "options": {
            "A": "CH₂=CH-CH₃",
            "B": "CH₃-CH₂-CH=CH-CH₃",
            "C": "CH₂=CH-CH₂-CH₂-CH₃",
            "D": "CH₃-CH₂=CH₂-CH₃",
            "E": "CH₃-CH=CH-CH₃",
        },
    },
    "CHIM-C12-NCOM-101": {
        "options": {"A": "CₙH₂ₙ₋₂", "B": "CₙH₂ₙ₊₂", "C": "CₙH₂ₙ₊₄", "D": "C₂ₙH₂ₙ", "E": "CₙHₙ"},
    },
    "CHIM-C12-NCOM-102": {
        "question": "A che formula corrisponde l'ottadecano?",
        "options": {"A": "C₈H₁₀", "B": "C₁₈H₃₈", "C": "C₁₀H₂₂", "D": "C₂₀H₄₂", "E": "C₃₀H₅₂"},
    },
    "CHIM-C12-NCOM-114": {
        "question": "Qual è la natura del composto organico C₄H₆?",
        "options": {"C": "Cicloalcano"},
    },
    "CHIM-C12-NCOM-115": {
        "options": {"A": "CₙH₂ₙ₊₄", "B": "CₙH₂ₙ₋₂", "C": "CₙH₂ₙ", "D": "CₙH₂ₙ₊₂", "E": "CₙHₙ"},
    },
    "CHIM-C12-NCOM-123": {
        "options": {
            "A": "CH₃-CH=C=CH-CH₂-CH₃",
            "B": "CH₂=C=CH-CH=CH-CH₃",
            "C": "CH₃-CH=CH-CH₂=CH",
            "D": "CH₃-CH=CH-CH=CH-CH₃",
            "E": "CH₂=CH-CH=CH-CH₃",
        },
    },
    "CHIM-C12-NCOM-127": {"options": {"A": "10", "B": "9", "C": "7", "D": "8", "E": "6"}},
    "CHIM-C12-NCOM-128": {
        "question": "Quale delle seguenti è la formula bruta di un idrocarburo lineare monoinsaturo?",
        "options": {"A": "CₙHₙ₋₂", "B": "CₙHₙ₊₂", "C": "CₙH₂ₙ₊₂", "D": "CₙH₂ₙ", "E": "CₙH₂ₙ₋₂"},
    },
    "CHIM-C12-NCOM-130": {"question": "C₅H₁₀ è la formula bruta del:"},
    "CHIM-C12-NCOM-133": {
        "question": "Il benzene ha formula C₆H₆ ed è:",
        "options": {"E": "un idrocarburo ciclico aromatico planare"},
    },
    "CHIM-C12-NCOM-136": {"question": "Il composto C₂H₆ è un:"},
    "CHIM-C12-NCOM-148": {"options": {"E": "Il benzene è una sostanza aromatica"}},
    "CHIM-C12-NCOM-155": {
        "options": {"A": "C₆H₈", "B": "C₆H₁₀", "C": "C₆H₆", "D": "C₆H₁₄", "E": "C₆H₁₂"},
    },
    "CHIM-C12-NCOM-156": {
        "question": "Come si chiama il gruppo alchilico che ha formula -CH₂CH₂CH₃?",
        "options": {"D": "Propano"},
    },
    "CHIM-C12-NCOM-160": {
        "options": {"A": "C₂H₄", "B": "C₂H₂", "C": "C₃H₈", "D": "C₄H₆", "E": "C₂H₆"},
    },
    "CHIM-C12-NCOM-162": {
        "options": {"A": "CCl₄", "B": "CHCl₃", "C": "CH₂Cl₂", "D": "CH₃Cl", "E": "CH₃Cl₃"},
    },
    "CHIM-C12-NCOM-174": {
        "options": {
            "A": "CH₂OHCH₂OH",
            "B": "CH₃CH₂CH₂CH₂OH",
            "C": "CH₃OH",
            "D": "CH₃CH₂OH",
            "E": "CH₃CH₂CH₂OH",
        },
    },
    "CHIM-C12-NCOM-180": {
        "options": {
            "A": "CH₃-COOH",
            "B": "CH₃-CO-CH₃",
            "C": "CH₃-CH₂-CHO",
            "D": "CH₃-CH₂-CO-CH₂-CH₃",
            "E": "nessuno dei composti indicati è un'aldeide",
        },
    },
    "CHIM-C12-NCOM-183": {
        "options": {
            "A": "H₃C-CO-CH₃",
            "B": "CH₃-CHO",
            "C": "H₂C=O",
            "D": "C₆H₁₁CH=O",
            "E": "CH₃-CH₂-CH₂-CHO",
        },
    },
    "CHIM-C12-NCOM-184": {
        "question": "Qual è la struttura dell'etere dietilico?",
        "options": {
            "A": "CH₃-O-CH₃",
            "B": "C₂H₅-O-C₂H₅",
            "C": "C₆H₁₁CH=O",
            "D": "CH₃-O-C₂H₅",
            "E": "C₃H₇-O-C₂H₅",
        },
    },
    "CHIM-C12-NCOM-185": {
        "question": "Qual è l'acetone?",
        "options": {
            "A": "CH₃-CO-OH",
            "B": "CH₃-CO-CH₃",
            "C": "CH₃-CH₂-CHO",
            "D": "CH₃-CHO",
            "E": "CH₃CHO",
        },
    },
    "CHIM-C12-NCOM-191": {
        "options": {
            "A": "CH₃-CH₂-COOH",
            "B": "COOH-COOH",
            "C": "(CH₃)₂-CH₂-CH₃",
            "D": "CH₃-CH₂-CH₂OH",
            "E": "sia la A che la B",
        },
    },
    "CHIM-C12-NCOM-194": {"question": "Il composto CH₃-CH₂-N(CH₃)₂ rappresenta:"},
    "CHIM-C12-NCOM-202": {
        "options": {
            "A": "(CH₃)₃N",
            "B": "CH₃-CH₂-CH₂-NH₂",
            "C": "CH₃-CH₂-CO-NH₂",
            "D": "CH₃-CH₂-NH-CH₃",
            "E": "CH₃-C-NH-CH",
        },
    },
    "CHIM-C12-NCOM-203": {
        "options": {
            "A": "C₆H₅-OH",
            "B": "C₆H₅-CH₂OH",
            "C": "C₆H₅-CHO",
            "D": "CH₃-CH₂-NH-CH₃",
            "E": "CH₃-CH₂OH",
        },
    },
    "CHIM-C12-NCOM-208": {"options": {"A": "Dipropil etere"}},
    "CHIM-C12-NCOM-210": {
        "options": {
            "A": "C₄H₉CH₂OH → C₄H₉CHO → C₄H₉COOCH₃",
            "B": "CH₃CH(OH)CH₃ → CH₃COCH₃ → CH₃CH₂COOH",
            "C": "HCOOH → HCHO → CH₃OH",
            "D": "CH₂=CH₂ → CH₃CHO → CH₃COOH",
            "E": "CH₃CH₂CH₂CH₂OH → CH₃CH₂CH₂CHO → CH₃CH₂CH₂COOH",
        },
    },
    "CHIM-C12-NCOM-218": {
        "question": "Il dimetilchetone ha struttura:",
        "options": {
            "A": "CH-CO-C",
            "B": "CH₃-CO-CH₃",
            "C": "CH₃-O-CH₃",
            "D": "CH₃-CH₂-CO-CH₃",
            "E": "CH₃-CHO",
        },
    },
    "CHIM-C12-NCOM-219": {"question": "Il gruppo ossidrile (-OH) è presente:"},
    "CHIM-C12-NCOM-224": {
        "options": {
            "A": "CH₃-CH₂-NH₂",
            "B": "CH-CH₂-NH",
            "C": "CH₃-CONH₂",
            "D": "CH₃-COONH₄",
            "E": "(CH₃)₂NH",
        },
    },
    "CHIM-C12-NCOM-231": {"question": "Passando dall'aldeide CH₃CHO all'alcool CH₃CH₂OH, è avvenuta:"},
    "CHIM-C12-NCOM-244": {
        "options": {
            "A": "CH₃-CH₂-CHO",
            "B": "CH-NOOH",
            "C": "CH₃-CO-CH₃",
            "D": "CH₃-CH₂-CO-O-CO-CH₂-CH₃",
            "E": "CH₃-CH₂-COOH",
        },
    },
    "CHIM-C12-NCOM-246": {"question": "Qual è il nome del composto C₃H₇-O-C₆H₅?"},
    "CHIM-C12-NCOM-248": {
        "options": {"A": "C₃H₆O", "B": "C₂H₄O₂", "C": "C₃H₈O", "D": "C₂H₄O", "E": "CH₃CH₂OH"},
    },
    "CHIM-C12-NCOM-249": {
        "options": {
            "A": "CH₃CH₂OH",
            "B": "CH₃-CH₂-CH₂-NH₂",
            "C": "CH₃-CH₂-COOH",
            "D": "(CH₃)₂CH₂-CH₃",
            "E": "COOH-COOH",
        },
    },
    "CHIM-C12-NCOM-251": {
        "question": "La formula CH₃CH₂CH₂CH₂CHO corrisponde a:",
        "options": {"E": "composto inesistente"},
    },
    "CHIM-C12-NCOM-256": {
        "question": "Quale delle seguenti formule è quella dell'acido formico?",
        "options": {
            "A": "CHHOC",
            "B": "HCOOH",
            "C": "C₆H₅CH₂COOH",
            "D": "CH₃OCH₃",
            "E": "CH₃CH₂COCH₂OH",
        },
    },
    "CHIM-C12-NCOM-263": {
        "options": {
            "A": "Ca(C₂H₃O₂)₃",
            "B": "Ca₂(C₂H₃O₂)₄",
            "C": "Ca(C₂H₃O₂)₂",
            "D": "Ca₂C₂H₃O₂",
            "E": "CaC₂H₃O₂",
        },
    },
    "CHIM-C12-NCOM-265": {
        "options": {
            "A": "R-O-NH₂",
            "B": "R-CH₂-NH₂",
            "C": "R-CO-NH₂",
            "D": "R-CH₂-N=N-CH₃",
            "E": "R₂C=NH",
        },
    },
    "CHIM-C12-NCOM-267": {
        "options": {"A": "O, N", "B": "H, O", "C": "O, Cl", "D": "H, Cl", "E": "H, N"},
    },
    "CHIM-C12-NCOM-269": {
        "question": "Individuare fra le seguenti molecole gli eteri: 1. R₁-CO-R₂; 2. R-COH; 3. R₁-O-R₂; 4. R-CO-NH₂; 5. CH₃OH",
        "options": {"A": "3", "B": "2, 3", "C": "1, 2, 3", "D": "1, 5", "E": "1, 3"},
    },
    "CHIM-C12-NCOM-306": {
        "options": {"A": "C₃H₅O", "B": "C₂H₄O", "C": "C₃H₆O", "D": "C₃H₆O₂", "E": "C₂H₃O₂"},
    },
    "CHIM-C12-NCOM-307": {
        "question": "Essendo R e R' generici residui organici, quale dei seguenti composti è un'aldeide?",
        "options": {"A": "R-CHO", "B": "-COOR'", "C": "R-CH₂-CH₃", "D": "R-CH₂OH", "E": "-COOH"},
    },
    "CHIM-C13-COMM-010": {
        "question": "Nella formazione di un disaccaride da due monosaccaridi:",
        "options": {"C": "il primo monosaccaride si ossida, il secondo si riduce"},
        "explanation": "Il legame glicosidico, legame caratteristico dei carboidrati, si forma per eliminazione di acqua fra l'ossidrile semiacetalico di un monosaccaride e un ossidrile di un altro monosaccaride.",
    },
    "CHIM-C13-COMM-019": {
        "explanation": "Tutte le proteine contengono C, H, N e O. Alcune proteine possono anche contenere fosforo (fosfoproteine) o zolfo. Il peso molecolare di una proteina è uguale alla somma dei pesi molecolari dei singoli amminoacidi che la compongono, sottraendo (n - 1) volte la massa molecolare di H₂O.",
    },
    "CHIM-C13-NCOM-021": {
        "options": {"A": "C, N, O", "B": "S, N, P", "C": "C, N, H", "D": "C, S, H", "E": "C, H, O"},
    },
    "CHIM-C13-NCOM-064": {
        "options": {"A": "CH₃COOH", "B": "H₂O e CO", "C": "CH₃CHO", "D": "H₂O e CO₂", "E": "CH₃COCOOH"},
    },
    "CHIM-C13-NCOM-104": {
        "question": "Valutare quali dei seguenti legami caratterizzano la struttura primaria di una proteina: (A) legami a idrogeno; (B) legami peptidici; (C) interazioni idrofobiche; (D) legami disolfuro; (E) forze di van der Waals.",
    },
    "CHIM-C13-NCOM-123": {
        "options": {
            "A": "H₂N-CH₂-COOH",
            "B": "H₂N-CH₂-CHO",
            "C": "H₂N-CH₂-CH₂OH",
            "D": "H₂N-CH₂-HOHN",
            "E": "HOHN-CH₂-CH₂OH",
        },
    },
    "CHIM-C13-NCOM-126": {"options": {"D": "quanti legami idrogeno al massimo può formare la proteina"}},
    "CHIM-C13-NCOM-140": {
        "options": {
            "A": "C, H, O, N, S",
            "B": "C, H, O",
            "C": "C, H, O, S",
            "D": "C, H, O, N",
            "E": "C, H, O, N, P",
        },
    },
    "FIS-C01-COMM-003": {
        "explanation": "Il newton è l'unità di misura della forza nel Sistema Internazionale (1 N = 1 kg·m/s²), la dina nel sistema c.g.s. (1 dina = 1 g·cm/s²), e vale l'equivalenza 1 N = 10⁵ dine. Per le altre grandezze vale: 1 atm = 760 torr, 1 Pa = 1 N/m², 2π rad (≈ 6,28 rad) = 360°, 1 Ω = 1 V/A.",
    },
    "FIS-C01-COMM-016": {"options": {"D": "F₁ = 0,5; F₂ = 0,5; F₃ = 1"}},
    "FIS-C01-NCOM-043": {
        "question": "Quale/i dei seguenti prodotti tra grandezze ha/hanno le stesse unità di misura di un lavoro? 1. Pressione × volume; 2. Massa × variazione di altezza; 3. Carica × differenza di potenziale",
    },
    "FIS-C01-NCOM-054": {
        "question": "Quanti metri cubi (m³) sono contenuti in un millilitro?",
        "options": {"A": "100", "B": "10⁻⁶", "C": "10⁻⁹", "D": "10⁻¹⁰", "E": "10⁻³"},
    },
    "FIS-C01-NCOM-057": {
        "options": {"A": "10⁻¹⁸", "B": "10⁻²¹", "C": "10⁻¹²", "D": "10⁻¹⁵", "E": "10⁻²⁴"},
    },
    "FIS-C01-NCOM-075": {
        "question": "Un solido di un certo materiale ha una densità uniforme di 2 g/cm³ e un volume V₀ a una temperatura di 20 °C. Il volume V del solido varia in funzione della temperatura T secondo la legge V - V₀ = V₀ × 0,002 × (T - 20 °C). Se il solido ha una massa di 10 g, quale sarà il suo volume alla temperatura T = 40 °C?",
        "options": {"A": "5,5 cm³", "B": "5,2 cm³", "C": "5,04 cm³", "D": "5,02 cm³", "E": "5,002 cm³"},
    },
    "FIS-C02-COMM-006": {
        "explanation": "Esprimendo la velocità dell'auto in m/s si ha: v = 120 km/h = 120 / 3,6 m/s = 33,3 m/s. Lo spazio percorso in Δt = 1 s è quindi x = 33,3 m/s × 1 s = 33,3 m.",
    },
    "FIS-C02-COMM-020": {
        "explanation": "Tra l'istante t₀ e l'istante t₁ il tram si muove di moto rettilineo uniformemente accelerato (v = v₀ + a·t), rappresentato da un tratto di retta con pendenza positiva. Tra l'istante t₁ e l'istante t₂ il tram decelera uniformemente (v = v₁ - |a|·t), rappresentato da un tratto di retta a pendenza negativa. Il grafico complessivo è quindi quello del diagramma 2.",
    },
    "FIS-C02-NCOM-057": {
        "question": "Abbiamo due palline che si muovono su due circonferenze di raggio diverso, compiendo entrambe un moto circolare uniforme. Quale delle seguenti affermazioni è corretta?",
    },
    "FIS-C02-NCOM-058": {"question": "L'accelerazione centripeta è:"},
    "FIS-C03-COMM-012": {
        "explanation": "Il sistema dei due vagoni è isolato e conserva la quantità di moto: m₁·v₀ = (m₁ + m₂)·v, da cui v = m₁·v₀ / (m₁ + m₂) < v₀. L'energia cinetica finale K_f = ½(m₁ + m₂)v² = K_i · m₁/(m₁ + m₂) è quindi minore dell'energia cinetica iniziale K_i = ½m₁v₀² (urto completamente anelastico).",
    },
    "FIS-C03-COMM-044": {
        "explanation": "Per la conservazione dell'energia meccanica in caduta libera (partenza da fermo): mgh = ½mv², da cui v = √(2gh). Per h = 0,2 m si ha v = √(2 × 9,8 × 0,2) ≈ 2 m/s; raddoppiando l'altezza (2h), la velocità finale aumenta di un fattore √2 (v' = √2 · v ≈ 2√2 m/s).",
    },
    "FIS-C03-COMM-045": {
        "explanation": "Quando il sasso si stacca dalla corda mantiene la velocità periferica del moto circolare uniforme: con f = 5 s⁻¹ e R = 1 m si ottiene v = 2πRf = 2 × 3,14 × 1 m × 5 s⁻¹ ≈ 31,4 m/s (circa 30 m/s).",
    },
    "FIS-C03-NCOM-060": {
        "question": "Per COMPRIMERE una molla di 10 cm rispetto alla posizione di equilibrio è necessario compiere un lavoro L = 1,7 J. Il lavoro necessario per ALLUNGARE la molla di 10 cm rispetto alla posizione di equilibrio è:",
    },
    "FIS-C04-NCOM-014": {
        "options": {"B": "è salito di 1 mm", "C": "è sceso di 10 mm", "D": "è sceso di 1 mm"},
    },
    "FIS-C04-NCOM-087": {
        "question": "Dalla parte superiore di un condotto verticale di sezione costante S₁ fuoriesce un getto di un liquido ideale. Come deve essere modificata la sezione del foro di uscita perché il getto di liquido possa raggiungere un'altezza doppia? (Sia S₂ la nuova sezione e si ipotizzi che la portata volumetrica del getto del liquido si mantenga costante; inoltre si trascuri la resistenza dell'aria).",
        "options": {"A": "S₂ = S₁ / 2", "B": "S₂ = 2 S₁", "C": "S₂ = S₁ / √2", "D": "S₂ = √2 S₁", "E": "S₂ = S₁"},
    },
    "FIS-C05-COMM-002": {
        "explanation": "Il calore ceduto dai 2 kg di acqua a 80 °C uguaglia il calore assorbito da 1 kg di acqua a 20 °C: c·m₁·(80 - t_eq) = c·m₂·(t_eq - 20), da cui t_eq = (2 × 80 + 1 × 20) / (2 + 1) = 60 °C.",
    },
    "FIS-C05-COMM-013": {
        "options": {"A": "t °C", "B": "0,1 t °C", "C": "0,5 t °C", "D": "0,9 t °C", "E": "2 t °C"},
        "explanation": "Imponendo che il calore ceduto dall'oggetto caldo sia pari a quello assorbito dall'oggetto freddo: m·9C·(t - x) = m·C·(x - 0) → 9t - 9x = x → x = 0,9 t.",
    },
    "FIS-C05-COMM-015": {
        "explanation": "Per il primo principio della termodinamica ΔU = Q - L (con Q positivo se assorbito e L positivo se compiuto dal sistema). In una trasformazione adiabatica (Q = 0) vale L = -ΔU: durante un'espansione adiabatica il lavoro viene compiuto a spese dell'energia interna del gas, che quindi diminuisce raffreddandosi.",
    },
    "FIS-C05-COMM-020": {
        "explanation": "A parità di calore specifico e di massa, la temperatura di equilibrio tra due masse uguali d'acqua a temperature t₁ = 20 °C e t₂ = 80 °C è la media aritmetica: t_eq = (80 + 20) / 2 = 50 °C.",
    },
    "FIS-C05-COMM-023": {
        "explanation": "Il lavoro compiuto da un gas che si espande a pressione costante P è pari a L = P · ΔV, dove ΔV è la variazione di volume del gas.",
    },
    "FIS-C05-COMM-033": {"options": {"C": "ΔQ = k · (t₂ - t₁) / m"}},
    "FIS-C05-COMM-034": {
        "question": "Un gas subisce una trasformazione ciclica rappresentata nel piano pressione/volume da un rettangolo percorso in senso orario avente lati (p₂ - p₁) > 0 e (V₂ - V₁) > 0 paralleli agli assi. La vera proposizione è:",
        "explanation": "La trasformazione ciclica è composta da due isobare (AB e CD) e due isocore (BC e DA). Il lavoro totale compiuto in un ciclo orario è positivo e pari all'area racchiusa dal rettangolo, L = (V₂ - V₁)·(p₂ - p₁), mentre la variazione di energia interna ΔU su un ciclo chiuso è nulla (T_fin = T_in).",
    },
    "FIS-C05-NCOM-055": {
        "question": "Se mescoliamo tra loro in un recipiente adiabatico due masse di acqua, rispettivamente m₁ alla temperatura t₁ ed m₂ alla temperatura t₂, la temperatura di equilibrio t_f sarà:",
        "options": {
            "A": "t_f = (m₁t₁ - m₂t₂) / 2",
            "B": "t_f = (m₁t₁ + m₂t₂) / 2",
            "C": "t_f = (m₁t₁ + m₂t₂) / [2(m₁ + m₂)]",
            "D": "t_f = (m₁t₁ - m₂t₂) / [2(m₁ + m₂)]",
            "E": "nessuna delle altre risposte è corretta",
        },
    },
    "FIS-C05-NCOM-057": {
        "question": "Una caraffa con 1 kg di acqua a temperatura ambiente (T_amb = 20 °C) viene appoggiata su un blocco di 100 g di ghiaccio. Considerando il calore latente del ghiaccio 300 kJ/kg, calcolare la temperatura che raggiunge l'acqua quando il ghiaccio è completamente liquefatto (si consideri il calore specifico dell'acqua 4 kJ/(kg × K); non si consideri la variazione di temperatura del recipiente).",
        "options": {"E": "15 °C"},
    },
    "FIS-C05-NCOM-078": {
        "options": {"B": "maggiore di quello di due moli di Cl₂ (Mr = 70)", "E": "di circa 45 L"},
    },
    "FIS-C05-NCOM-082": {
        "question": "Un recipiente a pareti rigide (volume costante) contiene due moli di gas perfetto in un volume V₀ a pressione P₀ e temperatura T₀. Se iniettiamo nel recipiente altre due moli di gas perfetto operando in modo che la temperatura dello stato finale di equilibrio sia uguale a quella iniziale, la pressione finale sarà:",
        "options": {"A": "P_f = P₀", "B": "P_f = P₀ / 2", "C": "P_f = P", "D": "P_f = 2 P₀", "E": "P_f = 4 P₀"},
    },
    "FIS-C05-NCOM-090": {
        "question": "Qual è il numero di moli di O₂ e di He di una miscela gassosa formata per il 70% da O₂ e per il restante 30% da He, contenuta in una bombola da 122 litri a una temperatura di 37 °C e a una pressione di 73 atm?",
        "options": {"A": "48 e 30", "B": "245 e 105", "C": "171 e 74", "D": "70 e 30", "E": "73 e 32"},
    },
    "FIS-C05-NCOM-109": {
        "question": "Gli urti, che nei gas ideali vengono supposti come perfettamente elastici, determinano un continuo trasferimento di energia cinetica da una molecola all'altra; ne consegue che, in un determinato istante, le molecole non posseggono tutte lo stesso valore di energia cinetica. Mediante calcoli statistici è possibile dimostrare che i valori dell'energia cinetica in un sistema contenente un gran numero di molecole sono distribuiti intorno ad un valore medio E_m, dipendente esclusivamente dalla temperatura assoluta, a cui è direttamente proporzionale; la statistica dimostra che, se il numero di molecole del sistema è sufficientemente elevato, è del tutto lecito sostituire alla popolazione reale delle molecole con valori individuali dell'energia cinetica una popolazione ideale in cui tutte le molecole posseggono il valore E_m. Quale delle seguenti informazioni non può essere dedotta dalla lettura del brano precedente?",
        "options": {"C": "Se la temperatura assoluta raddoppia, raddoppia anche il valore di E_m"},
    },
    "FIS-C06-COMM-002": {
        "explanation": "Per la prima legge di Ohm si ha: I = ΔV / R = 100 V / 50 Ω = 2 A.",
    },
    "FIS-C06-COMM-011": {
        "question": "Siano date 3 resistenze elettriche, ohmiche, poste in parallelo. Due di esse valgano 10 Ω, la terza valga 1 MΩ. La resistenza equivalente vale:",
        "options": {"A": "circa 5 Ω", "B": "circa 10 Ω", "C": "circa 1 MΩ", "D": "circa 1/20 MΩ", "E": "circa 2/10 Ω"},
        "explanation": "In un collegamento in parallelo: 1/R_eq = 1/R₁ + 1/R₂ + 1/R₃ = 1/10 + 1/10 + 1/10⁶ ≈ 0,2 Ω⁻¹, da cui R_eq ≈ 5 Ω.",
    },
    "FIS-C06-COMM-028": {
        "explanation": "La carica positiva genera un campo elettrico che diminuisce al crescere della distanza. Indicando con E_p l'energia potenziale elettrica di una carica di prova q in un punto, si definisce il potenziale elettrico V = E_p / q. Il potenziale, come l'energia potenziale, è una grandezza scalare.",
    },
    "FIS-C06-COMM-029": {
        "question": "Siano date 2 resistenze elettriche (ohmiche) R_a e R_b, con R_b > R_a ≠ 0. Quando poste in serie la resistenza equivalente valga R_s; quando poste in parallelo la resistenza equivalente valga R_p. Quale tra le seguenti relazioni è possibile?",
        "options": {"A": "R_s = R_p", "B": "R_s < R_b", "C": "R_b < R_p", "D": "R_s > R_p", "E": "R_p > R_a"},
        "explanation": "La resistenza equivalente in serie (R_s = R_a + R_b) è maggiore di ciascuna resistenza, mentre in parallelo è minore di ciascuna resistenza; pertanto risulta sempre R_s > R_p.",
    },
    "FIS-C06-COMM-030": {
        "explanation": "Collegando tre lampadine identiche (resistenza R) in parallelo alla stessa tensione V, ciascuna è attraversata dalla stessa corrente I = V/R e la corrente totale vale I_tot = 3I (R_eq = R/3). La potenza totale dissipata per effetto Joule è P_tot = V² / R_eq = 3(V²/R) = 3P₁: la luce emessa complessivamente è quindi tripla rispetto a una singola lampadina, ma anche l'energia elettrica consumata a parità di tempo (in kWh, dove 1 kWh = 3,6 × 10⁶ J) e la spesa triplicano.",
    },
    "FIS-C06-COMM-031": {
        "question": "Ai morsetti A e B della resistenza R è applicata una differenza di potenziale V_AB ed è quindi percorsa da una corrente I₁ (Figura). Una uguale differenza di potenziale V_CD = V_AB è applicata ai morsetti C e D di due resistenze in parallelo, ciascuna pure di valore R, che sono percorse rispettivamente da due correnti I₂ e I₃. Quale delle seguenti affermazioni è ERRATA?",
        "options": {"A": "I₁ = I₂ = I₃", "E": "I₁ = I₂ + I₃"},
        "explanation": "La resistenza equivalente tra C e D vale R_CD = R/2 (opzione B vera). Essendo V_CD = V_AB, ciascun ramo in parallelo porta corrente I₂ = I₃ = V_AB/R = I₁ (opzione A vera), per cui la corrente totale tra C e D è I_CD = I₂ + I₃ = 2I₁ (opzione D vera) e la potenza dissipata tra A e B è metà di quella tra C e D (opzione C vera). È quindi falsa la relazione I₁ = I₂ + I₃.",
    },
    "FIS-C06-COMM-032": {
        "options": {"B": "Si accendono entrambe, ciascuna con intensità luminosa metà di quando accese da sole (una per volta)"},
    },
    "FIS-C06-COMM-034": {
        "question": "Dato il circuito in figura in cui R₁ = 10 Ω, R₂ = R₃ = 20 Ω, V_A = 10 V, V_B = 0, allora:",
        "options": {
            "A": "V_M = 5 V",
            "B": "le tre resistenze equivalgono a una resistenza totale di 30 Ω",
            "C": "V_M = (40/50) · 10 V",
            "D": "la potenza complessiva è 100/30 W",
            "E": "la corrente complessiva è 10/40 A",
        },
        "explanation": "Le resistenze R₂ e R₃ in parallelo equivalgono a R_23 = (20 × 20)/(20 + 20) = 10 Ω. La resistenza totale vale R_tot = R₁ + R_23 = 20 Ω e la potenza dissipata vale P = ΔV²/R_tot = 100 / 20 = 5 W. Poiché R₁ = R_23 = 10 Ω, la tensione tra A (10 V) e B (0 V) si ripartisce equamente, per cui nel nodo intermedio M si ha V_M = 5 V.",
    },
    "FIS-C06-COMM-037": {
        "explanation": "Il teorema di Gauss afferma che il flusso del campo elettrostatico attraverso una qualunque superficie chiusa S nel vuoto è dato dal rapporto tra la somma algebrica Q delle cariche interne a S e la costante dielettrica del vuoto ε₀: Φ(E) = Q / ε₀. Il flusso è quindi proporzionale alla carica totale racchiusa entro S.",
    },
    "FIS-C06-NCOM-011": {
        "question": "Tre cariche Q₁, Q₂ e Q₃ sono disposte su di una stessa retta. Se Q₁ = Q₂ = -Q₃, la forza che agisce su Q₃:",
        "options": {
            "C": "è nulla se Q₂ è in posizione intermedia tra Q₁ e Q₃",
            "E": "è nulla se Q₃ è in posizione intermedia tra Q₁ e Q₂",
        },
    },
    "FIS-C06-NCOM-048": {
        "question": "Si consideri una lastra di dimensioni molto maggiori rispetto alla distanza considerata dalla lastra stessa. Se la lastra è carica con una densità di carica superficiale +σ, cosa succede al campo elettrico generato dalla lastra al raddoppiare della distanza dalla lastra stessa?",
    },
    "FIS-C06-NCOM-089": {
        "question": "Ai morsetti di due resistenze R₁ e R₂ sono applicate, rispettivamente, le differenze di potenziale elettrico V₁ e V₂. Si sa che R₁ vale due volte R₂ e inoltre V₁ vale un mezzo di V₂. Che relazione c'è tra le potenze P₁ e P₂ dissipate rispettivamente da R₁ e R₂ per effetto Joule?",
        "options": {
            "A": "P₁ = (1/8) P₂",
            "B": "P₁ = (1/4) P₂",
            "C": "P₁ = (4) P₂",
            "D": "P₁ = (8) P₂",
            "E": "P₁ è uguale a P₂",
        },
    },
    "FIS-C06-NCOM-091": {
        "options": {
            "A": "I = 4 A; R = 55 ohm",
            "B": "I = 9 A; R = 50 ohm",
            "C": "I = 4 A; R = 880 ohm",
            "D": "I = 0,25 A; R = 55 ohm",
            "E": "I = 0,25 A; R = 880 ohm",
        },
    },
    "FIS-C06-NCOM-098": {
        "question": "Due fili cilindrici A e B di rame ugualmente lunghi sono percorsi dalla stessa corrente elettrica. Il diametro del filo B è doppio di quello del filo A. Detta P_A la potenza dissipata dal filo A per effetto Joule e P_B la potenza dissipata dal filo B:",
        "options": {"A": "P_B = P_A / 8", "B": "P_B = P_A / 2", "C": "P_B = P_A / 4", "D": "P_B = 4 P_A", "E": "P_B = 2 P_A"},
    },
    "FIS-C06-NCOM-104": {
        "question": "La differenza di potenziale elettrico ai capi di una lampadina è costante e pari a 100 V. Per un periodo di tempo pari a 1000 s la lampadina assorbe una potenza elettrica di 160 W. Sapendo che la carica dell'elettrone è 1,60 × 10⁻¹⁹ C, quanti elettroni si può ritenere abbiano attraversato una sezione trasversale del filo che alimenta la lampadina nell'intervallo di tempo considerato?",
        "options": {"A": "10⁻¹⁶", "B": "6,02 · 10²³", "C": "10²²", "D": "10²³", "E": "1,60 · 10²²"},
    },
    "FIS-C06-NCOM-135": {
        "question": "Sia R₁ la resistenza equivalente ad una connessione di tre resistenze uguali di valore x di cui una è connessa in serie con le altre due connesse in parallelo; sia R₂ la resistenza equivalente ad una connessione di tre resistenze uguali di valore y di cui una è connessa in parallelo con le altre due connesse in serie. Quale relazione deve intercorrere fra x e y in modo che R₁ = R₂?",
        "options": {"A": "x = 4y/9", "B": "y = 4x/9", "C": "y = x", "D": "y = 3x/2", "E": "x = 3y/2"},
    },
    "FIS-C06-NCOM-149": {
        "question": "Tre resistenze in serie R = R₁, R = R₂, R = R₃ equivalgono ad un'unica resistenza R pari a:",
        "options": {
            "A": "R = 1/R₁ + 1/R₂ + 1/R₃",
            "B": "R = R₁·R₂ + R₁·R₃ + R₂·R₃",
            "C": "R = R₁ + R₂ + R₃",
            "D": "R = R₁ · R₂ · R₃",
            "E": "R = R₁ - R₂ - R₃",
        },
    },
    "FIS-C06-NCOM-152": {
        "question": "Si consideri il ramo di circuito mostrato in figura, ai capi A e B del quale è applicata una differenza di potenziale pari a V. Se ciascuno dei sei resistori esprime una resistenza pari ad R, quanto vale la resistenza equivalente tra i due punti A e B del ramo di circuito?",
    },
    "FIS-C06-NCOM-182": {
        "question": "Un filo elettrico nel vuoto (costante di permeabilità magnetica μ₀) è percorso da una corrente I e genera un campo magnetico B. Una carica elettrica +q si muove ad una distanza r dal filo con velocità costante v, in una direzione parallela al filo e con verso concorde a quello della corrente che attraversa il filo. La carica +q è soggetta ad una forza F. Quale delle seguenti affermazioni è FALSA?",
        "options": {
            "A": "Il modulo della forza avvertita dalla carica vale F = μ₀qvI / (2πr)",
            "D": "Se la carica fosse ferma, il modulo della forza F da essa avvertita sarebbe nullo",
            "E": "Il campo magnetico generato dal filo ha modulo B = μ₀I / (2πr)",
        },
    },
    "FIS-C06-NCOM-192": {
        "options": {"A": "si creerà una corrente indotta se e solo se lo sperimentatore avrà cura di seguire le linee del campo magnetico terrestre"},
    },
    "FIS-C06-COMP-102": {"question": "La forza magnetica su un filo percorso da corrente è F = I L × _____ ."},
    "FIS-C06-COMP-124": {"question": "L'espressione per la f.e.m. autoindotta è ε = - L dI / _____ ."},
    "FIS-C07-COMM-004": {
        "explanation": "Il potere penetrante dei raggi X aumenta all'aumentare della loro energia E = h·f, direttamente proporzionale alla frequenza f della radiazione.",
    },
    "FIS-C07-COMM-014": {
        "explanation": "Una lente convergente è più sottile ai bordi che al centro e fa convergere un fascio di raggi paralleli nel fuoco immagine: sovrapponendo un raggio di luce rossa e uno di luce verde si ottiene luce gialla (sintesi additiva). Nelle lenti reali si osserva tuttavia una lieve aberrazione cromatica dovuta alla dispersione dell'indice di rifrazione con la frequenza.",
    },
    "FIS-C07-NCOM-015": {
        "question": "La distanza focale del sistema ottico formato da due lenti sottili a contatto (1 e 2), le cui rispettive distanze focali sono f₁ e f₂, è:",
        "options": {
            "A": "f₁ + f₂",
            "B": "(f₁ + f₂) / (f₁ · f₂)",
            "C": "(f₁ · f₂) / (f₁ + f₂)",
            "D": "1/f₁ + 1/f₂",
            "E": "f₁ · f₂",
        },
    },
    "FIS-C07-NCOM-050": {
        "question": "Un fascio coerente di luce monocromatica incide perpendicolarmente su un diaframma con una fenditura. Su uno schermo parallelo al diaframma si produce una figura di diffrazione la cui distribuzione di intensità è rappresentata dalla figura seguente. Cosa avviene se si riduce la larghezza della fenditura?",
    },
}
