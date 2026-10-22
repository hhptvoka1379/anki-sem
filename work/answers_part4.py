# -*- coding: utf-8 -*-
A = {}
def m(qid, letter, conf, reason, flags=None):
    A[qid] = dict(kind='mcq', letter=letter, conf=conf, reason=reason, flags=flags or [])
def c(qid, answers, conf, reason, flags=None):
    A[qid] = dict(kind='cloze', answers=answers, conf=conf, reason=reason, flags=flags or [])

# ---------------- BIOLOGIA C5 ----------------
m('BIO-C05-COMM-046','B','high',
  "La Na⁺/K⁺ ATPasi è una pompa elettrogena che per ogni ATP idrolizzato espulsa 3 Na⁺ e introduce 2 K⁺, contro i rispettivi gradienti. Il bilancio è quindi 3 Na⁺ fuori e 2 K⁺ dentro, con una netta uscita di cariche positive.")
m('BIO-C05-COMM-087','E','high',
  "La sindrome di Zellweger è un disordine dei perossisomi dovuto a difetti dei recettori Pex5/Pex7 e delle proteine di importazione: gli enzimi perossisomiali non entrano nell'organello e i perossisomi risultano vuoti o assenti. Non è un difetto della β-ossidazione mitocondriale né della catalasi in sé.")
m('BIO-C05-COMM-101','C','high',
  "La clatrina forma rivestimenti vescicolari nelle endocitosi mediata da recettore e nel trasporto dal TGN verso gli endosomi e i lisosomi. Il trasporto retrogrado Golgi→RE utilizza invece le proteine COPI e il RE→Golgi le COPII.")
m('BIO-C05-NCOM-174','E','high',
  "Le GTPasi della superfamiglia Ras coinvolte nel traffico vescicolare sono le proteine Rab, che identificano la membrana bersaglio e regolano la fusione, e Ran, che controlla il trasporto nucleo-citoplasmatico. Actina, fibrina ed elastina sono proteine strutturali.")
m('BIO-C05-NCOM-182','B','high',
  "Nel citoplasma NF-κB è legato all'inibitore IκB; lo stimolo porta alla degradazione di IκB e all'esposizione della sequenza NLS, per cui NF-κB viene riconosciuto dall'importina e traslocato nel nucleo attraverso i pori. L'esportina media il trasporto inverso.")
m('BIO-C05-NCOM-189','C','high',
  "Nel trasporto nucleare classico l'importina α riconosce la sequenza NLS del carico e funziona da adattatore, mentre l'importina β interagisce con le nucleoporine e trasporta il complesso attraverso il poro. RanGAP e RanGEF regolano il ciclo di Ran, non l'adattamento del segnale.")
m('BIO-C05-NCOM-270','C','high',
  "Nella catena respiratoria l'ossigeno è l'accettore finale degli elettroni e viene ridotto ad acqua nel complesso IV. NAD⁺, FAD e coenzima Q sono trasportatori intermedi, il citocromo c è un trasportatore mobile tra i complessi III e IV.")
m('BIO-C05-NCOM-273','C','high',
  "Il complesso II (succinato deidrogenasi) trasferisce gli elettroni al coenzima Q senza accoppiare il trasferimento al pompaggio di protoni. I complessi I, III e IV sono invece pompe protoniche e l'ATP sintasi sfrutta il gradiente per sintetizzare ATP.")

# ---------------- BIOLOGIA C6 ----------------
m('BIO-C06-COMM-011','C','high',
  "Le caderine sono proteine transmembrana calcio-dipendenti che mediano l'adesione omofilica, cioè tra cellule che espongono la stessa caderina. Le integrine mediano l'adesione alla matrice e le selectine quella eterofilica con i carboidrati.")
m('BIO-C06-COMM-014','E','high',
  "Le giunzioni aderenti ancorano i fasci di actina del citoscheletro a quelli delle cellule adiacenti, attraverso le caderine. I desmosomi collegano invece i filamenti intermedi e le giunzioni comunicanti mettono in contatto i citoplasmi.")
