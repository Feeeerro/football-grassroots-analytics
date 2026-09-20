import sqlite3
from collections import defaultdict
from config import COMPETITION_FILTERS

CAMPI_IDENTIFICATIVI = {"player_id", "player_name", "season"}
CAMPI_CONTESTO = {"gol_scored", "team_gol_conceded", "team_position"}

filters = " AND ".join(COMPETITION_FILTERS)

QUERY_OFFENSIVE = f"""
    SELECT ps.player_id,
        p.name AS player_name,
        ps.season, ps.competition, ps.gol, ps.assist,
        ps.yellow_cards, ps.red_cards, ps.total_minutes, 
        s.gol_scored
    FROM player_stats ps
    JOIN players p ON p.player_id = ps.player_id
    LEFT JOIN standings s ON s.team_id = ps.team_id AND s.season = ps.season
    WHERE p.position = ? AND {filters}
    ORDER BY ps.player_id, ps.season DESC
"""

QUERY_DEFENSIVE = f"""
    SELECT ps.player_id,
        p.name AS player_name,
        ps.season, ps.competition, ps.gol, ps.assist, ps.clean_sheet, 
        ps.gol_conceded, ps.yellow_cards, ps.red_cards, ps.total_minutes, ps.appearances,
        s.gol_conceded AS team_gol_conceded, s.position AS team_position
    FROM player_stats ps
    JOIN players p ON p.player_id = ps.player_id
    LEFT JOIN standings s ON s.team_id = ps.team_id AND s.season = ps.season
    WHERE p.position = ? AND {filters}
    ORDER BY ps.player_id, ps.season DESC
"""

QUERY_MIDIFIELD = f"""
    SELECT ps.player_id,
        p.name AS player_name,
        ps.season, ps.competition, ps.gol, ps.assist, ps.gol_conceded,
        ps.yellow_cards, ps.red_cards, ps.total_minutes, ps.appearances,
        s.gol_scored,
        s.gol_conceded AS team_gol_conceded, s.position AS team_position
    FROM player_stats ps
    JOIN players p ON p.player_id = ps.player_id
    LEFT JOIN standings s ON s.team_id = ps.team_id AND s.season = ps.season
    WHERE p.position = ? AND {filters}
    ORDER BY ps.player_id, ps.season DESC
"""


def merge_split_seasons(rows):
    per_stagione = defaultdict(list)
    for r in rows:
        per_stagione[r["season"]].append(r)

    fuse = []
    for season, gruppo in per_stagione.items():
        if len(gruppo) == 1:
            fuse.append(gruppo[0])
            continue

        principale = max(gruppo, key=lambda r: r["total_minutes"] or 0)
        fusa = {}
        for campo in gruppo[0]:                     # scorre i nomi dei campi
            if campo in CAMPI_IDENTIFICATIVI:
                fusa[campo] = principale[campo]
            elif campo in CAMPI_CONTESTO:
                fusa[campo] = None
            elif campo == "competition":
                fusa[campo] = principale[campo]
            else:
                fusa[campo] = sum(r[campo] or 0 for r in gruppo)
        fuse.append(fusa)

    fuse.sort(key=lambda r: r["season"], reverse=True)
    return fuse
 
 
def load_role_data(conn, position, query):
    """{player_id: [stagioni]}, stagioni dalla piu' recente,
    con le stagioni spezzate gia' fuse in una."""
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, (position,))
 
    grezzo = defaultdict(list)
    for row in cur.fetchall():
        grezzo[row["player_id"]].append(dict(row))
 
    # fondi le stagioni spezzate di ogni giocatore
    return {pid: merge_split_seasons(rows) for pid, rows in grezzo.items()}