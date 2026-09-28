"""
backend/main.py — API di sola lettura per la GUI dell'ASI.

Legge i punteggi gia' precalcolati (player_scores / season_scores) e i dati
anagrafici, senza ricalcolare nulla. Tre endpoint:

  GET /players            lista per le card (filtro per posizione, ordinata)
  GET /players/{id}       profilo completo: bio + stagioni + punteggi
  GET /roles              elenco posizioni per il filtro del frontend

Avvio dalla ROOT del progetto (stessa cartella di config.py):
    uvicorn backend.main:app --reload
"""

import sqlite3
from datetime import date

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from config import DB_PATH


app = FastAPI(title="ASI API", version="1.0")

# il frontend gira su un'altra porta (Vite 5173 / CRA 3000): senza CORS
# il browser blocca le chiamate.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── HELPER ────────────────────────────────────────────────────

def get_conn():
    """Connessione read-only con righe accessibili per nome colonna."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def calc_age(dob_str):
    """Eta' a partire dalla data di nascita 'GG/MM/AAAA'. None se assente
    o malformata. Calcolata a runtime, cosi' resta sempre corretta."""
    if not dob_str:
        return None
    try:
        g, m, a = (int(x) for x in dob_str.split("/"))
        oggi = date.today()
        return oggi.year - a - ((oggi.month, oggi.day) < (m, g))
    except (ValueError, AttributeError):
        return None


# ─── ENDPOINT ──────────────────────────────────────────────────

@app.get("/roles")
def list_roles():
    """Posizioni distinte presenti nel DB, per il filtro a tendina."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT DISTINCT position FROM players "
        "WHERE position IS NOT NULL ORDER BY position"
    ).fetchall()
    conn.close()
    return [r["position"] for r in rows]


@app.get("/players")
def list_players(
    position: str | None = Query(None, description="filtro per posizione esatta"),
    search: str | None = Query(None, description="ricerca per nome"),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    """Lista per le card: id, nome, posizione, eta', squadra piu' recente,
    punteggio finale. Ordinata per punteggio decrescente."""
    conn = get_conn()
    rows = conn.execute(
        """
        SELECT p.player_id,
               p.name,
               p.position,
               p.date_of_birth,
               sc.final_score,
               (SELECT COALESCE(t.name, st.team_name)
                  FROM player_stats st
                  LEFT JOIN teams t ON t.team_id = st.team_id
                 WHERE st.player_id = p.player_id
                   AND COALESCE(t.name, st.team_name) IS NOT NULL
                   AND st.season LIKE '%/%'
                 ORDER BY st.season DESC, st.total_minutes DESC
                 LIMIT 1) AS team
        FROM player_scores sc
        JOIN players p ON p.player_id = sc.player_id
        WHERE (:position IS NULL OR p.position = :position)
          AND (:search   IS NULL OR p.name LIKE '%' || :search || '%')
        ORDER BY sc.final_score DESC
        LIMIT :limit OFFSET :offset
        """,
        {"position": position, "search": search, "limit": limit, "offset": offset},
    ).fetchall()
    conn.close()

    return [
        {
            "player_id": r["player_id"],
            "name": r["name"],
            "position": r["position"],
            "age": calc_age(r["date_of_birth"]),
            "team": r["team"],
            "final_score": round(r["final_score"], 1) if r["final_score"] is not None else None,
        }
        for r in rows
    ]


@app.get("/players/{player_id}")
def player_profile(player_id: int):
    """Profilo completo: anagrafica + punteggio finale + tutte le stagioni
    con statistiche e punteggio di stagione (in scala assoluta)."""
    conn = get_conn()

    p = conn.execute(
        "SELECT * FROM players WHERE player_id = ?", (player_id,)
    ).fetchone()
    if p is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Giocatore non trovato")

    fs = conn.execute(
        "SELECT final_score FROM player_scores WHERE player_id = ?", (player_id,)
    ).fetchone()

    seasons = conn.execute(
        """
        SELECT st.season,
               st.competition,
<<<<<<< HEAD
               COALESCE(t.name, st.team_name) AS team,   -- nome collegato, altrimenti quello grezzo
=======
               -- team_id c'e' solo per la Serie D: altrimenti nome dalla pagina
               COALESCE(t.name, st.team_name) AS team,
>>>>>>> 1f4b269471fcf4a6a2edcaa826bcd26abdff346e
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
              AND sc.competition IS st.competition   -- IS: match anche coi NULL
        WHERE st.player_id = ?
        ORDER BY st.season DESC
        """,
        (player_id,),
    ).fetchall()
    conn.close()

    bio = dict(p)
    bio["age"] = calc_age(bio.get("date_of_birth"))
    bio["final_score"] = round(fs["final_score"], 1) if fs and fs["final_score"] is not None else None
    bio["seasons"] = [dict(s) for s in seasons]
    return bio