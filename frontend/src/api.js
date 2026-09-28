import { API_BASE_URL } from "./config.js";

async function request(path, { params, signal } = {}) {
  const query = new URLSearchParams();
  for (const [key, value] of Object.entries(params || {})) {
    if (value !== undefined && value !== null && value !== "") {
      query.set(key, value);
    }
  }
  const qs = query.toString();
  const url = `${API_BASE_URL}${path}${qs ? `?${qs}` : ""}`;

  let response;
  try {
    response = await fetch(url, { signal, headers: { Accept: "application/json" } });
  } catch (err) {
    if (err.name === "AbortError") throw err;
    throw new Error(`Impossibile contattare l'API (${API_BASE_URL}).`);
  }

  if (!response.ok) {
    let detail = "";
    try {
      const body = await response.json();
      detail = typeof body?.detail === "string" ? body.detail : "";
    } catch {
      // corpo non JSON: ignora
    }
    const unreachable = [502, 503, 504].includes(response.status);
    const error = new Error(
      detail ||
        (unreachable
          ? `L'API non e' raggiungibile (errore ${response.status}). Verifica che il backend sia avviato.`
          : `Errore ${response.status} dall'API.`)
    );
    error.status = response.status;
    throw error;
  }
  return response.json();
}

export function getRoles(options) {
  return request("/roles", options);
}

export function getPlayers({ position, search, limit, offset } = {}, options) {
  return request("/players", {
    ...options,
    params: { position, search, limit, offset },
  });
}

export function getPlayer(playerId, options) {
  return request(`/players/${encodeURIComponent(playerId)}`, options);
}
