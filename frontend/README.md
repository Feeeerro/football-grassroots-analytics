# ASI Scouting — Frontend

Interfaccia web (Vite + React) per consultare i punteggi ASI prodotti dal backend.

## Avvio

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
```

Il backend deve essere attivo su `http://localhost:8000`.

## Configurazione

La base URL dell'API sta in `src/config.js` e si puo' sovrascrivere con la
variabile `VITE_API_BASE_URL` (vedi `.env.example`).

Se il backend non abilita CORS per `http://localhost:5173`, imposta
`VITE_API_BASE_URL=/api`: il dev server di Vite inoltra `/api/*` a
`http://localhost:8000/*` (proxy in `vite.config.js`).

## Viste

- `/` — griglia dei giocatori con filtro per posizione e ricerca per nome
  (i filtri restano nell'URL); paginazione "Carica altri" da 50.
- `/players/:id` — anagrafica, punteggio ASI e tabella delle stagioni
  (clean sheet e gol subiti solo per i portieri).
