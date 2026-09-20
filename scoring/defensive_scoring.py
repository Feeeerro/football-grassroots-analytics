"""
Modello ASI — Punteggio difensivo (portieri e difensori)

Calcola il punteggio 0-1 di una singola stagione per i ruoli difensivi,
applicando:
  - normalizzazione a percentile su benchmark storico per ruolo
  - contesto difensivo = solidita' squadra + sovraperformance vs posizione
  - shrinkage sui gol subiti per partita del portiere
  - moltiplicatore di categoria

Il punteggio aggregato del giocatore (media pesata con decadimento temporale)
e la normalizzazione finale 0-100 stanno nel modulo di aggregazione.
"""

import sqlite3
from collections import defaultdict
from config import (
    DB_PATH, C_SHRINK, K_BONUS, W_SOLIDITY, W_OVERPERF,
    WEIGHTS_DEFENSIVE, COMPETITION_FILTERS
)

from database.queries import load_role_data, QUERY_DEFENSIVE
from scoring.normalize import build_benchmark, pct, neg_norm, map_red
from scoring.aggregate import player_asi

# ─── CURVA ATTESA GOL SUBITI PER POSIZIONE ────────────────────────────────────────

def expected_gc_curve(conn):

    QUERY_EXPECTED_CURVE = """
        SELECT position, AVG(gol_conceded)
        FROM standings
        WHERE gol_conceded IS NOT NULL
        GROUP BY position
        ORDER BY position
    """
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(QUERY_EXPECTED_CURVE)

    curve = {position: mean for position, mean in cur.fetchall()}
    return curve

def build_residuals_benchmark(conn, mean_gc_per_pos):

    QUERY_GOL_CONCEDED = """
        SELECT position, gol_conceded
        FROM standings
        WHERE position IS NOT NULL AND gol_conceded IS NOT NULL
    """

    cur = conn.cursor()
    cur.execute(QUERY_GOL_CONCEDED)
    standings_rows = cur.fetchall()

    residuals = []
    for position, gol_conceded in standings_rows:
        residuals.append(mean_gc_per_pos[position] - gol_conceded)

    return residuals

def overperformance(team_position, team_gol_conceded, curve, residuals_benchmark):
    """Quanto la difesa della squadra ha fatto meglio del previsto data la
    posizione. Ritorna 0-1 (percentile dello scarto), o None se manca il
    contesto squadra (categorie senza standings)."""
    if team_position is None or team_gol_conceded is None:
        return None
    residual = curve[team_position] - team_gol_conceded
    return pct(residual, residuals_benchmark)

def team_solidity(team_gol_conceded, team_gc_benchmark):
    if team_gol_conceded is None:
        return None
    return neg_norm(team_gol_conceded, team_gc_benchmark)

def gspp_shrink(gc, app, mean_gspp, c=C_SHRINK):
    """Gol subiti per partita del portiere, protetto dai campioni piccoli.
    Con poche presenze il valore viene tirato verso la media del ruolo."""
    gc = gc or 0
    app = app or 0
    return (gc + c * mean_gspp) / (app + c)

def defensive_context(team_position, team_gol_conceded, curve, residuals_benchmark, team_gc_benchmark):
    solidity_bonus = team_solidity(team_gol_conceded, team_gc_benchmark)
    over_bonus = overperformance(team_position, team_gol_conceded, curve, residuals_benchmark)

    if solidity_bonus is None and over_bonus is None:
        return None
    elif solidity_bonus is None:
        return over_bonus
    elif over_bonus is None:
        return solidity_bonus
    else:
        return W_SOLIDITY * solidity_bonus + W_OVERPERF * over_bonus

def build_team_gc_benchmark(conn):
    """Distribuzione dei gol subiti dalle squadre (tutte le stagioni)."""
    cur = conn.cursor()
    cur.execute("SELECT gol_conceded FROM standings WHERE gol_conceded IS NOT NULL")
    return [r[0] for r in cur.fetchall()]

def mean_gspp_goalkeeper(players):
    """Media storica dei gol subiti per partita dei portieri.
    E' l'ancoraggio dello shrinkage: stessa metrica che si sta stimando."""
    values = [
        s["gol_conceded"] / s["appearances"]
        for seasons in players.values()
        for s in seasons
        if s["appearances"] and s["gol_conceded"] is not None
    ]
    return sum(values) / len(values) if values else 1.4


def build_gspp_benchmark(players, mean_gspp):
    """Benchmark dei gol-subiti-per-partita SHRINKATI dei portieri.
    Deve stare sulla stessa scala del valore che poi normalizzera'
    (il gspp del singolo portiere), quindi anche qui si applica lo shrinkage."""
    return [
        gspp_shrink(s["gol_conceded"], s["appearances"], mean_gspp)
        for seasons in players.values()
        for s in seasons
        if s["appearances"] and s["gol_conceded"] is not None
    ]

