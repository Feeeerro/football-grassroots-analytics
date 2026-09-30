import { formatScore, scoreTier } from "../format.js";

// Valutazione dell'ultima stagione, mostrata in piccolo accanto a quella complessiva.
export default function SeasonScore({ season, score, className = "" }) {
  const hasScore = score !== null && score !== undefined;
  return (
    <div
      className={`season-score ${scoreTier(hasScore ? score : null)} ${className}`}
      title={hasScore ? `Ultima stagione valutata: ${season}` : "Nessuna stagione valutata"}
    >
      <span className="season-score__value">{formatScore(hasScore ? score : null)}</span>
      <span className="season-score__label">{hasScore && season ? season : "Ult. stag."}</span>
    </div>
  );
}
