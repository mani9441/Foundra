# ============================================================
# Audience Research Tool
# Pain points / desires / objections
# ============================================================

from ...llm import get_llm

from ..atomic.social_trend_search import social_trend_search
from ..atomic.web_search import web_search
from ...utils.json_parser import parse_llm_json

llm = get_llm()


def audience_research_tool(icp: str):
    """
    Understand audience deeply
    """

    social = social_trend_search(icp, 8)
    web = web_search(f"{icp} biggest challenges pain points", 6)

    prompt = f"""
You are a customer psychologist.

ICP:
{icp}

Research:
Social:{social}
Web:{web}

Return JSON:

{{
  "top_pains": [],
  "desired_outcomes": [],
  "buying_triggers": [],
  "common_objections": [],
  "language_they_use": []
}}
"""

    raw = llm.invoke(prompt)

    return parse_llm_json(
        raw,
        {
            "top_pains": [],
            "desired_outcomes": [],
            "buying_triggers": [],
            "common_objections": [],
            "language_they_use": []
        }
    )