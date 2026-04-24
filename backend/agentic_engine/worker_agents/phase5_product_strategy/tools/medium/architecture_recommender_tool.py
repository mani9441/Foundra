# ============================================================
# File: phase5_product_strategy/tools/medium/architecture_recommender_tool.py
# Uses constraints + atomic tools + LLM reasoning
# ============================================================

import json

from backend.agentic_engine.LLMs.llm import get_llm

from ..atomic.tech_stack_lookup_tool import tech_stack_lookup

llm = get_llm()


def run_architecture_recommender(
    budget_level: str,
    product_type: str,
    ai_needed: bool,
    expected_scale: str
):
    stack = tech_stack_lookup(
        budget_level=budget_level,
        speed_priority=True,
        ai_needed=ai_needed
    )

    prompt = f"""
You are a startup CTO.

Recommend best architecture.

PRODUCT TYPE:
{product_type}

EXPECTED SCALE:
{expected_scale}

BUDGET:
{budget_level}

BASE STACK:
{json.dumps(stack, indent=2)}

Return STRICT JSON:

{{
  "architecture":"monolith/microservice/modular-monolith",
  "frontend":"...",
  "backend":"...",
  "database":"...",
  "hosting":"...",
  "auth":"...",
  "devops":"...",
  "notes":[...]
}}
"""

    from ...utils.json_parser import parse_llm_json

    result = llm.invoke(prompt)

    data = parse_llm_json(
        result,
        fallback={}
    )
    return data