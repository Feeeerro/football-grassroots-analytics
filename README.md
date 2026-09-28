# Football Grassroots Analytics

### A data-driven player scoring system for Italian lower-league football scouting

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

ASI is an end-to-end system that scrapes, structures, and analyzes historical
football data from Italy's Serie D to produce a role-specific player rating
(0–100). It builds a relational dataset that does not exist publicly, and on
top of it computes a scoring model that evaluates players in context — weighing
their statistics against the strength of their team and the level of their
competition. The goal is a scouting tool for a level of football that
professional data platforms largely ignore, because the granular event data
they rely on simply isn't available there.

## Motivation

Professional scouting increasingly runs on data, but that data stops at the
higher tiers. For Serie D — the fourth level of Italian football — there is no
organized, queryable dataset of squads, per-season player statistics, and
historical standings. Scouting at this level is still almost entirely manual.

This project starts from that gap. It builds the missing dataset from scratch
through web scraping, then designs a scoring model that works _precisely where
rich data is absent_: instead of shot-level or tracking data, it extracts
signal from what is available — aggregate seasonal statistics — and makes them
meaningful by placing them in context. The result is not a replacement for the
scout's eye, but a filter: a way to turn thousands of players into a shortlist
worth watching.

## Features

- **Resilient web scraping** of squads, player statistics, and historical
  standings, with anti-bot handling, lazy-load management, and a
  checkpoint/resume mechanism that recovers from interruptions without data loss.
- **Relational database** (SQLite) with a normalized schema and a migration
  layer that converts raw JSON into typed, validated records.
- **Entity resolution** that unifies historical team names — which change
  frequently over the years — under stable identifiers, enabling reliable joins
  between player statistics and team performance.
- **Role-specific scoring model** applying percentile normalization, shrinkage
  (regression to the mean), team-context adjustment, and time-weighted
  aggregation to produce a 0–100 rating per player.

## Architecture

The system is a linear pipeline with clearly separated stages, each producing
the input for the next:

```
Scraping  →  Raw JSON  →  Migration  →  SQLite database  →  Scoring  →  Player ratings
```

Each stage is independent and communicates through well-defined boundaries: the
scrapers produce JSON, the migration layer turns it into relational tables, and
the scoring engine reads those tables and writes ratings. This separation means
any stage can be re-run or replaced without touching the others — and it leaves
a clean insertion point for a future user interface, which would read
pre-computed ratings without re-running the model.

## Tech Stack

- **Python 3.10+**
- **Playwright** (async) — browser automation for rendering JavaScript-driven
  pages
- **BeautifulSoup4** — HTML parsing
- **SQLite3** — relational data persistence

## Data

All data is collected from [Transfermarkt](https://www.transfermarkt.it),
scraped and structured specifically for this project. Collection is limited to
seasons from 2014/15 onward, the point from which the standings data is
complete and consistent across all nine Serie D groups. Three distinct datasets
are gathered:

**Squads and player biographical data** — for each of the 162 Serie D teams,
the current squad is collected with each player's name, role, date of birth,
height, preferred foot, and contract expiry.

**Player statistics** — for every player, the full per-season, per-competition
statistical history: appearances, goals, assists, yellow and red cards, and
minutes played (plus clean sheets and goals conceded for goalkeepers). Crucially,
each statistical row also records the team the player represented that season,
which is what allows individual performance to be tied to team context.

**Historical standings** — for each group and season, the complete final league
table: position, matches played, points, goals scored and conceded, and the
end-of-season outcome (promotion, playoff, playout, relegation). This is the
source of the team context that the scoring model relies on — a player's output
is only meaningful once placed against how strong their team actually was.

A dedicated resolution step reconciles the fact that clubs frequently change
their registered name over the years: all historical names of a club are mapped
to a single stable identifier, so that a player's statistics can be reliably
joined to the correct team across seasons.

## Project Structure

```
.
├── config.py                 # Central configuration: paths and model parameters
├── scraping/                 # Data acquisition
│   ├── players_scraper.py    # Squads and player statistics
│   └── standings_scraper.py  # Historical league tables
├── database/                 # Persistence layer
│   ├── schema.py             # Table definitions
│   ├── migrate.py            # JSON → SQLite migration
│   └── queries.py            # Reusable data-access queries
├── scoring/                  # The ASI model
│   ├── normalize.py          # Percentile normalization, benchmarks
│   ├── aggregate.py          # Season aggregation, temporal weighting
│   ├── offensive_scoring.py  # Attacker scoring
│   ├── defensive_scoring.py  # Defender and goalkeeper scoring
│   └── midfield_scoring.py   # Midfielder scoring (offensive/defensive blend)
└── data/                     # Generated artifacts (not versioned)
```

## The Scoring Model (ASI)

The model evaluates every player independently within their role, on a 0–100
scale. It is a rule-based ranking system: the weights encode football
reasoning rather than being learned from labeled data. Each player's rating is
built in two stages — first a score for each individual season, then a
time-weighted aggregation of those seasons into a single value.

### Normalization

Raw statistics live on incompatible scales (minutes range in the thousands,
goals in the tens, cards in single digits). To make them comparable, every
statistic is converted to a **percentile** against a historical benchmark for
that role: "how does this value compare to every value ever recorded by players
in this position?" Percentile normalization is used instead of min-max scaling
because it is robust to outliers — a single anomalous season cannot distort the
scale for everyone else.

### Team Context

A raw statistic means little without context. Twelve goals for a title-winning
side is not the same as twelve goals for a relegated one. The model adjusts for
this in two directions:

- **Offensive context** measures a player's share of their team's goal output,
  corrected with shrinkage so that shares computed on very few team goals are
  pulled toward the role average and not trusted blindly.
- **Defensive context** combines a team's absolute solidity (how few goals it
  concedes) with its _overperformance_ — how much better its defense did than
  expected given its final league position. This isolates defensive merit from
  overall team strength, surfacing solid defenses in otherwise modest teams.

