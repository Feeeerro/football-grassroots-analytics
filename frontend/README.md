# ASI Scouting — Frontend

Interfaccia web (Vite + React) per consultare i punteggi ASI. Legge i dati da
file JSON statici: non serve nessun server API.

## Dati

I file stanno in `public/data/` e si generano dalla root del progetto:

```bash
python export_static.py
```

| File | Contenuto | Quando viene caricato |
|---|---|---|
| `roles.json` | posizioni per il filtro | apertura della lista |
| `players.json` | tutti i giocatori, ordinati per punteggio | apertura della lista, una volta sola |
| `profiles.json` | tutti i profili, `{ "id": profilo }` | primo profilo aperto, poi dalla cache |

Filtro per posizione e ricerca per nome avvengono nel browser. Gli URL sono
costruiti con `import.meta.env.BASE_URL`, quindi l'app funziona anche sotto un
sotto-percorso (es. `npx vite build --base=/nome-repo/` per GitHub Pages).

Nota: `public/data/` e' esclusa da git dalla regola `data/` del `.gitignore`
della root, quindi i JSON vanno generati prima della build.

## Avvio

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
```

## Viste

- `/` — griglia dei giocatori con filtro per posizione e ricerca per nome
  (i filtri restano nell'URL); paginazione "Carica altri" da 50. Ogni card
  mostra il punteggio ASI e, piu' in piccolo, quello dell'ultima stagione
  valutata.
- `/players/:id` — anagrafica, punteggio ASI, ultima stagione valutata e
  tabella delle stagioni (clean sheet e gol subiti solo per i portieri).
