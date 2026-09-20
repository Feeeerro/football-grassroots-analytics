import asyncio
import random
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# ─── CONFIGURAZIONE ────────────────────────────────────────────
GROUP_SLUG    = "serie-d-girone-"
GROUP_IDS     = ["A","B","C","D","E","F","G","H","I",]
SEASONS       = ["14/15","15/16","16/17","17/18","18/19","19/20","20/21","21/22","22/23","23/24","24/25","25/26",]
DELAY_MIN     = 2.0
DELAY_MAX     = 4.0
OUTPUT_FILE   = "seried_history.json"
# ───────────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}

# ─── SALVATAGGIO / CARICAMENTO PROGRESSIVO ─────────────────────

def load_progress(output_file) -> dict:
    """Load progress save, if exist."""
    data = {}
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"📂 Progress found: restart from the latest progress.")
        return data
    else:
        for group_id in GROUP_IDS:
            data[group_id] = {}
            for season in SEASONS:
                data[group_id][season] = None
        return data

def save_progress(data: dict):
    """Save the progress after each season."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── BROWSER ───────────────────────────────────────────────────

async def get_html(page, url: str, wait_selector: str) -> str:
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)

    await page.wait_for_selector(
        f"button.accept-all, {wait_selector}",
        timeout=6000
    )

    cookie_btn = page.locator("button.accept-all")
    if await cookie_btn.is_visible():
        await cookie_btn.click()
        print("    🍪 Cookie accettati")
        await page.wait_for_selector(wait_selector, timeout=6000)

    return await page.content()

# ─── PARSE ROSA ────────────────────────────────────────────────

def parse_groups(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", class_="items")
    if not table:
        print("⚠️  Tabella squadre non trovata.")
        return []
    
    teams = []
    for row in table.find("tbody").find_all("tr", recursive=False):
        cells = row.find_all(
            ["td"]
        )

        if len(cells) < 10:
            continue

        def val(idx):
            return cells[idx].get_text(strip=True) or "-"
        
        def val_img_title(idx):
            img = cells[idx].find("a")
            return img.get("title", "-") if img else "-"
        
        def val_anchor_link(idx):
            anchor = cells[idx].find("a")
            return anchor.get("href", "-") if anchor else "-"
        
        def val_status(idx):
            status = cells[idx].get("style", None)
            return status.split(":")[1].strip() if status else None
        

        teams.append({
            "name":             val_img_title(1),
            "slug":             val_anchor_link(1).split("/")[1],
            "id":               val_anchor_link(1).split("/")[4],
            "position":         val(0),
            "matches":          val(3),
            "win":              val(4),
            "draw":             val(5),
            "lose":             val(6),
            "gol_scored":       val(7).split(":")[0],
            "gol_concede":      val(7).split(":")[1],
            "gol_ratio":        val(8),
            "points":           val(9),
            "status":           val_status(0),
        })

    return teams

def set_status(table):
    num_teams = len(table)
    if table[0]["status"] is not None:
        for team in table:
                match team["status"]:
                    case "#afd179":
                        team["status"] = "Promoted"
                    case "#c3dc9a":
                        team["status"] = "Playoff"
                    case "#f8cfcd":
                        team["status"] = "Playout"
                    case "#f8a7a3":
                        team["status"] = "Relegated"
                    case None:
                        team["status"] = "Saved"
    else:            
        table[0]["status"] = "Promoted"

        for i in range(1, 5):
            table[i]["status"] = "Playoff"

        for i in range(num_teams-2, num_teams):
            table[i]["status"] = "Relegated"

        for i in range(num_teams-6, num_teams-2):
            table[i]["status"] = "Playout"

        if int(table[num_teams-6]["points"]) - int(table[num_teams-3]["points"]) > 7:
            table[num_teams-6]["status"] = "Saved"
            table[num_teams-3]["status"] = "Relegated"

        if int(table[num_teams-5]["points"]) - int(table[num_teams-4]["points"]) > 7:
            table[num_teams-5]["status"] = "Saved"
            table[num_teams-4]["status"] = "Relegated"

# ─── MAIN ───────────────────────────────────────────────────

async def main():
    # Initialize dictionary
    data = load_progress(OUTPUT_FILE)

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
            "**/*.{png,jpg,jpeg,gif,webp,svg,woff,woff2,ttf}",
            lambda route: route.abort(),
        )
        for group_id in GROUP_IDS:
            for season in SEASONS:
                if data[group_id][season] is None:
                    year = f"20{season.split('/')[0]}"
                    group_url = (
                            f"https://www.transfermarkt.it/{GROUP_SLUG}{group_id.lower()}"
                            f"/tabelle/wettbewerb/IT4{group_id}?saison_id={year}"
                        )
                    try:
                        html = await get_html(page, group_url, "table.items")
                        data[group_id][season] = parse_groups(html)
                        if data[group_id][season]:
                            set_status(data[group_id][season])
                    except Exception as e:
                        print(f"⚠️ {group_id} {season}: {e}")
                        data[group_id][season] = []
                    save_progress(data)

if __name__ == "__main__":
    asyncio.run(main())