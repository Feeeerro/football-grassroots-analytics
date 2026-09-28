# Abstract

In un mondo sempre più permeato dai dati e dalle valutazioni quantitative, anche
l'ambiente calcistico ha negli ultimi anni aperto le porte alla tecnologia e
all'analisi dei dati: per migliorare le prestazioni degli atleti, per costruire le
rose in maniera più mirata e per preparare con maggiore scrupolo le tattiche di
gioco. La Serie D, quarto livello calcistico italiano, rappresenta il gradino più
alto del calcio dilettantistico nazionale e costituisce da anni, per molti, una
porta d'ingresso al professionismo — tanto per i giocatori quanto per gli addetti
ai lavori. Per il livello tecnico del campionato e per l'applicazione dei suoi
interpreti, essa è a tutti gli effetti considerata una categoria
"semi-professionistica".

Nonostante il prestigio della lega, tuttavia, la tecnologia vi trova ancora
scarso accesso, per carenza di competenze o, più spesso, di fondi da destinare a
tali strumenti. È proprio questa scarsità di risorse a far sì che il Direttore
Sportivo — responsabile della composizione della rosa — si trovi ad affrontare in
solitaria una molteplicità di compiti, privo di collaboratori o strumenti che ne
supportino l'operato.

Il presente progetto intende sostenere questa figura, fornendole uno strumento
capace di condurre ricerche più mirate e di far risparmiare tempo, da reimpiegare
in altri compiti altrettanto essenziali al conseguimento degli obiettivi imposti
dalla società. L'esperienza narrata in "Moneyball" ha dimostrato come il ricorso
ai dati possa rendere competitivi nello sport pur a fronte di risorse limitate,
offrendo a chi decide un punto di vista più ampio per il raggiungimento dei propri
obiettivi. Si è consapevoli che il calcio sia uno sport profondamente diverso dal
baseball — meno situazionale, più esposto a variabili non predittive, e come tale
refrattario a soluzioni definitive. Lo strumento proposto non ambisce pertanto a
sostituire l'occhio o l'intuizione del Direttore Sportivo, bensì a supportarne il
lavoro: a restringere il campo entro cui muoversi, favorendo decisioni più mirate,
un risparmio di tempo e di risorse e, non da ultimo, l'emersione di soluzioni
sottovalutate cui nessuno avrebbe pensato.

---

# 2. Introduzione

## 2.1 Contesto e motivazione

Il Direttore Sportivo ricopre un ruolo di grande responsabilità all'interno di una
società calcistica, avendo il compito di comporre la rosa in funzione degli
obiettivi fissati dalla dirigenza. In Serie D, tuttavia, si tratta quasi sempre di
una figura che opera in solitaria: i budget ridotti delle società non consentono
di affiancarle collaboratori all'interno della classe dirigente.

La medesima limitazione economica si riflette nella fase di costruzione della
squadra. La Serie D non dispone di un flusso di cassa tale da sostenere spese
ingenti sul mercato in entrata, e si affida prevalentemente agli sponsor e alle
risorse proprie di chi ne guida la società. Ne consegue la ricerca ricorrente di
profili giovani, oppure di elementi ad alto rendimento ma dal costo contenuto,
tali da rientrare nei parametri economici e da consentire il raggiungimento degli
obiettivi prefissati.

Tale ricerca non è però agevole. La categoria conta oltre 4000 tesserati, e
individuare il profilo adatto può risultare estremamente dispendioso, in termini
di tempo e di risorse, per una figura che opera da sola — a maggior ragione
considerando la concorrenza delle altre 162 società. Da qui l'esigenza di uno
strumento capace di raccogliere in un unico luogo l'insieme dei tesserati, con le
relative informazioni e con una valutazione del rendimento di ciascun giocatore,
così da far risparmiare tempo e da venire incontro ai limiti operativi entro cui il
Direttore Sportivo si trova a lavorare.

## 2.2 Definizione del problema

Esiste già un portale che raccoglie le informazioni di carriera dei singoli
giocatori, pur non essendo dedicato esclusivamente alla Serie D. Tale portale
presenta però i soli dati individuali, senza tenere conto del contesto di squadra
in cui i giocatori si sono trovati a operare. Esso non consente inoltre di
confrontare i giocatori tra loro, né di ricavare una valutazione oggettiva del
singolo interprete a partire dal suo rendimento stagione dopo stagione.

Il presente progetto interviene precisamente su questi limiti. Raccoglie i dati in
un unico luogo e, per ciascun giocatore, produce una valutazione oggettiva
fondata sui dati individuali, incrociati con i dati della squadra in cui il
giocatore ha militato in ciascuna stagione. Da tale incrocio elabora un punteggio
per ogni singola stagione, e li aggrega mediante una media ponderata in un
risultato unico. Il sistema è inoltre in grado di confrontare i giocatori tra loro,
consentendo di stabilire una graduatoria relativa all'interno di ciascun ruolo. A
partire da questa prima valutazione oggettiva, saranno poi la competenza e
l'esperienza del Direttore Sportivo a orientare l'attenzione verso un profilo
piuttosto che verso un suo pari.

## 2.3 Obiettivi del lavoro

L'obiettivo del lavoro è, in conclusione, chiaramente definito: fornire ai
Direttori Sportivi uno strumento semplice e intuitivo che ne supporti l'operato
nella fase di mercato e nella costruzione della rosa. Partendo da una valutazione
oggettiva, lo strumento mira a indirizzare l'attenzione verso un gruppo ristretto
di potenziali obiettivi, riducendo il tempo e le risorse necessarie a giungere a
questa fase — tanto estenuante quanto delicata. Il Direttore Sportivo potrà così
concentrare le proprie energie là dove il suo apporto è insostituibile: nella
selezione mirata, condotta sulla base dell'esperienza e della conoscenza del
settore.

