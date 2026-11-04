#!/usr/bin/env python3
"""
apple_stock.py
Scrapes Apple (AAPL) historical stock prices from Yahoo Finance.
URL: https://finance.yahoo.com/quote/AAPL/history?p=AAPL
"""

import sys
import requests
from bs4 import BeautifulSoup

URL = "https://finance.yahoo.com/quote/AAPL/history?p=AAPL"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
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
        print("Could not find historical data table on page.", file=sys.stderr)
        return

    tbody = table.find("tbody")
    rows = tbody.find_all("tr") if tbody else table.find_all("tr")[1:]

    print(f"{'Date':<16} {'Close Price':<12}")
    print("-" * 28)

    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all("td")]
        # Typical historical row: Date, Open, High, Low, Close, Adj Close, Volume
        # Skip dividend/split rows which contain fewer standard columns
        if len(cols) >= 5:
            date = cols[0]
            close_price = cols[4]
            print(f"{date:<16} {close_price:<12}")

if __name__ == "__main__":
    main()