### Role-Specific Scoring

Each role is scored with the parameters and weights that matter for it.
Attackers are driven by goals and assists; goalkeepers by clean sheets and
goals conceded per game (shrinkage-corrected for low appearances); outfield
defenders — who lack individual defensive statistics in the available data — by
minutes played, refined by their team's defensive context. Midfielders combine
an offensive block (goals, assists) and a defensive block (contextualized
minutes) in a balanced blend, reflecting the dual nature of the role.

### Score Aggregation

Seasonal scores are combined into a single rating through a weighted average
that (a) gives more weight to a player's stronger seasons, (b) applies a gentle
temporal decay so recent form counts slightly more, and (c) scales the result
by a volume factor based on total career minutes — so a player with one strong
season is not ranked above one who has sustained that level over several. A
final normalization keeps ratings within the 0–100 range.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- The Playwright browser binaries (`playwright install`)

### Usage

The dataset is not included in the repository (see _Data Pipeline_ below), so
it must be generated first. Once the database is built, ratings for a role are
computed with, for example:

```bash
python -m scoring.offensive_scoring     # attackers
python -m scoring.defensive_scoring     # defenders and goalkeepers
python -m scoring.midfield_scoring      # midfielders
```

## Data Pipeline

Because the generated data (raw JSON and the SQLite database) is large and
fully reproducible, it is not versioned. To build it from scratch, run the
stages in order:

1. **Scraping** — collect squads, player statistics, and historical standings.
2. **Cleaning** — normalize formats and restrict the dataset to seasons from
   2014/15 onward for consistency.
3. **Migration** — load the cleaned JSON into the SQLite database.
4. **Scoring** — compute player ratings per role.

## Limitations

The model is designed around the data that exists for this level of football,
and it is important to be explicit about what that implies:

- **No event-level data.** There are no shots, passes, tackles, or tracking
  data at this level. The model works with aggregate seasonal statistics, which
  bounds how fine-grained its judgments can be.
- **Defenders are the hardest case.** Outfield defenders have no individual
  defensive statistics in the source data, so their rating leans heavily on
  team context. The model can indicate that a defender was a reliable presence
  in a solid unit, but it cannot isolate individual defensive skill.
- **It is a filter, not a verdict.** The rating is best used to narrow a large
  pool to a shortlist, not to deliver a final judgment on a player. Its value is
  in surfacing candidates worth watching, especially ones a human scout might
  miss across thousands of players.

## Roadmap

- **Aging curves** to weight ratings by a player's career stage, distinguishing
  established value from future potential.
- **Serie C integration** to extend team context to the third tier.
- **A user interface** for filtering and browsing pre-computed ratings.

## License

This project is released under the MIT License.

## Author

Personal project built to explore web scraping, data engineering, and applied
statistical modeling in a sports analytics context.