m('BIO-C06-COMM-028','E','high',
  "L'ossido nitrico è un gas piccolo e lipofilo che attraversa liberamente le membrane e diffonde rapidamente alle cellule vicine senza bisogno di trasportatori o recettori di superficie. Questa proprietà ne fa un messaggero paracrino a vita breve.")
m('BIO-C06-COMM-032','D','high',
  "Le proteine G eterotrimeriche sono formate dalle tre subunità α, β e γ, con la subunità α dotata di attività GTPasica. Le altre opzioni indicano un numero o una combinazione errata di subunità.")
m('BIO-C06-COMM-036','C','high',
  "Il cAMP è il secondo messaggero classico prodotto dall'adenilato ciclasi e capace di attivare la proteina chinasi A. Insulina è un ormone, la tirosina chinasi è un recettore o un enzima, GEF è un fattore di scambio dei nucleotidi.")
m('BIO-C06-COMM-040','D','high',
  "Le proteine G trimeriche vengono attivate dai recettori accoppiati a proteine G (GPCR), mentre le monomeriche servono tipicamente i recettori tirosin-chinasici. Entrambe legano GDP/GTP e hanno regolatori, per cui le altre opzioni sono errate.")
m('BIO-C06-NCOM-043','D','high',
  "Le CAM comprendono più famiglie: caderine, integrine, selectine e membri della superfamiglia delle immunoglobuline (Ig-CAM). Non si limitano quindi alle sole caderine, integrine, connessine o claudine.")
m('BIO-C06-NCOM-081','C','high',
  "La segnalazione sinaptica si distingue perché il neurotrasmettitore viene rilasciato nello spazio sinaptico e agisce su recettori della cellula postsinaptica in tempi molto brevi e a brevissima distanza. Le molecole segnale non restano ancorate alla membrana e il segnale non è ormonale a lunga distanza.")
m('BIO-C06-NCOM-104','B','high',
  "L'ossido nitrico diffonde nella cellula bersaglio e attiva la guanilil ciclasi solubile, che produce GMP ciclico e attiva la proteina chinasi G. Non agisce su recettori tirosin-chinasici né su integrine o complessi di trasporto.")

# ---------------- BIOLOGIA C7 ----------------
m('BIO-C07-COMM-007','D','high',
  "Per funzionare in mitosi un cromosoma artificiale deve contenere DNA, istoni per l'impacchettamento e un centromero per l'attacco al fuso e la segregazione. I telomeri proteggono le estremità ma non sono indispensabili per una singola divisione, e i centrioli non fanno parte del cromosoma.")
m('BIO-C07-COMM-010','E','high',
  "Nella via estrinseca dell'apoptosi il recettore di morte Fas (CD95) lega il ligando FasL e recluta la caspasi-8 attraverso il dominio FADD. EGFR, InsR e Notch sono recettori di crescita o differenziamento, non recettori di morte.")
m('BIO-C07-COMM-021','A','high',
  "Ogni spermatocita di primo ordine completa la meiosi producendo quattro spermatidi, che maturano in altrettanti spermatozoi. Per ottenere 4·10⁸ spermatozoi servono quindi 10⁸ spermatociti di primo ordine.")
m('BIO-C07-COMM-036','C','high',
  "Il complesso APC/C è una ubiquitina ligasi che poliubiquitina la ciclina B e la securina, destinandole alla degradazione proteasomiale. Questo spegne l'attività di Cdk1 e libera la separasi, consentendo la transizione metafase-anafase.")
m('BIO-C07-COMM-042','D','high',
  "APC/C determina la poliubiquitinazione e la degradazione della ciclina B, quindi la dissociazione e l'inattivazione del complesso Cdk1-ciclina B: è la cessazione dell'attività necessaria all'uscita dalla mitosi. Non fosforila Cdk1 né ne aumenta la sintesi.")
m('BIO-C07-COMM-045','E','high',
  "Se il solco di divisione si forma in posizione eccentrica, il citoplasma viene ripartito in modo diseguale e si generano due cellule figlie di dimensioni diverse. Il caso estremo di citodieresi incompleta dà una cellula multinucleata, ma non è la conseguenza della sola eccentricità.")
