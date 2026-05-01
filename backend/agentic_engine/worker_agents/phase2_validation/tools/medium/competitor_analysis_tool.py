# ============================================================
# File: phase2_validation/tools_medium/competitor_analysis_tool.py
# ============================================================

from typing import Dict, Any, List

from ...llm import get_llm
from ...utils.json_parser import extract_json

from ..atomic.competitor_scraper import competitor_scraper_tool
from ..atomic.pricing_lookup import pricing_lookup_tool


def run_competitor_analysis(competitors: List[str]) -> Dict[str, Any]:
    """
    Analyze alternatives and gaps.
    """

    llm = get_llm()

    data = []

    for name in competitors[:5]:
        profile = competitor_scraper_tool.invoke(name)
        pricing = pricing_lookup_tool.invoke(name)

        data.append(
            {
                "name": name,
                "profile": profile,
                "pricing": pricing,
            }
        )

    prompt = f"""
You are a strategic competitor analyst.

Competitor Data:
{data}

Return JSON:
{{
 "market_crowdedness":"",
 "main_patterns":[],
 "pricing_range":"",
 "unserved_gaps":[],
 "attack_angles":[]
}}
"""

    result = llm.invoke(prompt)
    return extract_json(result.content)