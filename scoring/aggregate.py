from config import (
    LAMBDA_QUALITA, LAMBDA_TEMPO, VOLUME_CAP,
    CATEGORY_MULT, DEFAULT_MULT
)

def player_asi(seasons, score_fn):
    """Aggrega le stagioni di un giocatore in un ASI (pre-normalizzazione).

    score_fn e' una closure che prende SOLO la stagione e restituisce il
    punteggio grezzo 0-1: tutti i benchmark sono gia' catturati al suo interno.
    Cosi' player_asi resta agnostica rispetto alla famiglia (off/dif).
    """
    anno_recente = anno_di(seasons[0]["season"])

    dati = []
    minuti_totali = 0
    for s in seasons:
        grezzo = score_fn(s)                                  # un solo argomento
        finale = grezzo * league_mult(s["competition"]) * 100
        eta = anno_recente - anno_di(s["season"])
        dati.append((finale, eta))
        minuti_totali += s["total_minutes"] or 0

    dati.sort(key=lambda x: x[0], reverse=True)

    num, den = 0.0, 0.0
    for i, (finale, eta) in enumerate(dati):
        w = (LAMBDA_QUALITA ** i) * (LAMBDA_TEMPO ** eta)
        num += finale * w
        den += w

    volume_fact = min(1.0, minuti_totali / VOLUME_CAP)
    return (num / den) * volume_fact if den else 0.0

def league_mult(competition):
    if not competition:
        return DEFAULT_MULT
    for chiave, mult in CATEGORY_MULT.items():
        if competition.startswith(chiave):
            return mult
    return DEFAULT_MULT

def anno_di(season_str):
    """'24/25' -> 2024. Robusto ai buchi tra stagioni."""
    return 2000 + int(season_str.split("/")[0])