Il presente lavoro non si propone dunque di automatizzare la decisione, bensì di
riorganizzare il processo che la precede: sostituire una ricognizione manuale,
onerosa e dispersiva, con un filtro sistematico che restituisca al decisore un
insieme di candidati già selezionati su base oggettiva, sul quale esercitare il
proprio giudizio.

## 2.4 Struttura del documento

Il presente documento è organizzato come segue.

Il **Capitolo 3** ripercorre lo stato dell'arte nella valutazione quantitativa dei
calciatori, esaminando i principali modelli impiegati nel calcio professionistico
e i motivi per cui essi risultano inapplicabili alle categorie dilettantistiche,
così da collocare il presente lavoro nello spazio da essi lasciato scoperto.

Il **Capitolo 4** descrive la raccolta e la struttura dei dati: la fonte impiegata,
gli insiemi di dati acquisiti e la loro organizzazione in una base dati
relazionale, con particolare attenzione al problema della corretta identificazione
delle squadre attraverso le stagioni.

Il **Capitolo 5** espone la metodologia del modello di valutazione: i principi
generali, la normalizzazione dei dati, il trattamento dei campioni statisticamente
esigui, l'integrazione del contesto di squadra, la logica specifica di ciascun
ruolo e l'aggregazione dei punteggi stagionali in una valutazione complessiva.

Il **Capitolo 6** tratta gli aspetti implementativi: l'architettura del sistema, le
scelte tecnologiche, l'acquisizione dei dati, la progettazione della base dati e
l'organizzazione del codice.

Il **Capitolo 7** presenta i risultati e la loro validazione, discutendo la
coerenza delle valutazioni prodotte e le tarature effettuate.

Il **Capitolo 8** espone i limiti del lavoro, mentre il **Capitolo 9** ne delinea i
possibili sviluppi futuri. Il **Capitolo 10**, infine, ne trae le conclusioni.

# 3. Stato dell'arte

## 3.1 I modelli di valutazione nel calcio professionistico

La valutazione quantitativa dei calciatori ha conosciuto negli ultimi anni un
progresso considerevole, trainato dalla crescente disponibilità di dati
dettagliati e dall'applicazione di tecniche di apprendimento automatico. I
modelli oggi più diffusi condividono un obiettivo comune — assegnare un valore
oggettivo al contributo di un giocatore — ma si distinguono per la granularità
del dato su cui operano e per la sofisticazione dell'apparato statistico
impiegato.

Il paradigma capostipite è quello degli **Expected Goals (xG)**, che stima la
probabilità che un tiro si trasformi in gol sulla base di fattori quali la
posizione e l'angolo di conclusione. Invece di limitarsi a conteggiare le reti,
il modello xG ne pesa la difficoltà, distinguendo un gol facile da uno di pregio.
Il suo limite intrinseco è tuttavia la focalizzazione sui soli tiri, che per la
maggior parte dei giocatori costituiscono una frazione minima delle azioni
complessive: i calciatori non deputati alla finalizzazione risultano di fatto
non valutabili con questa metrica.

Per superare tale limite sono stati sviluppati modelli che valutano ogni azione
di gioco, e non solo le conclusioni. Il framework **VAEP** (_Valuing Actions by
Estimating Probabilities_) assegna a ciascuna azione con la palla un valore pari
alla variazione che essa induce nella probabilità della squadra di segnare o di
subire gol nelle azioni immediatamente successive. In tal modo anche un passaggio
smarcante, un dribbling o un intervento difensivo ricevono una valutazione
proporzionata al loro reale contributo all'esito del gioco, e non soltanto il
tiro o l'assist. Modelli affini, quali l'_Expected Threat_ (xT) e l'_Expected
Possession Value_ (EPV), perseguono il medesimo scopo di attribuire valore alle
fasi di costruzione dell'azione, valutando quanto ciascun momento del possesso
accresca la probabilità di segnare.

Ciò che accomuna questi approcci è la loro dipendenza da **dati a livello di
evento** (_event data_) o addirittura da dati di tracciamento posizionale: la
registrazione puntuale di ogni singola azione di gioco — passaggi, tiri, dribbling,
contrasti — con le relative coordinate spaziali. È su questa materia prima,
raccolta manualmente o automaticamente per ogni partita, che tali modelli
costruiscono le proprie stime probabilistiche, tipicamente mediante algoritmi di
apprendimento automatico.

## 3.2 I limiti dei modelli esistenti nelle categorie dilettantistiche

La sofisticazione dei modelli descritti nella sezione precedente è resa possibile
esclusivamente dalla ricchezza dei dati su cui essi si fondano. Ed è precisamente
questa dipendenza a determinarne il principale limite di applicabilità: i dati a
livello di evento e di tracciamento sono disponibili, con continuità e
affidabilità, soltanto per i massimi livelli del calcio professionistico, dove la
raccolta è sostenuta da un considerevole investimento economico e infrastrutturale.

Man mano che si scende nella gerarchia dei campionati, la disponibilità di dati si
riduce drasticamente. Per le categorie dilettantistiche — e la Serie D, quarto
livello del calcio italiano, ne è un esempio emblematico — non esiste alcuna
raccolta sistematica di dati a livello di evento. Non sono disponibili né le
coordinate delle azioni, né il conteggio dei passaggi, dei contrasti o dei duelli,
né tantomeno dati di tracciamento. L'informazione statistica si riduce a poche
grandezze aggregate a livello di stagione: presenze, gol, assist, cartellini,
minuti giocati.

Ne consegue che l'intero apparato metodologico dei modelli professionistici
risulta, a questi livelli, semplicemente inapplicabile: mancando la materia prima,
non è possibile stimare le probabilità di segnare o subire su cui quei modelli si
fondano. Lo scouting nelle categorie dilettantistiche rimane pertanto un'attività
quasi esclusivamente manuale, affidata all'osservazione diretta, e priva di
strumenti quantitativi di supporto.

