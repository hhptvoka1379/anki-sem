# -*- coding: utf-8 -*-
# Answers chosen per id: letter. Reasoning + confidence written separately.
A = {}
def m(qid, letter, conf, reason, flags=None):
    A[qid] = dict(kind='mcq', letter=letter, conf=conf, reason=reason, flags=flags or [])
def c(qid, answers, conf, reason, flags=None):
    A[qid] = dict(kind='cloze', answers=answers, conf=conf, reason=reason, flags=flags or [])

# ---------------- CHIMICA C1 ----------------
m('CHIM-C01-NCOM-003','C','high',
  "Un liquido che bolle a 68 °C alla pressione atmosferica ha punto di ebollizione ben al di sotto dei 100 °C dell'acqua e comunque sopra la temperatura ambiente: a 25 °C è quindi liquido. In condizioni standard (25 °C, 1 atm) non può essere un gas. Le altre opzioni escludono stati che invece sono compatibili; l'unica certezza è che non è aeriforme.")
m('CHIM-C01-NCOM-097','E','high',
  "Gli isotopi dello stesso elemento hanno identico numero atomico (Z = 53 per lo iodio) e differiscono solo per il numero di neutroni: ¹²⁷I ha 74 neutroni, ¹³¹I ne ha 78, quindi il primo ha 4 neutroni in meno. Protoni ed elettroni restano uguali, per cui le opzioni che parlano di protoni o elettroni sono errate.")
m('CHIM-C01-NCOM-107','A','high',
  "La massa atomica relativa è la media ponderata delle masse degli isotopi in base alla loro abbondanza naturale. Poiché la maggior parte degli elementi è una miscela isotopica, tale media non è un numero intero. La massa dell'elettrone è trascurabile e la presenza di protoni ed elettroni non incide sulla massa in modo significativo.",
  ['needs_figure'])
# ---------------- CHIMICA C2 ----------------
m('CHIM-C02-COMM-002','D','high',
  "Una mole di O₂ ha massa molare 32 g/mol: quindi una mole pesa 32 g. Una singola molecola pesa 32 u (≈5,3·10⁻²³ g), non 32 g, e il volume di 22,414 L spetta a una mole, non a una molecola. L'opzione C è quindi errata nella quantità di sostanza indicata.")
m('CHIM-C02-COMM-007','D','high',
  "N₂ ha massa molare 2 × 14 = 28 g/mol, perciò una mole pesa 28 g. Una singola molecola pesa 28 u e 28 moli pesano 784 g, non 1 g. Il volume di 22,414 L in condizioni standard spetta a una mole, non a una molecola.")
m('CHIM-C02-NCOM-001','C','high',
  "Il modello di Bohr postula orbite stazionarie a energia e momento angolare quantizzati (L = nħ) e costanti, senza emissione; la radiazione è emessa o assorbita solo nelle transizioni tra orbite. Il momento angolare non è nullo ma multiplo intero di ħ, e non può assumere valori arbitrari.")
m('CHIM-C02-NCOM-012','E','high',
  "Il numero quantico magnetico m_l dipende dal numero quantico secondario l, che a sua volta è determinato da n: m_l assume i 2l+1 valori interi da −l a +l. Quindi dipende sia da n sia da l, e può essere zero.")
m('CHIM-C02-NCOM-014','B','high',
  "Il numero quantico principale è un intero positivo: n = 1, 2, 3, … senza limite superiore, quindi non può essere nullo, frazionario o negativo. Da ciò derivano le dimensioni e le energie degli orbitali.")
m('CHIM-C02-NCOM-021','B','high',
  "Il numero di orbitali per un dato n è n² (somma dei 2l+1 orbitali per ciascun l da 0 a n−1), non n³: n³ è invece il numero di orbitali se si conta anche il doppio valore di spin. Le altre affermazioni sono corrette: l va da 0 a n−1, n è intero positivo, m_s assume due valori e m_l descrive l'orientazione.")
m('CHIM-C02-NCOM-035','A','high',
  "Nel terzo periodo si riempiono prima gli orbitali 3s e poi i 3p, secondo l'ordine di energia crescente (regola della diagonale); il 3d è a energia più alta e si popola solo nel quarto periodo. Per questo gli elementi del terzo periodo hanno configurazione 3s → 3p.")
m('CHIM-C02-NCOM-037','C','high',
  "L'ordine di riempimento segue l'energia crescente degli orbitali: 5s < 5p < 5d e 5s < 6s < 6p. Tra 6p, 6s, 5s, 5p e 5d, l'orbitale a energia più bassa e quindi occupato per primo è il 5s.")
