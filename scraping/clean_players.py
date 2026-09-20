import json
import os
    
def main():
    """ Iterates all the squads file from data/squads """
    for filename in os.listdir("data/squads"):
        if filename.endswith(".json"):
            filepath = os.path.join("data/squads", filename)
            slug = filepath.split("/")[1]
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            """ Iterates all the season to delete those before 14/15 """
            total_season_deleted = 0
            for _, player_data in data["completed"].items():
                stats = player_data["stats"]
                updated_stats = []
                count = 0
                for season in stats:
                    if season["season"] != "-":
                        year = int(season["season"].split("/")[0])
                    if year >= 14:
                        updated_stats.append(season)
                    else:
                        count += 1
                total_season_deleted += count
                player_data["stats"] = updated_stats
            print(f"Total season deleted {slug}: {total_season_deleted}")

            with open (filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        

if __name__ == "__main__":
    main()