## 3.3 Posizionamento del presente lavoro

Il presente lavoro si colloca precisamente in questo spazio lasciato scoperto. Non
ambisce a competere con i modelli professionistici sul loro terreno — quello dei
dati granulari, che per definizione non sono disponibili nel contesto considerato
— bensì a costruire uno strumento di valutazione che operi _proprio là dove i dati
ricchi mancano_.

L'obiettivo non è replicare la finezza di VAEP o xG con dati che non esistono, ma
estrarre il massimo segnale possibile dalle sole grandezze aggregate disponibili,
rendendole significative attraverso la contestualizzazione. Se la singola
statistica individuale è, presa isolatamente, un indicatore grezzo, essa acquista
valore quando rapportata alla forza della squadra, al livello della competizione e
all'andamento nel tempo. È su questa intuizione — trasformare dati poveri in
valutazioni significative mediante il contesto — che si fonda il modello proposto.

Il contributo del presente lavoro è pertanto duplice. Sul piano dei dati, esso
costruisce da zero un dataset relazionale strutturato che, per la Serie D, non
esisteva in forma pubblica e interrogabile. Sul piano metodologico, esso propone
un modello di valutazione progettato specificamente attorno ai vincoli del dato
disponibile, che non aspira a sostituire il giudizio dell'osservatore, ma a
fornire un filtro capace di ridurre una popolazione di migliaia di giocatori a una
rosa ristretta di candidati meritevoli di attenzione.

---

# 4. Raccolta e struttura dei dati

## 4.1 Fonte dei dati

L'intero dataset è stato costruito a partire da Transfermarkt, portale che
raccoglie informazioni anagrafiche, statistiche e di rendimento relative al calcio
mondiale, ivi comprese le categorie dilettantistiche italiane. La scelta di tale
fonte è motivata dalla sua copertura della Serie D — raramente documentata altrove
in forma strutturata — e dalla presenza congiunta, sulle sue pagine, dei tre
insiemi di dati necessari al modello: le rose, le statistiche individuali dei
giocatori e le classifiche storiche.

I dati non sono resi disponibili dalla fonte in un formato direttamente
interrogabile, ma risiedono all'interno delle pagine web del portale. La loro
acquisizione ha pertanto richiesto un processo di _web scraping_, descritto nel
capitolo dedicato all'implementazione, volto a estrarre l'informazione dalle
pagine e a strutturarla in una forma idonea all'elaborazione.

La raccolta è stata circoscritta alle stagioni a partire dalla 2014/15. Tale
delimitazione risponde a un'esigenza di consistenza: è a partire da quella
stagione che i dati delle classifiche risultano completi e affidabili per tutti e
nove i gironi della Serie D. L'estensione a stagioni precedenti avrebbe introdotto
lacune e disomogeneità nel contesto di squadra, con conseguente indebolimento
della base su cui poggia l'intero modello valutativo.

## 4.2 Dati raccolti

Sono stati raccolti tre insiemi di dati distinti ma tra loro correlati.

**Rose e dati anagrafici dei giocatori.** Per ciascuna delle 162 squadre di Serie
D è stata acquisita la rosa, con i dati anagrafici di ogni giocatore: nome, ruolo,
data di nascita, altezza, piede preferito e scadenza del contratto. Tali
informazioni costituiscono l'anagrafica di base su cui si innestano le statistiche
di rendimento.

**Statistiche dei giocatori.** Per ogni giocatore è stato raccolto l'intero
storico statistico, articolato per stagione e per competizione: presenze, gol,
assist, cartellini gialli e rossi, minuti giocati, cui si aggiungono, per i
portieri, i clean sheet e i gol subiti. Ciascuna riga statistica registra inoltre
la squadra rappresentata dal giocatore in quella specifica stagione: si tratta di
un'informazione fondamentale, poiché è ciò che consente di collegare il rendimento
individuale al contesto della squadra, e senza la quale la contestualizzazione — su
cui l'intero modello si fonda — non sarebbe possibile.

**Classifiche storiche.** Per ciascun girone e per ciascuna stagione è stata
acquisita la classifica finale completa: posizione, partite disputate, punti, gol
fatti e subiti, ed esito di fine stagione (promozione, playoff, playout,
retrocessione). Le classifiche costituiscono la fonte del contesto di squadra su
cui il modello si appoggia: il rendimento di un giocatore acquista significato
soltanto una volta rapportato a quanto forte fosse effettivamente la squadra in cui
ha militato, e le classifiche forniscono la misura di tale forza.

## 4.3 Il problema della risoluzione delle entità

La correlazione fra le statistiche individuali e il contesto di squadra presuppone
la capacità di identificare univocamente ciascuna squadra attraverso le stagioni.
Tale requisito, apparentemente scontato, si scontra con una caratteristica
ricorrente del calcio dilettantistico italiano: le società mutano con frequenza la
propria denominazione, per cambi di ragione sociale, fusioni o rifondazioni. Una
medesima squadra può pertanto comparire, in stagioni diverse, sotto nomi
differenti.

Poiché le statistiche di un giocatore recano il nome della squadra così come esso
figurava nella stagione considerata, il semplice confronto per nome risulterebbe
inaffidabile: due nomi distinti potrebbero riferirsi alla stessa società, e il
collegamento al contesto di squadra fallirebbe o, peggio, produrrebbe
associazioni errate. La soluzione adottata, descritta in dettaglio nel capitolo
sull'implementazione, si fonda sull'impiego di un identificatore stabile, invariante
rispetto ai cambi di nome, al quale vengono ricondotte tutte le denominazioni
storiche di ciascuna società.

## 4.4 Struttura del dataset

