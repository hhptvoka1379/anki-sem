# -*- coding: utf-8 -*-
A = {}
def m(qid, letter, conf, reason, flags=None):
    A[qid] = dict(kind='mcq', letter=letter, conf=conf, reason=reason, flags=flags or [])
def c(qid, answers, conf, reason, flags=None):
    A[qid] = dict(kind='cloze', answers=answers, conf=conf, reason=reason, flags=flags or [])

# ---------------- CHIMICA C7 ----------------
m('CHIM-C07-COMM-004','E','medium',
  "In una neutralizzazione l'equivalente di acido (una mole di H⁺) reagisce con l'equivalente di base (una mole di OH⁻) di pari forza. Il rapporto è quindi in equivalenti, non in grammi né in moli di sostanza, perché una mole di un acido diprotico fornisce due equivalenti.")
m('CHIM-C07-COMM-012','A','high',
  "L'etanolo CH₃CH₂OH ha C1 legato a O (−1), l'aldeide CH₃CHO ha C1 con doppio legame a O e legame a C (+1), l'acido acetico CH₃COOH ha C1 con tre legami verso atomi più elettronegativi (+3). Il numero di ossidazione aumenta, quindi C1 si ossida.",
  ['needs_figure'])
m('CHIM-C07-NCOM-018','C','high',
  "I coefficienti stechiometrici indicano quante moli (o molecole) di ciascun reagente e prodotto partecipano alla reazione, garantendo il bilancio degli atomi. Non si riferiscono a grammi o millilitri, che dipendono dalle masse molari e dalla densità.")

# ---------------- CHIMICA C9 ----------------
m('CHIM-C09-COMM-003','C','high',
  "Nella semireazione Mn²⁺ + 2e⁻ → Mn lo ione manganese acquista due elettroni e il suo numero di ossidazione scende da +2 a 0: si riduce, comportandosi da ossidante. L'ossidazione consiste invece nella perdita di elettroni.")
m('CHIM-C09-NCOM-031','C','high',
  "Il fosforo è nel gruppo 15, quindi il numero di ossidazione massimo è +5 (pari al numero del gruppo); il valore inferiore di due unità è +3. Le due specie tipiche sono P(V) e P(III), come nei fosfati e nei fosfiti.")
m('CHIM-C09-NCOM-035','C','high',
  "La dissociazione di KBr in acqua separa gli ioni K⁺ e Br⁻ già presenti nel cristallo senza cambiare i numeri di ossidazione (+1 e −1). Tutte le altre trasformazioni sono scissioni o decomposizioni redox: l'acqua dà H₂ e O₂, HgO dà Hg e O₂, H₂O₂ dà O₂ e H₂O, l'NH₃ dà N₂ e H₂.")
m('CHIM-C09-NCOM-042','E','high',
  "I perossidi sono composti in cui l'ossigeno, con numero di ossidazione −1, forma un legame singolo O–O (gruppo perossidico –O–O–). Il legame caratteristico è quindi quello tra due atomi di ossigeno.")
m('CHIM-C09-NCOM-052','C','medium',
  "Nel bromo Br₂ il bromo ha numero di ossidazione 0 e nei bromuri è −1: si riduce. Il cloro passa da −1 (nei cloruri) a 0 (in Cl₂): si ossida. Il sodio resta +1 in entrambi i composti, quindi non si ossida né si riduce.")
m('CHIM-C09-NCOM-053','E','high',
  "L'ossidazione è la perdita di elettroni, con aumento del numero di ossidazione: il cadmio passa da Cd (0) a Cd²⁺. L'opzione inversa descrive una riduzione.")
m('CHIM-C09-NCOM-056','A','high',
  "Un elemento che funge da riducente cede elettroni e per questo si ossida, facendo ridurre l'altra specie. Aumentando il suo numero di ossidazione, non lo diminuisce e non acquista elettroni.")
