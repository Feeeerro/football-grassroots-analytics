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
