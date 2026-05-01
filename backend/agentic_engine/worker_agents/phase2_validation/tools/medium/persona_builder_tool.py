# ============================================================
# File: phase2_validation/tools_medium/persona_builder_tool.py
# ============================================================

from typing import Dict, Any, List

from ...llm import get_llm
from ...utils.json_parser import extract_json

from ..atomic.user_forum_scraper import user_forum_scraper_tool


def run_persona_builder(
    problem: str,
    users: str,
    pain: List[str]
) -> Dict[str, Any]:
    """
    Find strongest ICP persona.
    """

    llm = get_llm()

    forum = user_forum_scraper_tool.invoke(problem)

    prompt = f"""
Build an ideal customer profile.

Problem: {problem}
Target Segment: {users}
Pain: {pain}
Community: {forum}

Return JSON:
{{
 "persona_name":"",
 "role":"",
 "industry":"",
 "company_size":"",
 "pain_priority":"",
 "buying_trigger":"",
 "budget_power":"",
 "channel_reach":[]
}}
"""

    result = llm.invoke(prompt)
    return extract_json(result.content)