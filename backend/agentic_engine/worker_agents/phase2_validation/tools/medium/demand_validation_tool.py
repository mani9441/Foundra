# ============================================================
# File: phase2_validation/tools_medium/demand_validation_tool.py
# ============================================================

from typing import Dict, Any

from ...llm import get_llm
from ...utils.json_parser import extract_json

from ..atomic.google_search import google_search_tool
from ..atomic.reddit_search import reddit_search_tool
from ..atomic.web_trend_fetch import web_trend_fetch_tool


def run_demand_validation(problem: str) -> Dict[str, Any]:
    """
    Check real demand signals.
    """

    llm = get_llm()

    search = google_search_tool.invoke(problem)
    reddit = reddit_search_tool.invoke(problem)
    trends = web_trend_fetch_tool.invoke(problem)

    prompt = f"""
You are a demand analyst.

Problem: {problem}

Google:
{search}

Reddit:
{reddit}

Trend:
{trends}

Return JSON:
{{
 "demand_score":0,
 "search_signal":"",
 "community_signal":"",
 "trend_signal":"",
 "buyer_intent_estimate":"",
 "summary":""
}}
"""

    result = llm.invoke(prompt)
    return extract_json(result.content)