import asyncio
import random
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# ─── CONFIGURAZIONE ────────────────────────────────────────────
GROUP_SLUG   = "serie-d-girone-"
GROUP_IDS     = ["A","B","C","D","E","F","G","H","I",]
DELAY_MIN   = 2.0
DELAY_MAX   = 4.0
OUTPUT_FILE = "seried_teams.json"
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

def save_progress(data: dict):
    """Salva i progressi su file dopo ogni giocatore."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─── BROWSER ───────────────────────────────────────────────────

async def get_html(page, url: str, wait_selector: str) -> str:
    await page.goto(url, wait_until="domcontentloaded", timeout=60000)

    await page.wait_for_selector(
        f"button.accept-all, {wait_selector}",
        timeout=30000
    )

    cookie_btn = page.locator("button.accept-all")
    if await cookie_btn.is_visible():
        await cookie_btn.click()
        print("    🍪 Cookie accettati")
        await page.wait_for_selector(wait_selector, timeout=30000)

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
        team_tag = row.find("a")
        if not team_tag:
            continue

        team_name = team_tag["title"]
        team_link = team_tag["href"].split("/")
        team_slug = team_link[1]
        team_id = team_link[4]

        teams.append({
            "name": team_name,
            "slug": team_slug,
            "id":   team_id,
            "scraped": False,
        })
    return teams

# ─── MAIN ───────────────────────────────────────────────────

async def main():
    # Initialize dictonary
    data = {}
    for group_id in GROUP_IDS:
        data[group_id] = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
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
            if not data[group_id]:
                group_url = (
                        f"https://www.transfermarkt.it/{GROUP_SLUG}{group_id.lower()}"
                        f"/startseite/wettbewerb/IT4{group_id}"
                    )
                html = await get_html(page, group_url, "table.items")
                data[group_id] = parse_groups(html)
                save_progress(data)


if __name__ == "__main__":
    asyncio.run(main())