"""
Configurazione centrale del progetto.

Tutti i parametri tarabili del modello e i percorsi stanno qui, cosi'
la taratura tocca un solo file invece di essere sparsa nei moduli.
Gli altri moduli fanno: from config import ...
"""

from pathlib import Path


# ─── PERCORSI ──────────────────────────────────────────────────
# Costruiti relativi a questo file, cosi' funzionano da qualunque
# cartella si lanci lo script (BASE_DIR = cartella del progetto).
BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
SQUADS_DIR = RAW_DIR / "squads"
HISTORY_DIR = RAW_DIR / "history"
DB_PATH = DATA_DIR / "seried.db"


# ─── PARAMETRI SCORING — GLOBALI ───────────────────────────────
C_SHRINK = 10          # smoothing quota: sotto ~10 gol-squadra non ci si fida
K_BONUS = 0.15         # tetto del bonus contesto (offensivo e difensivo)
LAMBDA_QUALITA = 0.8   # peso decrescente per stagioni ordinate per qualita'
LAMBDA_TEMPO = 0.9     # attenuazione dolce delle stagioni lontane
VOLUME_CAP = 8000      # minuti totali per "piena valutabilita'" (~3 stagioni)

MIDFIELD_ALPHA = {
    "Mediano": 0.5,
    "Centrocampista centrale": 0.5,
    "Ala destra": 0.5,
    "Ala sinistra": 0.5,
}

W_SOLIDITY = 0.40      # peso solidita' assoluta dentro il contesto difensivo
W_OVERPERF = 0.60     # peso sovraperformance dentro il contesto difensivo


# ─── MOLTIPLICATORI DI CATEGORIA ───────────────────────────────
CATEGORY_MULT = {
    "Serie A": 1.35,
    "Serie B": 1.25,
    "Serie C": 1.10,
    "Serie D": 1.0,
}
DEFAULT_MULT = 0.7     # giovanili / competizioni non mappate


# ─── FILTRO COMPETIZIONI ───────────────────────────────────────
# Escludono coppe, spareggi e stagioni con formato anomalo (internazionali).
# Usati nel WHERE delle query di caricamento.
COMPETITION_FILTERS = (
    "ps.competition NOT LIKE 'Coppa%'",
    "ps.competition NOT LIKE '%play%'",
    "ps.competition NOT LIKE 'Poule%'",
    "ps.season LIKE '%/%'",
)


# ─── PESI PER RUOLO ────────────────────────────────────────────
# Ogni set somma a 1.0. Baseline da tarare sui giocatori noti.

WEIGHTS_OFFENSIVE = {
    "Punta centrale": {
        "gol": 0.40, "assist": 0.20, "total_minutes": 0.25,
        "yellow_cards": 0.05, "red_cards": 0.10,
    },
    "Seconda punta": {
        "gol": 0.35, "assist": 0.25, "total_minutes": 0.25,
        "yellow_cards": 0.05, "red_cards": 0.10,
    },
    "Esterno di destra": {
        "gol": 0.30, "assist": 0.30, "total_minutes": 0.25,
        "yellow_cards": 0.05, "red_cards": 0.10,
    },
    "Trequartista": {
        "gol": 0.30, "assist": 0.35, "total_minutes": 0.25,
        "yellow_cards": 0.05, "red_cards": 0.05,
    },
}

WEIGHTS_OFFENSIVE["Attacco"] = WEIGHTS_OFFENSIVE["Punta centrale"]
WEIGHTS_OFFENSIVE["Esterno di sinistra"] = WEIGHTS_OFFENSIVE["Esterno di destra"]

WEIGHTS_MIDFIELD = {
    "Centrocampista": {
        "total_minutes": 0.30, "gol": 0.25, "assist": 0.25, 
        "core": 0.80, "yellow_cards": 0.10, "red_cards": 0.10,
    },
    "Mediano": {
        "total_minutes": 0.45, "gol": 0.15, "assist": 0.20, 
        "core": 0.80, "yellow_cards": 0.10, "red_cards": 0.10,
    },
    "Ala destra": {
        "total_minutes": 0.25, "gol": 0.20, "assist": 0.35,  
        "core": 0.80, "yellow_cards": 0.10, "red_cards": 0.10,
    },

}

WEIGHTS_MIDFIELD["Centrocampo"] = WEIGHTS_MIDFIELD["Centrocampista"]
WEIGHTS_MIDFIELD["Ala sinistra"] = WEIGHTS_MIDFIELD["Ala destra"]

WEIGHTS_DEFENSIVE = {
    "Portiere": {
        "clean_sheet": 0.35, "gol_conceded": 0.30, "total_minutes": 0.25,
        "yellow_cards": 0.05, "red_cards": 0.05,
    },
    "Difensore centrale": {
        "gol": 0.15, "assist": 0.10, "total_minutes": 0.45,
        "yellow_cards": 0.10, "red_cards": 0.20,
    },
    # ... terzini da modificare
    "Terzino destro": {
        "gol": 0.15, "assist": 0.25, "total_minutes": 0.35,
        "yellow_cards": 0.10, "red_cards": 0.15,
    },
}

WEIGHTS_DEFENSIVE["Difesa"] = WEIGHTS_DEFENSIVE["Difensore centrale"]
WEIGHTS_DEFENSIVE["Terzino sinistro"] = WEIGHTS_DEFENSIVE["Terzino destro"]


# ─── PESI INTERNI CONTESTO DIFENSIVO ───────────────────────────
W_SOLIDITA = 0.40      # solidita' assoluta della squadra
W_SOVRAPERF = 0.60     # sovraperformance vs posizione attesa