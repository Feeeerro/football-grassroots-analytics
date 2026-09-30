"""
export_static.py — esporta il DB in file JSON statici per GitHub Pages.

I dati sono precalcolati e di sola lettura, quindi non serve un server: questo
script trasforma seried.db negli stessi payload che restituiva l'API, ma come
file statici che il frontend puo' leggere direttamente. Produce:

  <OUT_DIR>/players.json          lista per le card (tutti i giocatori)
  <OUT_DIR>/roles.json            posizioni per il filtro
  <OUT_DIR>/profiles.json         tutti i profili in un unico dizionario {id: profilo}

Le query sono le STESSE del backend, cosi' la forma dei dati e' identica e il
frontend deve solo cambiare l'URL da cui legge.

Lanciare dalla ROOT del progetto:
    python export_static.py
"""

import json
import sqlite3
from datetime import date
from pathlib import Path

from config import DB_PATH

# Cartella di output: i file finiscono in public/ del frontend, cosi' Vite li
# copia nella build e finiscono su Pages. ADATTA il nome della cartella frontend
# se Claude Code l'ha chiamata diversamente.
OUT_DIR = Path(__file__).resolve().parent / "frontend" / "public" / "data"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def calc_age(dob_str):
    """Eta' da 'GG/MM/AAAA'. Calcolata al momento dell'export: si aggiorna a
    ogni ricostruzione del sito. None se assente o malformata."""
    if not dob_str:
        return None
    try:
        g, m, a = (int(x) for x in dob_str.split("/"))
        oggi = date.today()
        return oggi.year - a - ((oggi.month, oggi.day) < (m, g))
    except (ValueError, AttributeError):
        return None


def season_start_year(season):
    """Anno di inizio stagione ('24/25' -> 2024, '99/00' -> 1999, '2024' -> 2024).
    L'ordine alfabetico metterebbe '99/00' dopo '24/25'."""
    head = (season or "").strip().split("/")[0]
    if not head.isdigit() or len(head) not in (2, 4):
        return None
    year = int(head)
    if len(head) == 4:
        return year
    return 1900 + year if year >= 50 else 2000 + year


def last_scored_seasons(conn):
    """{player_id: (stagione, punteggio)} dell'ultima stagione valutata. A parita'
    di stagione (piu' competizioni) vale quella con piu' minuti. Stessa regola
    usata dal frontend nel profilo."""
    rows = conn.execute(
        """
        SELECT sc.player_id, sc.season, sc.season_score,
               MAX(COALESCE(st.total_minutes, 0)) AS minutes
        FROM season_scores sc
        LEFT JOIN player_stats st
               ON st.player_id  = sc.player_id
              AND st.season      = sc.season
              AND st.competition IS sc.competition
        WHERE sc.season_score IS NOT NULL
        GROUP BY sc.player_id, sc.season, sc.competition
        """
    ).fetchall()
    best = {}
    for r in rows:
        year = season_start_year(r["season"])
        if year is None:
            continue
        key = (year, r["minutes"])
        pid = r["player_id"]
        if pid not in best or key > best[pid][0]:
            best[pid] = (key, (r["season"], round(r["season_score"], 1)))
    return {pid: value for pid, (_, value) in best.items()}


# ─── ESPORTAZIONI ──────────────────────────────────────────────

def export_players(conn):
    """Lista per le card (come GET /players, senza filtri: filtro e ricerca
    diventano lato client)."""
    rows = conn.execute(
        """
        SELECT p.player_id,
               p.name,
               p.position,
               p.date_of_birth,
               sc.final_score,
               (SELECT t.name
                  FROM player_stats st
                  JOIN teams t ON t.team_id = st.team_id
                 WHERE st.player_id = p.player_id
                   AND st.team_id IS NOT NULL
                   AND st.season LIKE '%/%'
                 ORDER BY st.season DESC, st.total_minutes DESC
                 LIMIT 1) AS team
        FROM player_scores sc
        JOIN players p ON p.player_id = sc.player_id
        ORDER BY sc.final_score DESC
        """
    ).fetchall()

    last = last_scored_seasons(conn)
    players = [
        {
            "player_id": r["player_id"],
            "name": r["name"],
            "position": r["position"],
            "age": calc_age(r["date_of_birth"]),
            "team": r["team"],
            "final_score": round(r["final_score"], 1) if r["final_score"] is not None else None,
            "last_season": last.get(r["player_id"], (None, None))[0],
            "last_season_score": last.get(r["player_id"], (None, None))[1],
        }
        for r in rows
    ]
    _write(OUT_DIR / "players.json", players)
    return [r["player_id"] for r in rows]