I dati acquisiti, inizialmente conservati in forma di file semi-strutturati, sono
stati consolidati in un database relazionale, che ne costituisce la
rappresentazione definitiva e la base per ogni successiva elaborazione. La scelta
di una struttura relazionale, in luogo di una conservazione in file piatti,
risponde alla natura intrinsecamente relazionale del dato: giocatori, squadre,
statistiche e classifiche sono entità distinte legate da relazioni ben definite —
un giocatore appartiene a una squadra, una statistica si riferisce a un giocatore e
a una squadra in una stagione, una classifica descrive le squadre di un girone in
una stagione.

Lo schema, articolato in cinque tabelle, modella tali entità e le loro relazioni, e
prevede in particolare una tabella dedicata ai nomi storici delle squadre, funzionale
alla risoluzione delle entità di cui alla sezione precedente. I dettagli della
progettazione dello schema, della migrazione dei dati e delle conversioni di tipo
operate in tale fase sono esposti nel capitolo dedicato all'implementazione.

# 5. Metodologia del modello

## 5.1 Principi generali

La valutazione prodotta dal modello si fonda su una discriminante fondamentale:
il ruolo. Ogni giocatore viene valutato e confrontato esclusivamente con gli
altri giocatori del proprio stesso ruolo, poiché ciascun ruolo presenta
caratteristiche e richieste diverse dagli altri, che rendono improprio un
confronto diretto. I ruoli sono a loro volta raggruppati in tre macro-reparti —
difensivo, centrocampo e offensivo — che ne definiscono l'impianto valutativo di
fondo.

La valutazione è generata sulla base di parametri sia individuali sia di
contesto squadra, ed è espressa mediante un punteggio compreso tra 0 e 100. Il
processo si articola in due fasi. La prima consiste in un calcolo fondato sui
parametri individuali, ciascuno dei quali incide sul punteggio finale con un
peso specifico che varia in funzione del ruolo. La seconda fase introduce un
aggiustamento basato sul contesto squadra, che opera in modo differente a
seconda che si tratti di un ruolo offensivo o difensivo. Il reparto di
centrocampo costituisce l'unico caso in cui entrambe le forme di contesto
coesistono, trattandosi di ruoli che ricoprono simultaneamente la fase offensiva
e quella difensiva.

Il punteggio di ciascun giocatore viene inoltre costruito su due livelli
temporali: dapprima si calcola un punteggio per ogni singola stagione disputata,
successivamente tali punteggi vengono aggregati in un unico valore complessivo
attraverso una media pesata, descritta nella sezione 5.6.

## 5.2 Normalizzazione a percentile

Le statistiche relative ai giocatori presentano scale tra loro incompatibili e
non direttamente confrontabili. I minuti totali si collocano nell'ordine delle
migliaia, i gol nell'ordine delle decine, i cartellini nell'ordine delle unità.
Sommare o confrontare grandezze di ordini così diversi produrrebbe un punteggio
dominato dai parametri con i valori numericamente più grandi,
indipendentemente dalla loro reale importanza. Per rendere i valori comparabili
è pertanto necessaria una normalizzazione, per la quale si è adottato il metodo
del percentile.

Il metodo consiste nel raccogliere, per ciascun parametro e per ciascun ruolo,
l'insieme di tutti i valori storici osservati, e nel collocare un dato valore
rispetto a tale distribuzione, esprimendone la posizione relativa come un numero
compreso tra 0 e 1. Il percentile risponde dunque alla domanda: "rispetto a
tutti i valori mai registrati dai giocatori di questo ruolo, quanti sono
inferiori o uguali a quello osservato?".

Questo metodo è stato preferito ad alternative quali il min-max scaling per la
sua robustezza rispetto ai valori anomali (_outlier_). Nel min-max scaling un
singolo valore estremo, comprimendo tutti gli altri verso il basso della scala,
distorcerebbe l'intera normalizzazione; il percentile, fondandosi
esclusivamente sull'ordinamento relativo dei valori e non sulla loro magnitudine
assoluta, non risente di questo problema.

## 5.3 Gestione dei campioni ridotti: lo shrinkage

La normalizzazione a percentile descritta nella sezione precedente assume che
ogni valore osservato costituisca un'informazione affidabile sul rendimento di
un giocatore. Questa assunzione, tuttavia, non è sempre valida: alcune metriche
derivate risultano statisticamente instabili quando calcolate su un numero
esiguo di eventi. Il caso più rilevante nel presente modello è quello delle
metriche espresse come rapporto — in particolare la quota offensiva (il
contributo di un giocatore ai gol della propria squadra) e i gol subiti per
partita da un portiere.

Si consideri la quota offensiva. Un attaccante con 3 reti in una squadra che ne
ha segnate 4 presenta una quota dello 0,75; un attaccante con 18 reti in una
squadra che ne ha segnate 45 presenta una quota dello 0,40. Il primo valore, pur
numericamente superiore, poggia su un denominatore minimo, tale per cui la
variazione di una singola rete lo sposterebbe drasticamente. Il secondo,
calcolato su un denominatore ampio, è invece stabile. Il percentile applicato al
valore grezzo non distingue tra le due situazioni, introducendo nel modello un
segnale spurio ogniqualvolta un rapporto elevato derivi da un numero ridotto di
eventi.

### La correzione tramite shrinkage

Per attenuare questo effetto si adotta una tecnica di _shrinkage_, ovvero di
regressione verso la media. Il principio consiste nel "tirare" la stima
osservata verso un valore di riferimento — la media della metrica nel ruolo
considerato — con un'intensità inversamente proporzionale alla quantità di dati
su cui la stima è calcolata. Le stime fondate su molti eventi restano
sostanzialmente inalterate; quelle fondate su pochi eventi vengono avvicinate al
comportamento medio, in assenza di prove sufficienti a giustificarne lo
scostamento.

La quota offensiva corretta è definita come:

$$
q_{\text{shrink}} = \frac{g + C \cdot \bar{q}}{G + C}
$$