m('CHIM-C09-NCOM-060','B','high',
  "In 2 HBr il bromo ha numero di ossidazione -1 e in Br2 passa a 0: perde elettroni e si ossida. Lo iodio in I2 ha numero di ossidazione 0 e in HI passa a -1: acquista elettroni e si riduce. Il potassio non compare tra i reagenti, quindi le opzioni che lo citano sono da scartare.")
m('CHIM-C09-NCOM-076','B','high',
  "Nella semireazione Ag⁺ + e⁻ → Ag lo ione argento acquista un elettrone e il numero di ossidazione scende da +1 a 0: Ag⁺ si riduce e funge da ossidante. Un riducente, al contrario, cederebbe elettroni.")

# ---------------- CHIMICA C10 ----------------
m('CHIM-C10-COMM-006','E','high',
  "Un sale si ottiene dalla reazione tra un ossido basico e un ossido acido, o tra un idrossido e un acido. Li₂O (ossido basico) e CO₂ (ossido acido) danno il carbonato Li₂CO₃. Al + O₂ dà un ossido, CaO + H₂O dà l'idrossido, Li + H₂O dà idrossido e idrogeno, FeO + K non porta a un sale.")
m('CHIM-C10-COMM-024','D','high',
  "Il nitrito ferrico contiene lo ione nitrito NO₂⁻ e lo ione ferrico Fe³⁺: si ottiene per neutralizzazione dell'acido nitroso HNO₂ con l'idrossido ferrico Fe(OH)₃. Con l'idrossido ferroso si otterrebbe il nitrito ferroso, con l'acido nitrico il nitrato.")
m('CHIM-C10-NCOM-017','B','high',
  "L'acido nitroso ha formula HNO₂, con azoto in stato di ossidazione +3; HNO₃ è l'acido nitrico (N +5), NO₂ è l'anidride nitrosa. La formula corretta è quindi HNO₂.")
m('CHIM-C10-NCOM-018','E','high',
  "L'anidride (ossido acido) corrispondente all'acido carbonico H₂CO₃ si ottiene per perdita di una molecola d'acqua: H₂CO₃ → H₂O + CO₂. La CO₂ è quindi l'anidride carbonica; CO è il monossido di carbonio, che non dà l'acido carbonico.",
  ['ambiguous'])
m('CHIM-C10-NCOM-020','C','high',
  "Nell'H₃PO₃ solo due atomi di idrogeno sono legati all'ossigeno e quindi ionizzabili; il terzo è legato direttamente al fosforo e non è acido. L'acido fosforoso è perciò diprotico.")
m('CHIM-C10-NCOM-080','A','high',
  "Lo ione perclorato deriva dall'acido perclorico HClO₄, in cui il cloro ha numero di ossidazione +7, e ha formula ClO₄⁻. ClO⁻ è l'ipoclorito, ClO₂⁻ il clorito, Cl⁻ lo ione cloruro.")
m('CHIM-C10-NCOM-096','E','high',
  "Il solfito d'ammonio è il sale dell'acido solforoso H₂SO₃ con l'ammoniaca: servono due ioni NH₄⁺ per bilanciare lo ione SO₃²⁻, quindi (NH₄)₂SO₃. La formula (NH₄)₂SO₄ è invece il solfato d'ammonio.")
m('CHIM-C10-NCOM-099','B','high',
  "Lo ione clorato deriva dall'acido clorico HClO₃, in cui il cloro ha numero di ossidazione +5, e ha formula ClO₃⁻. ClO₂⁻ è il clorito, ClO₄⁻ il perclorato e ClO⁻ l'ipoclorito.")

# ---------------- CHIMICA C11 ----------------
m('CHIM-C11-COMM-001','A','high',
  "Il brano dice che gli alcooli non si ionizzano in ioni ossidrile e «perciò» non hanno gusto amaro né consistenza scivolosa: questo implica che tali proprietà degli idrossidi metallici siano dovute agli ioni OH⁻. Non afferma che gli idrossidi non formino ossidrili, anzi li definisce composti ionici contenenti OH⁻.")
