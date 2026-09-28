import { useCallback, useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import { getPlayers, getRoles } from "../api.js";
import { PAGE_SIZE } from "../config.js";
import PlayerCard from "../components/PlayerCard.jsx";
import { ErrorMessage, Loading } from "../components/Status.jsx";

const SEARCH_DEBOUNCE_MS = 300;

export default function PlayerList() {
  // I filtri vivono nell'URL, cosi' tornando dal profilo restano applicati.
  const [searchParams, setSearchParams] = useSearchParams();
  const position = searchParams.get("position") || "";
  const search = searchParams.get("search") || "";

  const [searchInput, setSearchInput] = useState(search);
  const [roles, setRoles] = useState([]);
  const [rolesError, setRolesError] = useState(null);

  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState(null);
  const [hasMore, setHasMore] = useState(false);
  const [reloadKey, setReloadKey] = useState(0);

  const updateParam = useCallback(
    (key, value) => {
      setSearchParams(
        (prev) => {
          const next = new URLSearchParams(prev);
          if (value) next.set(key, value);
          else next.delete(key);
          return next;
        },
        { replace: true }
      );
    },
    [setSearchParams]
  );

  // Ruoli per il menu a tendina.
  useEffect(() => {
    const controller = new AbortController();
    getRoles({ signal: controller.signal })
      .then((data) => setRoles(Array.isArray(data) ? data : []))
      .catch((err) => {
        if (err.name !== "AbortError") setRolesError(err);
      });
    return () => controller.abort();
  }, []);

  // Debounce della ricerca per nome.
  useEffect(() => {
    const trimmed = searchInput.trim();
    if (trimmed === search) return;
    const timer = setTimeout(() => updateParam("search", trimmed), SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [searchInput, search, updateParam]);

  // Prima pagina: si ricarica a ogni cambio di filtro.
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    getPlayers({ position, search, limit: PAGE_SIZE, offset: 0 }, { signal: controller.signal })
      .then((data) => {
        const list = Array.isArray(data) ? data : [];
        setPlayers(list);
        setHasMore(list.length === PAGE_SIZE);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === "AbortError") return;
        setError(err);
        setPlayers([]);
        setHasMore(false);
        setLoading(false);
      });
    return () => controller.abort();
  }, [position, search, reloadKey]);

  async function loadMore() {
    setLoadingMore(true);
    setError(null);
    try {
      const data = await getPlayers({
        position,
        search,
        limit: PAGE_SIZE,
        offset: players.length,
      });
      const list = Array.isArray(data) ? data : [];
      setPlayers((prev) => [...prev, ...list]);
      setHasMore(list.length === PAGE_SIZE);
    } catch (err) {
      setError(err);
    } finally {
      setLoadingMore(false);
    }
  }

  return (
    <section>
      <div className="page-head">
        <h1>Giocatori</h1>
        <p className="muted">Ordinati per punteggio ASI (0-100).</p>
      </div>

      <form className="filters" role="search" onSubmit={(e) => e.preventDefault()}>
        <label className="field">
          <span>Posizione</span>
          <select
            value={position}
            onChange={(e) => updateParam("position", e.target.value)}
            disabled={!roles.length && !rolesError}
          >
            <option value="">Tutte le posizioni</option>
            {roles.map((role) => (
              <option key={role} value={role}>
                {role}
              </option>
            ))}
          </select>
          {rolesError && <small className="field__error">Ruoli non disponibili</small>}
        </label>
        <label className="field field--grow">
          <span>Cerca per nome</span>
          <input
            type="search"
            placeholder="Es. Rossi"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
        </label>
      </form>

      {loading ? (
        <Loading label="Caricamento giocatori..." />
      ) : error && players.length === 0 ? (
        <ErrorMessage error={error} onRetry={() => setReloadKey((k) => k + 1)} />
      ) : players.length === 0 ? (
        <div className="status">Nessun giocatore trovato con questi filtri.</div>
      ) : (
        <>
          <div className="grid">
            {players.map((player) => (
              <PlayerCard key={player.player_id} player={player} />
            ))}
          </div>
          {error && <ErrorMessage error={error} />}
          {hasMore && (
            <div className="more">
              <button type="button" className="btn" onClick={loadMore} disabled={loadingMore}>
                {loadingMore ? "Caricamento..." : "Carica altri"}
              </button>
            </div>
          )}
        </>
      )}
    </section>
  );
}
