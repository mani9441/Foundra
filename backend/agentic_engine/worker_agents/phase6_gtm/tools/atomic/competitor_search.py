# ============================================================
# File: phase6_gtm/tools/atomic/competitor_search.py
# Search competitors for niche
# ============================================================

from .web_search import web_search


def competitor_search(niche: str, max_results: int = 8):
    """
    Example:
    niche = ai email automation
    """

    query = f"best {niche} software competitors alternatives startups"

    return web_search(query=query, max_results=max_results)