m('CHIM-C11-COMM-002','C','high',
  "Il brano afferma che nella soluzione di un idrossido solubile gli ioni OH⁻ sono sempre presenti, ma non esclude la presenza di ioni H₃O⁺, che derivano dall'autoprotolisi dell'acqua. Le altre affermazioni sono tutte deducibili dal testo.")
m('CHIM-C11-COMM-003','C','high',
  "Negli ossiacidi gli idrogeni acidi sono legati all'ossigeno, con legame covalente polare O–H facilmente ionizzabile. Non sono legati all'atomo centrale né con legame ionico, e l'atomo centrale è tipicamente un non-metallo.")
m('CHIM-C11-COMM-007','A','high',
  "Da pH 2 a pH 4 la concentrazione di H⁺ diminuisce di 100 volte; a volume di soluzione costante di soluto la concentrazione si riduce di 100 volte quando il volume diventa 100 volte maggiore. Partendo da 1 L occorrono quindi 100 L di soluzione finale.")
m('CHIM-C11-COMM-011','B','high',
  "Diluire una soluzione tampone del 10% non cambia il pH, perché il rapporto tra le concentrazioni di acido e base coniugata resta invariato (equazione di Henderson-Hasselbalch). Il potere tamponante però diminuisce, perché calano le moli per unità di volume disponibili a neutralizzare aggiunte di acido o base.")
m('CHIM-C11-COMM-017','C','high',
  "In una neutralizzazione un acido e una base si consumano a vicenda: se non sono di pari forza e in rapporto equivalente il pH finale non coincide con quello iniziale. Il pH finale è uguale a quello iniziale solo in casi particolari, quindi non «sempre».")
m('CHIM-C11-COMM-018','D','high',
  "Il potassio è un metallo alcalino molto reattivo: in acqua si ossida a K⁺ e riduce l'idrogeno dell'acqua, con produzione di KOH e di idrogeno gassoso secondo 2 K + 2 H₂O → 2 KOH + H₂. Non si forma ossigeno, e la soluzione diventa basica.")
m('CHIM-C11-COMM-019','C','high',
  "La relazione pH + pOH = 14 deriva dal prodotto ionico dell'acqua a 25 °C (K_w = 10⁻¹⁴) e vale per qualunque soluzione acquosa, acida, basica o neutra, perché in acqua i due ioni sono sempre presenti.")
m('CHIM-C11-COMM-020','A','high',
  "Secondo Brønsted-Lowry un acido è una specie che cede un protone. NH₄⁺ può solo donare il proprio H⁺ per dare NH₃, che non ha un protone acido da perdere; HPO₃²⁻, HPO₄²⁻ e HSO₄⁻ sono anfiprotici, e PO₃³⁻ può solo accettare protoni.")
m('CHIM-C11-COMM-021','E','high',
  "L'aggiunta di HCl, acido forte completamente dissociato, aumenta la concentrazione di H⁺: per il principio di Le Châtelier l'equilibrio di ionizzazione dell'acido acetico si sposta verso sinistra (effetto dello ione comune). L'acido acetico contribuisce in modo trascurabile alla concentrazione di H⁺, che è determinata dall'HCl.")
m('CHIM-C11-COMM-022','A','high',
  "Il pH è il logaritmo negativo della concentrazione di ioni H₃O⁺: più basso è il pH, maggiore è la concentrazione. Tra i valori proposti il più basso è 3,11, che corrisponde alla massima concentrazione di H₃O⁺.")
m('CHIM-C11-COMM-023','B','high',
  "Lo ione HCO₃⁻ è anfiproteico, ma la sua costante basica (K_b = K_w/K_a1 ≈ 2,3·10⁻⁸) prevale sulla costante acida (K_a2 ≈ 4,7·10⁻¹¹). La soluzione di NaHCO₃ è quindi debolmente basica, con pH intorno a 8,3.")
m('CHIM-C11-COMM-027','E','high',
  "A pH 2 la concentrazione di H⁺ è 10⁻² M: in 10 L ci sono 0,1 mol di H⁺, che richiedono 0,1 mol di NaOH, cioè 0,1 × 40 = 4 g. Il calcolo va fatto sulle moli, non sui grammi.")
