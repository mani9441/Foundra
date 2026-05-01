# ============================================================
# File: phase5_product_strategy/agents/prioritization_agent.py
# Must / Should / Later scoring
# ============================================================

import json

from ..llm import get_llm

llm = get_llm()


def run_prioritization_agent(state):
    features = state["surviving_features"]
    mvp_scope = state["mvp_scope"]
    constraints = state["constraints"]

    prompt = f"""
You are a ruthless startup PM.

Prioritize features using:
- impact
- speed to build
- necessity for launch
- retention value

FEATURES:
{json.dumps(features, indent=2)}

MVP SCOPE:
{json.dumps(mvp_scope, indent=2)}

CONSTRAINTS:
{json.dumps(constraints, indent=2)}

Return STRICT JSON:

{{
  "must_have":[...],
  "should_have":[...],
  "later":[...],
  "quick_wins":[...],
  "technical_debt_acceptance":[...]
}}
"""

    from ..utils.json_parser import parse_llm_json

    result = llm.invoke(prompt)

    data = parse_llm_json(
        result,
        fallback={}
    )

    state["prioritized_features"] = data
    state["logs"].append("Prioritization Agent completed.")

    return state