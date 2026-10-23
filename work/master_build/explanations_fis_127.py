#!/usr/bin/env python3
"""Exact remediation & Italian scientific explanations for all 127 FIS items in fis_434.txt (+ FIS-C04-COMM-007)."""
from __future__ import annotations

FIS_127: dict[str, dict] = {
    "FIS-C01-NCOM-002": {
        "options": {"B": "gradi Réaumur", "D": "kelvin"},
        "answer_text": "kelvin",
        "explanation": "Nel Sistema Internazionale (SI) l'unità fondamentale della temperatura termodinamica è il kelvin (simbolo K, senza il simbolo di grado); le scale Celsius, Fahrenheit e Réaumur non sono unità fondamentali SI.",
    },
    "FIS-C01-NCOM-036": {
        "question": "L'erg è un'unità di misura di:",
        "explanation": "Nel sistema CGS (centimetro-grammo-secondo) l'erg (1 erg = 1 dyn · cm = 10⁻⁷ J) è l'unità di misura dell'energia e del lavoro meccanico.",
    },
    "FIS-C01-NCOM-038": {
        "options": {"E": "Temperatura assoluta"},
        "explanation": "Il joule (1 J = 1 N · m = 1 kg · m² · s⁻²) è l'unità derivata SI del lavoro, dell'energia e della quantità di calore (forza in N, potenziale elettrico in V = J/C, quantità di moto in kg·m/s, temperatura in K).",
    },
    "FIS-C01-NCOM-083": {
        "question": "Misurando la larghezza l e l'altezza h di un tavolo, si trovano i seguenti valori: l = 180 ± 0,2 cm e h = 80 ± 0,1 cm. Dire quale delle due misure è più precisa.",
        "options": {"A": "l"},
        "answer_text": "l",
        "explanation": "La precisione di due misure si confronta tramite l'errore relativo ε_r = Δx / x: per la larghezza ε_r(l) = 0,2 / 180 = 1/900 ≈ 0,111%, mentre per l'altezza ε_r(h) = 0,1 / 80 = 1/800 = 0,125%. Avendo errore relativo minore, è più precisa la misura di l.",
    },
    "FIS-C01-NCOM-090": {
        "question": "Tre forze di uguale intensità p sono applicate ai vertici di una lamina a forma di triangolo equilatero e dirette come i lati, nel verso indicato in figura. Il risultante di queste forze ha intensità pari a:",
        "options": {"A": "p·3^(1/2)/2"},
        "crop_figure": True,
        "explanation": "Le tre forze di uguale modulo p percorrono in senso ciclico i tre lati del triangolo equilatero (formando angoli di 120° l'una rispetto all'altra): traslate in coda-punta formano un triangolo chiuso, per cui il vettore risultante è nullo (pur essendo diverso da zero il momento torcente risultante).",
    },
    "FIS-C02-NCOM-004": {
        "options": {
            "C": "un moto uniformemente accelerato con accelerazione costante a = 2 m·s⁻²",
            "D": "un moto uniforme con velocità costante v = 4 m·s⁻¹",
        },
        "answer_text": "un moto uniforme con velocità costante v = 4 m·s⁻¹",
        "explanation": "La legge oraria lineare x(t) = x₀ + v·t descrive un moto rettilineo uniforme: confrontando con x = 4t + 5 si riconoscono la posizione iniziale x₀ = 5 m e la velocità costante v = dx/dt = 4 m·s⁻¹.",
    },
    "FIS-C02-NCOM-021": {
        "options": {"A": "18,0 m", "B": "96,0 m", "C": "48,0 m", "D": "108,0 m", "E": "216,0 m"},
        "answer_text": "48,0 m",
        "explanation": "Dalla relazione cinematica senza il tempo v² = v₀² − 2a·Δs, imponendo v = 0 all'arresto si ricava lo spazio di frenata Δs = v₀² / (2a) = (12,0 m/s)² / (2 × 1,50 m/s²) = 144 / 3,00 = 48,0 m.",
    },
    "FIS-C02-NCOM-022": {
        "explanation": "L'accelerazione media in un intervallo di tempo Δt = t₂ − t₁ è definita come il rapporto tra la variazione di velocità Δv = v₂ − v₁ e la durata dell'intervallo stesso: a_m = (v₂ − v₁) / (t₂ − t₁).",
    },
    "FIS-C02-NCOM-027": {
        "options": {
            "A": "10^(1/2) / (2 · 9,8)",
            "B": "100 / 9,8",
            "C": "5^(1/2) / 9,8",
            "D": "2^(1/2) · 9,8 · 10",
            "E": "nessuna delle altre risposte è corretta",
        },
        "answer": "E",
        "answer_text": "nessuna delle altre risposte è corretta",
        "explanation": "Per conservazione dell'energia meccanica (½mv₀² = mgh) la quota massima raggiunta vale h = v₀² / (2g) = 10² / (2 · 9,8) = 100 / (2 · 9,8) ≈ 5,10 m. Poiché sulla scansione originale l'opzione A riporta 10^(1/2)/(2·9,8) (radice quadrata invece del quadrato) e la B omette il fattore 2 a denominatore, nessuna delle espressioni A–D è esatta.",
    },
    "FIS-C02-NCOM-044": {
        "question": "Un proiettile viene sparato verso l'alto con un angolo di inclinazione α diverso da 0 rispetto all'orizzontale. La sua traiettoria sarà:",
        "explanation": "Trascurando la resistenza dell'aria, il moto balistico compone un moto rettilineo uniforme orizzontale (x = v₀ cos α · t) e un moto uniformemente accelerato verticale (y = v₀ sin α · t − ½gt²): eliminando il tempo t per lancio obliquo (0° < α < 90°) si ottiene l'equazione di una parabola.",
        "errata_note": "Nota: nel caso particolare limite α = 90° (lancio perfettamente verticale, dove cos 90° = 0) la traiettoria degenera in un segmento rettilineo verticale; per un generico angolo di tiro obliquo la traiettoria è parabolica (C).",
    },
    "FIS-C02-NCOM-047": {
        "options": {"E": "costante nel tempo"},
        "answer_text": "costante nel tempo",
        "explanation": "Nel moto ideale di un proiettile l'unica forza agente è la gravità diretta verticalmente (a_x = 0, a_y = −g): non essendovi accelerazione orizzontale, la componente v_x = v₀ cos α rimane costante nel tempo.",
    },
    "FIS-C02-NCOM-054": {
        "explanation": "La lancetta dei minuti compie un giro completo (Δθ = 2π rad) in esattamente 1 ora (T = 1 h): la sua velocità angolare vale quindi ω = 2π / T = 2π rad/h.",
        "errata_note": "Nota: il moto della lancetta è uniforme, quindi la velocità angolare è anche «costante» (opzione C); la chiave ufficiale EdiSES seleziona A perché fornisce il valore quantitativo esatto (2π rad/h).",
    },
    "FIS-C02-NCOM-061": {
        "explanation": "Nel puro rotolamento senza strisciamento (v_CM = ωR, punto di contatto istantaneamente fermo v_contatto = 0), la velocità di un punto della corona è la somma della velocità traslatoria del centro V₀ e di quella tangenziale rotatoria: nel punto sommitale i due vettori sono paralleli e concordi, dando v_top = V₀ + ωR = 2·V₀.",
    },
    "FIS-C02-NCOM-064": {
        "options": {
            "A": "Manca il valore del raggio del disco per poter eseguire il conto",
            "B": "Velocità angolare = 45 · (2π) / 360 = 0,8 radianti / secondo",
            "C": "Velocità angolare = 45 · (2π) / 60 = 4,7 radianti / secondo",
            "D": "Velocità angolare = 45 · (2π) / 180 = 1,6 radianti / secondo",
        },
        "answer_text": "Velocità angolare = 45 · (2π) / 60 = 4,7 radianti / secondo",
        "explanation": "Ogni giro sottende un angolo di 2π radianti e 1 minuto equivale a 60 secondi: a 45 giri/min la velocità angolare vale ω = 45 × 2π / 60 s = 1,5π rad/s ≈ 4,71 rad/s (indipendentemente dal raggio).",
    },
    "FIS-C02-NCOM-076": {
        "explanation": "Interpretando l'attraversamento come il raggiungimento del punto direttamente opposto sulla riva di fronte (deriva a valle nulla), la barca deve puntare a monte compensando la corrente v_f, per cui la velocità utile trasversale è √(v_b² − v_f²): aumentando v_f diminuisce la componente trasversale e il tempo di traversata aumenta sia all'andata sia al ritorno.",
        "errata_note": "Nota cinematica: se invece non si vincola il punto di approdo sulla riva opposta, il tempo minimo assoluto si ottiene puntando la prua perpendicolarmente alle sponde e vale t_min = L / v_barca, indipendente dalla velocità della corrente (il che renderebbe vera E, «resta invariato»); la chiave EdiSES presuppone traversata ortogonale senza deriva (C).",
    },
    "FIS-C02-COMP-045": {
        "cloze_stem": "La componente orizzontale della velocità iniziale di un proiettile è v₀ {{c1::cos θ}}.",
        "answer": "cos θ",
        "answer_text": "cos θ (theta)",
        "accepted_synonyms": ["cos θ", "cos theta", "cos(theta)", "cos θ (theta)", "coseno di theta"],
        "explanation": "Scomponendo il vettore velocità iniziale v₀ che forma un angolo θ con l'asse orizzontale x, la proiezione lungo l'orizzontale vale v₀ₓ = v₀ cos θ.",
    },
    "FIS-C02-COMP-046": {
        "cloze_stem": "La componente verticale della velocità iniziale di un proiettile è v₀ {{c1::sen θ}}.",
        "answer": "sen θ",
        "answer_text": "sen θ (theta)",
        "accepted_synonyms": ["sen θ", "sin θ", "sen theta", "sin theta", "sen θ (theta)"],
        "explanation": "Scomponendo v₀ rispetto all'angolo di alzo θ misurato dall'orizzontale, la componente lungo l'asse verticale y vale v₀ᵧ = v₀ sen θ.",
    },
    "FIS-C02-COMP-053": {
        "cloze_stem": "La posizione del proiettile in funzione del tempo si può esprimere come due equazioni separate per x e {{c1::y}}.",
        "answer": "y",
        "answer_text": "y",
        "accepted_synonyms": ["y"],
        "explanation": "Per il principio di indipendenza dei moti simultanei di Galileo, il moto bidimensionale nel piano verticale si descrive mediante due leggi orarie scalari indipendenti per l'ascissa x(t) e per l'ordinata y(t).",
    },
    "FIS-C03-NCOM-011": {
        "options": {"A": "2F√3", "B": "2F/2", "C": "F√2", "D": "F√3", "E": "2F"},
        "answer_text": "F√3",
        "explanation": "Per equilibrare due forze concorrenti occorre applicare una terza forza uguale e contraria alla loro risultante R = √(F² + F² + 2F² cos α) = 2F cos(α/2). Con α = 60° si ottiene esattamente R = 2F cos 30° = F√3 (chiave ufficiale EdiSES D).",
        "errata_note": "Refuso numerico nel testo EdiSES: la traccia stampata riporta «30°» (che darebbe R = 2F cos 15° ≈ 1,93 F, assente in forma esatta tra le opzioni) anziché «60°», valore per il quale vale esattamente F√3 (chiave ufficiale D).",
    },
    "FIS-C03-NCOM-029": {
        "options": {
            "A": "a₁ / a₂ = 2",
            "B": "a₁ / a₂ = 0,5",
            "C": "a₁ = a₂",
            "D": "a₁ / a₂ = −2",
            "E": "a₁ / a₂ = 1",
        },
        "answer_text": "a₁ / a₂ = 2",
        "explanation": "Per il secondo principio della dinamica (F = m·a), a parità di forza applicata l'accelerazione è inversamente proporzionale alla massa: a₁ / a₂ = m₂ / m₁ = (2m₁) / m₁ = 2.",
    },
    "FIS-C03-NCOM-033": {
        "explanation": "In assenza di attriti, per la seconda legge di Newton la forza necessaria vale semplicemente F = m · a = (6 × 10⁷ kg) × (0,1 m/s²) = 6 × 10⁶ N (il peso m·g è verticale ed è equilibrato dalla spinta idrostatica di Archimede).",
    },
    "FIS-C03-NCOM-035": {
        "options": {"E": "4 m/s²"},
        "answer_text": "4 m/s²",
        "explanation": "Dalla legge oraria s(t) = v₀t + ½at² si ha per t = 1 s: v₀ + ½a = 3, e per t = 2 s: 2v₀ + 2a = 10 ⇒ v₀ + a = 5. Sottraendo la prima dalla seconda equazione si ottiene ½a = 2, da cui a = 4 m/s² (e v₀ = 1 m/s).",
    },
    "FIS-C03-NCOM-036": {
        "crop_figure": True,
        "explanation": "Nella figura la massa m₁ poggia sul piano inclinato liscio di angolo α mentre m₂ pende verticalmente: all'equilibrio statico lungo il piano inclinato la tensione T della fune ideale bilancia esattamente la componente parallela del peso di m₁, per cui T = m₁g sin α (e vale anche T = m₂g sul tratto verticale).",
    },
    "FIS-C03-NCOM-045": {
        "options": {
            "A": "70 + 9,8 kg",
            "B": "70 / 9,8 kg",
            "C": "70 · 9,8 N",
            "D": "70 / 9,8 N",
            "E": "70 · 9,8 kg",
        },
        "answer_text": "70 · 9,8 N",
        "explanation": "Il peso è una forza (misurata nel SI in newton, N) data dal prodotto della massa m per l'accelerazione di gravità g ≈ 9,8 m/s²: P = m · g = 70 · 9,8 N = 686 N.",
    },
    "FIS-C03-NCOM-048": {
        "options": {"A": "9,8 N", "D": "9,2 N", "E": "1 N"},
        "answer_text": "9,8 N",
        "explanation": "Sulla superficie terrestre (g ≈ 9,8 m/s²) la forza peso agente su una massa m = 1 kg vale P = m · g = 1 kg × 9,8 m/s² = 9,8 N.",
    },
    "FIS-C03-NCOM-073": {
        "question": "Un satellite che percorre con velocità costante v₀ un'orbita stabile circolare a distanza R dal centro della Terra viene fatto frenare più volte ed immesso in un'orbita circolare stabile a distanza inferiore pari a 0,8R. Della velocità con cui percorre la nuova orbita possiamo dire che:",
        "options": {
            "B": "è più grande di v₀ perché la forza centripeta (gravitazionale) è maggiore",
            "D": "è sicuramente inferiore a v₀ a causa delle frenate",
        },
        "answer_text": "è più grande di v₀ perché la forza centripeta (gravitazionale) è maggiore",
        "explanation": "Su un'orbita circolare stabile la forza gravitazionale fornisce la forza centripeta: GMm/r² = mv²/r ⇒ v = √(GM/r). Scendendo a un raggio orbitale minore (r' = 0,8R < R), il lavoro positivo della gravità supera la perdita per frenata e la velocità orbitale aumenta (v' = v₀/√0,8 > v₀).",
    },
    "FIS-C03-NCOM-077": {
        "question": "Fra tutte le seguenti operazioni, una soltanto fa raddoppiare il periodo di oscillazione di un pendolo semplice che compie piccole oscillazioni attorno alla sua posizione di equilibrio. Quale?",
        "explanation": "Per piccole oscillazioni il periodo del pendolo semplice è T = 2π√(L/g), indipendente dalla massa e dall'ampiezza (isocronismo): poiché T ∝ √L, per raddoppiare T occorre quadruplicare la lunghezza L del filo (√(4L) = 2√L).",
    },
    "FIS-C03-NCOM-082": {
        "options": {
            "A": "70 kg · 1,5 m · 9,81 m/s² = 1030 chilogrammetri",
            "C": "70 kg · 1,5 m · 9,81 m/s² = 1030 calorie",
            "D": "70 kg · 1,5 m · 9,81 m/s² = 1030 joule",
            "E": "1/2 · 70 kg · 1,5 m · (9,81 m/s²)² = 5052 joule",
        },
        "answer_text": "70 kg · 1,5 m · 9,81 m/s² = 1030 joule",
        "explanation": "Il modulo del lavoro della forza peso per un dislivello verticale Δh = 1,5 m vale |L| = m · g · Δh = 70 kg × 9,81 m/s² × 1,5 m ≈ 1030 kg·m²/s² = 1030 J.",
    },
    "FIS-C03-NCOM-087": {
        "explanation": "Il lavoro di una forza costante è il prodotto scalare L = F · S · cos α: esso si annulla non soltanto quando F = 0 o S = 0 (casi C, D, E), ma anche quando forza e spostamento sono tra loro perpendicolari (α = 90°, cos 90° = 0, es. forza centripeta).",
    },
    "FIS-C03-NCOM-098": {
        "explanation": "L'energia cinetica dipende esclusivamente dalla massa e dal modulo della velocità nell'istante considerato: E_c = ½ m v² = 0,5 × 5 kg × (8,5 m/s)² = 2,5 × 72,25 = 180,625 J ≈ 180,62 J.",
    },
    "FIS-C03-NCOM-104": {
        "explanation": "Convertendo la velocità in unità SI si ha v = 100 / 3,6 ≈ 27,78 m/s; uguagliando l'energia potenziale gravitazionale mgh all'energia cinetica ½mv² (con g = 9,81 m/s²) si ricava la quota h = v² / (2g) = (27,78)² / 19,62 ≈ 39,34–39,37 m (indipendente dalla massa).",
    },
    "FIS-C03-NCOM-105": {
        "options": {"A": "0,05 L", "B": "3 L", "C": "1,05 L", "D": "0,3 L", "E": "0,5 L"},
        "answer_text": "0,05 L",
        "explanation": "Poiché 72 km/h = 20 m/s, l'energia cinetica richiesta è E_c = ½ M v² = 0,5 × 1000 × 400 = 2,0 × 10⁵ J. Con rendimento η = 0,1177 l'energia chimica necessaria è E_tot = 2,0 × 10⁵ / 0,1177 ≈ 1,70 × 10⁶ J, corrispondente a V = 1,70 × 10⁶ J / (3,4 × 10⁷ J/L) = 0,05 L di benzina.",
    },
    "FIS-C03-NCOM-159": {
        "question": "Un corpo di massa m si muove su di un piano orizzontale con velocità v. Ad un certo punto A della sua traiettoria incomincia a sentire l'effetto di una forza d'attrito che supponiamo di modulo costante nel tempo e per tutto il resto della traiettoria del corpo, il quale si ferma dopo un tempo Δt. Quanto vale il modulo della forza d'attrito?",
        "explanation": "Per il teorema dell'impulso (I = F · Δt = |Δp|), portandosi il corpo da velocità v a 0 in un intervallo Δt sotto forza frenante costante, si ha F · Δt = m · v, da cui F = m v / Δt.",
    },
    "FIS-C03-NCOM-164": {
        "explanation": "Prendendo l'origine nel centro del Sole, la distanza del centro di massa è x_CM = M_T · d / (M_S + M_T) ≈ (6·10²⁴ × 1,5·10¹¹ m) / (2·10³⁰) = 4,5 × 10⁵ m: poiché 4,5 × 10⁵ m è oltre mille volte minore del raggio solare R_S = 7 × 10⁸ m, il centro di massa cade ben all'interno del Sole.",
    },
    "FIS-C03-NCOM-176": {
        "options": {"A": "100 N", "B": "200 N", "C": "50 N", "D": "75 N", "E": "255 N"},
        "answer_text": "50 N",
        "explanation": "Assumendo la fune verticale all'estremo B, l'equilibrio dei momenti meccanici rispetto alla cerniera A (dove il peso P = 100 N agisce nel baricentro a distanza L/2) impone T · L = P · (L/2), da cui T = P / 2 = 50 N.",
    },
    "FIS-C03-NCOM-177": {
        "explanation": "All'equilibrio rotazionale della bilancia i momenti dei due pesi rispetto al fulcro sono uguali: M₁ g L₁ = M₂ g L₂, da cui L₁ / L₂ = M₂ / M₁ = 0,995 kg / 1,048 kg ≈ 0,9494 ≈ 0,949.",
    },
    "FIS-C03-NCOM-184": {
        "crop_figure": True,
        "options": {
            "A": "p = 4 N; q = 3 N",
            "B": "p = 3 N; q = 3 N",
            "C": "p = 5 N; q = 4 N",
            "D": "p = 2 N; q = 1 N",
            "E": "p = 6 N; q = 4 N",
        },
        "answer_text": "p = 6 N; q = 4 N",
        "explanation": "Dalla figura p è diretta verso il basso a braccio b_p = 2l/3 dal fulcro O, mentre q è diretta verso l'alto all'estremo a braccio b_q = l: l'equilibrio dei momenti rispetto a O impone p · (2l/3) = q · l, ossia p / q = 3 / 2. Tra le coppie proposte solo p = 6 N e q = 4 N soddisfa 6 / 4 = 3 / 2.",
    },
    "FIS-C03-NCOM-185": {
        "answer": "C",
        "answer_text": "G = X_P / X_R",
        "explanation": "Per l'equilibrio dei momenti rispetto al fulcro vale R · X_R = P · X_P; il guadagno meccanico di una macchina semplice è definito come il rapporto tra resistenza vinta e potenza applicata, G = R / P, che per sostituzione risulta G = X_P / X_R (confermato anche dalla scansione originale).",
    },
    "FIS-C03-COMP-028": {
        "cloze_stem": "Le forze interne a un sistema non influenzano il moto del centro di massa del sistema {{c1::stesso}} (solo le forze esterne lo modificano).",
        "answer": "stesso",
        "answer_text": "stesso (esterno nella stampa con refuso)",
        "accepted_synonyms": ["stesso", "esterno", "centro di massa"],
        "explanation": "Per il terzo principio della dinamica (azione e reazione) le forze interne a un sistema si elidono a coppie: pertanto non alterano la quantità di moto totale né il moto del centro di massa del sistema, che dipende unicamente dalla risultante delle forze esterne.",
        "errata_note": "Nota: nella generazione Cloze originaria era rimasta la parola «esterno» per contaminazione col concetto di «forze esterne»; sono accettate entrambe le risposte («stesso» / «esterno»).",
    },
    "FIS-C03-COMP-045": {
        "cloze_stem": "La velocità limite si raggiunge quando la forza di trascinamento (resistenza viscosa) è uguale alla forza {{c1::peso}}.",
        "accepted_synonyms": ["peso", "di gravità"],
        "explanation": "Un corpo in caduta in un fluido viscoso accelera finché la resistenza fluidodinamica crescente (trascurando o includendo la spinta di Archimede) eguaglia in modulo la forza peso: da quell'istante la risultante è nulla e il corpo scende a velocità costante detta velocità limite.",
    },
    "FIS-C03-COMP-058": {
        "cloze_stem": "Il lavoro compiuto da una forza costante è dato dalla formula W = F · Δr · {{c1::cos θ}}.",
        "answer": "cos θ",
        "answer_text": "cos θ (theta)",
        "accepted_synonyms": ["cos θ", "cos theta", "cos(theta)", "cos θ (theta)"],
        "explanation": "Il lavoro di una forza costante F lungo uno spostamento rettilineo Δr è il prodotto scalare W = F⃗ · Δr⃗ = F · Δr · cos θ, dove θ è l'angolo compreso tra i due vettori.",
    },
    "FIS-C03-COMP-073": {
        "cloze_stem": "La funzione coseno in W = F · Δr · cos θ tiene conto del {{c1::segno}} del lavoro.",
        "accepted_synonyms": ["segno", "verso"],
        "explanation": "Il fattore cos θ determina il segno algebrico del lavoro: positivo (motore) per 0° ≤ θ < 90°, nullo per θ = 90° e negativo (resistente) per 90° < θ ≤ 180°.",
    },
    "FIS-C03-COMP-079": {
        "cloze_stem": "La variazione di energia cinetica si indica come Δ{{c1::K}}.",
        "accepted_synonyms": ["K", "Ec", "E_c"],
        "explanation": "Indicando con K l'energia cinetica (K = ½mv²), la sua variazione tra stato finale e iniziale si scrive ΔK = K_f − K_i (pari al lavoro totale per il teorema delle forze vive).",
    },
    "FIS-C03-COMP-090": {
        "cloze_stem": "Quando l'energia meccanica si conserva, ΔE_mec è uguale a {{c1::zero}}.",
        "accepted_synonyms": ["zero", "0"],
        "explanation": "In presenza di sole forze conservative l'energia meccanica totale E_mec = K + U rimane costante nel tempo, per cui la sua variazione è nulla: ΔE_mec = 0.",
    },
    "FIS-C03-COMP-105": {
        "cloze_stem": "La conservazione dell'energia meccanica si esprime con l'equazione ΔK + ΔU = {{c1::zero}}.",
        "accepted_synonyms": ["zero", "0"],
        "explanation": "Poiché E_mec = K + U, la condizione ΔE_mec = 0 equivale a ΔK + ΔU = 0 (ogni aumento di energia cinetica è compensato da un'uguale diminuzione di energia potenziale e viceversa).",
    },
    "FIS-C03-COMP-156": {
        "cloze_stem": "Il momento di inerzia di un disco omogeneo rispetto al suo asse centrale è I = ½ M {{c1::R²}}.",
        "accepted_synonyms": ["R²", "R^2", "r²", "r^2"],
        "explanation": "Integrando r² dm su un cilindro o disco pieno omogeneo di massa M e raggio R rispetto all'asse di simmetria perpendicolare al piano del disco si ottiene I = ½ M R².",
    },
    "FIS-C03-COMP-181": {
        "cloze_stem": "L'energia cinetica istantanea è K = ½ m {{c1::v²}}.",
        "accepted_synonyms": ["v²", "v^2"],
        "explanation": "Nel moto traslatorio classico l'energia cinetica istantanea di un punto materiale di massa m e velocità istantanea v è definita da K = ½ m v².",
    },
    "FIS-C03-COMP-182": {
        "cloze_stem": "L'energia potenziale elastica è U = ½ k {{c1::x²}}.",
        "accepted_synonyms": ["x²", "x^2", "Δx²"],
        "explanation": "Per una molla ideale che obbedisce alla legge di Hooke (F = −kx), l'energia potenziale elastica accumulata per una deformazione x rispetto alla posizione di riposo vale U = ½ k x².",
    },
    "FIS-C03-COMP-184": {
        "cloze_stem": "Il valore massimo della velocità nel moto armonico è v_max = A · {{c1::ω}}.",
        "answer": "ω",
        "answer_text": "ω (omega)",
        "accepted_synonyms": ["ω", "omega", "ω (omega)"],
        "explanation": "Derivando la legge oraria del moto armonico x(t) = A cos(ωt + φ) si ottiene v(t) = −Aω sin(ωt + φ), il cui valore massimo (al passaggio per il centro di oscillazione) è v_max = A · ω.",
    },
    "FIS-C03-COMP-185": {
        "cloze_stem": "Il valore massimo dell'accelerazione nel moto armonico è a_max = A · {{c1::ω²}}.",
        "answer": "ω²",
        "answer_text": "ω² (omega²)",
        "accepted_synonyms": ["ω²", "ω^2", "omega^2", "omega²", "ω² (omega)"],
        "explanation": "Nel moto armonico semplice vale a(t) = −ω² x(t): il modulo dell'accelerazione raggiunge il valore massimo agli estremi dell'oscillazione (|x| = A) ed è pari ad a_max = A · ω².",
    },
    "FIS-C03-COMP-191": {
        "cloze_stem": "La componente tangenziale di richiamo della forza di gravità in un pendolo semplice ha modulo m g {{c1::sen}} θ.",
        "accepted_synonyms": ["sen", "sin", "seno"],
        "explanation": "Scomponendo il peso mg lungo la direzione radiale del filo (mg cos θ) e quella tangenziale alla traiettoria circolare, la componente di richiamo tangenziale vale F_t = −mg sen θ.",
    },
    "FIS-C03-COMP-193": {
        "cloze_stem": "Il parametro φ nell'equazione del moto armonico è detto costante di {{c1::fase}}.",
        "accepted_synonyms": ["fase", "fase iniziale"],
        "explanation": "Nella legge oraria x(t) = A cos(ωt + φ), l'angolo φ (fase iniziale o costante di fase, misurato in radianti) individua lo stato di oscillazione all'istante t = 0.",
    },
    "FIS-C04-COMM-007": {
        "crop_figure": True,
        "options": {"A": "P₁ > P₂", "B": "P₁ < P₂", "C": "P₁ = P₂"},
        "answer": "C",
        "answer_text": "P₁ = P₂",
        "explanation": "Trattandosi di un liquido incomprimibile perfetto (privo di attrito viscoso) in moto stazionario entro un condotto orizzontale (z₁ = z₂) a sezione costante (A₁ = A₂), l'equazione di continuità A₁v₁ = A₂v₂ impone v₁ = v₂; applicando allora il teorema di Bernoulli P₁ + ½ρv₁² + ρgz₁ = P₂ + ½ρv₂² + ρgz₂ segue immediatamente P₁ = P₂.",
    },
    "FIS-C04-NCOM-001": {
        "explanation": "La densità assoluta vale d = m / V = 150 g / 75 cm³ = 2 g/cm³ (poiché 1 mL = 1 cm³); la densità relativa rispetto all'acqua (d_H₂O = 1 g/cm³) è il rapporto adimensionale d / d_H₂O = 2.",
    },
    "FIS-C04-NCOM-034": {
        "question": "Un contenitore cilindrico e un contenitore conico hanno la stessa altezza, pari a 10 cm, e la stessa area di base, pari a 10³ cm². Entrambi poggiano con la loro base su un piano orizzontale e sono interamente riempiti con un olio avente una densità di 900 g/L. Assumendo che sia g = 10 m/s², l'intensità della forza esercitata dall'olio sul fondo del recipiente è:",
        "options": {
            "A": "9 N sia per il cilindro che per il cono",
            "B": "9 N per il cilindro e 3 N per il cono",
            "C": "90 N sia per il cilindro che per il cono",
            "E": "90 N per il cilindro e 30 N per il cono",
        },
        "answer_text": "90 N sia per il cilindro che per il cono",
        "explanation": "Per la legge di Stevin e il paradosso idrostatico di Pascal, la pressione relativa esercitata dal liquido sul fondo dipende solo da densità e altezza (p = ρgh = 900 kg/m³ × 10 m/s² × 0,10 m = 900 Pa) e non dalla forma del recipiente: su un'area A = 10³ cm² = 0,10 m² la forza vale F = p · A = 900 Pa × 0,10 m² = 90 N per entrambi.",
    },
    "FIS-C04-NCOM-039": {
        "options": {
            "A": "Altezza 2 m; sezione 1 cm²",
            "B": "Altezza 1,40 m; sezione 1 cm²",
            "C": "Altezza 0,80 m; sezione 0,1 m²",
            "D": "Altezza 1 m; sezione 10 cm²",
            "E": "Altezza 1 m; sezione 2 cm²",
        },
        "answer_text": "Altezza 2 m; sezione 1 cm²",
        "explanation": "Per la legge di Stevin (p = p₀ + ρgh) la pressione idrostatica sul fondo di una colonna liquida dipende unicamente dall'altezza h della colonna e non dall'area della sezione: la pressione maggiore è quindi esercitata dalla colonna più alta (h = 2 m).",
    },
    "FIS-C04-NCOM-060": {
        "explanation": "Per il principio di Archimede un corpo omogeneo galleggia parzialmente immerso alla superficie libera di un fluido se e solo se la sua densità D₁ è minore della densità D₂ del fluido (D₁ < D₂), indipendentemente dai pesi totali P₁ e P₂.",
    },
    "FIS-C04-NCOM-081": {
        "explanation": "In un condotto orizzontale a sezione uniforme (legge di Poiseuille per fluidi reali), il moto stazionario del fluido è sostenuto da una differenza di pressione ed è diretto dalla sezione a pressione maggiore verso quella a pressione minore.",
        "errata_note": "Nota fluidodinamica: l'avverbio «sempre» va inteso a parità di quota e sezione (regime viscoso tipo Poiseuille); in un diffusore divergente ideale di Venturi (dove il fluido rallenta) o in un tubo verticale discendente un fluido può invece avanzare verso zone a pressione statica maggiore.",
    },
    "FIS-C04-NCOM-086": {
        "question": "In una tubatura orizzontale a sezione circolare viene trasportato un flusso costante d'acqua. Se in un punto nel quale la tubatura ha una sezione di area 6 cm² l'acqua viaggia a 0,80 m/s, quale è la sua velocità in un punto nel quale l'area della sezione è di 4 cm²?",
        "explanation": "Per l'equazione di continuità dei fluidi incomprimibili la portata volumetrica Q = A · v è costante: A₁v₁ = A₂v₂ ⇒ v₂ = v₁ · (A₁ / A₂) = 0,80 m/s × (6 cm² / 4 cm²) = 1,20 m/s.",
    },
    "FIS-C04-COMP-017": {
        "cloze_stem": "L'equazione di continuità per un fluido incomprimibile si scrive A₁ v₁ = A₂ {{c1::v₂}}.",
        "accepted_synonyms": ["v₂", "v2"],
        "explanation": "La conservazione della massa in moto stazionario per un fluido a densità costante impone che la portata volumetrica Q = A · v resti costante lungo il condotto: A₁v₁ = A₂v₂.",
    },
    "FIS-C04-COMP-023": {
        "cloze_stem": "La pressione di un fluido incomprimibile a profondità h si calcola come P = P₀ + ρ g {{c1::h}}.",
        "accepted_synonyms": ["h"],
        "explanation": "Secondo la legge idrostatica di Stevin, la pressione assoluta a profondità h sotto la superficie libera (soggetta alla pressione esterna P₀) aumenta linearmente con la profondità secondo P = P₀ + ρgh.",
    },
    "FIS-C05-NCOM-023": {
        "options": {"A": "Q/4", "B": "3Q/4", "C": "Q/3", "D": "Q/2", "E": "2Q/3"},
        "answer_text": "Q/4",
        "explanation": "Dalla legge fondamentale della calorimetria Q = m · c · ΔT, dimezzando sia la massa (da 60 kg a 30 kg) sia il salto termico (da ΔT₁ = 40 °C a ΔT₂ = 20 °C) per lo stesso materiale, il calore richiesto si riduce a (1/2) × (1/2) = 1/4 del valore iniziale, ossia Q/4.",
    },
    "FIS-C05-NCOM-024": {
        "options": {"B": "Energia - calore"},
        "answer_text": "Energia - calore",
        "explanation": "Due grandezze fisiche si dicono dimensionalmente omogenee quando hanno le stesse dimensioni fisiche e si misurano con la medesima unità: energia e calore hanno entrambe dimensioni [M L² T⁻²] e si misurano in joule (J).",
    },
    "FIS-C05-NCOM-062": {
        "explanation": "Arrestandosi completamente su un piano orizzontale, ciascun corpo dissipa in calore per attrito l'intera propria energia cinetica iniziale: E₁ = ½ M V₁², mentre E₂ = ½ (M/4) (2V₁)² = ½ (M/4) (4V₁²) = ½ M V₁² = E₁. Essendo uguali le energie cinetiche iniziali, sviluppano esattamente la stessa quantità di calore.",
    },
    "FIS-C05-NCOM-067": {
        "explanation": "Per il principio di conservazione dell'energia (primo principio della termodinamica applicato a un sistema isolato, in cui Q = 0 e W = 0), l'energia totale di un sistema isolato rimane invariata (ΔE_tot = 0, cioè non aumenta né diminuisce).",
        "errata_note": "Nota: anche l'opzione E («resta costante nel tempo») esprime esattamente lo stesso principio fisico di B («non aumenta né diminuisce»); la chiave ufficiale EdiSES riporta B.",
    },
    "FIS-C05-NCOM-089": {
        "options": {"B": "4 dm³", "E": "4 m³"},
        "answer_text": "4 dm³",
        "explanation": "Convertendo le temperature in kelvin si ha T₁ = 27 + 273 = 300 K e T₂ = 327 + 273 = 600 K = 2 T₁; per la prima legge di Gay-Lussac (Charles) delle trasformazioni isobare (V / T = costante), raddoppiando la temperatura assoluta il volume raddoppia da 2 L a 4 L = 4 dm³.",
    },
    "FIS-C05-NCOM-114": {
        "options": {"A": "ΔU", "B": "ΔT", "C": "ΔG", "D": "ΔS", "E": "ΔH"},
        "answer_text": "ΔS",
        "explanation": "In termodinamica la funzione di stato entropia è indicata con la lettera S (variazione ΔS), mentre ΔU indica l'energia interna, ΔT la temperatura, ΔG l'energia libera di Gibbs e ΔH l'entalpia.",
    },
    "FIS-C05-COMP-008": {
        "cloze_stem": "La relazione ΔV = β Vᵢ ΔT descrive la dilatazione termica {{c1::volumica}}.",
        "answer": "volumica",
        "answer_text": "volumica (o cubica)",
        "accepted_synonyms": ["volumica", "cubica", "cubica (o volumica)", "volumetrica"],
        "explanation": "La legge ΔV = β Vᵢ ΔT esprime la variazione di volume ΔV in funzione del volume iniziale Vᵢ, del salto termico ΔT e del coefficiente di dilatazione volumica (o cubica) β ≈ 3α.",
    },
    "FIS-C05-COMP-037": {
        "cloze_stem": "Durante una fusione la variazione di entropia ΔS (nella stampa: Δm del liquido) è sempre {{c1::positiva}}.",
        "accepted_synonyms": ["positiva", "maggiore di zero"],
        "explanation": "Durante la fusione a temperatura costante T_f il sistema assorbe il calore latente di fusione Q = m·L_f > 0 passando dallo stato solido ordinato allo stato liquido: sia la massa di fase liquida formata sia la variazione di entropia ΔS = Q/T_f sono sempre positive.",
    },
    "FIS-C05-COMP-043": {
        "cloze_stem": "Il primo principio della termodinamica (nella convenzione IUPAC/chimica) si scrive ΔE_int = Q + {{c1::W}}.",
        "accepted_synonyms": ["W", "L"],
        "explanation": "Definendo positivo il lavoro W compiuto dall'ambiente sul sistema (convenzione chimica/anglosassone usata nel testo sorgente), la variazione di energia interna è la somma algebrica ΔE_int = Q + W (mentre indicando con L il lavoro compiuto dal sistema si scrive ΔU = Q − L).",
    },
    "FIS-C05-COMP-044": {
        "cloze_stem": "Il lavoro sul gas che si espande contro una pressione esterna costante si calcola come W = −P · Δ{{c1::V}}.",
        "accepted_synonyms": ["V"],
        "explanation": "In una trasformazione isobara reversibile o contro pressione esterna costante P, il lavoro scambiato dipende dalla variazione di volume ΔV: W_sul_gas = −P·ΔV (mentre il lavoro fatto dal gas sull'esterno vale +P·ΔV).",
    },
    "FIS-C05-COMP-056": {
        "cloze_stem": "La formula del rendimento di una macchina termica ciclica è η = 1 − (|Q_f| / {{c1::Q_c}}).",
        "answer": "Q_c",
        "answer_text": "Q_c (Qc)",
        "accepted_synonyms": ["Qc", "Q_c", "|Qc|"],
        "explanation": "Il rendimento termodinamico di una macchina termica è η = L / Q_c = (Q_c − |Q_f|) / Q_c = 1 − |Q_f| / Q_c, dove Q_c è il calore assorbito dalla sorgente calda e |Q_f| il calore ceduto alla sorgente fredda.",
    },
    "FIS-C05-COMP-069": {
        "cloze_stem": "La rappresentazione microscopica (statistica di Boltzmann) dell'entropia è S = k_B ln {{c1::W}}.",
        "accepted_synonyms": ["W", "Ω", "omega"],
        "explanation": "Nell'equazione di Boltzmann S = k_B ln W la grandezza W (o Ω) rappresenta la molteplicità termodinamica, cioè il numero di microstati microscopici accessibili compatibili con il macrostato del sistema.",
    },
    "FIS-C05-COMP-071": {
        "cloze_stem": "Il lavoro totale compiuto in un ciclo da una macchina termica è uguale alla differenza tra Q_c e {{c1::Q_f}}.",
        "answer": "Q_f",
        "answer_text": "Q_f (Qf)",
        "accepted_synonyms": ["Qf", "Q_f", "|Qf|"],
        "explanation": "Poiché al termine di un ciclo completo il sistema torna allo stato iniziale (ΔU_ciclo = 0), per il primo principio il lavoro netto prodotto vale L = Q_assorbito − Q_ceduto = Q_c − |Q_f|.",
    },
    "FIS-C06-NCOM-005": {
        "options": {"A": "r²", "B": "r⁻²", "C": "r⁻¹", "D": "r/2", "E": "r"},
        "answer_text": "r⁻²",
        "explanation": "Secondo la legge di Coulomb F = k |q₁q₂| / r², l'intensità della forza elettrostatica tra due cariche puntiformi è inversamente proporzionale al quadrato della loro distanza r, ossia proporzionale a r⁻².",
    },
    "FIS-C06-NCOM-011": {
        "explanation": "Ponendo Q₁ = Q₂ = Q: se Q₃ = −Q si trova all'esterno del segmento Q₁Q₂, le due forze attrattive verso Q₁ e Q₂ hanno lo stesso verso e non possono annullarsi; solo ponendo Q₃ tra Q₁ e Q₂ (esattamente nel punto medio per Q₁ = Q₂) le due attrazioni hanno versi opposti e si equilibrano dando risultante nulla.",
        "errata_note": "Nota di precisione: essendo Q₁ = Q₂, la forza su Q₃ si annulla esclusivamente nel punto medio esatto del segmento Q₁Q₂ (condizione necessaria è comunque trovarsi in posizione intermedia tra Q₁ e Q₂, opzione E della chiave EdiSES).",
    },
    "FIS-C06-NCOM-013": {
        "explanation": "In elettrostatica (cariche ferme, ∂B/∂t = 0) il campo elettrico è conservativo (circuitazione nulla ∮E⃗·dl⃗ = 0): le sue linee di forza nascono sempre sulle cariche positive e terminano su quelle negative, per cui non possono mai formare linee chiuse (chiave EdiSES A).",
        "errata_note": "Attenzione fisica importante: il quesito è inserito nella sezione di elettrostatica e la chiave EdiSES è A; tuttavia, in elettrodinamica generale, in presenza di un campo magnetico variabile nel tempo (induzione elettromagnetica di Faraday-Neumann, ∮E⃗·dl⃗ = −dΦ(B)/dt ≠ 0), il campo elettrico indotto è non conservativo e possiede effettivamente linee di forza chiuse (opzione B fisicamente vera in regime variabile).",
    },
    "FIS-C06-NCOM-014": {
        "question": "Una particella priva di carica, in moto rettilineo ed uniforme, che entra in un campo elettrico diretto perpendicolarmente alla direzione della velocità della particella, descrive una traiettoria:",
        "explanation": "La forza elettrica agente su una particella di carica q è F⃗ = qE⃗: per una particella elettricamente neutra (q = 0) la forza elettrica è identicamente nulla e, per il principio d'inerzia, essa prosegue di moto rettilineo uniforme.",
    },
    "FIS-C06-NCOM-028": {
        "options": {
            "A": "1 watt = 1 joule · 1 secondo",
            "B": "1 watt = 1 joule · 1 ora",
            "C": "1 joule = 1 volt · 1 ampere",
            "D": "1 joule = 1 volt · 1 coulomb",
            "E": "1 farad = 1 coulomb · 1 volt",
        },
        "answer_text": "1 joule = 1 volt · 1 coulomb",
        "explanation": "Dalla definizione di differenza di potenziale elettrico ΔV = L / q segue L = q · ΔV, e quindi tra le unità SI vale l'identità 1 J = 1 V · 1 C (mentre 1 W = 1 J/s, 1 V·A = 1 W e 1 F = 1 C/V).",
    },
    "FIS-C06-NCOM-032": {
        "options": {"A": "1 joule", "C": "1 metro/secondo", "D": "1 cm", "E": "1 watt"},
        "answer_text": "1 joule",
        "explanation": "Per definizione 1 V = 1 J / 1 C: tra due punti sussiste la differenza di potenziale di 1 volt quando le forze elettriche (o esterne) compiono il lavoro di 1 joule per spostare la carica di 1 coulomb.",
    },
    "FIS-C06-NCOM-033": {
        "explanation": "Poiché il potenziale elettrico V in un punto è definito come l'energia potenziale elettrica per unità di carica esploratrice (V = U / q), una carica q posta a potenziale V possiede energia potenziale elettrica U = q · V.",
    },
    "FIS-C06-NCOM-036": {
        "options": {"A": "nessuna delle altre risposte è corretta", "B": "−32 J", "D": "−2 J", "E": "+32 J"},
        "answer_text": "+32 J",
        "explanation": "Il lavoro compiuto dalle forze del campo elettrostatico nello spostamento di una carica q da V_A a V_B vale L = q · (V_A − V_B) = (+8 C) × (6 V − 2 V) = +32 J (positivo perché una carica positiva scende spontaneamente verso potenziali minori).",
    },
    "FIS-C06-NCOM-039": {
        "question": "Siano M ed N due punti di un campo elettrostatico. Una carica puntiforme q si sposta da M ad N seguendo uno dei percorsi indicati in figura e le forze del campo compiono il lavoro L. Delle seguenti affermazioni qual è quella corretta?",
        "options": {"A": "La differenza di potenziale tra N ed M è uguale al lavoro L"},
        "crop_figure": True,
        "explanation": "Il campo elettrostatico è conservativo (il lavoro L_M→N non dipende dal percorso seguito ed è una grandezza scalare), e il rapporto |ΔV| = L / q misura il modulo della differenza di potenziale tra i punti M ed N.",
        "errata_note": "Nota di segno: con la convenzione standard ΔV_NM = V_N − V_M vale più precisamente V_M − V_N = L_M→N / q (cioè V_N − V_M = −L/q); tra le alternative scalari proposte dal quesito l'unica dimensionalmente corretta è C (L/q).",
    },
    "FIS-C06-NCOM-041": {
        "explanation": "La carica del nucleo è Q = 50 × 1,6 × 10⁻¹⁹ C = 8,0 × 10⁻¹⁸ C; il potenziale elettrostatico a distanza r = 10⁻¹² m vale V = k · Q / r = (9 × 10⁹ N·m²/C² × 8,0 × 10⁻¹⁸ C) / 10⁻¹² m = 72 × 10³ V = 7,2 × 10⁴ V.",
    },
    "FIS-C06-NCOM-060": {
        "question": "Un condensatore a piastre piane e parallele in aria, carico e isolato, presenta una differenza di potenziale di 10 kV tra le sue armature; se viene posto tra le armature un materiale isolante (es. ceramica) con una costante dielettrica relativa ε_r = 10, la differenza di potenziale tra le armature:",
        "explanation": "Poiché il condensatore è isolato (scollegato dal generatore), la carica Q sulle armature rimane costante; l'inserimento del dielettrico aumenta la capacità di un fattore ε_r = 10 (C' = ε_r C₀), per cui la tensione ΔV' = Q / C' = ΔV₀ / 10 diminuisce di 10 volte (a 1 kV).",
    },
    "FIS-C06-NCOM-063": {
        "question": "Nello spazio presente tra le due facce parallele di un condensatore piano a facce parallele è presente dell'aria. Il condensatore è connesso ad un generatore da 100 V a corrente continua. In seguito, un foglio di materiale dielettrico viene inserito tra le due facce parallele del condensatore. I valori di quali grandezze cambiano quando il dielettrico viene inserito tra le due facce parallele?",
        "explanation": "Restando il condensatore collegato al generatore ideale da 100 V, la differenza di potenziale ΔV tra le armature è vincolata a restare costante; l'inserimento del dielettrico fa aumentare la capacità C' = ε_r C₀ e conseguentemente il generatore fornisce ulteriore carica facendo aumentare anche Q' = C' · ΔV.",
    },
    "FIS-C06-NCOM-073": {
        "question": "Tre condensatori sono collegati in serie all'interno di un circuito elettrico. Se le capacità dei tre condensatori sono rispettivamente 6 C, 4 C e 12 C, quale capacità avrà il condensatore equivalente?",
        "explanation": "Per condensatori collegati in serie i reciproci delle capacità si sommano: 1/C_eq = 1/(6C) + 1/(4C) + 1/(12C) = (2 + 3 + 1)/(12C) = 6/(12C) = 1/(2C), da cui C_eq = 2C.",
    },
    "FIS-C06-NCOM-076": {
        "options": {
            "B": "coulomb · ampere",
            "D": "ohm · volt",
            "E": "ampere · s",
        },
        "answer_text": "ampere · s",
        "explanation": "Dalla definizione di intensità di corrente elettrica I = Q / t segue Q = I · t: l'unità di carica elettrica, il coulomb (C), equivale nel SI al prodotto di 1 ampere per 1 secondo (1 C = 1 A · s).",
    },
    "FIS-C06-NCOM-077": {
        "explanation": "Dalla relazione Q = I · Δt si ricava il tempo di scarica Δt = Q / I = 1,08 × 10⁵ C / 10 A = 1,08 × 10⁴ s = 10.800 s; dividendo per 3.600 s/ora si ottengono esattamente 3 ore.",
    },
    "FIS-C06-NCOM-079": {
        "options": {
            "A": "Tra 10¹⁸ e 10¹⁹ elettroni/secondo",
            "C": "10⁹ elettroni/secondo",
            "E": "Un elettrone/secondo",
        },
        "answer_text": "Tra 10¹⁸ e 10¹⁹ elettroni/secondo",
        "explanation": "Una corrente di 1 A trasporta una carica Q = 1 C ogni secondo; essendo la carica elementare dell'elettrone e ≈ 1,60 × 10⁻¹⁹ C, il numero di elettroni al secondo vale N = 1 C / (1,60 × 10⁻¹⁹ C) ≈ 6,25 × 10¹⁸ elettroni/s, compreso tra 10¹⁸ e 10¹⁹.",
    },
    "FIS-C06-NCOM-082": {
        "options": {
            "A": "I = Q / t",
            "B": "I = A / t",
            "C": "I = Q · A / t",
            "D": "I = Q · t",
            "E": "I = Q · A · t",
        },
        "answer_text": "I = Q / t",
        "explanation": "L'intensità media di corrente elettrica I attraverso la sezione trasversale di un conduttore è definita dal rapporto tra la carica elettrica Q che attraversa la sezione nell'intervallo di tempo t e la durata t stessa: I = Q / t (indipendentemente dall'area A).",
    },
    "FIS-C06-NCOM-084": {
        "question": "Le potenze utilizzate dai seguenti elettrodomestici sono: P(ferro da stiro) = 1 kW; P(televisore) = 150 W; P(lavatrice) = 2,5 kW; P(forno elettrico) = 1.500 W. Se vengono collegati alla rete domestica (220 V), quale degli elettrodomestici è attraversato da una corrente di intensità maggiore?",
        "explanation": "A parità di tensione di alimentazione V = 220 V, dalla legge di Joule/potenza elettrica P = V · I segue I = P / V: l'intensità di corrente è direttamente proporzionale alla potenza assorbita ed è quindi massima nella lavatrice (2,5 kW = 2.500 W).",
    },
    "FIS-C06-NCOM-118": {
        "options": {
            "A": "1 ohm = 1 volt · 1 ampere",
            "C": "1 ohm = 1 volt / 1 ampere",
            "D": "1 ohm = 1 volt · 1 secondo",
            "E": "1 ohm = 10 volt · 1 ampere",
        },
        "answer_text": "1 ohm = 1 volt / 1 ampere",
        "explanation": "Dalla prima legge di Ohm R = V / I l'unità SI di resistenza elettrica, l'ohm (Ω), corrisponde al rapporto tra 1 volt e 1 ampere: 1 Ω = 1 V / 1 A.",
    },
    "FIS-C06-NCOM-123": {
        "crop_figure": True,
        "explanation": "Per un conduttore ohmico a temperatura costante vale la prima legge di Ohm V = R · I con resistenza R costante e positiva: nel piano cartesiano (I, V) la caratteristica tensione-corrente è quindi una semiretta/retta passante per l'origine con pendenza positiva costante (Grafico C).",
    },
    "FIS-C06-NCOM-126": {
        "question": "A una resistenza R = 1 ohm viene applicata una tensione V₁ = 6 V. Se si raddoppia il valore della resistenza, per mantenere costante la corrente che circola nel componente è necessario applicare una nuova tensione V₂ pari a:",
        "explanation": "Per la prima legge di Ohm V = R · I, volendo mantenere invariata l'intensità di corrente I (qui 6 A) quando la resistenza raddoppia (da R a 2R), occorre raddoppiare anche la differenza di potenziale applicata: V₂ = 2 V₁ = 12 V.",
    },
    "FIS-C06-NCOM-133": {
        "answer": "D",
        "answer_text": "Nessuna delle altre risposte è corretta",
        "explanation": "Nelle specie marine (acqua salata ben conduttrice) occorre erogare elevata corrente a basso voltaggio disponendo molte colonne di elettroplacche affiancate in parallelo tra loro, pur impilando le singole cellule in serie concorde (+ contro −) entro ciascuna colonna corta. Affacciare invece il polo positivo di una cellula a moneta contro il polo positivo dell'adiacente (opzione C) le collegherebbe in serie opposta annullando la f.e.m. totale, mentre E descrive una singola lunga pila in serie ad alto voltaggio (tipica dei pesci d'acqua dolce come Electrophorus): è perciò corretta D.",
    },
    "FIS-C06-NCOM-144": {
        "options": {"E": "La differenza di potenziale è la stessa ai capi dei due resistori"},
        "explanation": "In un collegamento in parallelo entrambi i resistori sono sottoposti alla medesima tensione ΔV_g, per cui I₁ = V_g/R₁ e I₂ = V_g/R₂: il rapporto tra le correnti è inversamente proporzionale alle resistenze (I₁/I₂ = R₂/R₁), rendendo certamente errata l'affermazione B (I₁/I₂ = R₁/R₂).",
    },
    "FIS-C06-NCOM-151": {
        "crop_figure": True,
        "explanation": "Nel circuito in figura i resistori uguali 1 e 2 sono in parallelo tra loro e il blocco (1∥2) è in serie con i resistori 3 e 4: la corrente totale I che attraversa per intero i resistori 3 e 4 si divide in due parti uguali (I/2 ciascuno) nei rami identici 1 e 2, per cui la corrente nel resistore 2 è esattamente la metà di quella nel resistore 3.",
    },
    "FIS-C06-NCOM-152": {
        "crop_figure": True,
        "explanation": "Dal diagramma tra A e B si incontrano in serie tre blocchi di resistori tutti di valore R: un singolo resistore (R), una coppia in parallelo (R/2) e una terna in parallelo (R/3). Sommando in serie si ottiene R_AB = R + R/2 + R/3 = (6 + 3 + 2)/6 R = 11/6 R.",
    },
    "FIS-C06-NCOM-186": {
        "crop_figure": True,
        "explanation": "Dalla figura i due fili rettilinei paralleli distano d = 0,8 m e il primo è percorso da I₁ = 5 A. Per la legge di Ampère la forza per unità di lunghezza è F/L = (μ₀ I₁ I₂)/(2πd) = 2·10⁻⁷ · I₁ · I₂ / d; sostituendo 8·10⁻⁶ = 2·10⁻⁷ × 5 × I₂ / 0,8 si ricava I₂ = (8·10⁻⁶ × 0,8) / 10⁻⁶ = 6,4 A.",
    },
    "FIS-C06-NCOM-191": {
        "crop_figure": True,
        "explanation": "Per la legge di Faraday-Neumann si induce corrente solo se varia nel tempo il flusso magnetico Φ(B) attraverso la spira C. Poiché B(x) è uniforme lungo la direzione y e varia solo con x, traslando rigidamente la spira lungo una retta parallela all'asse y ogni elemento di area continua a vedere lo stesso campo B: Φ(B) rimane costante e non si induce alcuna corrente (mentre traslazioni lungo x o rotazioni intorno ai diametri variano Φ).",
    },
    "FIS-C06-COMP-025": {
        "cloze_stem": "La costante elettrostatica di Coulomb nel vuoto può essere scritta come k = 1 / (4π {{c1::ε₀}}).",
        "answer": "ε₀",
        "answer_text": "ε₀ (epsilon con zero)",
        "accepted_synonyms": ["ε₀", "ε0", "epsilon0", "epsilon_0", "ε₀ (epsilon)"],
        "explanation": "Nel Sistema Internazionale la costante di proporzionalità della legge di Coulomb nel vuoto vale k₀ = 1/(4πε₀) ≈ 8,99 × 10⁹ N·m²/C², dove ε₀ ≈ 8,85 × 10⁻¹² F/m è la costante dielettrica del vuoto.",
    },
    "FIS-C06-COMP-034": {
        "cloze_stem": "Il modulo del lavoro compiuto dal campo elettrico quando una carica q attraversa una differenza di potenziale si esprime tramite il prodotto q · {{c1::ΔV}}.",
        "accepted_synonyms": ["ΔV", "delta V"],
        "explanation": "Il lavoro elettrico scambiato nello spostamento di una carica q tra due punti a diverso potenziale è legato al prodotto tra la carica e la variazione di potenziale (con segno W_campo = −qΔV = q(V_i − V_f)).",
    },
    "FIS-C06-COMP-041": {
        "cloze_stem": "L'energia potenziale elettrica di due cariche puntiformi q₁ e q₂ distanti r (posto nullo il potenziale all'infinito) è U = k q₁ q₂ / {{c1::r}}.",
        "accepted_synonyms": ["r"],
        "explanation": "L'energia potenziale elettrostatica di una coppia di cariche puntiformi (con riferimento U(∞) = 0) decresce inversamente con la prima potenza della distanza r secondo U = k q₁q₂ / r (mentre la forza varia come 1/r²).",
    },
    "FIS-C06-COMP-050": {
        "cloze_stem": "L'energia elettrostatica immagazzinata in un condensatore carico è U = ½ C {{c1::V²}}.",
        "accepted_synonyms": ["V²", "V^2", "ΔV²"],
        "explanation": "Il lavoro necessario per caricare un condensatore di capacità C fino alla tensione V viene immagazzinato nel campo elettrico tra le armature ed è pari a U = ½ C V² = ½ Q V = Q² / (2C).",
    },
    "FIS-C06-COMP-065": {
        "cloze_stem": "La densità di corrente microscopica è data dal prodotto n q v_d, dove q è la carica dei portatori, n la loro densità numerica e v_d la velocità di {{c1::deriva}}.",
        "accepted_synonyms": ["deriva"],
        "explanation": "Sotto l'azione di un campo elettrico nei conduttori, al moto caotico di agitazione termica degli elettroni si sovrappone un lento moto medio ordinato caratterizzato dalla velocità di deriva v_d, tale che J = n q v_d.",
    },
    "FIS-C06-COMP-071": {
        "cloze_stem": "La seconda legge di Ohm (relazione fra resistenza e resistività) è R = ρ l / {{c1::A}}.",
        "accepted_synonyms": ["A", "S"],
        "explanation": "Per la seconda legge di Ohm la resistenza elettrica di un filo conduttore omogeneo è direttamente proporzionale alla resistività ρ e alla lunghezza l, e inversamente proporzionale all'area A della sezione trasversale: R = ρ l / A.",
    },
    "FIS-C06-COMP-076": {
        "cloze_stem": "La potenza elettrica assorbita o erogata in corrente continua si calcola come P = I × {{c1::V}}.",
        "accepted_synonyms": ["V", "ΔV"],
        "explanation": "La potenza elettrica istantanea trasferita a un bipolo sottoposto alla tensione V e attraversato dalla corrente I vale P = dW/dt = I · V (misurata in watt: 1 W = 1 A · 1 V).",
    },
    "FIS-C06-COMP-084": {
        "cloze_stem": "Il simbolo della differenza di potenziale elettrico è Δ{{c1::V}}.",
        "accepted_synonyms": ["V"],
        "explanation": "Indicando con V il potenziale elettrico scalare, la differenza di potenziale (tensione elettrica) tra due punti si indica con ΔV = V_B − V_A.",
    },
    "FIS-C06-COMP-090": {
        "cloze_stem": "1 tesla equivale a 1 N · s / (C · {{c1::metro}}).",
        "accepted_synonyms": ["metro", "m"],
        "explanation": "Dalla forza magnetica di Lorentz F = q v B sin θ si ricava dimensionalmente B = F / (q · v), per cui 1 T = 1 N / (C · m/s) = 1 N · s / (C · m).",
    },
    "FIS-C06-COMP-106": {
        "cloze_stem": "L'area di una spira rettangolare è il prodotto della base per l'{{c1::altezza}}.",
        "accepted_synonyms": ["altezza"],
        "explanation": "Nel calcolo del momento magnetico μ = I · A e del momento torcente su una spira rettangolare di lati b e h, l'area racchiusa dalla spira vale A = base × altezza.",
    },
    "FIS-C06-COMP-109": {
        "cloze_stem": "Il momento meccanico (coppia) agente su una spira immersa in un campo magnetico uniforme è τ⃗ = μ⃗ × {{c1::B⃗}}.",
        "answer": "B",
        "answer_text": "B (campo magnetico)",
        "accepted_synonyms": ["B", "B⃗", "campo magnetico"],
        "explanation": "Una spira percorsa da corrente con momento di dipolo magnetico μ⃗ = N I A n̂ immersa in un campo magnetico uniforme B⃗ subisce una coppia meccanica orientatrice data dal prodotto vettoriale τ⃗ = μ⃗ × B⃗.",
    },
    "FIS-C06-COMP-112": {
        "cloze_stem": "Il campo magnetico uniforme generato all'interno di un solenoide lungo il suo asse si calcola come B = μ₀ n {{c1::I}} (con n = N/L densità di spire).",
        "accepted_synonyms": ["I", "i"],
        "explanation": "Per la legge della circuitazione di Ampère applicata a un solenoide ideale di lunghezza L e N spire percorse dalla corrente I (densità lineare n = N/L), il campo magnetico interno vale B = μ₀ (N/L) I = μ₀ n I.",
    },
    "FIS-C07-NCOM-010": {
        "question": "Si consideri uno specchio sferico. Detta p la distanza tra l'oggetto e lo specchio, q la distanza tra l'immagine (reale) e lo specchio ed f la distanza focale, per la formula dei punti coniugati si ha:",
        "options": {"C": "1/p − 1/q = 1/f", "D": "p + q = 1/f"},
        "explanation": "Nell'approssimazione parassiale di Gauss per specchi sferici (e lenti sottili), la distanza dell'oggetto p, la distanza dell'immagine q e la lunghezza focale f sono legate dalla legge dei punti coniugati: 1/p + 1/q = 1/f.",
    },
    "FIS-C07-NCOM-023": {
        "options": {"A": "Esse oscillano parallelamente alla direzione di propagazione"},
        "answer_text": "Esse oscillano parallelamente alla direzione di propagazione",
        "explanation": "Nei fluidi (liquidi come l'acqua e gas, privi di modulo di taglio elastico) le onde sonore sono esclusivamente onde meccaniche longitudinali di compressione e rarefazione: le particelle del mezzo oscillano avanti e indietro parallelamente alla direzione di propagazione dell'onda.",
    },
    "FIS-C07-NCOM-037": {
        "question": "Un'onda elettromagnetica di frequenza f si propaga nel vuoto con velocità c. La sua lunghezza d'onda λ è data da:",
        "options": {"A": "λ = 1/f", "B": "λ = f/c", "C": "λ = c·f", "D": "λ = c", "E": "λ = c/f"},
        "answer_text": "λ = c/f",
        "explanation": "Per qualunque onda periodica la velocità di fase è il prodotto della lunghezza d'onda per la frequenza (c = λ · f = λ / T): invertendo la relazione si ottiene λ = c / f.",
    },
    "FIS-C07-NCOM-040": {
        "question": "Le onde radio sono onde:",
        "explanation": "Le onde radio costituiscono la regione a maggiore lunghezza d'onda (e minore frequenza) dello spettro delle onde elettromagnetiche: non richiedono un mezzo materiale e si propagano nel vuoto alla velocità della luce c.",
    },
    "FIS-C07-NCOM-049": {
        "crop_figure": True,
        "explanation": "Il fascio incidente è già linearmente polarizzato lungo z (intensità iniziale I₀). Dalla figura il primo polarizzatore ha asse a θ₁ = 45° rispetto a z, quindi per la legge di Malus trasmette I₁ = I₀ cos²(45°) = 0,5 I₀ polarizzata a 45°; il secondo polarizzatore ha asse a 0° rispetto a z (angolo relativo Δθ = 45° rispetto al primo), per cui trasmette I₂ = I₁ cos²(45°) = 0,5 I₀ × 0,5 = 0,25 I₀, pari al 25% dell'intensità iniziale.",
    },
    "FIS-C07-NCOM-050": {
        "crop_figure": True,
        "explanation": "Nella diffrazione di Fraunhofer da singola fenditura di larghezza a il primo minimo cade a sin θ = λ/a, mentre il flusso luminoso totale trasmesso diminuisce restringendo la fenditura: riducendo a, l'angolo di diffrazione θ aumenta (la figura si allarga) e l'intensità luminosa di tutti i picchi (centrale e secondari) diminuisce.",
    },
    "FIS-C07-COMP-019": {
        "cloze_stem": "In un'onda stazionaria la distanza tra due nodi successivi è pari a {{c1::λ}} / 2.",
        "answer": "λ",
        "answer_text": "λ (lambda)",
        "accepted_synonyms": ["λ", "lambda", "λ (lambda)"],
        "explanation": "In un'onda stazionaria armonica i nodi (punti di ampiezza costantemente nulla) si ripetono ogni mezza lunghezza d'onda: la distanza tra due nodi consecutivi (o tra due ventri consecutivi) è d = λ / 2.",
    },
    "FIS-C07-COMP-038": {
        "cloze_stem": "La relazione n₁ sin θ₁ = n₂ sin θ₂ è la legge di {{c1::Snell}} (della rifrazione).",
        "accepted_synonyms": ["Snell", "Snell-Cartesio", "Cartesio"],
        "explanation": "La legge di Snell-Cartesio governa la rifrazione di un raggio luminoso al passaggio tra due mezzi trasparenti con indici di rifrazione n₁ e n₂: n₁ sin θ₁ = n₂ sin θ₂.",
    },
    "FIS-C07-COMP-045": {
        "cloze_stem": "La riflessione interna totale si può verificare solo se n₁ è {{c1::maggiore}} di n₂.",
        "accepted_synonyms": ["maggiore", "più grande", ">"],
        "explanation": "Dalla legge di Snell sin θ₂ = (n₁/n₂) sin θ₁, l'angolo limite θ_L (per cui θ₂ = 90° e sin θ_L = n₂/n₁ ≤ 1) esiste solo quando il raggio proviene dal mezzo otticamente più denso verso quello meno denso, ossia per n₁ > n₂.",
    },
    "FIS-C08-NCOM-004": {
        "options": {"E": "si trasforma in un protone"},
        "answer_text": "si trasforma in un protone",
        "explanation": "Nel decadimento radioattivo β⁻ mediato dall'interazione debole un neutrone nucleare si converte in un protone (rimanendo nel nucleo) con emissione di un elettrone veloce (β⁻) e di un antineutrino elettronico: n → p⁺ + e⁻ + ν̄_e.",
    },
    "FIS-C08-NCOM-006": {
        "question": "L'isotopo carbonio-14 (¹⁴C) ha una emivita di 5.760 anni. Dopo 17.280 anni la sua radioattività iniziale sarà ridotta a un:",
        "explanation": "L'intervallo di tempo trascorso corrisponde esattamente a k = 17.280 / 5.760 = 3 tempi di dimezzamento (emivite): l'attività residua vale quindi A = A₀ · (1/2)³ = A₀ / 8, ossia un ottavo di quella iniziale.",
    },
    "FIS-C08-NCOM-014": {
        "options": {
            "A": "l'isotopo 235 è l'unico isotopo naturale dell'uranio che subisce fissione per cattura di neutroni termici",
            "B": "l'isotopo 235 produce un'energia maggiore nella reazione nucleare, per cui l'uranio arricchito è un combustibile di migliore qualità",
        },
        "answer_text": "l'isotopo 235 è l'unico isotopo naturale dell'uranio che subisce fissione per cattura di neutroni termici",
        "explanation": "L'uranio naturale è composto per oltre il 99,2% da ²³⁸U (non fissile con neutroni lenti/termici) e solo per lo 0,72% da ²³⁵U, unico isotopo naturale termicamente fissile: nei reattori ad acqua leggera occorre arricchire la frazione di ²³⁵U al 3–5% per sostenere la reazione a catena.",
    },
    "FIS-C08-COMP-009": {
        "cloze_stem": "L'equazione di Einstein dell'effetto fotoelettrico è K_max = h f − {{c1::φ}}.",
        "answer": "φ",
        "answer_text": "φ (phi, lavoro di estrazione)",
        "accepted_synonyms": ["φ", "phi", "φ (phi)", "W₀", "L₀", "lavoro di estrazione"],
        "explanation": "Nell'effetto fotoelettrico un singolo fotone di energia E = hf cede la propria energia a un elettrone del metallo: sottratto il lavoro di estrazione minimo φ (o W₀) caratteristico del metallo, l'energia residua compare come energia cinetica massima K_max = hf − φ.",
    },
    "FIS-C08-COMP-013": {
        "cloze_stem": "La relazione dualistica λ = h / p fu proposta da {{c1::de Broglie}}.",
        "accepted_synonyms": ["de Broglie", "Louis de Broglie", "De Broglie"],
        "explanation": "Nel 1924 Louis de Broglie estese il dualismo onda-corpuscolo dalla radiazione alla materia, associando a ogni particella dotata di quantità di moto p = mv una lunghezza d'onda λ = h / p.",
    },
    "FIS-C08-COMP-029": {
        "cloze_stem": "La costante di Planck h ha un valore di circa 6,63 × 10⁻³⁴ {{c1::J}} · s.",
        "accepted_synonyms": ["J", "joule"],
        "explanation": "Dalla relazione di Planck E = h · f (con E in joule e f in s⁻¹ = Hz) si ricava che la costante di Planck h = 6,626 × 10⁻³⁴ J · s ha le dimensioni di un'azione (energia × tempo, joule per secondo).",
    },
}
