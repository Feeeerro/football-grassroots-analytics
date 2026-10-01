import { DATA_BASE_URL } from "./config.js";
import { lastScoredSeason } from "./format.js";

// Cache a livello modulo: ogni file viene scaricato una sola volta per sessione.
const cache = new Map();

function abortError() {
  return new DOMException("Richiesta annullata.", "AbortError");
}

async function fetchJSON(file) {
  let response;
  try {
    response = await fetch(`${DATA_BASE_URL}${file}`, {
      headers: { Accept: "application/json" },
    });
  } catch {
    throw new Error(`Impossibile caricare i dati (${file}).`);
  }
  if (!response.ok) {
    const error = new Error(`Dati non disponibili (${file}, errore ${response.status}).`);
    error.status = response.status;
    throw error;
  }
  try {
    return await response.json();
  } catch {
    throw new Error(`File dati non valido (${file}). Rigenera i dati con export_static.py.`);
  }
}

// Il download condiviso non riceve il signal del chiamante: se un componente
// si smonta, gli altri (e la cache) devono comunque ottenere i dati.
async function loadJSON(file, signal) {
  if (!cache.has(file)) {
    const promise = fetchJSON(file);
    cache.set(file, promise);
    promise.catch(() => cache.delete(file)); // permette il "Riprova"
  }
  const data = await cache.get(file);
  if (signal?.aborted) throw abortError();
  return data;
}

export async function getRoles({ signal } = {}) {
  const roles = await loadJSON("roles.json", signal);
  return Array.isArray(roles) ? roles : [];
}

// Filtro e ricerca lato client; players.json e' gia' ordinato per final_score desc.
export async function getPlayers({ position, search, limit, offset = 0 } = {}, { signal } = {}) {
  const all = await loadJSON("players.json", signal);
  const players = Array.isArray(all) ? all : [];
  const query = (search || "").trim().toLowerCase();

  const filtered = players.filter(
    (p) =>
      (!position || p.position === position) &&
      (!query || (p.name || "").toLowerCase().includes(query))
  );
  return limit === undefined ? filtered.slice(offset) : filtered.slice(offset, offset + limit);
}

// profiles.json e' caricato in modo lazy alla prima apertura di un profilo.
export async function getPlayer(playerId, { signal } = {}) {
  const profiles = await loadJSON("profiles.json", signal);
  const profile = profiles?.[String(playerId)];
  if (profile === undefined) {
    const error = new Error("Giocatore non trovato.");
    error.status = 404;
    throw error;
  }
  return profile;
}

let lastSeasonsCache = null;

// Ultima stagione valutata per ogni giocatore: Map(String(id) -> {season, score} | null).
// Usa i campi last_season/last_season_score di players.json quando l'export li
// contiene; con un export che non li scrive li ricava da profiles.json, con la
// stessa regola del profilo, cosi' card e profilo mostrano sempre lo stesso valore.
export async function getLastSeasons({ signal } = {}) {
  if (!lastSeasonsCache) {
    lastSeasonsCache = (async () => {
      const players = await loadJSON("players.json");
      const list = Array.isArray(players) ? players : [];
      if (list.length > 0 && "last_season_score" in list[0]) {
        return new Map(
          list.map((p) => [
            String(p.player_id),
            p.last_season_score == null
              ? null
              : { season: p.last_season, score: p.last_season_score },
          ])
        );
      }
      const profiles = await loadJSON("profiles.json");
      return new Map(
        Object.entries(profiles || {}).map(([id, profile]) => [id, lastScoredSeason(profile.seasons)])
      );
    })();
    lastSeasonsCache.catch(() => {
      lastSeasonsCache = null;
    });
  }
  const result = await lastSeasonsCache;
  if (signal?.aborted) throw abortError();
  return result;
}