m('CHIM-C11-COMM-028','A','high',
  "Se il pH scende da 7,4 a 7, la concentrazione di H⁺ aumenta: poiché il prodotto ionico dell'acqua resta costante, la concentrazione di OH⁻ deve diminuire. Le altre affermazioni non sono deducibili dal brano o sono contraddette dal testo.")
m('CHIM-C11-NCOM-007','C','high',
  "Un acido è una sostanza capace di cedere ioni H⁺ (definizione di Arrhenius) ovvero protoni (Brønsted-Lowry). La sola presenza di idrogeno non basta, e le altre opzioni descrivono basi o proprietà organolettiche.")
m('CHIM-C11-NCOM-009','C','high',
  "L'acido nitrico HNO₃ ha un solo idrogeno acido, legato all'ossigeno, e perciò è monoprotico: in acqua si dissocia in H⁺ e NO₃⁻ in un unico passaggio. Non è né biprotico né triprotico.")
m('CHIM-C11-NCOM-019','B','medium',
  "Una base è una specie che accetta un protone (Brønsted-Lowry) o che mette a disposizione una coppia di elettroni (Lewis): nessuna delle risposte elencate descrive questo comportamento, perché accettare elettroni o avere un orbitale vuoto sono proprietà di un acido. Il gusto amarognolo è una proprietà organolettica, non una definizione chimica.")
m('CHIM-C11-NCOM-051','E','high',
  "In soluzione acquosa vale K_w = [H⁺][OH⁻] = 10⁻¹⁴: se [OH⁻] = 10⁻³ mol/L, allora [H⁺] = 10⁻¹⁴/10⁻³ = 10⁻¹¹ mol/L. La soluzione è basica, con pH 11.")
m('CHIM-C11-NCOM-057','D','high',
  "Aggiungendo un acido aumenta la concentrazione di H⁺, quindi il pH diminuisce e la concentrazione di OH⁻ diminuisce per il prodotto ionico dell'acqua. La cartina al tornasole si colora di rosso, non di azzurro.")
m('CHIM-C11-NCOM-085','E','high',
  "HCl 0,1 N in 100 mL contiene 0,01 equivalenti, che vengono esattamente neutralizzati da 0,01 mol di NaOH: si ottiene una soluzione di NaCl, neutra, per cui il pH aumenta rispetto a quello iniziale dell'acido (da circa 1 a circa 7). L'aumento è dovuto alla riduzione della concentrazione di H⁺, cioè all'aumento degli ioni ossidrile.")
m('CHIM-C11-NCOM-090','D','high',
  "H₂SO₄ è un acido forte che cede due protoni: una soluzione 0,002 M fornisce 0,004 mol/L di H⁺. Il pH si calcola quindi come −log₁₀(0,004), che è circa 2,4.")
m('CHIM-C11-NCOM-170','D','medium',
  "L'aggiunta di NH₄Cl, sale che fornisce lo ione NH₄⁺ (acido coniugato dell'ammoniaca), sposta a sinistra l'equilibrio di protolisi dell'ammoniaca e aumenta la concentrazione di H⁺: il pH diminuisce rispetto alla soluzione di ammoniaca di partenza. Va notato che la miscela ottenuta è anche una soluzione tampone, quindi l'opzione E è in linea di principio vera.",
  ['multiple_correct'])
m('CHIM-C11-NCOM-171','B','high',
  "25 mL di NaOH 1 M contengono 0,025 mol di base, che richiedono 0,025 mol di HCl. L'opzione B (20 mL di HCl 1,25 M) contiene esattamente 0,025 mol; le altre danno quantità diverse (0,0375; 0,05; 0,0025; 0,0125 mol).")

# ---------------- CHIMICA C12-C13 ----------------
m('CHIM-C12-COMM-001','B','high',
  "Un atomo di carbonio asimmetrico (stereocentro) è legato a quattro gruppi diversi con ibridazione sp³, quindi geometria tetraedrica. Il fatto che sia legato agli stessi gruppi lo renderebbe non asimmetrico.")
