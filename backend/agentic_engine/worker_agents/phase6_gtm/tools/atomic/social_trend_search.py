# ============================================================
# File: phase6_gtm/tools/atomic/social_trend_search.py
# Search user pain points on forums/social sites
# ============================================================

from .web_search import web_search


def social_trend_search(topic: str, max_results: int = 8):

    query = f"{topic} problems reddit OR quora OR community OR forum"

    return web_search(query=query, max_results=max_results)