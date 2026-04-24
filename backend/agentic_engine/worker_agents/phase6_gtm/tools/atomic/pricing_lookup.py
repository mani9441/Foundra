# ============================================================
# File: phase6_gtm/tools/atomic/pricing_lookup.py
# Search competitor pricing pages
# ============================================================

from .web_search import web_search


def pricing_lookup(company_name: str, max_results: int = 5):
    """
    Search pricing pages
    """

    query = f"{company_name} pricing plans pricing page"

    return web_search(query=query, max_results=max_results)