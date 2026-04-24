# ============================================================
# File: phase5_product_strategy/tools/atomic/web_search_tool.py
# Free Web Search Tool (DuckDuckGo)
# ============================================================

from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        return results
    except Exception as e:
        return [{"error": str(e)}]