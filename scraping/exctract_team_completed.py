import json

def main():
    with open("seried_history.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    lookup = {}
    for _, seasons in data.items():
        for _, table in seasons.items():
            if table:
                for team in table:
                    if team["id"] not in lookup:
                        lookup[team["id"]] = {"names": [team["name"]], "slug": team["slug"]}
                    elif team["name"] not in lookup[team["id"]]["names"]:
                        lookup[team["id"]]["names"].append(team["name"])

    with open ("seried_teams_completed.json", "w", encoding="utf-8") as f:
                json.dump(lookup, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()