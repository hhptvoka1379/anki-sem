# -*- coding: utf-8 -*-
A = {}
def m(qid, letter, conf, reason, flags=None):
    A[qid] = dict(kind='mcq', letter=letter, conf=conf, reason=reason, flags=flags or [])
def c(qid, answers, conf, reason, flags=None):
    A[qid] = dict(kind='cloze', answers=answers, conf=conf, reason=reason, flags=flags or [])

# ---------------- FISICA C1-C2 ----------------
m('FIS-C01-COMM-016','A','high',
  "Se tutte e tre le forze giacciono nel primo quadrante, le loro componenti lungo x e lungo y sono tutte positive o nulle: la risultante ha perciò componenti positive e non può annullarsi. Per avere risultante nulla i tre vettori dovrebbero formare un triangolo chiuso, cosa impossibile restando tutti nello stesso quadrante.",
  ['needs_figure'])
m('FIS-C01-COMM-018','C','high',
  "Due forze perpendicolari si sommano con il teorema di Pitagora: R = √(1² + 1²) = √2 N. Il modulo non è la somma algebrica dei moduli, che varrebbe 2 N.")
m('FIS-C01-COMM-022','B','high',
  "La risultante di due vettori uguali di modulo F che formano un angolo α si ottiene dalla regola del parallelogramma: R = 2F·cos(α/2). Il caso α = 0 dà 2F, il caso α = 90° dà F√2, coerenti con la formula.",
  ['typo'])
m('FIS-C01-NCOM-002','D','high',
  "Nel Sistema Internazionale la temperatura termodinamica si misura in kelvin (K), una delle unità di base. Gradi Celsius, Fahrenheit e Réaumur sono scale pratiche, non unità SI.")
m('FIS-C01-NCOM-053','A','high',
  "Il prefisso milli- vale 10⁻³: una millimole è quindi pari a 10⁻³ moli, cioè un millesimo di mole. Il valore 10³ corrisponde invece al prefisso kilo-.")
m('FIS-C02-COMM-007','D','high',
  "La velocità del cane è 36 km/h = 10 m/s, mentre la pecora si muove a 1 m/s: la velocità relativa di avvicinamento è 9 m/s. Il tempo per colmare i 90 m di distacco è t = d/v_rel = 90/9 = 10 s.")
m('FIS-C02-NCOM-022','C','high',
  "L'accelerazione media è il rapporto tra la variazione di velocità e l'intervallo di tempo in cui essa avviene: a = (v₂ − v₁)/(t₂ − t₁). Le altre opzioni descrivono lo spazio percorso o tempi di raggiungimento di una velocità.")
m('FIS-C02-NCOM-027','A','high',
  "Nel moto uniformemente decelerato la quota massima è h = v₀²/(2g): con v₀ = 10 m/s si ottiene 100/(2·9,8) ≈ 5,1 m. La formula corretta è quindi quella che riporta il quadrato della velocità diviso il doppio di g.",
  ['typo'])
m('FIS-C02-NCOM-077','C','high',
  "La velocità dell'elicottero rispetto al terreno è la somma vettoriale della velocità rispetto all'aria e di quella del vento. Nord-Ovest e Nord-Est sono perpendicolari e hanno lo stesso modulo (70 km/h), quindi la risultante vale 70√2 ≈ 99 km/h, diretta a Nord.",
  ['needs_figure'])
c('FIS-C02-COMP-013',['accelerazione'],'high',
  "La pendenza del grafico velocità-tempo è la variazione di velocità diviso l'intervallo di tempo, cioè l'accelerazione del corpo.")
c('FIS-C02-COMP-022',['rallentando'],'high',
  "Quando velocità e accelerazione hanno segni opposti il modulo della velocità diminuisce: il corpo sta rallentando e il moto è decelerato.")
c('FIS-C02-COMP-037',['y'],'high',
  "Nel moto bidimensionale con accelerazione costante il moto si scompone in due moti rettilinei indipendenti, uno lungo l'asse x e uno lungo l'asse y: le due componenti si trattano separatamente.")
c('FIS-C02-COMP-031',['cartesiane'],'high',
  "Il moto in un piano viene descritto scomponendo il vettore posizione e il vettore velocità lungo gli assi di un sistema di coordinate cartesiane ortogonali.")

# ---------------- FISICA C3 ----------------
m('FIS-C03-COMM-023','B','high',
  "La massa è una proprietà intrinseca del corpo e non dipende dal campo gravitazionale, mentre il peso è la forza con cui il corpo è attratto ed è nullo in assenza di gravità. Resta quindi il peso nullo ma la massa diversa da zero.")
m('FIS-C03-NCOM-011','E','medium',
  "La risultante delle due forze di modulo F formanti 30° è 2F·cos15° ≈ 1,93F; la forza equilibrante deve avere lo stesso modulo e verso opposto. Tra le opzioni proposte il valore compatibile è 2F, che corrisponde a due forze quasi parallele.",
  ['ambiguous'])
m('FIS-C03-NCOM-093','D','high',
  "Il lavoro è il prodotto scalare della forza per lo spostamento: W = F·s·cosθ = 100 N × 1000 m × cos30° ≈ 86.600 J ≈ 87 kJ. Solo la componente della forza lungo lo spostamento compie lavoro.")
