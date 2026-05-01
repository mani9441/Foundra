# ============================================================
# File: phase5_product_strategy/agents/mvp_scope_agent.py
# Finalize smallest lovable MVP
# ============================================================

import json

from ..llm import get_llm

llm = get_llm()


def run_mvp_scope_agent(state):
    surviving_features = state["surviving_features"]
    constraints = state["constraints"]
    inputs = state["inputs"]

    prompt = f"""
You are an elite startup founder + product manager.

Design the SMALLEST MVP that can genuinely solve the user's main pain.

STARTUP IDEA:
{inputs.get("validated_solution_concept","")}

ICP:
{inputs.get("icp","")}

VALUE PROP:
{inputs.get("core_value_proposition","")}

SURVIVING FEATURES:
{json.dumps(surviving_features, indent=2)}

CONSTRAINTS:
{json.dumps(constraints, indent=2)}

Return STRICT JSON:

{{
  "core_problem":"...",
  "mvp_scope":[...],
  "excluded_for_now":[...],
  "manual_ops_allowed":[...],
  "success_metric":[...]
}}
"""

    
    from ..utils.json_parser import parse_llm_json

    result = llm.invoke(prompt)

    data = parse_llm_json(
        result,
        fallback={}
    )

    state["mvp_scope"] = data
    state["logs"].append("MVP Scope Agent completed.")

    return state