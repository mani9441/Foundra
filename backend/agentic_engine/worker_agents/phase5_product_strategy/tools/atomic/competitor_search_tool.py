# ============================================================
# File: phase5_product_strategy/tools/atomic/competitor_search_tool.py
# Competitor Discovery Tool
# ============================================================

from .web_search_tool import web_search


def competitor_search(product_type: str):
    query = f"best competitors for {product_type} SaaS startups tools platforms"
    results = web_search(query, max_results=8)

    competitors = []

    for r in results:
        title = r.get("title", "")
        link = r.get("href", "")
        body = r.get("body", "")

        competitors.append({
            "name": title,
            "url": link,
            "summary": body
        })

    return competitors