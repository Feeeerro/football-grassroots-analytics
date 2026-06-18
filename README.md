# Serie D Scraper & Database

A complete pipeline for collecting, cleaning, and structuring historical data
on Italian Serie D football — squads, player statistics, and historical
standings across all 9 groups — sourced from Transfermarkt, with the goal of
building a relational database ready for statistical analysis and player
evaluation models.

## Why this project

There is no publicly organized database with historical Serie D data
(squads, per-season statistics, standings). This project builds that
dataset from scratch through web scraping, with the end goal of developing
a 0-100 scoring model for player evaluation, contextualized by team
strength, competition level, and performance trend over time.

## What the pipeline does

1. **Squad and player statistics scraping** — for each of the 162 teams
   across the 9 Serie D groups, collects the current squad (personal info,
   role, date of birth, height, preferred foot) and historical statistics
   per season and competition (appearances, goals, assists, cards, minutes
   played).
2. **Historical standings scraping** — for each group and season (from
   2014/15 onward), collects the full standings table along with the
   end-of-season outcome (promotion, playoff, playout, relegation), derived
   from Transfermarkt's official color coding or, when unavailable,
   calculated by applying the "forbice" rule typical of Serie D.
3. **Data cleaning** — normalizes and filters out seasons prior to 2014/15
   to ensure consistency between the player and standings datasets.
4. **Team lookup construction** — unifies historical team names (which
   frequently change over the years) under a single stable ID, enabling the
   link between player statistics and team context.
5. **Migration to a relational database (SQLite)** — consolidates all data
   into a single database with a relational schema, ready for analytical
   queries or to serve as the foundation for a Machine Learning model.

## Tech stack

- **Python 3**
- **Playwright** (async) — browser automation for rendering Transfermarkt's
  JavaScript-driven pages
- **BeautifulSoup4** — HTML parsing
- **SQLite3** — relational data persistence

## Database structure

| Table          | Content                                                                      |
| -------------- | ---------------------------------------------------------------------------- |
| `teams`        | Team registry (ID, name, slug)                                               |
| `team_names`   | All historical names associated with each team                               |
| `players`      | Player registry (name, role, date of birth, height, foot, contract deadline) |
| `player_stats` | Per-player statistics by season and competition                              |
| `standings`    | Historical standings by group and season, with final outcome                 |

## Project structure

```
.
├── seried_player_scraper.py      # Squad and player statistics scraping
├── exctract_team.py              # Historical standings scraping
├── exctract_team_completed.py    # Unified team lookup construction
├── exctract_team_history.py      # Team history support utility
├── clean_players.py              # Cleanup of pre-2014/15 seasons
├── database/
│   ├── schema.py                 # SQLite schema definition
│   └── migrate.py                # JSON → SQLite migration
└── data/                         # Intermediate JSON output (not versioned)
```

## Technical notes

- The scraper robustly handles rate limiting, lazy-loaded statistics tables,
  and temporary IP blocks, with a resume mechanism to pick up where it left
  off without losing progress.
- Numeric data is normalized and converted (e.g. height from `"1,86m"` to
  `186`, minutes from `"2970'"` to `2970`), with explicit handling of
  missing values.
- Teams whose name has changed over the years are mapped to a single stable
  ID through a lookup system built from historical standings.

## Next steps

- A 0-100 player scoring model based on role-weighted statistics,
  contextualized by team strength and competition level, with a temporal
  decay factor favoring more recent seasons.

## Author

Personal project developed to deepen skills in web scraping, data
management, and relational database design in a sports analytics context.
