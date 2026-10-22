# -*- coding: utf-8 -*-
A = {}
def m(qid, letter, conf, reason, flags=None):
    A[qid] = dict(kind='mcq', letter=letter, conf=conf, reason=reason, flags=flags or [])
def c(qid, answers, conf, reason, flags=None):
    A[qid] = dict(kind='cloze', answers=answers, conf=conf, reason=reason, flags=flags or [])

# ---------------- BIOLOGIA C1 ----------------
m('BIO-C01-NCOM-202','B','medium',
  "L'informazione genetica è scritta nella sequenza delle basi degli acidi nucleici; tra le opzioni proposte l'unico acido nucleico è l'RNA (il DNA non è elencato). Le proteine e gli enzimi sono i prodotti dell'espressione genica, non il supporto dell'informazione.")
m('BIO-C01-NCOM-216','B','high',
  "Per unire tre nucleotidi in catena servono due legami fosfodiesterici, ciascuno formato per condensazione con perdita di una molecola d'acqua. Il numero di reazioni di condensazione è quindi n−1 = 2.")
c('BIO-C01-COMP-114',['ossidante','riducente'],'high',
  "In una reazione redox l'agente ossidante acquista elettroni e si riduce, mentre l'agente riducente cede elettroni e si ossida. I due ruoli sono complementari e definiti dal trasferimento di elettroni.")

# ---------------- BIOLOGIA C2 ----------------
m('BIO-C02-NCOM-005','A','high',
  "In G2 della meiosi la cellula diploide ha il DNA duplicato, cioè 4C: poniamo Y = 4C. Con la prima divisione meiotica la quantità di DNA si dimezza, perché si separano i cromosomi omologhi: ogni cellula figlia, aploide, ha 2C pur avendo cromosomi con due cromatidi. In metafase II la quantità per cellula è quindi 2C = Y/2 = 0,5 Y.")
m('BIO-C02-NCOM-006','E','high',
  "Con un rapporto di compattazione di 1:10⁴ il filamento svolto è lungo 4 µm × 10⁴ = 40.000 µm. Poiché 1 cm = 10⁴ µm, 40.000 µm equivalgono a 4 cm, che è la conversione riportata nell'opzione corretta.")
m('BIO-C02-NCOM-111','A','high',
  "Gli istoni sono le proteine che impacchettano il DNA di nuova sintesi: vengono espressi soprattutto nella fase S, in stretta correlazione con la replicazione del DNA. Nelle altre fasi la loro sintesi è minima.")
m('BIO-C02-NCOM-117','B','high',
  "I centromeri contengono DNA satellite alfa (α-satellite), costituito da ripetizioni in tandem che formano l'eterocromatina centromerica e legano il cinetocore. LINE-1 e SINE Alu sono retrotrasposoni distribuiti nel genoma, non specifici dei centromeri.")
c('BIO-C02-COMP-001',['nucleo'],'high',
  "Il nucleo delle cellule eucariotiche è delimitato dall'involucro nucleare, una doppia membrana con pori che racchiude DNA, RNA e proteine.")
c('BIO-C02-COMP-007',['cariotipo'],'high',
  "Il cariotipo umano è l'insieme dei cromosomi di una cellula, 46 in totale, organizzati in 22 coppie di autosomi e una coppia di cromosomi sessuali.")
c('BIO-C02-COMP-009',['omologhi'],'high',
  "I cromosomi omologhi sono le due copie di ciascun cromosoma, una di origine materna e una paterna, con la stessa sequenza di geni ma possibili alleli diversi.")
c('BIO-C02-COMP-015',['telocentrici'],'high',
  "I cromosomi telocentrici hanno il centromero all'estremità e non sono presenti nel cariotipo umano, che comprende cromosomi metacentrici, submetacentrici e acrocentrici.")
c('BIO-C02-COMP-016',['attivi'],'medium',
  "I territori cromosomici sono regioni del nucleo in cui i cromosomi occupano posizioni non casuali; la loro localizzazione riguarda in particolare i cromosomi attivi, cioè quelli trascrizionalmente competenti, e contribuisce alla regolazione genica.")
