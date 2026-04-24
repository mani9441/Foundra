from backend.agentic_engine.LLMs.llm import get_llm

from ..atomic.company_finder import find_companies
from ..atomic.pricing_scraper import scrape_pricing
from ...utils.json_parser import safe_json_parse

llm = get_llm()


def run_competitor_research(niche: str):
    companies = find_companies(niche, limit=6)

    enriched = []
    for c in companies:
        pricing = scrape_pricing(c["url"])
        enriched.append({
            "name": c["name"],
            "url": c["url"],
            "snippet": c["snippet"],
            "pricing": pricing["prices_found"][:10],
            "has_pricing": pricing["has_pricing"]
        })

    prompt = f"""
You are a market research strategist.

Analyze these competitors:
{enriched}

Return ONLY JSON:
{{
  "top_competitors": [],
  "common_pricing_patterns": [],
  "positioning_gaps": [],
  "premium_anchor_price": "",
  "budget_anchor_price": ""
}}
"""

    result = llm.invoke(prompt)
    summary = safe_json_parse(result)

    return {
        "raw_competitors": enriched,
        "summary": summary
    }