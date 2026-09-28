import { Link, useLocation } from "react-router-dom";
import { formatScore, scoreTier, show } from "../format.js";

export default function PlayerCard({ player }) {
  const location = useLocation();
  return (
    <Link
      to={`/players/${player.player_id}`}
      state={{ from: location.pathname + location.search }}
      className="card"
    >
      <div className="card__body">
        <h2 className="card__name">{player.name}</h2>
        <p className="card__position">{show(player.position)}</p>
        <dl className="card__meta">
          <div>
            <dt>Eta'</dt>
            <dd>{show(player.age)}</dd>
          </div>
          <div>
            <dt>Squadra</dt>
            <dd title={player.team || undefined}>{show(player.team)}</dd>
          </div>
        </dl>
      </div>
      <div className={`card__score ${scoreTier(player.final_score)}`}>
        <span className="score__value">{formatScore(player.final_score)}</span>
        <span className="score__label">ASI</span>
      </div>
    </Link>
  );
}
