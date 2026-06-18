import asyncio
import random
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# ─── CONFIGURATION ────────────────────────────────────────────
SEASON      = 2025
DELAY_MIN   = 1.0
DELAY_MAX   = 2.5
# ───────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}


# ─── SAVE / LOAD PROGRESSIVE ─────────────────────

def load_progress(output_file) -> dict:
    """Load progress save, if exist."""
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"📂 Progress found: {len(data['completed'])} players already completed")
        return data
    return {"completed": {}, "squad": []}


def save_progress(data: dict, output_file):
    """Save progress to file after each player."""
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ─── BROWSER ───────────────────────────────────────────────────

async def get_html(page, url: str, wait_selector: str) -> str:
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)

    await page.evaluate("window.scrollBy(0, 600)")

    await page.wait_for_selector(
        f"button.accept-all, {wait_selector}",
        timeout=30000
    )

    cookie_btn = page.locator("button.accept-all")
    if await cookie_btn.is_visible():
        await cookie_btn.click()
        print("    🍪 Cookies accepted")
        await page.wait_for_selector(wait_selector, timeout=30000)

    return await page.content()


# ─── PARSE SQAUD ────────────────────────────────────────────────

def parse_squad(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="items")
    if not table:
        print("⚠️  Squad table not found.")
        return []

    players = []
    for row in table.find("tbody").find_all("tr", recursive=False):
        number_tag = row.find("div", class_="rn_nummer")
        if not number_tag:
            continue

        inline = row.find("table", class_="inline-table")
        if not inline:
            continue

        inline_rows = inline.find_all("tr")

        name, player_href = "-", None
        name_td = inline_rows[0].find("td", class_="hauptlink") if inline_rows else None
        if name_td:
            a = name_td.find("a")
            if a:
                name = a.get_text(strip=True)
                player_href = a.get("href", "")

        position = "-"
        if len(inline_rows) > 1:
            position_td = inline_rows[1].find("td")
            if position_td:
                position = position_td.get_text(strip=True)
        
        tds = row.find_all("td", recursive=False)
        def val(idx):
            if idx >= len(tds):
                return "-"
            text = tds[idx].get_text(strip=True)
            return text if text else "-"
        
        data_birth = val(2).split(" (")[0]
        age = val(2).split(" (")[1].rstrip(")")
        height = val(4) or '-'
        feet = val(5) or '-'
        deadline = val(8) or '-'

        player_slug, player_id = None, None
        if player_href:
            parts = player_href.strip("/").split("/")
            if len(parts) >= 4:
                player_slug = parts[0]
                player_id   = parts[3]

        players.append({
            "number":             number_tag.get_text(strip=True),
            "name":               name,
            "position":           position,
            "height":             height,
            "date_of_birth":      data_birth,
            "age":                age,
            "feet":               feet,
            "deadline":           deadline,
            "player_slug":        player_slug,
            "player_id":          player_id,
        })

    return players


# ─── PARSE STATS ─────────────────────────────────────────

def parse_stats(html: str, player) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    rows = soup.find_all("div", role="row", attrs={"aria-rowindex": True})

    stats = []

    for row in rows:
        cells = row.find_all(
            ["div", "a"],
            class_=lambda c: c and ("tm-grid__cell" in c or "grid__cell" in c)
        )

        if len(cells) < 10:
            continue

        def val(idx):
            return cells[idx].get_text(strip=True) or "-"
        
        def val_img_title(idx):
            img = cells[idx].find("img")
            return img.get("title", "-") if img else "-"
        
        if player['position'] == "Portiere":
            stats.append({
                "season":                 val(0),
                "competition":            val(1),
                "team":                   val_img_title(2),
                "appearances":            val(3),
                "gol_conceded":           val(4),
                "clean_sheet":            val(5),
                "yellow_cards":           val(6),
                "double_yellow_cards":    val(7),
                "red_cards":              val(8),   
                "total_minutes":          val(9),
            })
        else:
            stats.append({
                "season":                 val(0),
                "competition":            val(1),
                "team":                   val_img_title(2),
                "appearances":            val(3),
                "gol":                    val(4),
                "assist":                 val(5),
                "yellow_cards":           val(6),
                "double_yellow_cards":    val(7),
                "red_cards":              val(8),
                "total_minutes":          val(9),
            })

    return stats

