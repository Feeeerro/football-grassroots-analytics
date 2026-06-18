import sqlite3
import json
import os
from schema import create_database

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # cartella di migrate.py
ROOT_DIR = os.path.dirname(BASE_DIR)                     # cartella superiore

DATA_DIR = os.path.join(ROOT_DIR, "data")
SQUADS_DIR = os.path.join(DATA_DIR, "squads")
DB_PATH = os.path.join(ROOT_DIR, "seried.db")

def migrate_teams(cursor, data):
    # Iterates data to retrive all teams
    for team_id, team_data in data.items():
        # INSERT IN teams (once for team_id)
        cursor.execute("""
            INSERT OR REPLACE INTO teams
            (team_id, name, slug)
            VALUES (?, ?, ?)
        """, (parse_int(team_id), 
              parse_text(team_data["names"][len(team_data["names"])-1]), 
              team_data["slug"])
        )
    
        # INSERT IN team_names (once for history name)
        for name in team_data["names"]:
            cursor.execute("""
                INSERT OR REPLACE INTO team_names
                (team_id, name)
                VALUES (?, ?)
            """, (parse_int(team_id), 
                  parse_text(name))
            )

def migrate_players(cursor, team, name_to_id):
    """ Iterates all the players """
    for player in team["squad"]:
        cursor.execute("""
        INSERT OR REPLACE INTO players
        (player_id, name, position, height, date_of_birth, age, feet, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (parse_int(player["player_id"]),
                parse_text(player["name"]),
                parse_text(player["position"]),
                parse_height(player["height"]),
                parse_text(player["date_of_birth"]),
                parse_int(player["age"]),
                parse_text(player["feet"]),
                parse_text(player["deadline"]))
    )
        
    for player_id, player_data in team["completed"].items():
        for season in player_data["stats"]: 
            team_id = None
            if "Serie D" in season["competition"]:
                team_id = name_to_id.get(season["team"])   
            cursor.execute("""
            INSERT INTO player_stats
            (player_id, team_id, season, competition, appearances, gol, assist, gol_conceded, clean_sheet, yellow_cards, double_yellow_cards, red_cards, total_minutes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (parse_int(player_id), 
                  parse_int(team_id), 
                  parse_text(season["season"]), 
                  parse_text(season["competition"]), 
                  parse_int(season["appearances"]), 
                  parse_int(season.get("gol")), 
                  parse_int(season.get("assist")),
                  parse_int(season.get("gol_conceded")), 
                  parse_int(season.get("clean_sheet")), 
                  parse_int(season["yellow_cards"]), 
                  parse_int(season["double_yellow_cards"]),
                  parse_int(season["red_cards"]), 
                  parse_minutes(season["total_minutes"]))
        )
            
def migrate_history(cursor, history):
    for group_id, seasons in history.items():
        for season, table in seasons.items():
            for team in table:
                cursor.execute("""
                INSERT INTO standings
                (team_id, season, group_id, position, matches, points, gol_scored, gol_conceded, gol_ratio, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (parse_int(team["id"]),
                        parse_text(season),
                        parse_text(group_id),
                        parse_int(team["position"]),
                        parse_int(team["matches"]),
                        parse_int(team["points"]),
                        parse_int(team["gol_scored"]),
                        parse_int(team["gol_conceded"]),
                        parse_int(team["gol_ratio"]),
                        parse_text(team["status"]))
            )
            
def parse_text(value):
    if not value or value == "-":
        return None
    return value

def parse_int(value):
    if not value or value == "-":
        return None
    return int(value)

def parse_height(value):
    if not value or value == "-":
        return None
    return int(value.replace(",", "").replace("m", ""))

def parse_minutes(value):
    if not value or value == "-":
        return None
    return int(value.rstrip("'"))
        
def main():
    create_database(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    """ Open JSON file with all teams to fill the table (teams) and (teams_name) """
    with open(os.path.join(DATA_DIR, "seried_teams_completed.json"), "r", encoding="utf-8") as f:
        teams = json.load(f)
    migrate_teams(cursor, teams)

    name_to_id = {
                name: team_id
                for team_id, team_data in teams.items()
                for name in team_data["names"]
    }
    
    """ Iterates all the squads file from data/squads """
    for filename in os.listdir(SQUADS_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(SQUADS_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                team = json.load(f)
            migrate_players(cursor, team, name_to_id)

    """ Open JSON file with the seried history """
    with open(os.path.join(DATA_DIR, "seried_history.json"), "r", encoding="utf-8") as f:
        history = json.load(f)
    migrate_history(cursor, history)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()