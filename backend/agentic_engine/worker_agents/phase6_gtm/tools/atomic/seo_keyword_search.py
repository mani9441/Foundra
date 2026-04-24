# ============================================================
# File: phase6_gtm/tools/atomic/seo_keyword_search.py
# Search keyword opportunities
# ============================================================

from .web_search import web_search


def seo_keyword_search(topic: str, max_results: int = 10):

    query = f"{topic} best tools alternatives guide how to"

    return web_search(query=query, max_results=max_results)