# ---------------- CHIMICA C3 ----------------
m('CHIM-C03-COMM-003','A','high',
  "Passando da un elemento al successivo nella tavola periodica Z aumenta di una unità: l'atomo guadagna un protone e, per restare neutro, un elettrone. Il numero di neutroni varia in modo irregolare e non è definito dal semplice avanzamento nella tavola.")
m('CHIM-C03-COMM-008','A','high',
  "Carbonio e silicio sono nello stesso gruppo (gruppo 14, IV gruppo) e quindi hanno la stessa configurazione dello strato di valenza (ns²np²): quattro elettroni nell'ultimo livello. Appartengono a periodi diversi e non sono entrambi metalli.")
m('CHIM-C03-COMM-016','D','high',
  "Lungo un periodo il raggio atomico diminuisce da sinistra a destra perché aumenta la carica nucleare efficace a parità di strato: i gas nobili, all'estrema destra, hanno raggio minore del metallo alcalino dello stesso periodo. Gli alcalino-terrosi hanno energia di seconda ionizzazione maggiore della prima, il carattere metallico aumenta scendendo nel gruppo, i semimetalli non sono elementi di transizione e l'opzione E confonde l'elettronegatività con l'affinità elettronica.")
m('CHIM-C03-COMM-017','C','high',
  "Il fosforo appartiene al gruppo 15, quindi il numero di ossidazione massimo è +5; il valore inferiore di due unità è +3. I numeri di ossidazione tipici del fosforo sono perciò +5 e +3, come in P₄O₁₀ e P₄O₆.")
m('CHIM-C03-COMM-022','D','high',
  "Procedendo lungo un periodo da sinistra a destra l'elettronegatività aumenta con la carica nucleare efficace: l'elemento del sesto gruppo è quindi meno elettronegativo di quello del settimo. Per la stessa ragione ha carattere più metallico e raggio maggiore, non minore.")
m('CHIM-C03-NCOM-001','E','high',
  "L'unità di massa atomica è definita come 1/12 della massa dell'atomo di carbonio-12, cioè dell'isotopo con numero di massa 12, e non del carbonio naturale. La definizione con 1/16 dell'ossigeno è storica e superata.")
m('CHIM-C03-NCOM-012','B','high',
  "Il peso atomico è la media ponderata delle masse isotopiche secondo l'abbondanza naturale. Il cloro è una miscela di ³⁵Cl e ³⁷Cl, quindi il valore medio risulta 35,453 e non un numero intero. Il numero di protoni o neutroni di un singolo atomo non spiega la media.")
m('CHIM-C03-NCOM-019','B','high',
  "Il numero di moli è n = m/M = 64,132 g / 32,006 g·mol⁻¹ ≈ 2,00 mol. La massa molare va usata come fattore di conversione, non come risultato.")
m('CHIM-C03-NCOM-020','B','high',
  "La massa molare del cromo è 52 g/mol: n = 104 g / 52 g·mol⁻¹ = 2 moli. Il calcolo si imposta dividendo la massa per la massa molare dell'elemento.")
m('CHIM-C03-NCOM-033','D','high',
  "Volume, temperatura e pressione sono uguali, quindi per l'equazione di stato dei gas il numero di moli e di molecole è lo stesso. Le masse molari differiscono (64 vs 17 g/mol), per cui cambiano massa totale e numero di atomi presenti in ciascun pallone.")
m('CHIM-C03-NCOM-130','C','high',
  "Il simbolo chimico del fosforo è P, dal latino phosphorus; gli altri simboli proposti non esistono o indicano elementi diversi (Po è il polonio).")
m('CHIM-C03-NCOM-137','C','high',
  "Le prime tre energie di ionizzazione sono basse (578, 1817 e 2745 kJ/mol), poi la quarta balza a 11577 kJ/mol, circa quattro volte la terza: dopo aver strappato tre elettroni occorre molta più energia perché si intacca il guscio interno. L'elemento ha quindi tre elettroni di valenza e appartiene al gruppo 13; i valori corrispondono esattamente all'alluminio.",
  ['needs_figure'])
# ---------------- CHIMICA C4 ----------------
m('CHIM-C04-COMM-001','D','high',
  "Il brano afferma che i sali contenuti nel terreno agiscono da elettroliti, cioè sostanze capaci di dissociarsi in ioni in soluzione. Non dice che l'ammoniaca sia la causa principale, né che i gas formino correnti vaganti, né che nell'aria avvengano elettrolisi.")
m('CHIM-C04-COMM-008','C','high',
  "L'HCN ha struttura H–C≡N: un legame semplice (σ) tra H e C, un triplo legame (1 σ + 2 π) tra C e N. In totale si hanno quindi 2 legami σ e 2 legami π.")
