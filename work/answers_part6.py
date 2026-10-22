# -*- coding: utf-8 -*-
A = {}
def m(qid, letter, conf, reason, flags=None):
    A[qid] = dict(kind='mcq', letter=letter, conf=conf, reason=reason, flags=flags or [])
def c(qid, answers, conf, reason, flags=None):
    A[qid] = dict(kind='cloze', answers=answers, conf=conf, reason=reason, flags=flags or [])

# ---------------- FISICA C6 ----------------
m('FIS-C06-COMM-007','B','high',
  "La legge di Coulomb afferma che la forza tra due cariche puntiformi è direttamente proporzionale al prodotto delle cariche e inversamente proporzionale al quadrato della distanza: F = k·q₁q₂/R². L'andamento è quindi con R² al denominatore.")
m('FIS-C06-COMM-012','D','high',
  "Con una batteria ideale da 6 V su 24 Ω la corrente vale I = V/R = 0,25 A e la potenza dissipata P = V²/R = 36/24 = 1,5 W. Il calcolo si può fare anche come P = I²R.")
m('FIS-C06-COMM-028','B','high',
  "Il potenziale elettrico è una grandezza scalare, definita come energia potenziale per unità di carica e misurata in volt. Il campo elettrico è invece un vettore e si misura in volt/metro.")
m('FIS-C06-COMM-033','A','high',
  "Due pile da 4,5 V in serie forniscono 9 V; su una resistenza di 90 Ω la corrente è 0,1 A e la potenza P = V²/R = 81/90 = 0,9 W. La potenza è quindi poco inferiore a 1 watt.")
m('FIS-C06-COMM-037','E','high',
  "Il teorema di Gauss afferma che il flusso del campo elettrico attraverso una superficie chiusa è pari alla somma algebrica delle cariche racchiuse diviso la costante dielettrica ε₀. È quindi proporzionale alla carica netta interna, non al potenziale.")
m('FIS-C06-NCOM-005','B','high',
  "Per la legge di Coulomb la forza elettrostatica è inversamente proporzionale al quadrato della distanza: F ∝ r⁻². La dipendenza lineare o cubica non è compatibile con la legge.")
m('FIS-C06-NCOM-026','E','high',
  "Il farad è l'unità di capacità e vale 1 F = 1 C/V; invertendo la relazione C = Q/V si ottiene V = Q/C, quindi 1 volt equivale a 1 coulomb / 1 farad. Le opzioni con il prodotto joule-coulomb o con il watt non hanno le dimensioni di un potenziale.")
m('FIS-C06-NCOM-032','A','high',
  "La differenza di potenziale di 1 V corrisponde al lavoro di 1 joule per unità di carica, cioè per spostare 1 coulomb. La definizione discende da V = L/q.")
m('FIS-C06-NCOM-033','A','high',
  "L'energia potenziale elettrica di una carica q in un punto di potenziale V è U = qV. Il potenziale è energia per unità di carica, quindi si moltiplica per la carica.")
m('FIS-C06-NCOM-036','E','high',
  "Il lavoro compiuto dal campo è L = q·ΔV = q(V_iniziale − V_finale) = 8 C × (6 − 2) V = +32 J. Il segno è positivo perché la carica positiva si muove spontaneamente verso potenziali minori.")
m('FIS-C06-NCOM-045','B','high',
  "Il campo generato da un piano infinito uniformemente carico è E = σ/(2ε₀) e non dipende dalla distanza dal piano. Solo per una carica puntiforme o una superficie sferica il campo varia con 1/r².")
m('FIS-C06-NCOM-047','A','high',
  "All'interno di un conduttore in equilibrio elettrostatico il campo è nullo, indipendentemente dalla carica presente sulla superficie: le cariche si distribuiscono sulla superficie esterna e la loro azione si annulla all'interno. Per r < R vale quindi E = 0.")
m('FIS-C06-NCOM-059','D','high',
  "La capacità di un condensatore è definita come il rapporto tra la carica accumulata su un'armatura e la differenza di potenziale tra le armature: C = Q/V, misurata in farad. Il rapporto inverso definisce invece l'elastanza.")
m('FIS-C06-NCOM-079','A','high',
  "Con 1 A passano 1 C al secondo e, poiché la carica dell'elettrone è 1,6·10⁻¹⁹ C, il numero di elettroni al secondo è 1/1,6·10⁻¹⁹ ≈ 6,25·10¹⁸. Il valore cade quindi tra 10¹⁸ e 10¹⁹ elettroni al secondo.")
m('FIS-C06-NCOM-082','A','high',
  "L'intensità di corrente è la carica che attraversa la sezione nell'unità di tempo: I = Q/t. L'area della sezione non compare nella definizione, ma solo nel legame con la densità di corrente.")
m('FIS-C06-NCOM-118','C','high',
  "Per la prima legge di Ohm la resistenza è R = V/I: un ohm è la resistenza di un conduttore che, sottoposto a 1 volt, è percorso da 1 ampere. L'unità è quindi volt/ampere.")
m('FIS-C06-NCOM-133','C','high',
  "Nelle specie marine servono scariche ad alto amperaggio e basso voltaggio, cioè un collegamento in parallelo. In parallelo i poli dello stesso segno sono collegati tra loro: il polo positivo di una cellula è quindi affacciato al polo positivo di quella adiacente.")
m('FIS-C06-NCOM-142','D','high',
  "In parallelo la conduttanza totale è la somma delle conduttanze, per cui la resistenza equivalente è minore di ciascuna delle resistenze componenti, e quindi anche della più piccola. Non è mai la somma delle resistenze.")
m('FIS-C06-NCOM-143','B','high',
  "In serie le resistenze si sommano: due resistenze uguali in serie danno una resistenza totale doppia rispetto a ciascuna. La resistenza totale è quindi maggiore di quella di ogni singolo componente.")
m('FIS-C06-NCOM-157','A','high',
  "Un nodo è il punto di un circuito in cui convergono almeno tre rami, cioè più di due conduttori: è il punto a cui si applica la prima legge di Kirchhoff. I rami possono essere percorsi da correnti che si sommano o si sottraggono.",
  ['multiple_correct'])
c('FIS-C06-COMP-136',['intensità'],'high',
  "La forza elettromotrice dinamica indotta in un conduttore in moto in un campo magnetico è proporzionale alla velocità del conduttore, all'intensità del campo magnetico e alla lunghezza del conduttore.")

# ---------------- FISICA C8 ----------------
m('FIS-C08-NCOM-001','C','high',
  "I raggi X sono radiazioni ionizzanti: strappano elettroni alle molecole dell'aria creando coppie di ioni che neutralizzano la carica dell'elettroscopio, che si scarica. La scarica è quindi dovuta al potere ionizzante, non all'assorbimento di energia o alla lunghezza d'onda in sé.")
m('FIS-C08-NCOM-004','E','high',
  "Nel decadimento beta meno un neutrone del nucleo si trasforma in un protone, emettendo un elettrone e un antineutrino: n → p⁺ + e⁻ + ν̄. Il neutrone non si annichila né resta inalterato.")
m('FIS-C08-NCOM-014','A','high',
  "Solo l'uranio-235 è fissile, cioè subisce fissione quando cattura un neutrone termico, mentre l'uranio-238 tende ad assorbire il neutrone senza fissionare. Per sostenere una reazione a catena il combustibile deve quindi essere arricchito in ²³⁵U oltre una soglia critica.")
