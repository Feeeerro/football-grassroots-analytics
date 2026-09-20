"""
Modello ASI — Punteggio centrocampisti (mediani, centrocampisti centrali, ali)

Combina due blocchi:
  - blocco offensivo: gol + assist, col bonus quota offensiva (come attacco)
  - blocco difensivo: minuti, col bonus contesto difensivo (come difesa)
I due blocchi sono mescolati con ALPHA (0.5 = pari peso). I cartellini
restano fuori dai blocchi, come penalita' neutra.

Il punteggio aggregato del giocatore e la normalizzazione finale 0-100
stanno nel modulo di aggregazione.
"""

import sqlite3
from config import (
    DB_PATH, K_BONUS, WEIGHTS_MIDFIELD, MIDFIELD_ALPHA
)
from database.queries import load_role_data, QUERY_MIDIFIELD
from scoring.normalize import build_benchmark, pct, neg_norm, map_red
from scoring.aggregate import player_asi

# le funzioni di contesto difensivo sono le stesse del modulo difensivo
from scoring.defensive_scoring import (
    expected_gc_curve,
    build_team_gc_benchmark,
    build_residuals_benchmark,
    defensive_context,
    apply_context,
)

from scoring.offensive_scoring import (
    quota_shrink,
    compute_mean_quote,
    build_quote_benchmark
)


# ─── PUNTEGGIO STAGIONE ────────────────────────────────────────

def midfielder_score(row, bench, ctx_data, off_data, position):
    """Punteggio 0-1 di una stagione di un centrocampista.

    ctx_data = (curve, team_gc_benchmark, residuals_benchmark)  -> contesto difensivo
    off_data = (mean_quote, quote_benchmark)                    -> contesto offensivo
    """
    curve, team_gc_benchmark, residuals_benchmark = ctx_data
    mean_quote, quote_benchmark = off_data

    # ── blocco offensivo: gol (col bonus quota) + assist ──
    q = quota_shrink(row["gol"], row["gol_scored"], mean_quote)
    off_bonus = K_BONUS * pct(q, quote_benchmark) if q is not None else 0.0
    gol_score = min(1.0, pct(row["gol"], bench["gol"]) * (1 + off_bonus))
    ass_norm = pct(row["assist"], bench["assist"])

    w = WEIGHTS_MIDFIELD[position]
    blocco_off = (
        gol_score * w["gol"] + ass_norm * w["assist"]
    ) / (w["gol"] + w["assist"])          # normalizzato 0-1 dentro il blocco

    # ── blocco difensivo: minuti col contesto difensivo ──
    ctx = defensive_context(
        row["team_position"], row["team_gol_conceded"],
        curve, residuals_benchmark, team_gc_benchmark,
    )
    min_norm = pct(row["total_minutes"], bench["total_minutes"])
    blocco_dif = apply_context(min_norm, ctx)     # gia' 0-1

    # ── combinazione dei due blocchi con ALPHA ──
    alpha = MIDFIELD_ALPHA[position]
    core = alpha * blocco_off + (1 - alpha) * blocco_dif

    # ── cartellini fuori dai blocchi, come penalita' ──
    yc_norm = neg_norm(row["yellow_cards"], bench["yellow_cards"])
    rc_norm = map_red(row["red_cards"])

    score = (
        core * w["core"]
        + yc_norm * w["yellow_cards"]
        + rc_norm * w["red_cards"]
    )
    return score


def make_midfield_score_fn(bench, ctx_data, off_data, position):
    """Confeziona la funzione punteggio con tutti i benchmark catturati."""
    def score_fn(row):
        return midfielder_score(row, bench, ctx_data, off_data, position)
    return score_fn


def run(conn, position):
    players = load_role_data(conn, position, QUERY_MIDIFIELD)

    # benchmark dei parametri individuali
    bench = {
        p: build_benchmark(players, p)
        for p in ("gol", "assist", "total_minutes", "yellow_cards")
    }

    # contesto offensivo (dai dati in memoria)
    mean_quote = compute_mean_quote(players)
    quote_benchmark = build_quote_benchmark(players, mean_quote)
    off_data = (mean_quote, quote_benchmark)

    # contesto difensivo (da standings)
    curve = expected_gc_curve(conn)
    team_gc_benchmark = build_team_gc_benchmark(conn)
    residuals_benchmark = build_residuals_benchmark(conn, curve)
    ctx_data = (curve, team_gc_benchmark, residuals_benchmark)

    # confeziona e calcola
    score_fn = make_midfield_score_fn(bench, ctx_data, off_data, position)
    raw = {
        pid: player_asi(seasons, score_fn)
        for pid, seasons in players.items()
    }

    # normalizzazione come rete di sicurezza (solo se qualcuno supera 100)
    asi_max = max(raw.values()) if raw else 1.0
    if asi_max > 100:
        scores = {pid: (v / asi_max) * 100 for pid, v in raw.items()}
    else:
        scores = dict(raw)
    return scores, players


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    scores, players = run(conn, "Mediano")
    conn.close()

    for pid, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]:
        name = players[pid][0]["player_name"]
        print(f"{score:5.1f}  {name}")