c('BIO-C02-COMP-017',['nucleolo'],'high',
  "La costrizione secondaria è la regione in cui il DNA è meno condensato e contiene l'organizzatore del nucleolo, cioè i geni per l'rRNA attorno a cui si assembla il nucleolo.")
c('BIO-C02-COMP-018',['ripetute'],'high',
  "La variabilità del genoma eucariotico dipende non solo dalla quantità totale di DNA ma anche dalla frazione e distribuzione delle sequenze ripetute, che costituiscono gran parte del genoma.")

# ---------------- BIOLOGIA C3 ----------------
m('BIO-C03-COMM-016','B','high',
  "Il primo amminoacido della catena è quello N-terminale: il suo gruppo α-amminico non è impegnato in alcun legame peptidico e resta libero, mentre il gruppo carbossilico è già legato al secondo amminoacido. Il gruppo COOH libero si trova all'estremità C-terminale.")
m('BIO-C03-COMM-036','A','high',
  "Negli eucarioti l'RNA polimerasi II trascrive i geni per gli mRNA (e per alcuni snRNA). L'RNA polimerasi I sintetizza gli rRNA maggiori e la III i tRNA e l'rRNA 5S.")
m('BIO-C03-COMM-041','A','high',
  "Il cap 5' (7-metilguanosina) protegge l'estremità 5' dell'mRNA dalla degradazione da parte delle esonucleasi e viene riconosciuto dai fattori di inizio per il legame al ribosoma. Non interviene nello splicing né nella poliadenilazione.")
m('BIO-C03-COMM-049','D','high',
  "Nei procarioti l'attività peptidil-transferasica è svolta dall'rRNA 23S della subunità maggiore del ribosoma, che catalizza la formazione del legame peptidico: il ribosoma è quindi un ribozima. I fattori di allungamento e le sintetasi hanno altre funzioni.")
m('BIO-C03-NCOM-001','D','high',
  "La sintesi proteica avviene sui ribosomi, presenti nel citoplasma e all'interno di mitocondri e cloroplasti, che possiedono un proprio corredo di ribosomi. Nel nucleo avviene la trascrizione, non la traduzione.")
m('BIO-C03-NCOM-018','A','high',
  "L'mRNA porta l'informazione genetica dal DNA ai ribosomi, dove viene tradotta in proteina. Il legame con proteine per formare i ribosomi è funzione dell'rRNA, il trasporto degli amminoacidi del tRNA.")
m('BIO-C03-NCOM-041','A','high',
  "Nelle cellule vegetali la maggior parte dell'RNA è trascritto nel nucleo, dove si trovano il genoma principale e gli enzimi della trascrizione. Cloroplasti e mitocondri sintetizzano solo una piccola quota di RNA.")
m('BIO-C03-NCOM-066','C','high',
  "Splicing alternativo e metilazione del DNA sono meccanismi di regolazione che agiscono sul pre-mRNA o sulla cromatina e precedono la traduzione. La rimozione enzimatica dei peptidi segnale avviene invece dopo la traduzione, sul polipeptide.")
m('BIO-C03-NCOM-095','C','high',
  "Durante l'allungamento il tRNA che porta la catena in crescita occupa il sito P, mentre il tRNA carico dell'amminoacido successivo entra nel sito A. Il sito E è quello da cui esce il tRNA scarico.")
m('BIO-C03-NCOM-178','D','high',
  "Rat1 è una esoribonucleasi 5'→3' che, nel lievito e negli eucarioti, degrada il trascritto nascente dopo il taglio al sito di poliadenilazione e contribuisce alla terminazione della trascrizione da RNA polimerasi II. Non interviene nell'inizio né nella maturazione dei tRNA.")
m('BIO-C03-NCOM-189','A','medium',
  "Nello spliceosoma U2 riconosce il punto di ramificazione e, con U5 e U6, partecipa all'allineamento del sito accettore; il riconoscimento del sito 3' AG è mediato da U2 snRNA. U1 riconosce il sito 5' di splicing.")
