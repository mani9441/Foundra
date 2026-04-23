# ============================================================
# File: phase2_validation/tools_atomic/user_forum_scraper.py
# Atomic Tool
# ============================================================

from typing import Dict, Any
from langchain.tools import tool


@tool("user_forum_scraper_tool")
def user_forum_scraper_tool(topic: str) -> Dict[str, Any]:
    """
    Search founder forums / indiehackers / communities.
    Mock mode.
    """

    return {
        "topic": topic,
        "mentions": [
            "Need faster validation",
            "Hard to know if idea is good",
            "Need customer interviews"
        ],
        "pain_frequency": "high"
    }