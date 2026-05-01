# ============================================================
# File: phase2_validation/tools_medium/market_research_tool.py
# Medium Tool (LangGraph-style reasoning pipeline)
# ============================================================

from typing import Dict, Any

from ...llm import get_llm
from ...utils.json_parser import extract_json

from ..atomic.google_search import google_search_tool
from ..atomic.web_trend_fetch import web_trend_fetch_tool
from ..atomic.user_forum_scraper import user_forum_scraper_tool


def run_market_research(problem: str, user_segment: str) -> Dict[str, Any]:
    """
    Combines:
    - search
    - trends
    - community pain signals
    - LLM synthesis
    """

    llm = get_llm()

    search = google_search_tool.invoke(
        f"{problem} solutions market startup founders {user_segment}"
    )

    trends = web_trend_fetch_tool.invoke(problem)

    forums = user_forum_scraper_tool.invoke(problem)

    prompt = f"""
You are a startup market analyst.

Problem: {problem}
Target Users: {user_segment}

Search Results:
{search}

Trend Data:
{trends}

Forum Signals:
{forums}

Return JSON:
{{
 "market_direction":"",
 "estimated_interest_level":0,
 "why_market_exists":[],
 "emerging_opportunities":[],
 "risks":[]
}}
"""

    result = llm.invoke(prompt)
    return extract_json(result.content)