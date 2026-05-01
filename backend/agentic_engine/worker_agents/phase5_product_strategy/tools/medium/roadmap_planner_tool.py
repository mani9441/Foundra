# ============================================================
# File: phase5_product_strategy/tools/medium/roadmap_planner_tool.py
# LLM + constraints driven roadmap planning
# ============================================================

import json

from ...llm import get_llm

llm = get_llm()


def run_roadmap_planner(
    features,
    timeline_weeks,
    developers,
    budget
):
    prompt = f"""
You are an elite startup PM.

Create realistic MVP roadmap.

FEATURES:
{json.dumps(features, indent=2)}

TEAM SIZE:
{developers}

TIMELINE WEEKS:
{timeline_weeks}

BUDGET:
{budget}

Return STRICT JSON:

{{
  "phase_1_weeks_1_2":[...],
  "phase_2_weeks_3_4":[...],
  "phase_3_weeks_5_plus":[...],
  "launch_readiness":[...]
}}
"""

    from ...utils.json_parser import parse_llm_json

    result = llm.invoke(prompt)

    data = parse_llm_json(
        result,
        fallback={}
    )
    return data