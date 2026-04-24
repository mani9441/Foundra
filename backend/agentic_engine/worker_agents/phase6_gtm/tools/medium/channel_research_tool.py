# ============================================================
# Channel Research Tool
# Finds best acquisition channels
# ============================================================

from backend.agentic_engine.LLMs.llm import get_llm

from ..atomic.web_search import web_search
from ..atomic.social_trend_search import social_trend_search
from ..atomic.seo_keyword_search import seo_keyword_search

from ...utils.json_parser import parse_llm_json

llm = get_llm()


def channel_research_tool(product: str, icp: str):
    """
    Determine best acquisition channels
    """

    web_data = web_search(f"{product} marketing channels startups", 6)
    social = social_trend_search(icp, 6)
    seo = seo_keyword_search(product, 6)

    prompt = f"""
You are a GTM strategist.

Product:
{product}

ICP:
{icp}

Research:
Web:{web_data}
Social:{social}
SEO:{seo}

Return JSON:

{{
  "recommended_channels": [
    {{
      "channel": "",
      "why": "",
      "difficulty": "",
      "speed": "",
      "estimated_cac": ""
    }}
  ],
  "top_3_priority_channels": []
}}
"""

    raw = llm.invoke(prompt)

    return parse_llm_json(
        raw,
        {
            "recommended_channels": [],
            "top_3_priority_channels": []
        }
    )