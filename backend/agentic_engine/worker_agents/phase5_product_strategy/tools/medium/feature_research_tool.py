# ============================================================
# File: phase5_product_strategy/tools/medium/feature_research_tool.py
# Replace full file
# Fix: Robust JSON extraction from LLM output
# ============================================================

import json
import re

from backend.agentic_engine.LLMs.llm import get_llm

from ..atomic.competitor_search_tool import competitor_search
from ..atomic.pricing_lookup_tool import pricing_lookup

llm = get_llm()


# ============================================================
# HELPERS
# ============================================================

def extract_json(text: str):
    """
    Handles:
    - raw json
    - markdown ```json blocks
    - extra commentary before/after json
    """

    if not text:
        return {}

    text = text.strip()

    # remove markdown fences
    text = text.replace("```json", "").replace("```", "").strip()

    # direct parse
    try:
        return json.loads(text)
    except:
        pass

    # find first json object
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    # fallback
    return {
        "must_have": [],
        "common_features": [],
        "delight_features": [],
        "admin_features": [],
        "monetizable_features": []
    }


# ============================================================
# MAIN TOOL
# ============================================================

def run_feature_research(
    solution_concept: str,
    icp,
    value_proposition: str
):
    competitors = competitor_search(solution_concept)

    pricing_samples = []
    for c in competitors[:3]:
        pricing_samples.extend(
            pricing_lookup(c["name"])
        )

    prompt = f"""
You are a startup product strategist.

Return ONLY valid JSON.

IDEA:
{solution_concept}

ICP:
{json.dumps(icp, indent=2)}

VALUE PROP:
{value_proposition}

COMPETITORS:
{json.dumps(competitors[:5], indent=2)}

Return:

{{
  "must_have": [],
  "common_features": [],
  "delight_features": [],
  "admin_features": [],
  "monetizable_features": []
}}
"""

    from ...utils.json_parser import parse_llm_json

    result = llm.invoke(prompt)

    data = parse_llm_json(
        result,
        fallback={}
    )

    return data