m('BIO-C07-COMM-053','A','high',
  "p21 è un inibitore delle Cdk: si lega ai complessi ciclina-Cdk (soprattutto ciclina E/A-Cdk2 e ciclina D-Cdk4/6) e ne blocca l'attività, impedendo la fosforilazione di Rb e la progressione G1/S. Non fosforila Rb né attiva E2F.")
m('BIO-C07-COMM-058','A','high',
  "Il crossing-over avviene durante il pachitene della profase I, quando i cromosomi omologhi sono appaiati nei bivalenti e i cromatidi non fratelli si scambiano segmenti corrispondenti. Nelle fasi successive i chiasmi restano visibili ma lo scambio è già avvenuto.")
m('BIO-C07-COMM-069','B','high',
  "Le caspasi iniziatrici sono la caspasi-8, attivata dai recettori di morte nella via estrinseca, e la caspasi-9, attivata dal citocromo c nella via intrinseca. Le caspasi 3 e 7 sono esecutrici.")
m('BIO-C07-COMM-070','B','high',
  "Le caspasi esecutrici sono la caspasi-3 e la caspasi-7, che degradano i substrati cellulari causando il fenotipo apoptotico. Le caspasi 8 e 9 sono invece iniziatrici.")
m('BIO-C07-NCOM-009','D','high',
  "Il ciclo cellulare procede con G1 (crescita), S (duplicazione del DNA), G2 (ulteriore crescita e controlli) e M (mitosi e citodieresi). L'ordine corretto è quindi G1, S, G2, M.")
m('BIO-C07-NCOM-022','D','high',
  "La meiosi presenta due divisioni successive e quindi due separazioni dei cromatidi, l'anafase I e l'anafase II. La mitosi ha una sola anafase; l'interfase è comune a entrambi i processi.")
m('BIO-C07-NCOM-024','B','high',
  "L'interfase è la fase tra due divisioni e comprende G1, S e G2, durante le quali la cellula cresce e duplica il DNA. Non comprende la fase M, che è la divisione vera e propria.")
m('BIO-C07-NCOM-029','D','high',
  "Le fibre del fuso si attaccano ai cromosomi a livello del cinetocore, struttura che si assembla sul centromero. Telomeri, costrizioni secondarie e organizzatori del nucleolo hanno altre funzioni.")
m('BIO-C07-NCOM-153','C','high',
  "Il checkpoint della transizione metafase-anafase verifica che tutti i cromosomi siano allineati sulla piastra metafasica e correttamente legati al fuso prima di consentire la separazione dei cromatidi. I checkpoint G1/S e G2/M controllano rispettivamente l'ingresso in S e in M.")
m('BIO-C07-NCOM-188','D','high',
  "Le cellule germinali primordiali (PGC) esprimono i fattori di pluripotenza Blimp1 (Prdm1) e Prdm14, che reprimono il programma somatico e mantengono il destino germinale. Sox9 e Sry sono implicati nella determinazione del sesso, non nell'identità delle PGC.")
m('BIO-C07-NCOM-201','D','high',
  "Le cellule staminali sono importanti nella medicina rigenerativa per la loro capacità di autorinnovarsi e di differenziarsi in diversi tipi cellulari, potendo riparare tessuti danneggiati. Non sono geneticamente instabili né producono solo gameti.")
c('BIO-C07-COMP-056',['G0'],'high',
  "In assenza di fattori di crescita la cellula esce dal ciclo e entra nello stato quiescente G0, in cui non si divide ma resta metabolicamente attiva.")
c('BIO-C07-COMP-074',['Blimp1'],'high',
  "Il destino germinale è guidato dai fattori Blimp1 (Prdm1) e Prdm14, che reprimono il programma somatico e stabiliscono l'identità delle cellule germinali primordiali.")
c('BIO-C07-COMP-077',['profase I'],'high',
  "La profase I della meiosi è molto lunga e si suddivide in leptotene, zigotene, pachitene, diplotene e diacinesi, tappe in cui avvengono appaiamento, crossing-over e condensazione dei cromosomi.")
c('BIO-C07-COMP-090',['meiosi II'],'high',
  "Nella femmina l'ovocita resta bloccato in metafase II e completa la seconda divisione meiotica solo al momento della fecondazione, quando lo spermatozoo innesca la ripresa del ciclo.")
