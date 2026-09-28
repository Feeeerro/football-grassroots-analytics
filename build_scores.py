"""
build_scores.py — precalcolo e persistenza degli ASI.

Gira tutti i reparti una volta sola e salva i punteggi nel DB, cosi'
l'API non deve ricalcolare niente a ogni richiesta. Due tabelle:

  - player_scores  : un punteggio finale per giocatore  (card)
  - season_scores  : un punteggio per ogni stagione      (profilo giocatore)

Le tabelle vengono ricreate da zero a ogni esecuzione: e' un ricalcolo
completo, non un aggiornamento incrementale, quindi il modo piu' semplice
e sicuro e' azzerarle e riempirle.

Lanciare dalla ROOT del progetto (stessa cartella di config.py):
    python build_scores.py
"""

import sqlite3

from config import DB_PATH
from scoring.offensive_scoring import run as run_offensive
from scoring.midfield_scoring import run as run_midfield
from scoring.defensive_scoring import run as run_defensive


# ─── INSTRADAMENTO RUOLO → REPARTO ─────────────────────────────
# Ogni posizione (stringa esatta come in players.position) va alla run()
# del suo reparto. L'appartenenza deriva dai pesi definiti in config:
# una posizione qui deve avere una voce nei WEIGHTS_* del suo modulo,
# altrimenti run() va in KeyError.
REPARTI = [
    ("OFFENSIVO", run_offensive, [
        "Punta centrale", "Seconda punta",
        "Esterno di destra", "Esterno di sinistra",
        "Trequartista", "Attacco",
    ]),
    ("CENTROCAMPO", run_midfield, [
        "Mediano", "Ala destra", "Ala sinistra",
        "Centrocampista", "Centrocampo",
    ]),
    ("DIFENSIVO", run_defensive, [
        "Portiere", "Difensore centrale",
        "Terzino destro", "Terzino sinistro", "Difesa",
    ]),
]


# ─── TABELLE ───────────────────────────────────────────────────

def create_score_tables(conn):
    """Ricrea le tabelle dei punteggi da zero (ricalcolo completo)."""
    conn.executescript("""
        DROP TABLE IF EXISTS player_scores;
        DROP TABLE IF EXISTS season_scores;

        CREATE TABLE player_scores (
            player_id   INTEGER PRIMARY KEY,
            final_score REAL,
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        );

        CREATE TABLE season_scores (
            player_id    INTEGER,
            season       TEXT,
            competition  TEXT,
            season_score REAL,
            PRIMARY KEY (player_id, season, competition),
            FOREIGN KEY (player_id) REFERENCES players(player_id)
        );
    """)


# ─── SALVATAGGIO ───────────────────────────────────────────────

def save_scores(conn, scores, season_detail):
    """Scrive un reparto: punteggio finale + dettaglio per stagione."""
    cur = conn.cursor()
    for pid, final_score in scores.items():
        cur.execute(
            "INSERT INTO player_scores (player_id, final_score) VALUES (?, ?)",
            (pid, final_score),
        )
        for s in season_detail[pid]:
            cur.execute("""
                INSERT INTO season_scores
                    (player_id, season, competition, season_score)
                VALUES (?, ?, ?, ?)
            """, (pid, s["season"], s["competition"], s["score"]))


# ─── CONTROLLO COPERTURA ───────────────────────────────────────

def check_coverage(conn):
    """Avverte se nel DB c'e' una posizione non instradata in nessun
    reparto: quei giocatori resterebbero senza punteggio."""
    instradate = {pos for _, _, positions in REPARTI for pos in positions}
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT position FROM players WHERE position IS NOT NULL")
    nel_db = {r[0] for r in cur.fetchall()}
    scoperte = nel_db - instradate
    if scoperte:
        print("  ATTENZIONE — posizioni nel DB non instradate (nessun punteggio):")
        for pos in sorted(scoperte):
            print(f"    - {pos}")


# ─── MAIN ──────────────────────────────────────────────────────

def main():
    conn = sqlite3.connect(DB_PATH)
    create_score_tables(conn)
    check_coverage(conn)

    totale = 0
    for nome_reparto, run_fn, positions in REPARTI:
        print(f"\n{nome_reparto}")
        for position in positions:
            scores, season_detail, _players = run_fn(conn, position)
            save_scores(conn, scores, season_detail)
            totale += len(scores)
            print(f"  {position:<22} {len(scores):>4} giocatori")

    conn.commit()
    conn.close()
    print(f"\nFatto: {totale} giocatori salvati in player_scores / season_scores.")


if __name__ == "__main__":
    main()