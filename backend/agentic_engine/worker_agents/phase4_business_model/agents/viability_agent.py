from ..llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


def run_viability_agent(state):
    revenue = state.get("revenue_model", {})
    pricing = state.get("pricing_strategy", {})
    economics = state.get("unit_economics_model", {})
    research = state.get("research", {})

    prompt = f"""
You are a VC investor evaluating startup viability.

Revenue:
{revenue}

Pricing:
{pricing}

Economics:
{economics}

Research:
{research}

Return ONLY JSON:
{{
 "decision": "PROCEED / PIVOT / REJECT",
 "confidence": 0.0,
 "risks": [],
 "opportunities": [],
 "why": ""
}}
"""
    result = llm.invoke(prompt)
    return {"viability_decision": safe_json_parse(result)}