import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router-dom";
import { getPlayer } from "../api.js";
import { ErrorMessage, Loading } from "../components/Status.jsx";
import { DASH, formatScore, lastScoredSeason, scoreTier, seasonStartYear, show } from "../format.js";
import SeasonScore from "../components/SeasonScore.jsx";

const GOALKEEPER = "Portiere";

function redCards(season) {
  const { red_cards: red, double_yellow_cards: doubleYellow } = season;
  if (red == null && doubleYellow == null) return DASH;
  return (red || 0) + (doubleYellow || 0);
}

export default function PlayerProfile() {
  const { id } = useParams();
  // Se arriviamo dalla lista, torniamo agli stessi filtri.
  const backTo = useLocation().state?.from || "/";
  const [player, setPlayer] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    getPlayer(id, { signal: controller.signal })
      .then((data) => {
        setPlayer(data);
        setLoading(false);
      })
      .catch((err) => {
        if (err.name === "AbortError") return;
        if (err.status === 404) {
          const notFound = new Error("Giocatore non trovato.");
          notFound.status = 404;
          setError(notFound);
        } else {
          setError(err);
        }
        setLoading(false);
      });
    return () => controller.abort();
  }, [id, reloadKey]);

  const backLink = (
    <Link to={backTo} className="back">
      ← Torna alla lista
    </Link>
  );

  if (loading) {
    return (
      <section>
        {backLink}
        <Loading label="Caricamento profilo..." />
      </section>
    );
  }

  if (error) {
    return (
      <section>
        {backLink}
        <ErrorMessage
          error={error}
          onRetry={error.status === 404 ? undefined : () => setReloadKey((k) => k + 1)}
        />
      </section>
    );
  }

  const isGoalkeeper = player.position === GOALKEEPER;
  // Dalla piu' recente: l'ordine testuale del file metterebbe "99/00" prima di "24/25".
  const seasons = [...(player.seasons || [])].sort(
    (a, b) => seasonStartYear(b.season) - seasonStartYear(a.season)
  );
  const lastSeason = lastScoredSeason(seasons);

  return (
    <section>
      {backLink}

      <header className="profile">
        <div className="profile__info">
          <h1>{player.name}</h1>
          <p className="profile__position">{show(player.position)}</p>
          <dl className="profile__facts">
            <div>
              <dt>Eta'</dt>
              <dd>{show(player.age)}</dd>
            </div>
            <div>
              <dt>Altezza</dt>
              <dd>{show(player.height, " cm")}</dd>
            </div>
            <div>
              <dt>Piede</dt>
              <dd>{show(player.feet)}</dd>
            </div>
            <div>
              <dt>Scadenza contratto</dt>
              <dd>{show(player.deadline)}</dd>
            </div>
          </dl>
        </div>
        <div className="scores">
          <div className={`profile__score ${scoreTier(player.final_score)}`}>
            <span className="score__value">{formatScore(player.final_score)}</span>
            <span className="score__label">Punteggio ASI</span>
          </div>
          <SeasonScore
            season={lastSeason?.season}
            score={lastSeason?.score}
            className="season-score--lg"
          />
        </div>
      </header>

      <h2 className="section-title">Stagioni</h2>
      {seasons.length === 0 ? (
        <div className="status">Nessuna stagione disponibile.</div>
      ) : (
        <div className="table-wrap">
          <table className="seasons">
            <thead>
              <tr>
                <th>Stagione</th>
                <th>Competizione</th>
                <th>Squadra</th>
                <th className="num">Presenze</th>
                <th className="num">Minuti</th>
                <th className="num">Gol</th>
                <th className="num">Assist</th>
                <th className="num">Ammonizioni</th>
                <th className="num" title="Rossi diretti + doppie ammonizioni">
                  Espulsioni
                </th>
                {isGoalkeeper && <th className="num">Clean sheet</th>}
                {isGoalkeeper && <th className="num">Gol subiti</th>}
                <th className="num">Score stagione</th>
              </tr>
            </thead>
            <tbody>
              {seasons.map((s, i) => (
                <tr key={`${s.season}-${s.competition}-${s.team}-${i}`}>
                  <td>{show(s.season)}</td>
                  <td>{show(s.competition)}</td>
                  <td>{show(s.team)}</td>
                  <td className="num">{show(s.appearances)}</td>
                  <td className="num">{show(s.total_minutes)}</td>
                  <td className="num">{show(s.gol)}</td>
                  <td className="num">{show(s.assist)}</td>
                  <td className="num">{show(s.yellow_cards)}</td>
                  <td className="num">{redCards(s)}</td>
                  {isGoalkeeper && <td className="num">{show(s.clean_sheet)}</td>}
                  {isGoalkeeper && <td className="num">{show(s.gol_conceded)}</td>}
                  <td className="num">
                    <span className={`pill ${scoreTier(s.season_score)}`}>
                      {formatScore(s.season_score)}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
