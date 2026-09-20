"""Funzioni di normalizzazione, condivise da tutti i ruoli."""

def build_benchmark(players, param):
    """Distribuzione storica di un parametro, None esclusi."""
    return [
        s[param]
        for seasons in players.values()
        for s in seasons
        if s[param] is not None
    ]

def pct(x, benchmark):
    """Percentile di x nel benchmark storico. Ritorna 0-1.
    None -> 0.0, cosi' i dati mancanti non gonfiano il punteggio."""
    if x is None or not benchmark:
        return 0.0
    return sum(1 for v in benchmark if v <= x) / len(benchmark)


def neg_norm(x, benchmark):
    """Per parametri dove basso = buono (cartellini). Percentile invertito."""
    return 1.0 - pct(x, benchmark)


def map_red(rc):
    """Rossi: distribuzione degenere (quasi tutti 0), mappatura diretta."""
    if rc is None or rc == 0:
        return 1.0
    if rc == 1:
        return 0.5
    return 0.0