dove $g$ indica i gol del giocatore, $G$ i gol della squadra, $\bar{q}$ la quota
media del ruolo (il valore di ancoraggio) e $C$ una costante di smoothing. La
costante $C$ rappresenta il numero di gol di squadra al di sotto del quale la
stima è considerata poco affidabile: quando $G$ è piccolo rispetto a $C$, il
termine $C \cdot \bar{q}$ domina il numeratore e la quota tende alla media di
ruolo; quando $G$ è grande rispetto a $C$, il contributo di $C$ diviene
trascurabile e la quota corretta converge a quella grezza.

A titolo esemplificativo, assumendo $C = 10$ e $\bar{q} = 0{,}30$, la quota
fondata su pochi dati passa da 0,75 a circa 0,43, mentre quella fondata su molti
dati passa da 0,40 a circa 0,38: la correzione interviene in misura
proporzionata alla numerosità del campione, come desiderato.

### Applicazione ai portieri

La medesima tecnica è applicata alla valutazione dei portieri, per i quali la
metrica dei gol subiti per partita presenta un problema speculare: un portiere
impiegato in pochi incontri può presentare una media particolarmente favorevole
o sfavorevole per effetto del caso, non del proprio rendimento. La formula
assume la forma:

$$
\text{gspp}_{\text{shrink}} = \frac{c + C \cdot \overline{\text{gspp}}}{p + C}
$$

dove $c$ indica i gol subiti, $p$ le presenze e $\overline{\text{gspp}}$ la media
dei gol subiti per partita nel ruolo. Anche in questo caso, un portiere con poche
presenze vede la propria media ricondotta verso il comportamento medio del
ruolo, mentre un portiere con molte presenze conserva il proprio valore
effettivo.

## 5.4 Il contesto squadra

Prendere in esame i soli valori individuali di un giocatore risulterebbe
eccessivamente approssimativo ai fini di una valutazione. Il calcio è uno sport
di squadra e tra quelli a più elevato impatto di variabili esterne al singolo:
il rendimento individuale è profondamente condizionato dalla qualità dei
compagni, dal contesto tattico e dalla forza complessiva dell'organico.
L'inclusione del contesto squadra, combinato alle statistiche individuali, rende
pertanto la stima del punteggio significativamente più accurata.

### 5.4.1 Contesto offensivo

Il contesto offensivo nasce da un'osservazione tanto semplice quanto
fondamentale per comprendere l'impatto di un giocatore di caratteristiche
offensive. Si considerino due giocatori, entrambi autori di 20 reti in una
stagione: a un primo sguardo si sarebbe indotti a ritenere che abbiano avuto il
medesimo impatto. Tuttavia, se il primo milita in una squadra di alta classifica
— e si può dunque presumere circondato da compagni di valore elevato — e il
secondo in una squadra di bassa classifica, i due rendimenti devono essere
valutati diversamente. Il primo giocatore è stato verosimilmente agevolato dai
propri compagni nel raggiungimento di quel risultato; il secondo ha
presumibilmente incontrato maggiori difficoltà, avendo prodotto lo stesso bottino
in un contesto meno favorevole.

Per misurare l'impatto di un giocatore in rapporto alla propria squadra si
calcola quanto le sue reti abbiano inciso sul totale dei gol prodotti
dall'organico, ottenendo così una misura del suo peso offensivo. La quota così
definita — corretta con lo shrinkage descritto nella sezione 5.3 — viene
normalizzata rispetto alla distribuzione storica delle quote del ruolo, e da tale
valore si ricava un bonus. Il bonus è quindi applicato in forma moltiplicativa al
punteggio dei gol, incrementandolo in misura tanto maggiore quanto più elevato è
stato il peso offensivo del giocatore all'interno della propria squadra. Si tratta
di un raffinamento contenuto, volto a distinguere fra loro giocatori dal bottino
simile senza tuttavia sovvertire la gerarchia fondata sulla produzione assoluta.

$$
\text{bonus}_{\text{off}} = k \cdot \text{pct}(q_{\text{shrink}})
\qquad
\text{score}_{\text{gol}} = \min\big(1,\; \text{pct}(g) \cdot (1 + \text{bonus}_{\text{off}})\big)
$$

dove $\text{pct}(\cdot)$ denota la normalizzazione a percentile e $k$ l'intensità
massima del bonus.

### 5.4.2 Contesto difensivo

Il contesto difensivo opera secondo una logica differente rispetto a quello
offensivo. Per i difensori, infatti, i dati disponibili non comprendono parametri
individuali in grado di quantificare oggettivamente la bontà delle prestazioni
difensive: mancano informazioni quali contrasti, intercetti o duelli vinti. In
assenza di tali dati, e disponendo per i difensori dei soli parametri comuni a
ogni ruolo, si è resa necessaria un'assunzione di fondo: che un reparto
difensivo il cui rendimento stagionale sia stato positivo presupponga un
contributo altrettanto positivo da parte dei suoi singoli interpreti. Il contesto
difensivo si fonda pertanto sul concetto di _overperformance_ difensiva.

L'overperformance si costruisce a partire da una curva attesa dei gol subiti: per
ciascuna posizione di classifica si calcola, sull'intero dataset, la media dei
gol subiti dalle squadre giunte in quella posizione. Qualora una squadra abbia
subìto meno gol rispetto alla media attesa per la posizione effettivamente
raggiunta in una determinata stagione, si può affermare che il suo reparto
difensivo — e con esso i suoi interpreti — abbia reso al di sopra delle
aspettative. Lo scarto tra il valore atteso e quello effettivo costituisce la
misura dell'overperformance.

Tale scarto viene normalizzato a percentile rispetto alla distribuzione di tutti
gli scarti osservati nel dataset, e il bonus che ne deriva viene applicato ai
minuti totali disputati dal giocatore: quanto più elevato è il minutaggio, tanto
più il giocatore ha contribuito in modo diretto e continuativo al risultato
difensivo del reparto, e tanto più il contesto lo valorizza.

