#!/usr/bin/env python3
"""Exact remediation & Italian scientific explanations for all 118 BIO items in bio_434.txt (+ tie-breaks)."""
from __future__ import annotations

BIO_118: dict[str, dict] = {
    "BIO-C01-NCOM-003": {
        "options": {"D": "Iodio"},
        "answer_text": "Iodio",
        "explanation": "Idrogeno, ossigeno e azoto sono macroelementi plastici primari e il calcio è un macroelemento secondario, mentre lo iodio (I, essenziale per gli ormoni tiroidei T₃ e T₄) è un oligoelemento presente in tracce (< 0,01%).",
    },
    "BIO-C01-NCOM-012": {
        "explanation": "Tra le macromolecole organiche elencate nelle opzioni A–D, le proteine costituiscono la frazione ponderalmente più abbondante della cellula (~15–18% del peso fresco e oltre il 50% del peso secco).",
        "errata_note": "Nota: considerando l'intera composizione chimica (inclusi i composti inorganici), il costituente principale della cellula è l'acqua (~70–80% della massa cellulare, il che renderebbe difendibile E); la chiave EdiSES seleziona C intendendo il principale costituente macromolecolare organico.",
    },
    "BIO-C01-NCOM-015": {
        "explanation": "Escludendo l'acqua (peso secco), la materia vivente è costituita prevalentemente da biomolecole organiche del carbonio (proteine, acidi nucleici, carboidrati e lipidi).",
        "errata_note": "Nota: sul peso fresco complessivo degli organismi viventi predomina l'acqua (65–85%, composto inorganico, opzione A); la chiave EdiSES seleziona E riferendosi alle componenti strutturali e funzionali caratteristiche dei viventi (peso secco).",
    },
    "BIO-C01-NCOM-021": {
        "options": {"B": "Sono composti da C, H e O"},
        "explanation": "Nel catabolismo energetico cellulare (glicolisi e respirazione cellulare) i glucidi vengono ossidati (e non ridotti) fino a CO₂ e H₂O liberando energia chimica: pertanto l'affermazione E è falsa.",
    },
    "BIO-C01-NCOM-052": {
        "options": {
            "A": "il dalton (Da)",
            "C": "il micron (µm)",
            "D": "l'ångström (Å)",
        },
        "answer_text": "il micron (µm)",
        "explanation": "La maggior parte delle cellule eucariotiche umane ha un diametro compreso tra circa 10 e 30 micrometri (micron, 1 µm = 10⁻⁶ m).",
    },
    "BIO-C01-NCOM-056": {
        "question": "La figura si riferisce ad un microscopio ottico. La struttura indicata con la lettera A prende il nome di:",
        "crop_figure": True,
        "explanation": "Nella figura del microscopio ottico composto la manopola inferiore/interna indicata con A regola gli spostamenti verticali fini del tavolino portaoggetti per la messa a fuoco di precisione ed è la vite micrometrica.",
    },
    "BIO-C01-NCOM-058": {
        "options": {"A": "i nuclei", "B": "i batteri"},
        "answer_text": "i batteri",
        "explanation": "Le cellule procariotiche (batteri) possiedono tipicamente un singolo cromosoma costituito da una molecola di DNA circolare a doppia elica immersa nel nucleoide (i virus non sono cellule, mentre eucarioti animali e funghi hanno cromosomi nucleari lineari).",
    },
    "BIO-C01-NCOM-091": {
        "crop_figure": True,
        "explanation": "La figura mostra una cellula dotata di parete, flagello batterico e DNA sparso nel citoplasma (nucleoide) privo di involucro nucleare e di organelli membranosi interni: si tratta quindi di una cellula procariotica.",
    },
    "BIO-C01-NCOM-174": {
        "explanation": "Nella classificazione trofica generale (riferita in particolare agli animali), gli organismi eterotrofi ricavano carbonio e azoto da molecole organiche preformate (amminoacidi, glucidi) e non sono in grado di organicare azoto inorganico ossidato sotto forma di nitrati (NO₃⁻), prerogativa tipica di piante e microrganismi assimilatori.",
        "errata_note": "Nota: in microbiologia diversi funghi e batteri chemioeterotrofi sono in realtà capaci di assimilare o respirare nitrati; nel contesto generale dei test medico-biologici EdiSES «eterotrofi» è riferito agli eterotrofi animali (chiave D).",
    },
    "BIO-C01-NCOM-212": {
        "explanation": "Partendo da 1 molecola di DNA interamente ¹⁵N/¹⁵N e replicando in ¹⁴N: dopo la 1ª divisione si ottengono 2 molecole ibride ¹⁵N/¹⁴N (100%); dopo la 2ª divisione 4 molecole di cui 2 ibride (50%); dopo la 3ª divisione 2³ = 8 molecole totali, di cui sempre 2 ibride ¹⁵N/¹⁴N e 6 leggere ¹⁴N/¹⁴N, cioè 2/8 = 25%.",
    },
    "BIO-C01-NCOM-216": {
        "answer": "A",
        "answer_text": "8",
        "explanation": "Partendo dai singoli costituenti liberi (fosfato, deossiribosio e basi azotate): la sintesi di ciascun mononucleotide richiede 2 condensazioni (1 legame N-glicosidico base-zucchero + 1 legame fosfoestereo zucchero-fosfato), quindi 3 × 2 = 6 condensazioni per formare i 3 nucleotidi; la loro successiva polimerizzazione in un trinucleotide richiede altri 2 legami fosfodiesterici (n − 1 = 2 condensazioni), per un totale complessivo di 6 + 2 = 8 reazioni di condensazione.",
        "errata_note": "Errata corrige chiave EdiSES (tie-break risolto): la chiave stampata (p. 605) riportava erroneamente D («6») dimenticando i 2 legami fosfodiesterici tra i tre nucleotidi (mentre «2», opzione B, varrebbe solo partendo da nucleotidi già preformati). Partendo da fosfato, zucchero e basi libere il valore esatto è 8 (opzione A).",
    },
    "BIO-C01-NCOM-263": {
        "crop_figure": True,
        "explanation": "Nell'albero filogenetico in figura l'asse orizzontale rappresenta la divergenza morfologica/specifica e l'asse verticale il tempo fino ad «oggi»: il ramo X–Q–X¹ sale verticalmente senza biforcarsi in linee distinte, indicando che Q è una forma ancestrale lungo la medesima linea filetica di X¹ (mentre X¹ si arresta prima di «oggi» ma l'opzione selezionata dalla chiave per quel diagramma segue la continuità di specie X–Q–X¹).",
        "errata_note": "Nota sul grafico: nel cladogramma originale X¹ termina anche prima della linea «oggi» (specie estinta, opzione E); la chiave ufficiale EdiSES per questo quesito è B.",
    },
    "BIO-C01-COMP-066": {
        "cloze_stem": "I {{c1::legami covalenti}} si formano quando due atomi condividono una o più coppie di elettroni, creando molecole stabili.",
        "answer": "legami covalenti",
        "answer_text": "legami covalenti",
        "accepted_synonyms": ["legami covalenti", "covalenti"],
        "explanation": "La condivisione di una, due o tre coppie di elettroni di valenza tra due atomi definisce i legami covalenti (singoli, doppi o tripli), responsabili della stabilità delle molecole biologiche.",
    },
    "BIO-C01-COMP-083": {
        "cloze_stem": "I {{c1::carboidrati}} sono composti organici con formula generale approssimativa Cₙ(H₂O)ₙ, comprendenti monosaccaridi, disaccaridi e polisaccaridi.",
        "accepted_synonyms": ["carboidrati", "glucidi", "zuccheri", "idrati di carbonio"],
        "explanation": "I carboidrati (o glucidi, «idrati di carbonio» dalla stechiometria empirica Cₙ(H₂O)ₙ dei monosaccaridi) si suddividono in monosaccaridi, oligosaccaridi (tra cui i disaccaridi) e polisaccaridi.",
    },
    "BIO-C01-COMP-120": {
        "cloze_stem": "L'{{c1::ossidazione aerobica}} del piruvato nei mitocondri, attraverso il ciclo di Krebs, produce CO₂, NADH, FADH₂ e ATP.",
        "accepted_synonyms": ["ossidazione aerobica", "ossidazione", "decarbossilazione ossidativa"],
        "explanation": "In condizioni aerobiche il piruvato entra nella matrice mitocondriale, viene decarbossilato ad acetil-CoA e completamente ossidato nel ciclo di Krebs a CO₂, riducendo i coenzimi NAD⁺ e FAD a NADH e FADH₂ e generando GTP/ATP.",
    },
    "BIO-C02-COMP-016": {
        "cloze_stem": "I territori cromosomici sono aree specifiche del nucleo in cui si localizzano i cromosomi {{c1::interfasici}}, contribuendo alla regolazione genica.",
        "answer": "interfasici",
        "answer_text": "interfasici",
        "accepted_synonyms": ["interfasici", "in interfase"],
        "explanation": "Durante l'interfase i cromosomi decondensati non si mescolano casualmente come un gomitolo indistinto, ma occupano ciascuno una regione nucleare discreta detta territorio cromosomico (cromosomi interfasici), la cui posizione radiale influenza l'accessibilità trascrizionale.",
    },
    "BIO-C02-NCOM-005": {
        "question": "Se in una cellula diploide nella fase G₂ della meiosi la quantità di DNA è pari a Y, quale sarà la quantità di DNA presente in metafase II in ogni singola cellula?",
        "options": {"A": "0,5Y", "E": "0,25Y"},
        "answer_text": "0,5Y",
        "explanation": "In fase G₂ premeiotica il DNA è già duplicato (4c = Y). Al termine della meiosi I (divisione riduzionale) gli omologhi si separano in due cellule aploidi con cromosomi dicromatidici: ciascuna cellula in metafase II possiede quindi metà del DNA presente in G₂, cioè 2c = 0,5Y (scenderà a 0,25Y solo nei gameti finali dopo la meiosi II).",
    },
    "BIO-C02-NCOM-006": {
        "question": "Il rapporto di compattazione del DNA in un cromosoma durante la metafase, in cui è massima la condensazione di cromatina, è di 1:10⁴. Ciò significa che se il DNA di un cromosoma lungo circa 4 µm fosse completamente svolto, si otterrebbe un filamento lungo:",
        "options": {
            "A": "16.000 µm cioè 16 mm",
            "B": "4.000 µm cioè 40 cm",
            "C": "40.000 µm cioè 40 m",
            "D": "40.000 µm cioè 40 cm",
            "E": "40.000 µm cioè 4 cm",
        },
        "answer_text": "40.000 µm cioè 4 cm",
        "explanation": "Moltiplicando la lunghezza metafasica per il fattore di compattazione si ottiene 4 µm × 10⁴ = 40.000 µm; poiché 1 µm = 10⁻⁴ cm (1 cm = 10.000 µm), 40.000 µm equivalgono esattamente a 4 cm.",
    },
    "BIO-C02-NCOM-107": {
        "explanation": "La metilazione delle code istoniche (su residui di lisina e arginina) è il classico marchio epigenetico ambivalente: può attivare la trascrizione (es. H3K4me3 sui promotori attivi) oppure reprimerla stabilmente (es. H3K9me3 e H3K27me3 nell'eterocromatina).",
        "errata_note": "Nota: anche la monoubiquitinazione istonica (opzione D) può avere effetti opposti a seconda dell'istone bersaglio (H2BK120ub1 attiva, H2AK119ub1 reprime); nei manuali di riferimento del Semestre Filtro il paradigma canonico di modifica istonica attivante o repressiva è la metilazione (E).",
    },
    "BIO-C03-NCOM-064": {
        "question": "In figura è rappresentato uno schema della sequenza genica che costituisce l'operone Lac (sequenza genica che regola la produzione delle lattasi) dei procarioti. Si tratta di una sequenza regolatrice che determina la produzione di lattasi:",
        "options": {"C": "non è influenzata dalla presenza di lattosio nel mezzo di coltura"},
        "crop_figure": True,
        "explanation": "L'operone lac di Escherichia coli è un sistema inducibile a controllo negativo: in assenza di lattosio il repressore LacI si lega all'operatore bloccando la trascrizione, mentre quando è presente lattosio nel mezzo l'induttore (allolattosio) inattiva il repressore consentendo la sintesi degli enzimi per il metabolismo del lattosio.",
    },
    "BIO-C03-NCOM-076": {
        "explanation": "Nella formulazione divulgativa adottata dalla chiave EdiSES l'espressione viene riferita all'informazione genetica codificata nella sequenza nucleotidica del DNA (opzione D).",
        "errata_note": "Attenzione concettuale importante: in biologia molecolare rigorosa il «codice genetico» NON è la sequenza di basi del DNA di un singolo organismo (che ne costituisce il genoma/genotipo), bensì il dizionario universale di corrispondenza tra i 64 codoni (triplette di mRNA) e i 20 amminoacidi più i segnali di stop (il che renderebbe rigorosamente corretta E); si mantiene D per allineamento con la banca dati EdiSES segnalando l'imprecisione.",
    },
    "BIO-C03-NCOM-129": {
        "options": {
            "A": "5' → 3'",
            "B": "3' → 5'",
            "D": "Solo 5' → 5'",
        },
        "answer_text": "5' → 3'",
        "explanation": "Tutte le DNA polimerasi note aggiungono deossiribonucleotidi trifosfato esclusivamente all'ossidrile libero 3'-OH dell'innesco, leggendo lo stampo in direzione 3' → 5' e sintetizzando quindi la nuova catena sempre in direzione 5' → 3'.",
    },
    "BIO-C03-NCOM-138": {
        "options": {
            "A": "DNA polimerasi δ",
            "B": "DNA polimerasi ε",
            "C": "DNA polimerasi α",
            "D": "DNA polimerasi β",
            "E": "DNA polimerasi γ",
        },
        "answer_text": "DNA polimerasi γ",
        "explanation": "Negli eucarioti la replicazione e la riparazione del genoma circolare mitocondriale (mtDNA) sono affidate specificamente alla DNA polimerasi γ, mentre α, δ ed ε operano nella replicazione nucleare e β nella riparazione per escissione di basi (BER).",
    },
    "BIO-C03-NCOM-141": {
        "options": {
            "A": "DNA polimerasi ε",
            "B": "DNA polimerasi α",
            "C": "DNA polimerasi γ",
            "D": "DNA polimerasi δ",
            "E": "DNA polimerasi β",
        },
        "answer_text": "DNA polimerasi δ",
        "explanation": "Nella forcella replicativa nucleare eucariotica, dopo la sintesi dell'innesco RNA-DNA da parte del complesso Pol α/primasi, l'allungamento dei frammenti di Okazaki sul filamento ritardato (lagging) è catalizzato dalla DNA polimerasi δ associata a PCNA (mentre Pol ε sintetizza il filamento leading).",
    },
    "BIO-C03-NCOM-169": {
        "question": "Quale RNA polimerasi sintetizza l'rRNA 18S, 28S e 5,8S negli eucarioti?",
        "options": {"C": "RNA polimerasi III"},
        "explanation": "Negli eucarioti la RNA polimerasi I, localizzata nel nucleolo, trascrive il grande precursore pre-rRNA 45S da cui per maturazione derivano gli rRNA ribosomiali 18S, 5,8S e 28S (mentre l'rRNA 5S e i tRNA sono trascritti dalla Pol III e gli mRNA dalla Pol II).",
    },
    "BIO-C03-NCOM-170": {
        "question": "Quale RNA polimerasi è responsabile della sintesi di tRNA e rRNA 5S?",
        "explanation": "Nelle cellule eucariotiche la RNA polimerasi III sintetizza tutti gli RNA transfer (tRNA), l'rRNA ribosomiale 5S e alcuni piccoli RNA nucleari/citoplasmatici (come U6 snRNA e 7SL RNA).",
    },
    "BIO-C03-NCOM-189": {
        "options": {"C": "U5"},
        "answer_text": "U5",
        "explanation": "Nello spliceosoma le snRNP agiscono in modo coordinato: U1 riconosce il sito donatore GU al 5', U2 lega il punto di ramificazione A, mentre l'ansa conservata di U5 snRNA (insieme al fattore proteico U2AF35 sul dinucleotide AG) posiziona e allinea i margini esonici presso il sito accettore 3' AG.",
        "errata_note": "Nota: biochimicamente il dinucleotide AG al 3' è riconosciuto direttamente dalla subunità proteica U2AF35 (che recluta U2 snRNP sul branch point), mentre tra gli snRNA U5 interagisce con le sequenze esoniche adiacenti ai siti 5' e 3'; la chiave EdiSES indica C (U5).",
    },
    "BIO-C03-NCOM-216": {
        "explanation": "La degenerazione (o ridondanza) del codice genetico indica che 61 codoni codificanti specificano 20 amminoacidi, per cui più codoni sinonimi possono codificare per il medesimo amminoacido (mentre la «non ambiguità» indica che ogni codone specifica un solo amminoacido).",
        "errata_note": "Nota editoriale: nella stampa EdiSES compaiono sia «Degenerazione» (A, termine tecnico canonico scelto dalla chiave ufficiale) sia il sinonimo «Ridondanza» (E).",
    },
    "BIO-C03-NCOM-234": {
        "explanation": "La degradazione selettiva delle proteine poliubiquitinate nel proteasoma 26S è un processo strettamente ATP-dipendente: sia l'attivazione dell'ubiquitina da parte dell'enzima E1 sia il dispiegamento meccanico e la traslocazione del substrato nell'anello AAA+ della subunità regolatrice 19S consumano ATP.",
        "errata_note": "Nota: in senso biologico ampio anche la replicazione, la trascrizione, l'anabolismo glucidico e l'importazione mitocondriale richiedono idrolisi di NTP/ATP; nel capitolo sulla regolazione post-traduzionale delle proteine la chiave EdiSES punta specificamente alla degradazione proteasomica ATP-dipendente (E).",
    },
    "BIO-C03-NCOM-239": {
        "options": {"A": "Foglietti β", "B": "α-eliche"},
        "answer_text": "Foglietti β",
        "explanation": "Nelle fibrille amiloidi (associate a patologie neurodegenerative come Alzheimer, Parkinson ed encefalopatie prioniche) le proteine malripiegate convertono la loro conformazione nativa in aggregati insolubili ricchi di foglietti β incrociati (cross-β) molto stabili.",
    },
    "BIO-C03-COMP-011": {
        "cloze_stem": "Nei procarioti, la DNA polimerasi {{c1::III}} è l'enzima principale della sintesi, con una velocità di circa 1000 nucleotidi al secondo.",
        "answer": "III",
        "answer_text": "III",
        "accepted_synonyms": ["III", "3", "DNA polimerasi III"],
        "explanation": "In Escherichia coli e negli altri procarioti l'oloenzima replicativo principale ad alta processività (~1000 nt/s) è la DNA polimerasi III, mentre la DNA polimerasi I rimuove gli inneschi di RNA (attività esonucleasica 5'→3') e riempie le brevi interruzioni.",
        "errata_note": "Errata corrige OCR/chiave: il database precedente riportava «I» per troncamento del numero romano «III»; l'enzima procariotico che polimerizza a ~1000 nt/s è inequivocabilmente la DNA polimerasi III.",
    },
    "BIO-C03-COMP-013": {
        "cloze_stem": "Le DNA polimerasi eucariotiche sono indicate con lettere greche; la {{c1::α}} è coinvolta nell'inizio della sintesi, la δ nel filamento lento e la ε nel filamento guida.",
        "answer": "α",
        "answer_text": "α (alfa)",
        "accepted_synonyms": ["α", "alfa", "alpha"],
        "explanation": "Negli eucarioti il complesso DNA polimerasi α-primasi sintetizza i brevi primer ibridi RNA-DNA dando inizio alla sintesi, dopodiché avviene lo scambio polimerasico con Pol δ (filamento ritardato/lagging) e Pol ε (filamento guida/leading).",
    },
    "BIO-C03-COMP-042": {
        "cloze_stem": "L'{{c1::RNA polimerasi}} batterica è l'enzima responsabile della trascrizione e necessita di un fattore σ per il riconoscimento del promotore.",
        "accepted_synonyms": ["RNA polimerasi"],
        "explanation": "Nei batteri un'unica RNA polimerasi DNA-dipendente (core α₂ββ'ω) si associa transitoriamente alla subunità regolatrice σ (fattore sigma) formando l'oloenzima capace di riconoscere le sequenze consenso (−35 e −10) del promotore.",
    },
    "BIO-C03-COMP-045": {
        "cloze_stem": "I geni strutturali dell'operone Lac comprendono lacZ, lacY e {{c1::lacA}}, che codificano rispettivamente per β-galattosidasi, permeasi e transacetilasi.",
        "accepted_synonyms": ["lacA", "lac A"],
        "explanation": "L'mRNA policistronico dell'operone lac contiene in ordine i tre geni strutturali lacZ (β-galattosidasi), lacY (β-galattoside permeasi di membrana) e lacA (β-galattoside transacetilasi).",
    },
    "BIO-C03-COMP-046": {
        "cloze_stem": "La {{c1::β-galattosidasi}} scinde il lattosio in glucosio e galattosio, permettendo al batterio di utilizzarlo come fonte di energia.",
        "answer": "β-galattosidasi",
        "answer_text": "β-galattosidasi",
        "accepted_synonyms": ["β-galattosidasi", "beta-galattosidasi", "lattasi"],
        "explanation": "Codificata dal gene lacZ, la β-galattosidasi idrolizza il legame β-1,4-glicosidico del lattosio liberando D-glucosio e D-galattosio (e catalizza inoltre l'isomerizzazione di una piccola quota di lattosio nell'induttore allolattosio).",
    },
    "BIO-C03-COMP-050": {
        "cloze_stem": "L'{{c1::allolattosio}}, derivato del lattosio, agisce come induttore legandosi al repressore e inattivandolo.",
        "accepted_synonyms": ["allolattosio"],
        "explanation": "L'allolattosio (isomero β-1,6 del lattosio) è l'induttore fisiologico dell'operone lac: legandosi allostericamente al repressore LacI ne riduce l'affinità per l'operatore, rendendo il repressore inattivo e sbloccando la trascrizione.",
    },
    "BIO-C03-COMP-074": {
        "cloze_stem": "L'{{c1::RNA polimerasi I}} è localizzata nel nucleolo e trascrive l'rRNA 45S, precursore di 28S, 18S e 5,8S.",
        "accepted_synonyms": ["RNA polimerasi I", "Pol I"],
        "explanation": "Nel nucleolo eucariotico la RNA polimerasi I trascrive le ripetizioni geniche ribosomiali producendo il pre-rRNA 45S, che viene metilato, pseudouridilato e tagliato negli rRNA maturi 18S (subunità 40S) e 28S + 5,8S (subunità 60S).",
    },
    "BIO-C03-COMP-099": {
        "cloze_stem": "Un esempio di {{c1::RNA editing}} è la produzione di due forme dell'apolipoproteina B, diverse tra fegato e intestino.",
        "accepted_synonyms": ["RNA editing", "editing dell'RNA"],
        "explanation": "Nel gene umano APOB una citidina deaminasi tessuto-specifica (APOBEC1) nell'intestino converte una specifica citosina (CAA, Gln) in uracile (UAA, codone di stop), generando la forma corta ApoB-48 per i chilomicroni, mentre nel fegato non editato si traduce l'intera ApoB-100.",
    },
    "BIO-C03-COMP-106": {
        "cloze_stem": "L'{{c1::RNA interference}} è un processo di silenziamento genico mediato da piccoli RNA, come siRNA e miRNA.",
        "answer": "RNA interference",
        "answer_text": "RNA interference (RNAi)",
        "accepted_synonyms": ["RNA interference", "RNAi", "RNA interference (RNAi)", "interferenza a RNA"],
        "explanation": "L'interferenza a RNA (RNAi) è un meccanismo post-trascrizionale conservato in cui piccoli RNA non codificanti (siRNA e miRNA maturati da Dicer) guidano il complesso RISC/Argonauta a degradare o reprimere la traduzione di mRNA bersaglio complementari.",
    },
    "BIO-C03-COMP-115": {
        "cloze_stem": "Gli {{c1::rRNA}} maturi 28S, 18S e 5,8S derivano da un precursore trascritto nel nucleolo (mentre il 5S è trascritto nel nucleoplasma).",
        "accepted_synonyms": ["rRNA", "RNA ribosomiali"],
        "explanation": "Gli RNA ribosomiali (rRNA) costituiscono l'impalcatura strutturale e catalitica del ribosoma: 28S, 18S e 5,8S maturano dal pre-rRNA 45S nucleolare (Pol I), cui si associa nel nucleolo l'rRNA 5S sintetizzato nel nucleoplasma dalla Pol III.",
    },
    "BIO-C03-COMP-123": {
        "cloze_stem": "I {{c1::fattori di elongazione}} guidano l'ingresso dei nuovi amminoacil-tRNA nel sito A e promuovono l'avanzamento della sintesi proteica.",
        "accepted_synonyms": ["fattori di elongazione", "fattori di allungamento"],
        "explanation": "I fattori di elongazione GTP-dipendenti (EF-Tu/eEF1A e EF-G/eEF2) scortano correttamente l'amminoacil-tRNA nel sito A ribosomiale (proofreading cinetico) e promuovono la traslocazione, mentre il legame peptidico vero e proprio è catalizzato dal ribozima rRNA 23S/28S.",
    },
    "BIO-C04-COMM-014": {
        "question": "In una razza di cani il carattere «assenza di pelo» è dovuto al genotipo eterozigote Hh. I cani con pelo normale sono omozigoti recessivi (hh); il genotipo omozigote dominante (HH) è letale e gli individui nascono morti. Se un allevatore vuole cani privi di pelo, gli converrà fare un accoppiamento tra:",
        "options": {"A": "entrambi i genitori mancanti di pelo"},
        "answer": "A",
        "answer_text": "entrambi i genitori mancanti di pelo",
        "explanation": "Incrociando due cani privi di pelo (Hh × Hh) i genotipi zigotici seguono il rapporto 1 HH : 2 Hh : 1 hh; poiché gli omozigoti HH muoiono prima/alla nascita, tra i cuccioli vitali 2 su 3 (66,7%) sono privi di pelo (Hh) e 1 su 3 (33,3%) ha pelo normale (hh). Nell'incrocio Hh × hh (opzione B) i cuccioli senza pelo sono invece solo 1 su 2 (50%); pertanto l'incrocio A fornisce la frazione più elevata di cani privi di pelo.",
    },
    "BIO-C04-NCOM-017": {
        "options": {"E": "allotipo"},
        "explanation": "Le forme alternative di uno stesso gene che occupano il medesimo locus su cromosomi omologhi si chiamano alleli.",
        "errata_note": "Nota: «allelomorfo» (opzione B, termine originario introdotto da Bateson da cui deriva per abbreviazione «allele») è storicamente sinonimo esatto di «allele» (opzione A, forma moderna standard selezionata dalla chiave EdiSES).",
    },
    "BIO-C04-NCOM-030": {
        "question": "Dall'incrocio tra due individui con genotipo Aa, quali genotipi e con quali probabilità si potranno avere in F₁?",
        "options": {
            "B": "25% AA, 50% Aa, 25% aa",
            "D": "50% Aa, 50% aa",
            "E": "50% AA, 25% Aa, 25% aa",
        },
        "answer_text": "25% AA, 50% Aa, 25% aa",
        "explanation": "Per la legge della segregazione di Mendel ciascun genitore Aa produce gameti 50% A e 50% a: il quadrato di Punnett fornisce 1/4 (25%) AA, 2/4 (50%) Aa e 1/4 (25%) aa.",
    },
    "BIO-C04-NCOM-035": {
        "crop_figure": True,
        "explanation": "Con epistasi recessiva (cc = bianco, B_C_ = nero, bbC_ = marrone): l'Incrocio 1 (nero × nero → nero, marrone e bianco) richiede che entrambi i genitori portino gli alleli recessivi b e c, ossia BbCc × BbCc; l'Incrocio 2 (nero × marrone → tutti neri) richiede il genitore nero omozigote dominante BB (es. BBCc × bbCC); l'Incrocio 3 (bianco × nero → neri o marroni, nessun bianco) richiede il genitore bianco cc ma portatore di b e l'altro omozigote CC eterozigote Bb (bbcc × BbCC): tale combinazione corrisponde esattamente alla Riga 4 della tabella.",
    },
    "BIO-C04-NCOM-057": {
        "explanation": "La donna sana figlia di un genitore albino (aa) è portatrice obbligata eterozigote Aa. Il maschio sano con genitori e nonni tutti fenotipicamente normali non ha alcuna anamnesi familiare nota per questo carattere raro, per cui la probabilità che sia portatore eterozigote è solo quella della popolazione generale (molto bassa, ~1–2%) e la probabilità di un figlio albino è quindi trascurabile («praticamente nulla»); tuttavia nei quesiti scolastici semplificati la chiave EdiSES ipotizza implicitamente anche il padre eterozigote Aa dando 1/4 = 25% (opzione D).",
        "errata_note": "Attenzione critica: geneticamente, senza consanguineità né casi familiari nel ramo paterno, il padre NON è portatore obbligato (se q ≈ 1/100, P(figlio aa) = 2pq/(1+2pq) × 1/4 ≈ 0,5%, cioè A «praticamente nulla»); la chiave EdiSES riporta D (25%) assumendo impropriamente un incrocio Aa × Aa.",
    },
    "BIO-C04-NCOM-076": {
        "explanation": "Poiché la coppia ha già avuto due figlie femmine (eventi già realizzati con probabilità condizionata pari a 1) e ogni concepimento successivo è statisticamente indipendente con p(femmina) = 1/2, per avere una famiglia complessiva di sei figlie occorre che siano femmine le restanti 4 nascite: P = (1/2)⁴ = 1/16. La chiave EdiSES riporta tuttavia E (1/64 = (1/2)⁶), calcolando la probabilità a priori di sei figlie femmine (o intendendo «altri sei figli»).",
        "errata_note": "Nota di probabilità: se «sei figli» indica il totale della famiglia (avendo già 2 figlie), la risposta matematicamente corretta per la probabilità condizionata è D (1/16 = (1/2)⁴); la chiave ufficiale EdiSES riporta E (1/64 = (1/2)⁶).",
    },
    "BIO-C04-NCOM-121": {
        "question": "Il sesso dell'uomo è determinato:",
        "explanation": "Nella specie umana la femmina è omogametica (XX, produce solo ovociti X) mentre il maschio è eterogametico (XY, produce 50% spermatozoi X e 50% spermatozoi Y): al momento della fecondazione il sesso cromosomico dello zigote dipende quindi dal cromosoma sessuale portato dallo spermatozoo fecondante.",
        "errata_note": "Nota: in generale la determinazione genetica del sesso nell'uomo è cromosomica (sistema XX/XY, opzione D), ma a livello gametica dipende specificamente dallo spermatozoo (opzione A, chiave ufficiale EdiSES).",
    },
    "BIO-C04-NCOM-130": {
        "crop_figure": True,
        "explanation": "Nell'albero genealogico per un carattere X-linked recessivo (daltonismo), la donna sana F₁-₃ genera figli maschi affetti (XᵃY) nella generazione F₂: poiché i figli maschi ereditano l'unico cromosoma X dalla madre (e il cromosoma Y dal padre F₁-₄), la donna F₁-₃ è sicuramente portatrice eterozigote (XᴬXᵃ).",
    },
    "BIO-C04-NCOM-132": {
        "crop_figure": True,
        "explanation": "Nel pedigree X-linked recessivo il padre della femmina di F₃ è un maschio malato (XᵃY, quadrato nero in F₂) mentre la femmina di F₃ è fenotipicamente sana (cerchio bianco): avendo necessariamente ereditato il cromosoma Xᵃ paterno ed essendo sana (possiede quindi anche un allele Xᴬ materno), il suo genotipo è sicuramente eterozigote (XᴬXᵃ).",
    },
    "BIO-C04-NCOM-135": {
        "explanation": "Una cellula uovo a «corredo cromosomico ignoto» può essere euploide normale (23,X → zigote 46,XX femmina) oppure aneuploide per non-disgiunzione materna (es. nullisomica 22,0 → zigote 45,X sindrome di Turner, fenotipicamente femmina; disomica 24,XX → 47,XXX metafemmina): in assenza del cromosoma Y (gene SRY), la fecondazione con uno spermatozoo X dà in ogni caso un individuo di sesso femminile.",
    },
    "BIO-C04-NCOM-150": {
        "question": "I difetti di rifrazione della vista, il diabete, il labbro leporino, la spina bifida, il glaucoma e lo strabismo tendono a ricorrere all'interno di un gruppo familiare, ma non è stato possibile ricondurli alla mutazione di un singolo gene. Per questo motivo, disturbi o malattie similari vengono definite:",
        "explanation": "Le patologie a familiarità complessa che non seguono rapporti mendeliani monogenici dipendono dal contributo additivo di varianti in più loci genici distinti (spesso modulati da fattori ambientali) e vengono perciò definite malattie poligeniche (o multifattoriali).",
    },
    "BIO-C04-NCOM-152": {
        "crop_figure": True,
        "explanation": "Trattandosi di una malattia autosomica recessiva (aa), la femmina sana di F₂ (coniugata con il maschio sano esterno) ha un figlio affetto (aa) in F₃: entrambi i genitori della coppia di F₂ devono aver trasmesso un allele recessivo a e, poiché sono fenotipicamente sani, la femmina sana di F₂ è con certezza eterozigote (Aa).",
    },
    "BIO-C04-NCOM-156": {
        "crop_figure": True,
        "explanation": "Per un carattere autosomico dominante (A_), tutti gli individui sani hanno genotipo certo omozigote recessivo (aa). La femmina malata di F₃ nasce da un padre malato (in F₂) e da una madre fenotipicamente sana (aa): avendo ricevuto obbligatoriamente un allele recessivo a dalla madre sana ed essendo affetta, è con certezza eterozigote (Aa).",
    },
    "BIO-C04-NCOM-162": {
        "crop_figure": True,
        "explanation": "Nell'albero genealogico due genitori sani in F₁ (1 e 2) generano una figlia affetta in F₂ (individuo 4, cerchio nero): un carattere assente in entrambi i genitori che compare nella prole è autosomico recessivo (aa), il che dimostra con certezza che entrambi gli individui sani della F₁ sono portatori eterozigoti (Aa).",
    },
    "BIO-C04-NCOM-173": {
        "question": "I gruppi sanguigni nel sistema AB0 sono determinati dalla presenza/assenza di antigeni di tipo A e B sulla membrana dei globuli rossi. Il gene responsabile della loro produzione presenta tre alleli, Iᴬ, Iᴮ (codominanti) e i (recessivo). Quale sarà il gruppo sanguigno di un individuo che non possiede antigeni A e B sulla membrana dei suoi globuli rossi?",
        "options": {"A": "A oppure B"},
        "explanation": "L'allele recessivo i codifica per una glicosiltransferasi non funzionale che non aggiunge né N-acetilgalattosamina (antigene A) né galattosio (antigene B) alla sostanza H: l'omozigote ii è privo di antigeni A e B sugli eritrociti ed è di gruppo sanguigno 0.",
    },
    "BIO-C04-NCOM-177": {
        "options": {
            "D": "il genotipo è I⁰I⁰",
            "E": "il genotipo è IᴬIᴬ",
        },
        "explanation": "Il testo stesso dichiara che entrambi i genitori sono «di gruppo sanguigno A», ossia hanno fenotipo A; poiché hanno avuto un figlio di gruppo 0 (genotipo ii), ciascun genitore ha trasmesso un allele i ed entrambi hanno genotipo eterozigote Iᴬi e fenotipo A.",
    },
    "BIO-C04-NCOM-183": {
        "explanation": "Secondo la legge di Landsteiner il plasma contiene le agglutinine dirette contro gli antigeni AB0 assenti sui propri eritrociti: gli anticorpi anti-A sono presenti sia negli individui di gruppo B (che hanno solo anti-A) sia in quelli di gruppo 0 (che hanno sia anti-A sia anti-B); poiché il referto menziona il riscontro dei soli anticorpi anti-A, la chiave EdiSES seleziona «probabilmente B».",
        "errata_note": "Nota immunoematologica: se il test ha ricercato esclusivamente gli anticorpi anti-A (senza testare gli anti-B), nella popolazione europea il gruppo 0 (~40%) è più frequente del gruppo B (~10%), rendendo difendibili B o A; la chiave EdiSES intende che dal referto completo sia emersa la sola presenza di anti-A (compatibile tipicamente col gruppo B).",
    },
    "BIO-C04-NCOM-202": {
        "explanation": "Una mutazione puntiforme missenso (di senso errato) trasforma un codone codificante in un codone diverso che specifica un altro amminoacido, determinando la sostituzione di un singolo residuo amminoacidico nella catena polipeptidica (mentre un codone di stop prematuro è una mutazione nonsenso).",
    },
    "BIO-C04-NCOM-204": {
        "options": {
            "E": "Un cambiamento di tutta la sequenza amminoacidica dopo l'inserimento dell'amminoacido Ile",
        },
        "answer": "C",
        "answer_text": "L'interruzione della catena amminoacidica",
        "explanation": "Suddividendo l'mRNA selvatico in codoni si ha CUG (Leu) – AUC (Ile) – GUA (Val) – AUG (Met) – CGC (Arg). La delezione del 7° nucleotide (la G di GUA) fa slittare la cornice di lettura producendo CUG (Leu) – AUC (Ile) – UAA – UGC – GC: il terzo codone diventa UAA, un codone di stop (ocra) che arresta immediatamente la traduzione subito dopo Ile causando l'interruzione prematura della catena amminoacidica.",
        "errata_note": "Errata corrige chiave EdiSES (tie-break risolto): la chiave stampata (p. 634) indicava meccanicamente E (regola generica delle delezioni frameshift), senza avvedersi che nella specifica sequenza data la rimozione di G₇ genera all'istante il codone di terminazione UAA (nessun amminoacido viene inserito dopo Ile; risposta esatta C).",
    },
    "BIO-C05-NCOM-030": {
        "crop_figure": True,
        "explanation": "Nella figura schematica la cellula vegetale 1 mostra il protoplasto contratto e staccato dalla parete cellulare rigida (plasmolisi), fenomeno che si verifica per perdita osmotica di acqua in soluzione ipertonica salina; la cellula 2 appare invece rigonfia e distesa contro la parete (turgore), condizione tipica dell'immersione in acqua distillata ipotonica.",
    },
    "BIO-C05-NCOM-077": {
        "question": "Un'immagine al microscopio elettronico mostra all'interno di una cellula del fegato umano decine di organelli di forma simile e di dimensioni comprese tra 0,25 µm e 0,75 µm. Questi organelli hanno una membrana singola e liscia. Quali tra gli organelli elencati di seguito potrebbero essere?",
        "explanation": "Tra le strutture elencate, nucleoli, centrioli e ribosomi sono privi di membrana e i mitocondri possiedono una doppia membrana (con creste interne); soltanto i lisosomi sono organelli vescicolari sferoidali di 0,2–0,8 µm delimitati da una singola membrana liscia (abbondanti negli epatociti insieme ai perossisomi).",
    },
    "BIO-C05-NCOM-136": {
        "explanation": "In condizioni di intenso sforzo muscolare con apporto di O₂ insufficiente alla fosforilazione ossidativa, le fibre muscolari scheletriche rigenerano rapidamente NAD⁺ per sostenere la glicolisi anaerobica riducendo il piruvato a lattato (fermentazione lattica, impropriamente indicata nel quesito EdiSES come «respirazione anaerobica»).",
        "errata_note": "Nota biochimica: rigorosamente il muscolo umano compie fermentazione lattica (e mobilizza glicogeno tramite glicogenolisi, opzione A), mentre la «respirazione anaerobica» in senso stretto è esclusiva di procarioti che usano accettori inorganici finali diversi da O₂ (es. NO₃⁻, SO₄²⁻); nei test EdiSES «respirazione anaerobica» è tuttavia usato come sinonimo colloquiale di metabolismo glicolitico anaerobico (chiave D).",
    },
    "BIO-C05-NCOM-189": {
        "options": {"C": "Importina α"},
        "answer_text": "Importina α",
        "explanation": "Nel trasporto nucleare canonico l'importina α agisce da subunità adattatrice: lega direttamente la sequenza di localizzazione nucleare (NLS, ricca di lisine e arginine) della proteina cargo e recluta l'importina β, che media l'attraversamento dei complessi del poro nucleare.",
    },
    "BIO-C05-NCOM-200": {
        "options": {"A": "α e β", "B": "F₀ e F₁", "C": "NADH e FADH₂"},
        "answer_text": "F₀ e F₁",
        "explanation": "Il complesso dell'ATP sintasi mitocondriale (Complesso V) è un motore rotazionale formato da due domini multiproteici principali: il canale protonico transmembrana F₀ (sensibile all'oligomicina) immerso nella membrana interna e la testa catalitica F₁ sporgente nella matrice che sintetizza ATP.",
    },
    "BIO-C05-NCOM-202": {
        "options": {"B": "Succinato deidrogenasi (Complesso II)", "E": "α-chetoglutarato deidrogenasi"},
        "answer_text": "Succinato deidrogenasi (Complesso II)",
        "explanation": "La succinato deidrogenasi è l'unico enzima del ciclo di Krebs integrato nella membrana mitocondriale interna (gli altri sono solubili nella matrice) e coincide strutturalmente con il Complesso II della catena di trasporto degli elettroni, ossidando il succinato a fumarato e trasferendo gli elettroni tramite FAD direttamente all'ubichinone (CoQ).",
    },
    "BIO-C05-NCOM-204": {
        "explanation": "La fusione dei mitocondri è mediata da GTPasi della famiglia della dinamina: le mitofusine Mfn1 e Mfn2 ancorate alla membrana mitocondriale esterna promuovono l'aggancio e la fusione delle membrane esterne (mentre DRP1 e Fis1 mediano la fissione mitocondriale).",
        "errata_note": "Nota: anche la GTPasi Opa1 (opzione E) partecipa al processo regolando specificamente la fusione della membrana mitocondriale interna e il rimodellamento delle creste; la chiave EdiSES seleziona B (Mitofusine Mfn1/Mfn2) come regolatori primari dell'evento di fusione tra due organelli.",
    },
    "BIO-C05-NCOM-215": {
        "explanation": "A differenza di mitocondri e cloroplasti (organelli semiautonomi di origine endosimbiontica provvisti di genoma proprio e mitoribosomi/plastoribosomi), il perossisoma è delimitato da singola membrana ed è completamente privo di DNA e ribosomi, importando tutte le sue proteine dal citosol.",
        "errata_note": "Nota: anche il lisosoma (opzione E) è privo di DNA e ribosomi propri; nel contesto della biogenesi degli organelli metabolici (spesso confrontati con mitocondri e cloroplasti) la chiave EdiSES indica D (Perossisoma).",
    },
    "BIO-C05-NCOM-217": {
        "options": {"B": "Importina α", "C": "Pex5"},
        "answer_text": "Pex5",
        "explanation": "La maggioranza delle proteine della matrice perossisomiale possiede al C-terminale il tripeptide segnale PTS1 (Ser-Lys-Leu, SKL), riconosciuto nel citosol dal recettore solubile Pex5 (mentre il più raro segnale N-terminale PTS2 è riconosciuto da Pex7).",
    },
    "BIO-C05-NCOM-234": {
        "question": "Quale difetto caratterizza la mutazione ΔF508 nella fibrosi cistica?",
        "explanation": "La mutazione più frequente nella fibrosi cistica (ΔF508, delezione della fenilalanina in posizione 508 nel canale del cloro CFTR) impedisce il corretto ripiegamento (folding) della proteina nel reticolo endoplasmatico, causandone la ritenzione da parte del controllo qualità (ERAD) e la degradazione proteasomica prima di raggiungere la membrana apicale.",
    },
    "BIO-C05-NCOM-253": {
        "question": "Quale complesso contribuisce a selezionare le proteine da includere in una vescicola COPII?",
        "explanation": "Nel rivestimento delle vescicole COPII che gemmano dal reticolo endoplasmatico verso il Golgi, il dimero interno Sec23/Sec24 viene reclutato da Sar1-GTP e la subunità Sec24 lega direttamente i segnali citosolici di esportazione delle proteine cargo transmembrana e dei recettori cargo.",
    },
    "BIO-C05-NCOM-270": {
        "explanation": "Nella fosforilazione ossidativa mitocondriale l'accettore finale ad alta affinità degli elettroni è l'ossigeno molecolare O₂, che a livello della citocromo c ossidasi (Complesso IV) riceve 4 elettroni e 4 protoni riducendosi a due molecole di H₂O.",
    },
    "BIO-C05-NCOM-273": {
        "options": {
            "A": "Complesso I (NADH deidrogenasi)",
            "B": "Complesso III (citocromo bc₁)",
            "C": "Complesso II (succinato deidrogenasi)",
        },
        "answer_text": "Complesso II (succinato deidrogenasi)",
        "explanation": "La variazione di energia libera nel trasferimento di elettroni dal FADH₂ del Complesso II al coenzima Q è troppo esigua per traslocare protoni attraverso la membrana interna: pertanto il Complesso II non è una pompa protonica, a differenza dei Complessi I, III e IV.",
    },
    "BIO-C05-NCOM-297": {
        "question": "Quale proteina nuclea i microtubuli nel centrosoma?",
        "options": {"A": "α-tubulina", "B": "β-tubulina", "D": "γ-tubulina"},
        "answer_text": "γ-tubulina",
        "explanation": "Nel materiale pericentriolare del centrosoma (MTOC) i complessi ad anello di γ-tubulina (γ-TuRC) fungono da stampo per la nucleazione dei nuovi microtubuli ancorandone l'estremità meno (−), mentre i dimeri di α- e β-tubulina si aggiungono all'estremità più (+).",
    },
    "BIO-C05-COMP-048": {
        "cloze_stem": "Le {{c1::importine}} riconoscono i segnali NLS e trasportano le proteine nel nucleo (rilasciandole per legame con Ran-GTP).",
        "accepted_synonyms": ["importine"],
        "explanation": "Le importine legano nel citosol le proteine provviste di segnale di localizzazione nucleare (NLS) e le trasportano attraverso i pori nucleari; una volta nel nucleoplasma, il legame di Ran-GTP all'importina induce il rilascio del carico proteico.",
    },
    "BIO-C05-COMP-088": {
        "cloze_stem": "I {{c1::perossisomi}} sono organuli delimitati da una singola membrana, con diametro medio di 0,5 µm e contenenti oltre 50 enzimi.",
        "accepted_synonyms": ["perossisomi"],
        "explanation": "I perossisomi sono organelli metabolici sferici (~0,5 µm) circondati da una singola membrana lipidica, ricchi di enzimi ossidativi (ossidasi flaviniche e catalasi) coinvolti nella β-ossidazione degli acidi grassi a catena molto lunga e nella detossificazione del perossido di idrogeno.",
    },
    "BIO-C05-COMP-091": {
        "cloze_stem": "Nei perossisomi avviene la {{c1::β-ossidazione}} degli acidi grassi a lunga catena (>20 atomi di carbonio), più rapida rispetto ai mitocondri.",
        "answer": "β-ossidazione",
        "answer_text": "β-ossidazione",
        "accepted_synonyms": ["β-ossidazione", "beta-ossidazione"],
        "explanation": "Gli acidi grassi a catena molto lunga (VLCFA, >20–22 C) non possono entrare direttamente nei mitocondri e vengono accorciati nei perossisomi mediante cicli di β-ossidazione fino a catene medie (ottanoil-CoA), poi trasferite ai mitocondri.",
    },
    "BIO-C05-COMP-102": {
        "cloze_stem": "L'enzima {{c1::catalasi}}, che costituisce circa il 15% delle proteine perossisomiali, converte l'H₂O₂ in acqua e ossigeno.",
        "accepted_synonyms": ["catalasi"],
        "explanation": "La catalasi è l'enzima marcatore emoproteico dei perossisomi e detossifica rapidamente il perossido di idrogeno generato dalle ossidasi perossisomiali secondo la dismutazione 2 H₂O₂ → 2 H₂O + O₂.",
    },
    "BIO-C05-COMP-123": {
        "cloze_stem": "Le COP{{c1::II}} formano vescicole dal reticolo endoplasmatico al Golgi.",
        "answer": "II",
        "answer_text": "II",
        "accepted_synonyms": ["II", "2", "COPII"],
        "explanation": "Il traffico vescicolare anterogrado in uscita dai siti di uscita del reticolo endoplasmatico (ERES) verso il cis-Golgi è mediato da vescicole rivestite da COPII, mentre le vescicole COPI mediano il recupero retrogrado dal Golgi al RE e tra cisterne del Golgi.",
    },
    "BIO-C06-NCOM-051": {
        "explanation": "Le giunzioni occludenti (tight junctions, formate da claudine e occludine) sigillano lo spazio intercellulare apicale tra cellule epiteliali adiacenti bloccando la diffusione paracellulare incontrollata e costringendo i soluti ad attraversare l'epitelio per via transcellulare tramite specifiche proteine di trasporto di membrana.",
        "errata_note": "Nota fisiologica: più precisamente sono le giunzioni strette a imporre il trasporto transcellulare mediato da trasportatori apicali/basolaterali (mentre alcune claudine formano anche pori paracellulari selettivi per specifici ioni).",
    },
    "BIO-C06-NCOM-067": {
        "options": {"A": "10 nm", "E": "1,5 nm"},
        "answer_text": "1,5 nm",
        "explanation": "I connessoni delle giunzioni comunicanti (gap junctions, ciascuno formato da 6 subunità di connessina) delimitano un poro acquoso idrofilo del diametro interno di circa 1,5 nm, permeabile a ioni inorganici e piccoli metaboliti/secondi messaggeri (< 1 kDa) ma non a proteine o acidi nucleici.",
    },
    "BIO-C06-NCOM-124": {
        "explanation": "Le proteine G eterotrimeriche accoppiate ai recettori a sette eliche transmembrana (GPCR) sono costituite da tre subunità distinte denominate α (che lega i nucleotidi guanilici), β e γ (che formano il dimero stabile Gβγ).",
    },
    "BIO-C06-NCOM-125": {
        "options": {
            "A": "Subunità β",
            "B": "Subunità α",
            "C": "Subunità γ",
            "E": "Il dimero βγ",
        },
        "answer_text": "Subunità α",
        "explanation": "Nelle proteine G eterotrimeriche il sito di legame per GDP/GTP e l'attività GTPasica intrinseca risiedono esclusivamente nella subunità Gα.",
    },
    "BIO-C06-NCOM-126": {
        "options": {
            "A": "Quando la subunità α lega GDP",
            "B": "Quando la subunità α lega ATP",
            "C": "Quando la subunità α lega AMP",
            "D": "Quando la subunità α lega GTP",
            "E": "Quando la subunità α lega NADH",
        },
        "answer_text": "Quando la subunità α lega GTP",
        "explanation": "L'attivazione del GPCR da parte del ligando agisce da GEF promuovendo il rilascio del GDP e il legame del GTP sulla subunità Gα: nello stato legato a GTP la proteina G è attiva e dissocia Gα-GTP dal complesso Gβγ.",
    },
    "BIO-C06-NCOM-127": {
        "question": "Le subunità βγ:",
        "explanation": "Una volta dissociatosi da Gα-GTP, anche il complesso eterodimerico Gβγ ancorato alla membrana agisce da molecola segnale attiva, potendo aprire direttamente canali ionici (es. canali al K⁺ GIRK cardiaci) e regolare enzimi effettori come specifiche isoforme di PLCβ, adenilato ciclasi e PI3Kγ.",
    },
    "BIO-C06-NCOM-133": {
        "options": {"B": "NF-κB"},
        "explanation": "La piccola proteina G monomerica Ras, attivata a valle dei recettori tirosin-chinasici (RTK) tramite il complesso Grb2-SOS, innesca canonicamente la cascata mitogena delle MAP chinasi: Ras-GTP → Raf (MAPKKK) → MEK (MAPKK) → ERK (MAPK).",
        "errata_note": "Nota: Ras-GTP può anche legare e contribuire ad attivare la subunità catalitica p110 della PI3K (opzione A); tuttavia la via canonica per eccellenza associata a Ras nella didattica della trasduzione del segnale è la cascata delle MAP chinasi (C).",
    },
    "BIO-C06-NCOM-146": {
        "explanation": "Mantenuto a riposo a concentrazioni citosoliche bassissime (~10⁻⁷ M) rispetto all'ambiente extracellulare e al lume del RE (~10⁻³ M), un rapido ingresso di ioni Ca²⁺ (tramite canali attivati da IP₃ o voltaggio-dipendenti) agisce come universale secondo messaggero intracellulare (attivando calmodulina, PKC, troponina C).",
    },
    "BIO-C06-NCOM-148": {
        "options": {"C": "IP₃"},
        "explanation": "La proteina chinasi A (PKA, chinasi cAMP-dipendente) è un tetramero inattivo R₂C₂: il legame cooperativo di quattro molecole di AMP ciclico (cAMP) alle due subunità regolatrici R rilascia le due subunità catalitiche C attive.",
    },
    "BIO-C06-NCOM-185": {
        "question": "La fosfatidilinositolo-3-chinasi (PI3K) fosforila:",
        "options": {"A": "DAG a IP₃", "D": "PIP₂ a PIP₃"},
        "answer_text": "PIP₂ a PIP₃",
        "explanation": "L'enzima lipidico PI3K fosforila in posizione 3 dell'anello inositolico il fosfatidilinositolo-4,5-bisfosfato (PIP₂) di membrana convertendolo in fosfatidilinositolo-3,4,5-trisfosfato (PIP₃), sito di ancoraggio per chinasi con dominio PH come AKT/PKB.",
    },
    "BIO-C06-NCOM-189": {
        "question": "PTEN è una fosfatasi che converte:",
        "options": {"C": "PIP₃ in PIP₂"},
        "answer_text": "PIP₃ in PIP₂",
        "explanation": "L'oncosoppressore PTEN è una fosfatasi lipidica specifica che rimuove il gruppo fosfato in posizione 3 dal PIP₃ rigenerando PIP₂, spegnendo così la via di sopravvivenza e proliferazione PI3K-AKT-mTOR.",
    },
    "BIO-C06-COMP-005": {
        "cloze_stem": "I {{c1::proteoglicani}}, ricchi in GAG, idratano la matrice e ne regolano la compressibilità.",
        "accepted_synonyms": ["proteoglicani"],
        "explanation": "I proteoglicani della matrice extracellulare sono formati da un core proteico a cui sono legate covalentemente numerose catene polisaccaridiche anioniche di glicosamminoglicani (GAG), che richiamano acqua formando un gel idratato resistente alla compressione.",
    },
    "BIO-C06-COMP-011": {
        "cloze_stem": "Negli {{c1::emidesmosomi}} l'integrina α₆β₄ collega la MEC alle citocheratine.",
        "accepted_synonyms": ["emidesmosomi"],
        "explanation": "Gli emidesmosomi ancorano il dominio basale delle cellule epiteliali alla lamina basale della matrice extracellulare (laminina) mediante l'integrina α₆β₄ connessa sul versante citoplasmatico (tramite plectina) ai filamenti intermedi di cheratina.",
    },
    "BIO-C06-COMP-054": {
        "cloze_stem": "Gli ormoni {{c1::steroidei}}, come testosterone ed estradiolo, derivano da modificazioni del colesterolo e agiscono tramite recettori intracellulari.",
        "accepted_synonyms": ["steroidei"],
        "explanation": "Tutti gli ormoni steroidei (androgeni come il testosterone, estrogeni come l'estradiolo, progesterone, glucocorticoidi e mineralcorticoidi) sono molecole lipofile sintetizzate a partire dal colesterolo (tramite il pregnenolone) e attraversano la membrana plasmatica legandosi a recettori nucleari/intracellulari.",
    },
    "BIO-C06-COMP-060": {
        "cloze_stem": "L'integrazione tra recettori {{c1::di superficie}} e recettori intracellulari consente alla cellula di rispondere sia a segnali rapidi che a segnali di lunga durata.",
        "accepted_synonyms": ["di superficie", "di membrana", "superficie"],
        "explanation": "I recettori di superficie (di membrana: canali ionotropi, GPCR, RTK) mediano risposte citoplasmatiche rapide a ligandi idrofili, mentre i recettori intracellulari/nucleari modulano direttamente la trascrizione genica generando risposte più lente e durature.",
    },
    "BIO-C06-COMP-064": {
        "cloze_stem": "Le {{c1::proteine G}} trimeriche sono composte da tre subunità: α, β e γ.",
        "accepted_synonyms": ["proteine G", "G-proteine"],
        "explanation": "Le proteine G eterotrimeriche trasducono il segnale dai GPCR agli effettori di membrana e sono formate dalle tre subunità distinte Gα, Gβ e Gγ.",
    },
    "BIO-C06-COMP-065": {
        "cloze_stem": "La subunità {{c1::α}} della proteina G lega GDP nello stato inattivo e GTP nello stato attivo, regolando l'attivazione degli effettori.",
        "answer": "α",
        "answer_text": "α (alfa)",
        "accepted_synonyms": ["α", "alfa", "alpha", "Gα"],
        "explanation": "La subunità α della proteina G trimerica funziona da interruttore molecolare: nello stato basale lega GDP ed è associata a βγ, mentre lo scambio GDP→GTP indotto dal recettore attivo la porta nella conformazione attiva.",
    },
    "BIO-C06-COMP-066": {
        "cloze_stem": "Le subunità {{c1::βγ}} della proteina G rimangono ancorate alla membrana e possono anch'esse modulare enzimi o canali ionici.",
        "answer": "βγ",
        "answer_text": "βγ (beta-gamma)",
        "accepted_synonyms": ["βγ", "beta-gamma", "beta gamma", "By"],
        "explanation": "Il dimero obbligato Gβγ resta ancorato al foglietto citosolico della membrana plasmatica (grazie alla prenilazione di Gγ) e dopo la dissociazione da Gα-GTP regola direttamente canali ionici ed effettori enzimatici.",
    },
    "BIO-C06-COMP-067": {
        "cloze_stem": "La subunità α della proteina G possiede attività {{c1::GTPasica}}, che idrolizza GTP a GDP ritornando allo stato inattivo.",
        "accepted_synonyms": ["GTPasica", "GTPasi"],
        "explanation": "L'attività GTPasica intrinseca della subunità Gα (accelerata dalle proteine RGS/GAP) idrolizza il GTP legato a GDP + Pᵢ, facendo cessare il segnale e favorendo la riassociazione del trimero inattivo Gαβγ.",
    },
    "BIO-C06-COMP-073": {
        "cloze_stem": "I {{c1::secondi messaggeri}} (cAMP, DAG, IP₃, Ca²⁺) diffondono rapidamente nel citoplasma amplificando il segnale.",
        "accepted_synonyms": ["secondi messaggeri"],
        "explanation": "Piccole molecole non proteiche o ioni intracellulari come cAMP, cGMP, IP₃, diacilglicerolo (DAG) e Ca²⁺ fungono da secondi messaggeri, propagando e amplificando enormemente il segnale iniziato dal primo messaggero extracellulare.",
    },
    "BIO-C06-COMP-074": {
        "cloze_stem": "La {{c1::PKA}} è attivata da cAMP, mentre la PKC da DAG e Ca²⁺, generando fosforilazioni a cascata.",
        "accepted_synonyms": ["PKA", "proteina chinasi A"],
        "explanation": "La proteina chinasi A (PKA) è una serina/treonina chinasi attivata dal secondo messaggero cAMP (via Gs/adenilato ciclasi), mentre la proteina chinasi C (PKC) convenzionale è attivata da diacilglicerolo (DAG) e ioni Ca²⁺ (via Gq/fosfolipasi C).",
    },
    "BIO-C07-NCOM-009": {
        "question": "Il ciclo cellulare è comunemente diviso in 4 fasi. Le fasi G (G₁ e G₂) sono quelle durante le quali avviene la crescita cellulare, ossia il raddoppio di tutto il contenuto cellulare; nella fase S avviene la duplicazione del DNA; nella fase M avviene la divisione cellulare. La corretta successione delle fasi del ciclo cellulare è:",
        "explanation": "Una cellula appena nata dalla mitosi entra dapprima in G₁ (prima fase di crescita), poi replica il proprio genoma in fase S (sintesi), completa la preparazione alla divisione in G₂ e infine si divide in fase M: l'ordine ciclico è G₁ → S → G₂ → M.",
    },
    "BIO-C07-NCOM-014": {
        "crop_figure": True,
        "explanation": "Nel grafico quantità di DNA vs tempo la cellula parte da 2 unità arbitrarie (G₁, 0–6 h), raddoppia gradualmente il DNA fino a 4 unità tra 6 e 10–12 h (fase S) e dimezza bruscamente il contenuto a 2 unità attorno a 12 h (divisione mitotica in cellule somatiche cutanee).",
        "errata_note": "Errata corrige interpretativa: dal grafico a 6 ore la cellula somatica cutanea inizia in realtà la fase S di duplicazione del DNA (la mitosi vera e propria avviene dopo il plateau 4C, fra 10 e 12 ore); tra le sole alternative offerte dal quesito (meiosi e morte escluse perché la coltura è somatica e torna vitale a 2C), la chiave ufficiale EdiSES indica E («6 ore ha iniziato la mitosi», usando impropriamente «mitosi» per l'intero ingresso nel ciclo replicativo-divisivo).",
    },
    "BIO-C07-NCOM-022": {
        "options": {"D": "presenta l'anafase I e l'anafase II"},
        "answer_text": "presenta l'anafase I e l'anafase II",
        "explanation": "La meiosi comprende due divisioni nucleari consecutive (meiosi I riduzionale e meiosi II equazionale) precedute da un'unica fase S, presentando perciò due anafasi distinte: anafase I (separazione degli omologhi) e anafase II (separazione dei cromatidi fratelli).",
    },
    "BIO-C07-NCOM-024": {
        "options": {
            "B": "è l'insieme delle fasi G₁-S-G₂ del ciclo cellulare",
            "E": "comprende le fasi S-G₂-M del ciclo cellulare",
        },
        "answer_text": "è l'insieme delle fasi G₁-S-G₂ del ciclo cellulare",
        "explanation": "L'interfase costituisce il lungo periodo metabolicamente attivo compreso tra due divisioni cellulari successive e raggruppa in sequenza le tre fasi G₁, S e G₂ (escludendo la fase M).",
    },
    "BIO-C07-NCOM-035": {
        "explanation": "Nelle cellule animali la coppia di centrioli situata nel centrosoma organizza i poli del fuso mitotico da cui si irradiano le fibre microtubulari (motivo per cui la chiave EdiSES seleziona D).",
        "errata_note": "Nota citologica: in senso rigoroso i centrioli sono cilindri formati da 9 triplette di microtubuli (opzione E) situati nel centro organizzatore dei microtubuli (centrosoma/poli del fuso), mentre i «punti di attacco» dei microtubuli sui cromosomi sono i cinetocori/centromeri; la chiave EdiSES seleziona D intendendo i poli di ancoraggio del fuso.",
    },
    "BIO-C07-NCOM-040": {
        "crop_figure": True,
        "explanation": "Nella figura si osservano coppie di cromosomi omologhi dicromatidici (con segmenti ricombinati per pregresso crossing-over) che migrano interi verso i poli opposti senza scissione dei centromeri: si tratta dell'anafase della 1ª divisione meiotica (anafase I).",
    },
    "BIO-C07-NCOM-043": {
        "options": {
            "D": "La riduzione del numero dei cromosomi avviene durante la meiosi II",
            "E": "I cromosomi omologhi si separano durante l'anafase II",
        },
        "explanation": "Durante la metafase I della meiosi i cromosomi omologhi appaiati in bivalenti (tetradi di quattro cromatidi) si allineano sulla piastra equatoriale (mentre non c'è fase S tra meiosi I e II, gli omologhi si separano in anafase I riducendo il corredo in meiosi I e l'ovocita aploide ha un solo cromosoma X).",
    },
    "BIO-C07-NCOM-044": {
        "crop_figure": True,
        "explanation": "Nell'anafase I meiotica mostrata in figura migrano 2 cromosomi dicromatidici verso il polo sinistro e 2 verso il polo destro: nella cellula madre erano dunque presenti in totale 4 cromosomi (2 coppie di omologhi), ossia un corredo diploide iniziale 2n = 4.",
    },
    "BIO-C07-NCOM-055": {
        "crop_figure": True,
        "explanation": "Un singolo evento di crossing-over coinvolge soltanto due dei quattro cromatidi della tetrade (uno materno e uno paterno non fratelli): al termine della meiosi II delle 4 cellule aploidi ottenute, due ricevono i cromatidi parentali intatti (uno tutto scuro e uno tutto chiaro) e due ricevono i cromatidi ricombinati reciproci (Serie C).",
    },
    "BIO-C07-NCOM-064": {
        "explanation": "La mitosi è una divisione equazionale che conserva inalterato il grado di ploidia della cellula madre: negli organismi animali diploidi, da una cellula somatica diploide (2n) genera due cellule figlie geneticamente identiche ed entrambe diploidi (2n).",
        "errata_note": "Nota: nei funghi, nelle alghe e nei gametofiti vegetali anche cellule aploidi possono dividersi per mitosi generando due cellule aploidi (opzione C); riferendosi implicitamente agli eucarioti animali/umani, la chiave ufficiale EdiSES è E.",
    },
    "BIO-C07-NCOM-114": {
        "crop_figure": True,
        "explanation": "Nello schema del ciclo vitale umano il Processo A (Adulto → Gameti) è la meiosi/gametogenesi, mentre il Processo B (Gameti → Zigote) rappresenta la fecondazione, che nella specie umana avviene fisiologicamente nel terzo laterale (ampolla) della tuba uterina o ovidotto.",
    },
    "BIO-C07-NCOM-115": {
        "crop_figure": True,
        "explanation": "Nello schema riproduttivo il Processo A porta dagli individui adulti diploidi alla formazione dei gameti aploidi dimezzando il corredo cromosomico: rappresenta pertanto la meiosi (mentre il Processo B che unisce i gameti nello zigote è la fecondazione).",
    },
    "BIO-C07-NCOM-137": {
        "explanation": "Se il gamete aploide (n) contiene una quantità di DNA pari a C, una cellula somatica diploide (2n) in G₁ contiene 2C; dopo la replicazione del DNA in fase S, durante G₂, profase e metafase mitotica la cellula contiene il doppio di DNA, cioè 4C.",
    },
    "BIO-C07-NCOM-153": {
        "options": {"C": "Checkpoint metafase/anafase"},
        "answer_text": "Checkpoint metafase/anafase",
        "explanation": "Il checkpoint dell'assemblaggio del fuso (SAC, checkpoint della transizione metafase/anafase) controlla che tutti i cinetocori dei cromatidi fratelli siano correttamente attaccati in modo bipolare (anfitelico) ai microtubuli dei poli opposti prima di attivare la separasi.",
    },
    "BIO-C07-NCOM-156": {
        "options": {"C": "Wee1"},
        "explanation": "Finché anche un solo cinetocore non è attaccato al fuso, il complesso del checkpoint mitotico (MCC: Mad2, BubR1, Bub3) sequestra e blocca il coattivatore Cdc20, impedendo l'attivazione dell'ubiquitina-ligasi APC/C e quindi la degradazione di securina e ciclina B.",
        "errata_note": "Nota molecolare: più precisamente Cdc20 è il bersaglio/coattivatore di APC/C sequestrato da Mad2 e BubR1 nel complesso MCC (nessuna tra Mad2/BubR1 figura tra A–D, dove Cdk2, Aurora A, Wee1 e p21 regolano fasi diverse); per questo Cdc20 (E) è l'unica componente del modulo MCC–APC/C presente tra le opzioni.",
    },
    "BIO-C07-NCOM-164": {
        "explanation": "Al termine della mitosi (telofase) la defosforilazione delle lamine nucleari e delle proteine di membrana associata ai cromosomi decondensati guida la riorganizzazione dell'involucro nucleare attorno ai due nuovi nuclei figli.",
        "errata_note": "Nota: durante la telofase si riforma anche il nucleolo (opzione B) e si riassembla l'apparato di Golgi (opzione C); l'evento citologico cardine che definisce classicamente il completamento della telofase nucleare nei manuali EdiSES è la ricostituzione dell'involucro nucleare (E).",
    },
    "BIO-C07-NCOM-188": {
        "options": {"D": "Blimp1 e Prdm14"},
        "answer_text": "Blimp1 e Prdm14",
        "explanation": "La specificazione delle cellule germinali primordiali (PGC) nei mammiferi è guidata dai regolatori trascrizionali Blimp1 (Prdm1), Prdm14 e Tfap2c, che reprimono il programma mesodermico somatico, riattivano i geni di pluripotenza e avviano la riprogrammazione epigenetica.",
    },
    "BIO-C07-COMP-028": {
        "cloze_stem": "La chinesina-{{c1::14}} si muove verso l'estremità (−) dei microtubuli nel fuso mitotico.",
        "accepted_synonyms": ["14", "chinesina-14"],
        "explanation": "A differenza della maggior parte delle chinesine (dirette verso il polo +, come la chinesina-5/Eg5 che spinge i poli lontani), le chinesine C-terminali della famiglia chinesina-14 (es. HSET/Ncd) sono motori diretti verso l'estremità (−) che focalizzano i poli del fuso e bilanciano la tensione bipolare.",
        "errata_note": "Nota biofisica: è la chinesina-5 (+ diretta) a spingere i poli del fuso lontano l'uno dall'altro, mentre la chinesina-14 (− diretta) esercita una forza antagonista che avvicina/compatta i poli; la risposta attesa per il motore diretto all'estremità (−) è «14».",
    },
    "BIO-C07-COMP-094": {
        "cloze_stem": "I corpi apoptotici vengono rapidamente eliminati grazie all'esposizione di segnali «{{c1::eat me}}» (in inglese) sulla membrana plasmatica.",
        "answer": "eat me",
        "answer_text": "eat me",
        "accepted_synonyms": ["eat me", "eat-me", "eatme"],
        "explanation": "Durante l'apoptosi la traslocazione della fosfatidilserina dal foglietto interno a quello esterno della membrana plasmatica espone segnali fagocitici «eat me» riconosciuti dai macrofagi per l'efferocitosi senza infiammazione.",
    },
    "BIO-C07-COMP-101": {
        "cloze_stem": "La MOMP (permeabilizzazione della membrana mitocondriale esterna) è l'evento chiave della via {{c1::intrinseca}}.",
        "accepted_synonyms": ["intrinseca", "mitocondriale"],
        "explanation": "Nella via apoptotica intrinseca (mitocondriale), l'oligomerizzazione delle proteine pro-apoptotiche Bax e Bak induce la MOMP con rilascio nel citosol del citocromo c, che si lega ad Apaf-1 formando l'apoptosoma e attivando la caspasi-9.",
    },
}
