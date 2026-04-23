# ============================================================
# File: phase2_validation/tools_atomic/competitor_scraper.py
# REAL TOOL - scrape homepage metadata
# ============================================================

from typing import Dict, Any
from langchain.tools import tool
from bs4 import BeautifulSoup

from ..atomic.base_http import SESSION


@tool("competitor_scraper_tool")
def competitor_scraper_tool(url: str) -> Dict[str, Any]:
    """
    Input:
        https://typeform.com

    Returns:
        metadata + page summary
    """

    try:
        r = SESSION.get(url, timeout=8)
        html = r.text[:300000]

        soup = BeautifulSoup(html, "html.parser")

        title = soup.title.text.strip() if soup.title else ""

        desc = ""
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            desc = meta.get("content", "")

        headings = [
            h.get_text(" ", strip=True)
            for h in soup.find_all(["h1", "h2"])[:10]
        ]

        links = [
            a.get("href")
            for a in soup.find_all("a", href=True)
        ]

        pricing_links = [
            x for x in links
            if "pricing" in x.lower()
        ][:5]

        return {
            "url": url,
            "title": title,
            "description": desc,
            "headings": headings,
            "pricing_links": pricing_links
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }