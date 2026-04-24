from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


def run_repair_agent(state):
    critic = state.get("critic_report", {})
    payload = {
        "revenue_model": state.get("revenue_model", {}),
        "pricing_strategy": state.get("pricing_strategy", {}),
        "unit_economics_model": state.get("unit_economics_model", {}),
        "viability_decision": state.get("viability_decision", {})
    }

    prompt = f"""
You are a repair strategist.

Current Outputs:
{payload}

Critic Feedback:
{critic}

Fix only targeted weak areas.

Return ONLY JSON:
{{
 "revenue_model": {{}},
 "pricing_strategy": {{}},
 "unit_economics_model": {{}},
 "viability_decision": {{}},
 "changes_summary": []
}}
"""
    result = llm.invoke(prompt)
    repaired = safe_json_parse(result)

    updates = {}

    for k in [
        "revenue_model",
        "pricing_strategy",
        "unit_economics_model",
        "viability_decision"
    ]:
        if isinstance(repaired.get(k), dict) and repaired.get(k):
            updates[k] = repaired[k]

    updates["repair_report"] = repaired
    return updates