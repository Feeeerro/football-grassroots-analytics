export const DASH = "—";

export function show(value, suffix = "") {
  return value === null || value === undefined || value === "" ? DASH : `${value}${suffix}`;
}

export function formatScore(score) {
  if (score === null || score === undefined || Number.isNaN(Number(score))) return DASH;
  return Number(score).toFixed(1);
}

// Classe CSS in base alla fascia di punteggio (scala 0-100).
export function scoreTier(score) {
  if (score === null || score === undefined) return "score--none";
  if (score >= 75) return "score--high";
  if (score >= 55) return "score--mid";
  return "score--low";
}

// Anno di inizio di una stagione ("24/25" -> 2024, "99/00" -> 1999, "2024" -> 2024),
// per ordinarle correttamente: l'ordine alfabetico mette "99/00" dopo "24/25".
export function seasonStartYear(season) {
  const match = /^(\d{2}|\d{4})(?:\/\d{2,4})?$/.exec(String(season ?? "").trim());
  if (!match) return -Infinity;
  const year = Number(match[1]);
  if (match[1].length === 4) return year;
  return year >= 50 ? 1900 + year : 2000 + year;
}

// Ultima stagione valutata (season_score non null). A parita' di stagione
// (piu' competizioni) vale quella con piu' minuti giocati.
export function lastScoredSeason(seasons) {
  let best = null;
  for (const s of seasons || []) {
    if (s.season_score === null || s.season_score === undefined) continue;
    const year = seasonStartYear(s.season);
    if (
      !best ||
      year > best.year ||
      (year === best.year && (s.total_minutes || 0) > (best.season.total_minutes || 0))
    ) {
      best = { year, season: s };
    }
  }
  return best ? { season: best.season.season, score: best.season.season_score } : null;
}