$$
\text{scarto} = \overline{\text{gc}}(\text{pos}) - \text{gc}_{\text{squadra}}
\qquad
\text{contesto}_{\text{dif}} = w_s \cdot \text{sol} + w_o \cdot \text{pct}(\text{scarto})
$$

dove $\overline{\text{gc}}(\text{pos})$ è la media dei gol subiti attesa per la
posizione finale della squadra, $\text{sol}$ la solidità difensiva assoluta
(complemento del percentile dei gol subiti dalla squadra) e $w_s, w_o$ i pesi
attribuiti rispettivamente alla solidità e all'overperformance.

## 5.5 Scoring specifico per ruolo

Sebbene l'impianto metodologico — normalizzazione, shrinkage, contesto squadra —
sia comune a tutti i ruoli, i parametri considerati e i pesi loro attribuiti
variano in funzione delle richieste specifiche di ciascun ruolo. Ciò che
distingue un ruolo dall'altro non è la logica di calcolo, bensì la
configurazione dei parametri che vi concorrono e la loro importanza relativa.

### 5.5.1 Ruoli offensivi

Per i ruoli offensivi il punteggio è dominato dalla produzione realizzativa. Il
parametro principale è costituito dai gol, ai quali si applica il bonus di
contesto offensivo descritto nella sezione 5.4.1; concorrono inoltre gli assist,
i minuti giocati e, con peso ridotto e segno negativo, i cartellini. La quota
offensiva è calcolata sui soli gol, e non sulla somma di gol e assist, al fine di
evitare che il contributo degli assist venga conteggiato due volte — una prima
volta come parametro autonomo e una seconda all'interno della quota.

### 5.5.2 Portieri

I portieri dispongono, a differenza degli altri ruoli difensivi, di parametri
difensivi individuali: i clean sheet e i gol subiti. Il punteggio si fonda
pertanto su tali parametri, con i gol subiti espressi in forma di media per
partita corretta con lo shrinkage, così che un portiere con poche presenze non
risulti artificiosamente favorito. A clean sheet e gol subiti si applica il bonus
di contesto difensivo, che valorizza le prestazioni del portiere in rapporto alla
solidità del reparto in cui ha operato.

### 5.5.3 Difensori

I difensori di movimento costituiscono il caso più delicato, non disponendo di
alcuna statistica difensiva individuale. Il loro punteggio si fonda pertanto sui
minuti giocati — raffinati dal bonus di contesto difensivo — quale indicatore
della loro presenza continuativa in un reparto di determinata solidità. A tale
componente si aggiungono gol e assist come elemento di appetibilità
supplementare, dal momento che un difensore in grado di contribuire alla fase
offensiva rappresenta una risorsa rara e pregiata, e i cartellini come
penalizzazione. Va riconosciuto che, per la natura dei dati disponibili, la
valutazione dei difensori misura la solidità del reparto di appartenenza più che
l'abilità difensiva del singolo: un limite discusso più estesamente nel capitolo
dedicato.

### 5.5.4 Centrocampisti

I centrocampisti ricoprono simultaneamente la fase offensiva e quella difensiva,
e la loro valutazione riflette questa duplice natura combinando due blocchi. Il
blocco offensivo raccoglie gol e assist, con il bonus di contesto offensivo; il
blocco difensivo raccoglie i minuti giocati con il bonus di contesto difensivo. I
due blocchi sono combinati in un'unica misura mediante una media pesata, il cui
coefficiente determina il bilanciamento fra le due fasi. Poiché ogni ruolo è
valutato esclusivamente rispetto ai propri pari ruolo, tale coefficiente è
mantenuto bilanciato: il punteggio premia così i centrocampisti capaci di
rendere efficacemente in entrambe le fasi, collocando in posizione intermedia
coloro che eccellono in una sola di esse e in coda coloro che non si distinguono
in nessuna. I cartellini intervengono, come per gli altri ruoli, quale
penalizzazione esterna ai due blocchi.

## 5.6 Aggregazione temporale e fattore volume

I punteggi calcolati per le singole stagioni devono essere ricondotti a un unico
valore rappresentativo dell'intera carriera del giocatore. Tale aggregazione è
realizzata mediante una media pesata governata da tre principi.

In primo luogo, alle stagioni migliori è attribuito un peso maggiore: ordinando
i punteggi stagionali in senso decrescente e applicando pesi progressivamente
minori, si valorizza il rendimento di picco del giocatore senza tuttavia
ignorare le stagioni meno brillanti, che concorrono comunque al risultato in
misura ridotta.

In secondo luogo, si applica un lieve decadimento temporale, in virtù del quale
le stagioni più recenti pesano marginalmente più di quelle remote. Il
decadimento è volutamente contenuto, poiché il modello mira a una valutazione
complessiva del giocatore e non del suo solo stato di forma recente.

In terzo luogo, il valore così ottenuto è scalato da un fattore volume, funzione
dei minuti complessivamente disputati in carriera. Tale fattore garantisce che un
giocatore reduce da una singola stagione eccellente non prevalga su chi abbia
sostenuto un rendimento analogo per un numero maggiore di stagioni: il punteggio
riflette così non solo la qualità del rendimento, ma anche la sua continuità e
affidabilità nel tempo. Il fattore cresce con i minuti disputati fino a una
soglia oltre la quale il giocatore è considerato pienamente valutabile.

## 5.7 Normalizzazione finale

I punteggi aggregati, prima di essere presentati sulla scala 0–100, sono
sottoposti a un controllo di scala. Poiché i moltiplicatori di categoria — che
valorizzano le stagioni disputate in campionati di livello superiore — possono
in linea teorica condurre a punteggi eccedenti il limite superiore della scala,
si applica una normalizzazione finale che interviene esclusivamente qualora il
punteggio massimo osservato superi 100. In tal caso l'intera distribuzione viene
riscalata proporzionalmente, così che il valore massimo coincida con 100 e tutti
gli altri vi si rapportino. In assenza di superamenti, i punteggi sono mantenuti
nel loro valore assoluto, preservando l'interpretabilità della scala e la
comparabilità fra esecuzioni successive del modello.

