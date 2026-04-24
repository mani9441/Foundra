# ============================================================
# File: phase5_product_strategy/tools/atomic/pricing_lookup_tool.py
# Competitor Pricing Discovery
# ============================================================

from .web_search_tool import web_search


def pricing_lookup(product_name: str):
    query = f"{product_name} pricing plans pricing page"
    results = web_search(query, max_results=5)

    pricing_data = []

    for r in results:
        pricing_data.append({
            "title": r.get("title", ""),
            "url": r.get("href", ""),
            "snippet": r.get("body", "")
        })

    return pricing_data