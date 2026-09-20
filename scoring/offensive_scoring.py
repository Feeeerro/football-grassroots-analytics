"""
Modello ASI — Punteggio offensivo (attaccanti / punte centrali)

Pipeline batch: calcola l'ASI di tutti i giocatori di un ruolo in un colpo solo.
Struttura a tre livelli:
    batch (tutti i giocatori)
      -> giocatore (aggregazione temporale delle sue stagioni)
        -> stagione (funzioni pure di calcolo)

Le funzioni di calcolo sono pure (prendono numeri, restituiscono numeri).
I valori di riferimento (benchmark, media quota, ASI_max) sono globali e
precalcolati una volta, poi passati dentro.
"""

import sqlite3
from collections import defaultdict
from config import (
    DB_PATH, C_SHRINK, K_BONUS, WEIGHTS_OFFENSIVE
)

from database.queries import load_role_data, QUERY_OFFENSIVE
from scoring.normalize import build_benchmark, pct, neg_norm, map_red
from scoring.aggregate import player_asi


def quota_shrink(gol, gol_scored, mean_quote, c=C_SHRINK):
    """Quota offensiva (solo gol) corretta con shrinkage.
    Solo gol e non gol+assist per non contare due volte gli assist,
    che pesano gia' come parametro autonomo.
    Ritorna None se manca il contesto squadra."""
    if gol_scored is None or gol_scored == 0:
        return None
    g = gol or 0
    return (g + c * mean_quote) / (gol_scored + c)



# ─── PRECALCOLI GLOBALI (una volta per ruolo) ──────────────────

def compute_mean_quote(players):
    """Media delle quote (gol/gol_scored) sulle sole righe con contesto.
    E' l'ancoraggio dello shrinkage: stessa metrica che stima."""
    tot, n = 0.0, 0
    for seasons in players.values():
        for s in seasons:
            if s["gol_scored"] and s["gol"] is not None:
                tot += s["gol"] / s["gol_scored"]
                n += 1
    return tot / n if n else 0.0


def build_quote_benchmark(players, mean_quote):
    """Benchmark delle quote shrinkate, per normalizzare il bonus."""
    out = []
    for seasons in players.values():
        for s in seasons:
            q = quota_shrink(s["gol"], s["gol_scored"], mean_quote)
            if q is not None:
                out.append(q)
    return out


# ─── PUNTEGGIO STAGIONE ────────────────────────────────────────

def season_score(s, bench, mean_quote, quote_bench, position):
    """Punteggio 0-1 (pre-categoria) di una stagione."""
    # bonus quota: solo dove c'e' contesto squadra
    q = quota_shrink(s["gol"], s["gol_scored"], mean_quote)
    bonus = K_BONUS * pct(q, quote_bench) if q is not None else 0.0

    score_gol = min(1.0, pct(s["gol"], bench["gol"]) * (1 + bonus))

    return (
        score_gol                                        * WEIGHTS_OFFENSIVE[position]["gol"]
        + pct(s["assist"], bench["assist"])              * WEIGHTS_OFFENSIVE[position]["assist"]
        + pct(s["total_minutes"], bench["total_minutes"]) * WEIGHTS_OFFENSIVE[position]["total_minutes"]
        + neg_norm(s["yellow_cards"], bench["yellow_cards"]) * WEIGHTS_OFFENSIVE[position]["yellow_cards"]
        + map_red(s["red_cards"])                        * WEIGHTS_OFFENSIVE[position]["red_cards"]
    )


# ─── ORCHESTRAZIONE BATCH ──────────────────────────────────────

def make_offensive_score_fn(bench, mean_quote, quote_bench, position):
    def score_fn(riga):
        return season_score(riga, bench, mean_quote, quote_bench, position)
    return score_fn

def run(conn, position):
    players = load_role_data(conn, position, QUERY_OFFENSIVE)

    bench = {
        p: build_benchmark(players, p)
        for p in ("gol", "assist", "total_minutes", "yellow_cards")
    }
    mean_quote = compute_mean_quote(players)
    quote_bench = build_quote_benchmark(players, mean_quote)

    score_fn = make_offensive_score_fn(bench, mean_quote, quote_bench, position)
    raw = {
        pid: player_asi(seasons, score_fn)
        for pid, seasons in players.items()
    }

    # normalizzazione finale 0-100 sul massimo osservato
    asi_max = max(raw.values()) if raw else 1.0
    if asi_max > 100:
        scores = {pid: (v / asi_max) * 100 for pid, v in raw.items()}
    else:
        scores = dict(raw)

    return scores, players


if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    scores, players = run(conn, "Punta centrale")
    conn.close()

    for pid, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]:
        name = players[pid][0]["player_name"]
        print(f"{score:5.1f}  {name}")