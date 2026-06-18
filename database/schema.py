import sqlite3

def create_database(dbpath):
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()

    # Create tables
    players = """
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            name TEXT,
            position TEXT,
            height INTEGER,
            date_of_birth TEXT,
            age INTEGER,
            feet TEXT,
            deadline TEXT
        );
    """
    cursor.execute(players)
    teams = """
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            name TEXT,
            slug TEXT
        );
    """
    cursor.execute(teams)
    team_names = """
        CREATE TABLE IF NOT EXISTS team_names (
            team_id INTEGER,
            name TEXT,
            PRIMARY KEY (team_id, name),
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        );
    """
    cursor.execute(team_names)
    stats = """
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_id INTEGER,
            team_id INTEGER,
            season TEXT,
            competition TEXT,
            appearances INTEGER,
            gol INTEGER,
            assist INTEGER,
            gol_conceded INTEGER,
            clean_sheet INTEGER,
            yellow_cards INTEGER,
            double_yellow_cards INTEGER,
            red_cards INTEGER,
            total_minutes INTEGER,
            FOREIGN KEY (player_id) REFERENCES players(player_id),
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        );
    """
    cursor.execute(stats)
    standings = """
        CREATE TABLE IF NOT EXISTS standings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER,
            season TEXT,
            group_id TEXT,
            position INTEGER,
            matches INTEGER,
            points INTEGER,
            gol_scored INTEGER,
            gol_conceded INTEGER,
            gol_ratio INTEGER,
            status TEXT,
            FOREIGN KEY (team_id) REFERENCES teams(team_id)
        );
    """
    cursor.execute(standings)
    
    conn.commit()
    conn.close()