# 6. Implementazione

Il presente capitolo descrive la realizzazione concreta del sistema, dalle
scelte tecnologiche all'organizzazione del codice. Laddove il capitolo
precedente ha illustrato la logica del modello e le motivazioni che ne sono alla
base, questo si concentra sugli aspetti ingegneristici: come i dati vengono
acquisiti, strutturati e resi disponibili al motore di calcolo, e secondo quali
principi il codice è stato organizzato per risultare manutenibile ed estensibile.

## 6.1 Architettura del sistema

Il sistema è concepito come una pipeline lineare, articolata in stadi successivi
e indipendenti, ciascuno dei quali produce l'input dello stadio seguente:

```
Scraping  →  JSON grezzo  →  Migrazione  →  Database SQLite  →  Scoring  →  Valutazioni
```

Ogni stadio comunica con il successivo esclusivamente attraverso un confine ben
definito: gli scraper producono file JSON, il livello di migrazione li converte
in tabelle relazionali, e il motore di scoring interroga tali tabelle per
produrre le valutazioni. Questa separazione delle responsabilità costituisce una
scelta architetturale deliberata: ogni stadio può essere rieseguito, corretto o
sostituito senza intervenire sugli altri. La rigenerazione del dataset non impone
di modificare la logica di scoring, così come una revisione del modello non
richiede di ripetere l'acquisizione dei dati.

Tale disaccoppiamento offre inoltre un punto di innesto naturale per sviluppi
successivi. Una futura interfaccia grafica, in particolare, potrebbe collocarsi a
valle della pipeline e attingere direttamente alle valutazioni pre-calcolate,
senza necessità di rieseguire il modello a ogni interrogazione: i punteggi sono
infatti calcolati una sola volta in modalità batch e resi persistenti, non
ricalcolati dinamicamente.

## 6.2 Scelte tecnologiche

Le tecnologie adottate rispondono ciascuna a un vincolo specifico del problema,
piuttosto che a una preferenza generica.

**Playwright** è stato scelto quale strumento di automazione del browser in luogo
di semplici librerie di richieste HTTP. Le pagine della fonte dati costruiscono
gran parte del proprio contenuto — in particolare le tabelle statistiche —
mediante codice JavaScript eseguito lato client; una richiesta HTTP diretta
restituirebbe pertanto un documento privo dei dati di interesse. Playwright,
pilotando un browser reale, garantisce il completo rendering della pagina prima
dell'estrazione.

**BeautifulSoup** è impiegato per il parsing del codice HTML così ottenuto,
offrendo un'interfaccia agevole per la navigazione e l'estrazione selettiva degli
elementi.

**SQLite** è stato preferito a sistemi di gestione di basi di dati più
strutturati, quali PostgreSQL o MySQL. La scelta è motivata dalle caratteristiche
del dataset: un volume contenuto (nell'ordine delle decine di migliaia di
record), l'assenza di accessi concorrenti e la natura monoutente
dell'applicazione. SQLite, non richiedendo alcun processo server né
configurazione, e risiedendo in un unico file, si rivela adeguato allo scopo e
notevolmente più semplice da gestire. La separazione fra il livello di
persistenza e il resto del sistema fa sì che, qualora esigenze future imponessero
un database più robusto, la migrazione risulterebbe circoscritta e non
pregiudicherebbe la logica applicativa.

## 6.3 Acquisizione dei dati

L'acquisizione dei dati costituisce, sul piano implementativo, la componente più
articolata del sistema, dovendo far fronte tanto alla natura dinamica delle
pagine quanto alla necessità di operare in modo robusto su un volume elevato di
richieste.

**Gestione del contenuto dinamico.** Le tabelle statistiche non sono presenti nel
documento al momento del caricamento iniziale, bensì vengono generate dal codice
JavaScript soltanto quando l'elemento entra nell'area visibile della pagina
(_lazy loading_). Per innescarne il rendering si è reso necessario simulare uno
scorrimento programmatico della pagina, in assenza del quale la tabella non
verrebbe mai costruita e l'estrazione fallirebbe.

**Robustezza e ripresa.** Lo scraping di un dataset esteso è un processo di lunga
durata, esposto a interruzioni di varia natura — errori di rete, blocchi
temporanei del servizio, indisponibilità momentanee. Per non compromettere il
lavoro svolto in caso di interruzione, è stato implementato un meccanismo di
salvataggio incrementale: i progressi vengono resi persistenti dopo il
completamento di ciascuna unità, e uno stato di avanzamento consente, a un
successivo riavvio, di riprendere esattamente dal punto di interruzione senza né
perdere né riscaricare i dati già acquisiti.

**Mitigazione del blocco.** L'esecuzione di numerose richieste ravvicinate verso
il medesimo servizio espone al rischio di blocco dell'indirizzo di provenienza.
Per contenere tale rischio si sono adottati ritardi variabili fra le richieste,
volti a simulare un pattern di navigazione meno riconoscibile come automatico, e
si è disabilitato il caricamento delle risorse non necessarie all'estrazione —
immagini, fogli di stile, caratteri tipografici — riducendo così il peso di
ciascuna richiesta e il tempo complessivo di acquisizione.

## 6.4 Progettazione del database

Il dato acquisito, inizialmente conservato in forma di file JSON, viene
consolidato in un database relazionale mediante un apposito livello di
migrazione. Lo schema è organizzato in cinque tabelle, che modellano
rispettivamente i giocatori, le squadre, i nomi storici delle squadre, le
statistiche stagionali dei giocatori e le classifiche storiche.