def export_roles(conn):
    """Posizioni distinte (come GET /roles)."""
    rows = conn.execute(
        "SELECT DISTINCT position FROM players "
        "WHERE position IS NOT NULL ORDER BY position"
    ).fetchall()
    _write(OUT_DIR / "roles.json", [r["position"] for r in rows])


def export_profiles(conn, player_ids):
    """Tutti i profili in un unico file {id: profilo} (come GET /players/{id},
    ma raccolti in un dizionario). Poche query bulk invece di una per giocatore,
    cosi' l'export e' veloce anche con migliaia di giocatori."""
    id_set = set(player_ids)

    # bio di tutti i giocatori con punteggio, in un colpo
    print("    carico bio...", flush=True)
    bios = {}
    for p in conn.execute("SELECT * FROM players"):
        d = dict(p)
        pid = d["player_id"]
        if pid in id_set:
            d["age"] = calc_age(d.get("date_of_birth"))
            d["final_score"] = None
            d["seasons"] = []
            bios[pid] = d

    # punteggi finali, in un colpo
    print("    carico punteggi finali...", flush=True)
    for r in conn.execute("SELECT player_id, final_score FROM player_scores"):
        b = bios.get(r["player_id"])
        if b is not None:
            b["final_score"] = round(r["final_score"], 1) if r["final_score"] is not None else None

    # tutte le stagioni di tutti i giocatori, in un colpo, gia' ordinate
    print("    raggruppo le stagioni...", flush=True)
    rows = conn.execute(
        """
        SELECT st.player_id,
               st.season,
               st.competition,
               COALESCE(t.name, st.team_name) AS team,
               st.appearances,
               st.gol,
               st.assist,
               st.gol_conceded,
               st.clean_sheet,
               st.yellow_cards,
               st.double_yellow_cards,
               st.red_cards,
               st.total_minutes,
               sc.season_score
        FROM player_stats st
        LEFT JOIN teams t
               ON t.team_id = st.team_id
        LEFT JOIN season_scores sc
               ON sc.player_id  = st.player_id
              AND sc.season      = st.season
              AND sc.competition IS st.competition
        ORDER BY st.player_id, st.season DESC
        """
    )
    n = 0
    for s in rows:
        b = bios.get(s["player_id"])
        if b is not None:
            row = dict(s)
            row.pop("player_id", None)   # ridondante dentro il profilo
            b["seasons"].append(row)
        n += 1
        if n % 5000 == 0:
            print(f"\r      stagioni processate: {n}", end="", flush=True)
    print(f"\r      stagioni processate: {n}        ", flush=True)

    # un unico file, chiavi come stringhe (JSON non ha chiavi intere)
    print("    scrivo profiles.json...", flush=True)
    profiles = {str(pid): bio for pid, bio in bios.items()}
    _write(OUT_DIR / "profiles.json", profiles)


# ─── UTILITY ───────────────────────────────────────────────────

def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_conn()

    print("[1/3] Esporto la lista giocatori (players.json)...", flush=True)
    player_ids = export_players(conn)
    print(f"      -> {len(player_ids)} giocatori", flush=True)

    print("[2/3] Esporto le posizioni (roles.json)...", flush=True)
    export_roles(conn)
    print("      -> ok", flush=True)

    print("[3/3] Esporto i profili (profiles.json)...", flush=True)
    export_profiles(conn, player_ids)
    print(f"      -> {len(player_ids)} profili", flush=True)

    conn.close()
    print(f"Esportati {len(player_ids)} giocatori in {OUT_DIR}")
    print("  - players.json (lista)")
    print("  - roles.json (posizioni)")
    print(f"  - profiles.json (dizionario con {len(player_ids)} profili)")


if __name__ == "__main__":
    main()