# ─── SCRAPE TEAM MODULE ──────────────────────────────────────────────────────

async def scrape_team(page, slug, team_id):

    # load existing progress
    os.makedirs("data/squads", exist_ok=True)
    data = load_progress(f"data/squads/{slug}.json")

    # ── Step 1: team (only if already saved) ─────────────
    if not data["squad"]:
        squad_url = (
            f"https://www.transfermarkt.it/{slug}"
            f"/kader/verein/{team_id}/saison_id/{SEASON}/plus/1"
        )
        print(f"🔍 Team: {squad_url}")
        html = await get_html(page, squad_url, "table.items")
        data["squad"] = parse_squad(html)
        save_progress(data, f"data/squads/{slug}.json")
        print(f"   → {len(data['squad'])} players found\n")
    else:
        print(f"   → Squad already saved: {len(data['squad'])} players\n")

    # ── Step 2: stats — skip already completed ───────
    todo = [
        p for p in data["squad"]
        if p["player_id"] and p["player_id"] not in data["completed"]
    ]
    print(f"⏳ Players to complete: {len(todo)}/{len(data['squad'])}\n")

    for i, player in enumerate(todo):

        stats_url = (
            f"https://www.transfermarkt.it/{player['player_slug']}"
            f"/leistungsdatendetails/spieler/{player['player_id']}/plus/0"
        )
        print(f"  [{i+1}/{len(todo)}] {player['name']:<28} → {stats_url}")

        html = await get_html(
            page,
            stats_url,
            "tm-player-performance-table-new .grid-row"
        )
        stats = parse_stats(html, player)
        data["completed"][player["player_id"]] = {
            "name":  player["name"],
            "stats": stats,
        }
        save_progress(data, f"data/squads/{slug}.json")
        print(f"    ✅ {len(stats)} stat rows saved")

        

        delay = random.uniform(DELAY_MIN, DELAY_MAX)
        print(f"    ⏳ Waiting {delay:.1f}s...")
        await asyncio.sleep(delay)

    

    # ── Step 3: print results completed ──────────────────────
    completed = len(data["completed"])
    total     = len(data["squad"])
    print(f"\n✅ Completed {completed}/{total} players")

    if completed != total:
        print(f"ℹ️  Restart the script to complete the {total - completed} remaining.")

# ─── MAIN ──────────────────────────────────────────────────────

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            user_agent=HEADERS["User-Agent"],
            locale="it-IT",
            extra_http_headers={"Accept-Language": HEADERS["Accept-Language"]},
            viewport={"width": 1280, "height": 800},
        )
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            window.chrome = { runtime: {} };
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3] });
            Object.defineProperty(navigator, 'languages', { get: () => ['it-IT', 'it', 'en'] });
        """)

        page = await context.new_page()
        await page.route(
            "**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,ttf,css}",
            lambda route: route.abort(),
        )
        try:
            with open("seried_teams.json", "r", encoding="utf-8") as f:
                teams = json.load(f)
            for group, squads in teams.items():
                for team in squads:
                    if team["scraped"] == False:
                        await scrape_team(page, team["slug"], team["id"])
                        team["scraped"] = True
                        with open("seried_teams.json", "w", encoding="utf-8") as f:
                            json.dump(teams, f, ensure_ascii=False, indent=2)
                    else:
                        print(f"{team['name']} already scraped")
        except Exception as e:
            print(f"    ⚠️  Error: {e}")
            print(f"    💾 Progress saved. Start again the app in a few minutes.")
            await browser.close()
            return  # exit but progess saved.
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())