def apply_context(param_norm, ctx, k=K_BONUS):
    """Raffina un parametro col contesto difensivo. Cap obbligatorio a 1.0."""
    if ctx is None:
        return param_norm
    return min(1.0, param_norm * (1 + k * ctx))

# ─── PUNTEGGIO STAGIONE ────────────────────────────────────────

def goalkeeper_score(row, bench, curve, team_gc_benchmark, residuals_benchmark, mean_gspp):
    """Punteggio 0-1 di una stagione di un portiere."""
    ctx = defensive_context(
        row["team_position"], row["team_gol_conceded"],
        curve, residuals_benchmark, team_gc_benchmark,
    )

    cs_norm = pct(row["clean_sheet"], bench["clean_sheet"])

    # gol subiti: si usa il valore per-partita shrinkato, non il totale grezzo,
    # cosi' un portiere con poche presenze non risulta artificialmente ottimo
    gspp = gspp_shrink(row["gol_conceded"], row["appearances"], mean_gspp)
    gc_norm = neg_norm(gspp, bench["gspp"])

    min_norm = pct(row["total_minutes"], bench["total_minutes"])
    yc_norm = neg_norm(row["yellow_cards"], bench["yellow_cards"])
    rc_norm = map_red(row["red_cards"])

    w = WEIGHTS_DEFENSIVE["Portiere"]
    score = (
        apply_context(cs_norm, ctx) * w["clean_sheet"]
        + apply_context(gc_norm, ctx) * w["gol_conceded"]
        + min_norm * w["total_minutes"]
        + yc_norm * w["yellow_cards"]
        + rc_norm * w["red_cards"]
    )
    return score


def defender_score(row, bench, curve, team_gc_benchmark, residuals_benchmark, position):
    ctx = defensive_context(
        row["team_position"], row["team_gol_conceded"],
        curve, residuals_benchmark, team_gc_benchmark,
    )

    min_norm = pct(row["total_minutes"], bench["total_minutes"])
    gol_norm = pct(row["gol"], bench["gol"])
    ass_norm = pct(row["assist"], bench["assist"])
    yc_norm = neg_norm(row["yellow_cards"], bench["yellow_cards"])
    rc_norm = map_red(row["red_cards"])

    w = WEIGHTS_DEFENSIVE[position]
    score = (
        apply_context(min_norm, ctx) * w["total_minutes"]   # ← contesto sui minuti
        + gol_norm * w["gol"]
        + ass_norm * w["assist"]
        + yc_norm * w["yellow_cards"]
        + rc_norm * w["red_cards"]
    )
    return score

def make_defensive_score_fn(bench, curve, team_gc_benchmark, residuals_benchmark, mean_gspp, position):
    """Confeziona la funzione punteggio difensiva con tutti i benchmark
    catturati dentro. Restituisce una score_fn(row) che player_asi puo'
    chiamare con la sola stagione."""
    def score_fn(row):
        if position == "Portiere":
            return goalkeeper_score(row, bench, curve, team_gc_benchmark, residuals_benchmark, mean_gspp)
        else:
            return defender_score(row, bench, curve, team_gc_benchmark, residuals_benchmark, position)
    return score_fn

def run(conn, position):
    players = load_role_data(conn, position, QUERY_DEFENSIVE)
    # benchmark dei parametri individuali (dipende dal ruolo)
    params = ["total_minutes", "yellow_cards"]

    if position == "Portiere":
        params += ["clean_sheet"]
    else:
        params += ["gol", "assist"]

    bench = {
        p: build_benchmark(players, p)
        for p in params
    }

    # precalcoli difensivi (da standings)
    mean_gc_per_pos = expected_gc_curve(conn)                        # compute the mean of goal conceded for each position
    team_gc_benchmark = build_team_gc_benchmark(conn)               # build benchmark of goal conceded by the team
    residuals_benchmark = build_residuals_benchmark(conn, mean_gc_per_pos)  # build benchmark of difference between gol conceded and the mean of its position

    # solo per il portiere: media gspp e benchmark dei gspp shrinkati
    mean_gspp = None
    if position == "Portiere":
        mean_gspp = mean_gspp_goalkeeper(players)
        bench["gspp"] = build_gspp_benchmark(players, mean_gspp)       # benchmark dei gspp shrinkati

    # confeziona e calcola
    score_fn = make_defensive_score_fn(bench, mean_gc_per_pos, team_gc_benchmark, residuals_benchmark, mean_gspp, position)
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
    scores, players = run(conn, "Portiere")
    conn.close()

    for pid, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)[:100]:
        name = players[pid][0]["player_name"]
        print(f"{score:5.1f}  {name}")