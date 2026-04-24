# ============================================================
# Competitor Research Tool
# Uses atomic tools + LLM reasoning
# ============================================================

from backend.agentic_engine.LLMs.llm import get_llm

from ..atomic.competitor_search import competitor_search
from ..atomic.pricing_lookup import pricing_lookup
from ..atomic.scrape_url import scrape_url

from ...utils.json_parser import parse_llm_json

llm = get_llm()


def competitor_research_tool(niche: str):
    """
    Research competitors, positioning, pricing, gaps
    """

    competitors = competitor_search(niche, max_results=6)

    enriched = []

    for item in competitors[:5]:
        url = item["url"]
        content = scrape_url(url)

        pricing = pricing_lookup(item["title"], max_results=3)

        enriched.append({
            "name": item["title"],
            "url": url,
            "snippet": item["snippet"],
            "pricing": pricing,
            "content": content[:4000]
        })

    prompt = f"""
You are a startup market strategist.

Analyze competitors in this niche:
{niche}

Data:
{enriched}

Return JSON:

{{
  "top_competitors": [],
  "common_positioning_angles": [],
  "pricing_patterns": [],
  "market_gaps": [],
  "opportunities_for_new_startup": []
}}
"""

    raw = llm.invoke(prompt)

    return parse_llm_json(
        raw,
        {
            "top_competitors": [],
            "common_positioning_angles": [],
            "pricing_patterns": [],
            "market_gaps": [],
            "opportunities_for_new_startup": []
        })