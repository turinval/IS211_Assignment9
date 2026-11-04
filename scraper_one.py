#!/usr/bin/env python3
"""
football_stats.py
Scrapes top 20 NFL touchdown leaders from CBS Sports.
URL: https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/
"""

import sys
import requests
from bs4 import BeautifulSoup

URL = "https://www.cbssports.com/nfl/stats/player/scoring/nfl/regular/all/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

def main():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching page: {e}", file=sys.stderr)
        return

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    if not table:
        print("Could not find stats table on page.", file=sys.stderr)
        return

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

    print(f"{'Rank':<5} {'Player':<25} {'Pos':<6} {'Team':<6} {'Touchdowns':<10}")
    print("-" * 55)

    count = 0
    for row in rows:
        if count >= 20:
            break

        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        if not cols or len(cols) < 7:
            continue

        # Column structure on CBS scoring leaders:
        # Col 0: Player name, Pos, Team (often grouped or formatted with sub-elements)
        player_cell = row.find("span", class_="CellPlayerName--long")
        if player_cell:
            player_name = player_cell.get_text(strip=True)
            pos_cell = row.find("span", class_="CellPlayerName-position")
            team_cell = row.find("span", class_="CellPlayerName-team")
            position = pos_cell.get_text(strip=True) if pos_cell else "N/A"
            team = team_cell.get_text(strip=True) if team_cell else "N/A"
        else:
            player_name = cols[0]
            position = cols[1] if len(cols) > 1 else "N/A"
            team = cols[2] if len(cols) > 2 else "N/A"

        # CBS Scoring table layout:
        # TDs is column index 6 in standard CBS scoring tables (Rank, Player, G, PTS, FGM, XPM, TD)
        touchdowns = cols[6] if len(cols) > 6 else cols[-1]

        count += 1
        print(f"{count:<5} {player_name:<25} {position:<6} {team:<6} {touchdowns:<10}")

if __name__ == "__main__":
    main()
