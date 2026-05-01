# ============================================================
# File: phase5_product_strategy/agents/build_spec_agent.py
# Engineering-ready build specification
# ============================================================

import json

from ..llm import get_llm
from ..tools.medium import run_architecture_recommender

llm = get_llm()


def run_build_spec_agent(state):
    inputs = state["inputs"]
    constraints = state["constraints"]
    prioritized = state["prioritized_features"]

    product_type = inputs.get("validated_solution_concept", "startup product")

    architecture = run_architecture_recommender(
        budget_level=constraints.get("budget_level", "low"),
        product_type=product_type,
        ai_needed=True,
        expected_scale="early_stage"
    )

    prompt = f"""
You are a senior startup CTO.

Create an engineering build specification.

ARCHITECTURE:
{json.dumps(architecture, indent=2)}

PRIORITIZED FEATURES:
{json.dumps(prioritized, indent=2)}

Return STRICT JSON:

{{
  "frontend": {{
    "framework":"...",
    "pages":[...],
    "components":[...]
  }},
  "backend": {{
    "framework":"...",
    "modules":[...],
    "apis":[...]
  }},
  "database": {{
    "engine":"...",
    "tables":[...]
  }},
  "infra": {{
    "hosting":"...",
    "auth":"...",
    "storage":"...",
    "monitoring":"..."
  }},
  "delivery_plan":[...]
}}
"""

    from ..utils.json_parser import parse_llm_json

    result = llm.invoke(prompt)

    build_spec = parse_llm_json(
        result,
        fallback={}
    )

    state["build_specification"] = build_spec
    state["logs"].append("Build Spec Agent completed.")

    return state