from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


def run_critic_agent(state):
    payload = {
        "revenue_model": state.get("revenue_model", {}),
        "pricing_strategy": state.get("pricing_strategy", {}),
        "unit_economics_model": state.get("unit_economics_model", {}),
        "viability_decision": state.get("viability_decision", {}),
        "research": state.get("research", {})
    }

    prompt = f"""
You are a startup strategy critic.

Audit consistency, realism, and execution quality.

Data:
{payload}

Check:
1. Pricing realistic?
2. Revenue model aligned with market?
3. CAC / LTV believable?
4. Decision justified?
5. Contradictions?

Return ONLY JSON:
{{
 "approved": true,
 "score": 0.0,
 "issues": [],
 "repair_targets": [],
 "summary": ""
}}
"""
    result = llm.invoke(prompt)
    return {"critic_report": safe_json_parse(result)}