m('FIS-C03-NCOM-105','A','high',
  "L'energia cinetica finale è ½mv² = ½ × 1000 × 20² = 2·10⁵ J (72 km/h = 20 m/s). Poiché se ne utilizza solo l'11,77%, servono circa 1,7·10⁶ J, pari al contenuto di 1,7·10⁶ / 3,4·10⁷ ≈ 0,05 L di benzina.")
m('FIS-C03-NCOM-131','B','high',
  "Nel pendolo l'energia si trasforma continuamente da potenziale a cinetica e viceversa: massima potenziale agli estremi, massima cinetica nel punto più basso. Il sistema è conservativo e l'energia meccanica resta costante.")
m('FIS-C03-NCOM-152','D','high',
  "In un urto anelastico l'energia cinetica non si conserva, ma la quantità di moto totale si conserva purché non agiscano forze esterne risultanti sul sistema. La conservazione della quantità di moto non richiede l'elasticità dell'urto.")
m('FIS-C03-NCOM-159','D','high',
  "L'impulso della forza d'attrito è uguale alla variazione della quantità di moto: F·Δt = m·v, da cui F = mv/Δt. La forza è costante e si oppone al moto fino all'arresto.")
m('FIS-C03-NCOM-176','C','high',
  "Per l'equilibrio dei momenti rispetto alla cerniera A, il momento della tensione (T·L) deve bilanciare quello del peso applicato al centro dell'asta (100 N · L/2). Si ottiene quindi T = 50 N, metà del peso dell'asta.",
  ['needs_figure'])
m('FIS-C03-NCOM-185','C','high',
  "L'equilibrio della leva impone R·X_R = P·X_P, da cui il guadagno meccanico G = R/P = X_P/X_R, cioè il rapporto tra il braccio della potenza e quello della resistenza. Il vantaggio è tanto maggiore quanto più lungo è il braccio della forza applicata.")

# ---------------- FISICA C4 ----------------
m('FIS-C04-COMM-004','A','high',
  "La pressione idrostatica al fondo di un recipiente dipende solo dalla densità del liquido, dall'accelerazione di gravità e dall'altezza della colonna: p = ρgh. Non dipende quindi dalla sezione, dal volume né dalla massa totale di liquido.")
m('FIS-C04-COMM-007','C','high',
  "In un condotto orizzontale a sezione costante, per l'equazione di continuità la velocità del liquido è la stessa nelle due sezioni. Per il teorema di Bernoulli, a parità di quota e di velocità, la pressione è la stessa: P₁ = P₂.",
  ['needs_figure'])
m('FIS-C04-COMM-008','C','high',
  "Un corpo galleggiante sposta un peso di liquido pari al proprio peso: essendo sommersa metà del volume, la densità del materiale è metà di quella del liquido, cioè 0,6 g/cm³. I lati del parallelepipedo non servono perché il rapporto dei volumi è già dato.")
m('FIS-C04-COMM-009','D','high',
  "La pressione idrostatica aumenta di circa 1 atm ogni 10 m di profondità: a 40 m l'aumento rispetto alla superficie è quindi di circa 4 atm. La pressione assoluta sarebbe 5 atm, ma la domanda chiede l'aumento.")
m('FIS-C04-NCOM-001','C','high',
  "La densità assoluta è d = m/V = 150 g / 75 mL = 2 g/cm³; la densità relativa, essendo 2 g/cm³ il doppio dell'acqua, vale 2. I due valori coincidono numericamente perché l'acqua ha densità 1 g/cm³.")
m('FIS-C04-NCOM-002','D','high',
  "Il peso specifico relativo è il rapporto tra il peso del corpo e quello di un ugual volume d'acqua; la densità relativa è il rapporto analogo tra le masse. Poiché il fattore g si semplifica, i due valori numerici coincidono.")
m('FIS-C04-NCOM-034','C','high',
  "La forza sul fondo è p·A = ρgh·A e dipende solo dall'altezza e dall'area di base, non dalla forma del recipiente (paradosso idrostatico). Con ρ = 900 kg/m³, g = 10 m/s², h = 0,1 m e A = 10³ cm² = 0,1 m² si ottiene 900 Pa × 0,1 m² = 90 N, uguale per cilindro e cono.")
m('FIS-C04-NCOM-044','E','high',
  "Una colonna d'acqua di 10 m esercita una pressione di circa 1 atm, cioè 760 mmHg, che si somma alla pressione esterna. Supera quindi di circa 1 atm la pressione atmosferica, pur restando inferiore a 2 atm in valore assoluto.")
m('FIS-C04-NCOM-053','D','high',
  "Finché i soldatini sono sulla barca il sistema sposta un volume d'acqua pari al loro peso; gettati in acqua, spostano solo il proprio volume. Poiché il piombo è più denso dell'acqua, il volume spostato diminuisce e il livello dell'acqua scende: non aumenta.")
m('FIS-C04-NCOM-060','C','high',
  "Un corpo galleggia quando la sua densità è minore di quella del fluido in cui è immerso, perché in equilibrio la spinta di Archimede uguaglia il peso. Deve quindi valere D₁ < D₂, indipendentemente dal valore assoluto dei pesi.")
m('FIS-C04-NCOM-085','A','high',
  "La pressione necessaria a spingere il sangue dipende anche dalla colonna idrostatica da vincere: nel piccolo circolo gli organi sono più o meno alla stessa quota, mentre nel circolo sistemico il sangue deve essere spinto anche verso l'alto. Le altre spiegazioni fisiche proposte sono scorrette.")