m('CHIM-C12-COMM-002','A','medium',
  "L'attività ottica, cioè la capacità di deviare la luce polarizzata, richiede la presenza di un centro stereogeno: un atomo di carbonio con quattro gruppi diversi e ibridazione tetraedrica sp³. Le altre caratteristiche non sono né necessarie né sufficienti.")
m('CHIM-C12-COMM-023','B','high',
  "Il benzene è un aromatico e subisce reazioni di sostituzione elettrofila: nitrazione con HNO₃/H₂SO₄, alogenazione con Cl₂ e alchilazione con clorometano. L'addizione elettrofila non avviene perché distruggerebbe l'aromaticità.")
m('CHIM-C12-COMM-029','C','high',
  "È falsa l'affermazione che l'ossidazione di un alcol dia sempre chetone o aldeide: un alcol terziario, privo di idrogeno sul carbonio ossidrilico, non si ossida in condizioni blande. Gli alcoli primari danno aldeidi e poi acidi carbossilici, i secondari chetoni.")
m('CHIM-C12-COMM-033','A','high',
  "La formula (CH₃CH₂)₂O è il dietil etere: presenta un atomo di ossigeno legato a due gruppi alchilici, che è la struttura generale degli eteri (R–O–R). Non è un estere, che ha formula R–COO–R.")
m('CHIM-C12-COMM-036','A','high',
  "Un'ammina terziaria ha tre gruppi alchilici legati all'azoto: per una struttura minima servono almeno tre atomi di carbonio, uno per ciascun gruppo metilico, come nella trimetilammina. Non bastano due atomi.")
m('CHIM-C12-NCOM-005','B','high',
  "Gli isomeri sono composti diversi che hanno la stessa formula molecolare (o grezza) ma diversa disposizione degli atomi. Proprietà e classe di appartenenza possono differire, quindi non ne fanno parte della definizione.")
m('CHIM-C12-NCOM-010','A','high',
  "L'isomeria si riferisce a molecole con la stessa formula molecolare ma diversa disposizione degli atomi; il caso descritto è quello in cui, sullo stesso scheletro, i sostituenti occupano posizioni diverse (isomeria di posizione). Le altre opzioni descrivono composti con formule diverse.")
m('CHIM-C12-NCOM-038','A','high',
  "L'idratazione degli alcheni per addizione di acqua secondo Markovnikov porta agli alcoli: l'OH si lega al carbonio più sostituito. Gli idrocarburi saturi (alcani) derivano invece dall'idrogenazione.")
m('CHIM-C12-NCOM-055','D','high',
  "Un eterociclo aromatico contiene un eteroatomo nell'anello e rispetta la regola di Hückel: la piridina, con sei elettroni π su un anello esatomico contenente azoto, ne è l'esempio classico. Il benzene è aromatico ma carbociclico; tetraidrofurano e cicloesene non sono aromatici.")
m('CHIM-C12-NCOM-059','D','high',
  "Nel propano tutti i legami C–C sono legami semplici, formati dalla sovrapposizione frontale di orbitali ibridi sp³: si tratta quindi di legami σ. Non ci sono doppi o tripli legami in un alcano.")
m('CHIM-C12-NCOM-108','C','high',
  "Negli alcani i carboni sono ibridati sp³ e formano tra loro solo legami semplici σ. Non ci sono legami π né legami dativi, perché tutti gli atomi sono saturi.")
m('CHIM-C13-NCOM-089','B','high',
  "I grassi sono esteri della glicerina con acidi grassi, cioè acilgliceroli (trigliceridi). Non sono carboidrati né peptidi né acidi carbossilici liberi.")
m('CHIM-C13-NCOM-104','E','high',
  "La struttura primaria di una proteina è la sequenza lineare degli amminoacidi, tenuta insieme esclusivamente dai legami peptidici. Legami a idrogeno, interazioni idrofobiche, ponti disolfuro e forze di van der Waals stabilizzano i livelli strutturali superiori.")