m('CHIM-C04-COMM-011','A','high',
  "Nel legame metallico i cationi del reticolo sono immersi in un mare di elettroni di valenza delocalizzati, che li tengono uniti. Non ci sono ioni negativi, tipici dei composti ionici.")
m('CHIM-C04-COMM-019','E','high',
  "Il legame ionico si forma tra un elemento molto elettropositivo, che cede elettroni, e uno molto elettronegativo, che li acquista: K (metallo alcalino) e F (alogeno) sono la coppia tipica. He, Ne e Ar hanno l'ottetto completo e non formano legami ionici.")
m('CHIM-C04-NCOM-003','E','high',
  "La forza elettrostatica tra ioni di segno opposto dà origine a un reticolo cristallino tridimensionale, che si estende nelle tre direzioni dello spazio. Non si formano coppie isolate di ioni né molecole.")
m('CHIM-C04-NCOM-012','C','high',
  "Il triplo legame è formato da un legame σ, dovuto alla sovrapposizione frontale degli orbitali, e da due legami π, dovuti alla sovrapposizione laterale dei p. Lo stesso schema vale per l'azoto e l'acetilene.")
m('CHIM-C04-NCOM-014','E','high',
  "Quando due atomi si legano il sistema raggiunge uno stato a energia minore e libera energia verso l'esterno: l'energia di legame è appunto l'energia perduta dagli atomi nella formazione del legame, uguale a quella necessaria per romperlo. Le opzioni che parlano di energia «donata» o «acquistata» invertono il segno.")
m('CHIM-C04-NCOM-029','D','high',
  "In CCl₄ i quattro legami C–Cl sono polari, ma la geometria tetraedrica dispone i dipoli in modo simmetrico: la loro risultante è nulla e la molecola è apolare. La polarità dei singoli legami non è quindi sufficiente a rendere polare la molecola.")
m('CHIM-C04-NCOM-030','E','high',
  "Due atomi identici hanno la stessa elettronegatività, quindi condividono gli elettroni in modo simmetrico dando un legame covalente omopolare (puro). Il legame polare richiede una differenza di elettronegatività.")
m('CHIM-C04-NCOM-040','C','high',
  "Due atomi di azoto, con cinque elettroni di valenza ciascuno, mettono in comune tre coppie formando un triplo legame (N≡N): si tratta quindi di legami multipli, oltre che covalenti.")
m('CHIM-C04-NCOM-051','D','high',
  "Un composto binario è tanto più ionico quanto maggiore è la differenza di elettronegatività: un elemento del gruppo I (metallo alcalino) con uno del gruppo VII (alogeno) dà il caso tipico, come NaCl. Due non-metalli o due metalli danno invece legami covalenti o metallici, e un composto ionico conduce corrente allo stato fuso o in soluzione, non da solido.")
m('CHIM-C04-NCOM-056','C','high',
  "K è un metallo alcalino con bassa elettronegatività e Cl un alogeno molto elettronegativo: la grande differenza di elettronegatività rende il legame prevalentemente ionico. Fe–Fe, Se–O, Si–I e H–C hanno differenze troppo piccole o coinvolgono non metalli.")
m('CHIM-C04-NCOM-057','A','high',
  "Il legame covalente diventa polare quando gli atomi hanno elettronegatività diverse e la coppia di legame è spostata verso l'atomo più elettronegativo. Nell'acqua l'ossigeno è molto più elettronegativo dell'idrogeno, da cui la parziale carica negativa su O e positiva su H.")
m('CHIM-C04-NCOM-066','C','high',
  "Metano e ione ammonio hanno entrambi quattro coppie elettroniche attorno all'atomo centrale (C e N) e ibridazione sp³, quindi geometria tetraedrica. Non hanno proprietà acide o basiche spiccate in comune, né struttura planare.")
# ---------------- CHIMICA C5 ----------------
m('CHIM-C05-NCOM-025','D','high',
  "L'azoto è molto più elettronegativo del fosforo e l'NH₃ forma legami a idrogeno intermolecolari grazie all'H legato a N, mentre la PH₃ no: servono perciò più energia per separare le molecole di ammoniaca. Le due molecole hanno dimensioni e masse simili e sono entrambe covalenti.")
m('CHIM-C05-NCOM-042','E','high',
  "L'acqua è un solvente polare e dissolve meglio le sostanze polari o ioniche: NaCl è un sale ionico che si idrata e si dissocia. Grassi, benzina ed etere sono apolari e vi si sciolgono male; il sapone è anfipatico e forma micelle, non una vera soluzione.")
# ---------------- CHIMICA C6 ----------------
m('CHIM-C06-COMM-004','B','high',
  "n = 2 g / 40 g·mol⁻¹ = 0,05 mol; la molarità è M = n/V = 0,05 mol / 0,5 L = 0,1 M. Il calcolo richiede di convertire la massa in moli e di dividere per il volume in litri. Le altre opzioni riportano valori errati o unità di molalità.")
