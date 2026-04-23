# ============================================================
# File: phase3_market_research/tools/scrape_tool.py
# Atomic Web Scraper
# ============================================================

import requests
from bs4 import BeautifulSoup
from langchain.tools import tool


@tool
def scrape_page(url: str) -> str:
    """
    Scrape visible text content from webpage.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        html = requests.get(url, headers=headers, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:6000]

    except Exception as e:
        return f"ERROR: {str(e)}"