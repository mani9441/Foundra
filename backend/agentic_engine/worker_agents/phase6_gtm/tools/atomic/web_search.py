# ============================================================
# File: phase6_gtm/tools/atomic/web_search.py
# Free web search using DuckDuckGo
# pip install duckduckgo_search
# ============================================================

from duckduckgo_search import DDGS


def web_search(query: str, max_results: int = 5):
    """
    Returns list of search results:
    [
        {
            title,
            snippet,
            url
        }
    ]
    """

    output = []

    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)

        for r in results:
            output.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("href", "")
            })

    return output