La progettazione dello schema riflette alcune decisioni di modellazione degne di
nota. In primo luogo, i nomi storici delle squadre non sono conservati come lista
serializzata all'interno della tabella delle squadre, bensì normalizzati in una
tabella dedicata, in cui a ciascun nome corrisponde una riga collegata
all'identificatore stabile della società. Tale scelta, coerente con i principi
della progettazione relazionale, consente interrogazioni efficienti per nome —
funzionali alla risoluzione delle entità descritta nella sezione seguente — che
una rappresentazione serializzata renderebbe farraginose.

In secondo luogo, la migrazione si fa carico della conversione e della validazione
dei tipi. I valori numerici, memorizzati nella fonte come testo e talvolta
recanti segnaposto per i dati assenti, vengono convertiti in interi o resi nulli
ove mancanti; grandezze quali l'altezza, originariamente espresse in formato
testuale, vengono ricondotte a una rappresentazione numerica omogenea. Il
database risultante contiene pertanto dati tipizzati e coerenti, pronti per
l'interrogazione da parte del motore di scoring.

## 6.5 Il problema della risoluzione delle entità

Fra i problemi affrontati in fase di implementazione, la risoluzione delle entità
si è rivelato il più insidioso e, al contempo, il più significativo. Le società
calcistiche mutano con frequenza la propria denominazione nel corso degli anni —
per cambi di ragione sociale, fusioni o rifondazioni — con la conseguenza che una
medesima squadra compare, in stagioni diverse, sotto nomi differenti. Poiché le
statistiche di un giocatore recano il nome della squadra rappresentata in ciascuna
stagione, collegare tali statistiche al contesto di squadra corretto richiede di
riconoscere quando nomi distinti si riferiscano alla stessa entità.

La soluzione adottata si fonda sull'identificatore stabile assegnato dalla fonte a
ciascuna società, invariante rispetto ai cambi di denominazione. A partire dai
dati storici delle classifiche, si costruisce una struttura che associa a ogni
identificatore l'insieme di tutti i nomi sotto i quali la società è comparsa nel
tempo. Da tale struttura si deriva una mappatura inversa, dal nome
all'identificatore, che consente di ricondurre qualunque denominazione storica
alla società corrispondente. Le statistiche di un giocatore possono così essere
collegate in modo affidabile alla squadra corretta, e per suo tramite al relativo
contesto di rendimento, indipendentemente dal nome sotto il quale la squadra
figurava in quella stagione.

Il collegamento è circoscritto alle competizioni per le quali si dispone dei dati
di classifica; per le stagioni disputate in altre categorie, per le quali il
contesto di squadra non è ricostruibile, l'associazione non viene tentata e la
loro valutazione è affidata al solo moltiplicatore di categoria.

## 6.6 Organizzazione del codice

Il codice è organizzato secondo il principio della separazione per responsabilità,
in pacchetti distinti dedicati rispettivamente all'acquisizione dei dati, alla
persistenza e al calcolo dei punteggi. Tale organizzazione rispecchia la struttura
a pipeline dell'architettura e mantiene ciascuna componente indipendente e
sostituibile.

All'interno del modulo di scoring, la suddivisione del codice segue una
distinzione fondamentale: da un lato le funzioni condivise da tutti i ruoli — la
normalizzazione a percentile, la costruzione dei benchmark, l'aggregazione
temporale — dall'altro le funzioni specifiche di ciascuna famiglia di ruoli, che
ne implementano la particolare logica di punteggio. Questa distinzione evita la
duplicazione del codice comune e circoscrive le differenze fra i ruoli ai soli
punti in cui esse sono effettive.

Un accorgimento di progettazione merita particolare menzione. La funzione di
aggregazione, che combina i punteggi stagionali di un giocatore in un valore
complessivo, è comune a tutti i ruoli; tuttavia il calcolo del punteggio di
singola stagione differisce fra ruoli offensivi, difensivi e di centrocampo. Per
mantenere la funzione di aggregazione indipendente dalla specifica famiglia — ed
evitare che essa debba conoscere i dettagli di ciascun tipo di punteggio — si è
adottato il meccanismo delle _closure_: la funzione di calcolo del punteggio
stagionale viene "confezionata", assieme a tutti i parametri di riferimento che le
occorrono, in una funzione che accetta come unico argomento la stagione da
valutare. La funzione di aggregazione riceve quindi tale funzione già completa e
la invoca senza alcuna conoscenza della sua natura, risultando così pienamente
agnostica rispetto al ruolo. Questa scelta ha consentito di implementare il
punteggio difensivo e quello di centrocampo riutilizzando integralmente la logica
di aggregazione, senza alcuna modifica a quest'ultima e senza introdurre
dipendenze circolari fra i moduli.

I parametri di taratura del modello — le costanti dello shrinkage, l'intensità dei
bonus, i coefficienti di decadimento temporale, i pesi attribuiti a ciascun
parametro per ciascun ruolo — sono centralizzati in un unico file di
configurazione. La taratura del modello si traduce così nella modifica di un solo
file, anziché nell'intervento sparso su più moduli, e i valori adottati risultano
raccolti e documentati in un unico punto.

## 6.7 Riproducibilità

I dati generati dal sistema — i file JSON grezzi e il database — non sono inclusi
nel repository, in ragione della loro dimensione e, soprattutto, della loro
completa riproducibilità a partire dal codice. La ricostruzione dell'intero
dataset a partire da zero è ottenibile eseguendo in sequenza gli stadi della
pipeline: l'acquisizione dei dati, la loro pulizia e restrizione alle stagioni di
interesse, la migrazione nel database e infine il calcolo dei punteggi. Le
dipendenze del progetto sono dichiarate esplicitamente, così da consentire la
predisposizione dell'ambiente di esecuzione in modo deterministico. Questa
impostazione garantisce che il sistema sia integralmente ricostruibile da terzi,
requisito essenziale tanto per la verificabilità del lavoro quanto per la sua
eventuale prosecuzione.
