from duckduckgo_search import DDGS
from ...config import settings


def search_web(query: str, max_results: int = None):
    max_results = max_results or settings.SEARCH_RESULTS_LIMIT
    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r.get("title", ""),
                "url": r.get("href", ""),
                "snippet": r.get("body", "")
            })

    return results