# ============================================================
# File: phase3_market_research/tools/search_tool.py
# Atomic Search Tool
# ============================================================

from langchain.tools import tool
from duckduckgo_search import DDGS


@tool
def web_search(query: str) -> list:
    """
    Search public web for market research data.
    """
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=5):
            results.append({
                "title": r.get("title"),
                "link": r.get("href"),
                "snippet": r.get("body")
            })

    return results