m('BIO-C03-NCOM-193','B','high',
  "I veri ribozimi sono gli introni che si auto-splicano, cioè gli introni dei gruppi I e II, capaci di catalizzare la propria escissione. Gli introni GU-AG del gruppo dei geni nucleari sono rimossi dallo spliceosoma, che è un complesso ribonucleoproteico.")
m('BIO-C03-NCOM-216','A','high',
  "La degenerazione del codice genetico indica che più codoni diversi possono codificare lo stesso amminoacido; nel libro è sinonimo di ridondanza. Universalità, non ambiguità e specificità descrivono altre proprietà del codice.")

# ---------------- BIOLOGIA C4 ----------------
m('BIO-C04-COMM-014','B','high',
  "Poiché HH è letale, i cani senza pelo sono eterozigoti Hh e quelli con pelo hh. Incrociando un pelo normale (hh) con uno senza pelo (Hh) nasce il 50% Hh (senza pelo) e il 50% hh (con pelo), tutti vitali. Incrociando due Hh si perderebbe un quarto della prole per la letalità.")
m('BIO-C04-COMM-015','A','high',
  "Il genitore a fenotipo dominante può essere AA o Aa: incrociato con aa dà solo Aa se è AA, oppure Aa e aa in rapporto 1:1 se è Aa. I genotipi possibili della progenie sono quindi Aa oppure aa.")
m('BIO-C04-COMM-016','A','high',
  "Due eterozigoti Rr × Rr danno i genotipi RR, Rr, Rr, rr in rapporti 1:2:1 (fenotipi 3 rossi : 1 bianco). La discendenza comprende cioè tutte le combinazioni con la proporzione attesa.")
m('BIO-C04-COMM-035','A','high',
  "Francesca non è daltonica ma ha il padre daltonico (X^d Y): è quindi portatrice obbligata X^D X^d. Il marito Paolo, non daltonico, è X^D Y. La figlia femmina riceve X^D dal padre e quindi non sarà mai daltonica (0%); il figlio maschio riceve Y dal padre e ha il 50% di probabilità di ereditare X^d dalla madre.")
m('BIO-C04-COMM-056','A','medium',
  "La trasmissione è verticale: ogni generazione ha individui malati, la femmina malata trasmette il carattere a metà della progenie di entrambi i sessi e i maschi non malati non trasmettono il carattere. Questo esclude l'eredità recessiva legata all'X, quella legata al cromosoma Y (solo maschi) e quella autosomica recessiva, ed è tipico dell'eredità autosomica dominante.",
  ['needs_figure'])
m('BIO-C04-COMM-060','A','high',
  "La madre è non sensibile, quindi tt; il padre è sensibile e, avendo un figlio ricevuto comunque t dalla madre, questi è necessariamente Tt. Il genotipo del padre può essere TT o Tt e resta indeterminato, mentre quello del figlio è certo: Tt.")
m('BIO-C04-COMM-066','B','high',
  "L'emofilia è una malattia genetica dovuta a mutazioni di geni della coagulazione, ereditaria e legata al cromosoma X. Rosolia e AIDS sono malattie infettive, ictus e iperuricemia hanno cause metaboliche o vascolari, non un difetto genetico ereditario.")
m('BIO-C04-COMM-083','E','high',
  "La discendenza 50% Ab e 50% aB indica che i geni A e B sono associati in trans nei genitori AB, i quali devono essere doppi eterozigoti AaBb con gli alleli A e b su un cromosoma e a e B sull'omologo. Se i geni fossero indipendenti la progenie sarebbe di quattro classi fenotipiche.")
m('BIO-C04-NCOM-026','B','high',
  "Un carattere recessivo si manifesta solo in omozigosi rr, e ciascun genitore deve aver trasmesso una r pur non manifestando il carattere: entrambi sono quindi portatori eterozigoti Rr. Due eterozigoti danno un quarto di figli rr.")
m('BIO-C04-NCOM-030','B','high',
  "L'incrocio Aa × Aa dà i genotipi AA, Aa e aa nel rapporto 1:2:1, cioè 25% AA, 50% Aa e 25% aa. È il risultato della segregazione dei due alleli in ciascun genitore.")
m('BIO-C04-NCOM-033','C','high',
  "Incrociando RRyy × rrYY ciascun genitore trasmette un solo tipo di gamete (Ry e rY): tutta la F₁ è quindi doppia eterozigote RrYy. Il fenotipo sarà liscio e giallo, ma il genotipo richiesto è RrYy.")
m('BIO-C04-NCOM-046','A','high',
  "La femmina X produce 9 neri e 7 bruni, cioè circa 1:1, quindi è eterozigote Bb e il maschio bruno è bb. La femmina Y (14 neri) è omozigote BB. I genotipi sono quindi Bb per X e BB per Y.")
m('BIO-C04-NCOM-055','C','high',
  "Per ottenere il 50% di fiori rossi e il 50% di bianchi occorre un incrocio tra un eterozigote e un omozigote recessivo: Aa × aa dà Aa (rossi) e aa (bianchi) in rapporto 1:1. Aa × Aa darebbe 3:1 e AA × aa solo rossi.")
m('BIO-C04-NCOM-063','C','high',
  "Dall'incrocio AABb × Aabb, il genitore primo trasmette sempre A e quindi la progenie non può essere aa; B/b può dare BB, Bb o bb. Il genotipo AaBB richiederebbe un allele a dal primo genitore, impossibile: non è atteso.")
m('BIO-C04-NCOM-079','E','high',
  "Il test-cross consiste nell'incrociare l'individuo di genotipo incognito con un omozigote recessivo yy: se compaiono discendenti gialli e verdi l'individuo è Yy, se sono tutti gialli è YY. Serve quindi il genotipo yy.")
m('BIO-C04-NCOM-082','B','high',
  "L'eterozigosi richiede due alleli diversi dello stesso gene: Gg è l'unico genotipo con due alleli diversi. GG, AA, aa e gg sono tutti omozigoti.")
m('BIO-C04-NCOM-084','C','high',
  "Un doppio eterozigote AaBb con geni indipendenti, per l'assortimento indipendente, produce quattro tipi di gameti in ugual proporzione: AB, Ab, aB, ab. Ogni gamete riceve un allele per ciascun gene.")
m('BIO-C04-NCOM-085','B','high',
  "Il reincrocio AaBb × aabb (test-cross) permette di distinguere l'assortimento indipendente dall'associazione: con geni indipendenti si ottengono quattro classi fenotipiche in rapporto 1:1:1:1, mentre con geni associati le classi parentali sono più frequenti. Gli altri incroci non permettono questa lettura.")
m('BIO-C04-NCOM-090','D','high',
  "Il crossing-over è lo scambio di segmenti corrispondenti tra cromatidi non fratelli di cromosomi omologhi, e avviene nella profase I della meiosi (pachitene). Non coinvolge cromatidi fratelli né la mitosi, e non è uno scambio nucleo-citoplasmatico.")
m('BIO-C04-NCOM-159','C','high',
  "Nell'eredità poligenica additiva ogni allele dominante aggiunge una quota di pigmento: la massima produzione si ha con il genotipo che contiene il maggior numero di alleli dominanti. AaBBCc ne possiede quattro (A, B, B, C), più di AaBbCc che ne ha tre e degli altri genotipi.")
m('BIO-C04-NCOM-182','A','high',
  "Il padre di gruppo A può essere IAIA o IAi e la madre di gruppo B può essere IBIB o IBi: dal loro incrocio, se entrambi sono eterozigoti, possono nascere figli di gruppo A, B, AB e 0. La serie completa dei gruppi possibili è quindi A, B, AB, 0.")
m('BIO-C04-NCOM-204','C','high',
  "La delezione di un nucleotide non multiplo di tre provoca uno slittamento della cornice di lettura: tutti i codoni successivi cambiano e compare prematuramente un codone di stop. La catena polipeptidica viene quindi interrotta e la proteina risulta tronca e non funzionale.")
