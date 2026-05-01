# ============================================================
# Acquisition Channel Strategy Agent
# ============================================================

import json

from ..llm import get_llm
from ..utils.json_parser import parse_llm_json

llm = get_llm()


def run_channel_strategy_agent(state):

    intelligence = state.get("market_intelligence", {})
    budget = state.get("marketing_budget", {})
    access = state.get("channel_access", {})
    sales = state.get("sales_resources", {})

    prompt = f"""
You are a GTM strategist.

Use the following data to build an acquisition channel plan.

Market Intelligence:
{json.dumps(intelligence)}

Budget:
{json.dumps(budget)}

Channel Access:
{json.dumps(access)}

Sales Resources:
{json.dumps(sales)}

Return JSON:

{{
  "top_channels": [],
  "why_each_channel": [],
  "budget_allocation": {{}},
  "execution_sequence": [],
  "channel_tests": [],
  "estimated_first_customer_sources": []
}}
"""

    raw = llm.invoke(prompt)

    result = parse_llm_json(
        raw,
        {
            "top_channels": [],
            "why_each_channel": [],
            "budget_allocation": {},
            "execution_sequence": [],
            "channel_tests": [],
            "estimated_first_customer_sources": []
        }
    )

    return {
        "acquisition_channel_plan": result
    }