m('CHIM-C06-COMM-019','E','high',
  "Dal brano si deduce che le proteine hanno peso molecolare elevato e concentrazione molare bassissima, e che i sali danno la maggior parte della pressione osmotica (0,045 atm su 7,63 sono meno dell'1%). Non si può invece dedurre che anche i sali abbiano peso molecolare elevato: i sali hanno anzi massa molare piccola.")
m('CHIM-C06-NCOM-003','C','high',
  "n = 36 g / 180 g·mol⁻¹ = 0,20 mol in 0,5 L: M = 0,20 / 0,50 = 0,4 M. Il calcolo richiede di convertire la massa in moli e di dividere per il volume in litri.")
m('CHIM-C06-NCOM-006','B','high',
  "La molarità è moli di soluto per litro di soluzione: 5 mol / 10 L = 0,5 M. Non va confusa con la molalità, che si riferisce ai kg di solvente.")
m('CHIM-C06-NCOM-010','B','high',
  "La concentrazione molare si ottiene dividendo le moli per il volume in litri: A = 0,33 M, B = 0,125 M, C = 0,25 M, D = 1 M, E = 0,2 M. Il valore più basso è quello di B.")
m('CHIM-C06-NCOM-021','D','high',
  "La frazione molare è il rapporto tra le moli di un componente e le moli totali della soluzione: x_soluto = n_soluto / (n_soluto + n_solvente). Non coinvolge masse o grammi.")
m('CHIM-C06-NCOM-023','D','high',
  "Una soluzione 0,1 M contiene 0,1 mol di soluto per litro, cioè 0,0001 mol per millilitro. L'opzione con 0,001 mol in 100 mL corrisponde invece a 0,01 M, quella con 0,001 mol in 1 L a 0,001 M e quella con 0,1 mol in 100 mL a 1 M.")
m('CHIM-C06-NCOM-032','B','high',
  "La normalità si indica con N ed esprime il numero di equivalenti di soluto per litro di soluzione. M indica la molarità e m la molalità.")
m('CHIM-C06-NCOM-037','A','high',
  "La molarità è moli per litro di soluzione: 0,07 mol in 0,100 L danno 0,7 M. Le opzioni 0,07 M o 0,07 N riportano le moli senza convertirle in concentrazione.")
m('CHIM-C06-NCOM-038','D','medium',
  "A parità di volume e di molarità servono moli uguali, quindi le masse devono stare nel rapporto dei pesi molecolari 60:36. L'opzione con 60 × 10⁻² g di acido acetico e 36 × 10⁻² g di HCl dà 0,6 g e 0,36 g, cioè 0,01 mol di entrambi: le due soluzioni hanno la stessa molarità. Le altre opzioni danno rapporti o quantità diverse.",
  ['typo'])
m('CHIM-C06-NCOM-041','C','high',
  "Una soluzione 0,1 M contiene 0,1 mol per litro: in 100 mL ci sono 0,01 mol e in 1 mL 0,0001 mol. L'opzione con 0,1 mol in 100 mL corrisponde invece a una soluzione 1 M, quella con 0,001 mol in 1 L a 0,001 M.")
m('CHIM-C06-NCOM-044','E','high',
  "0,05 mol in 0,100 L danno 0,5 M. Le opzioni che riportano 0,05 M o 0,05 N ripropongono le moli senza dividerle per il volume.")
m('CHIM-C06-NCOM-057','D','high',
  "Aggiungendo solvente aumenta il volume a parità di soluto e la concentrazione diminuisce: la soluzione si diluisce. Il fenomeno non comporta necessariamente variazioni termiche rilevanti.")
m('CHIM-C06-NCOM-059','A','high',
  "Nella diluizione si conserva il numero di moli: M₁V₁ = M₂V₂, quindi V₂ = (6 M × 50 mL) / 0,2 M = 1500 mL. Il risultato è 1,5 L di soluzione finale.")
m('CHIM-C06-NCOM-070','E','high',
  "NaCl è un composto ionico che in acqua si dissocia negli ioni Na⁺ e Cl⁻ per idratazione. Non si formano NaOH e HCl né specie neutre indissociate.")
m('CHIM-C06-NCOM-088','E','high',
  "La pressione osmotica si indica con la lettera greca π, che non compare tra le opzioni proposte (M è la molarità, P la pressione generica, p un pedice). Nessuna delle risposte elencate riporta quindi il simbolo corretto.")
c('CHIM-C06-COMP-030',['non'],'high',
  "Un elettrolita che non produce ioni e non conduce corrente è un non elettrolita: le sue molecole restano indissociate in soluzione, come glucosio o urea.")
