from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


def run_explainability_agent(state):
    prompt = f"""
Explain clearly why this business model was selected.

Revenue:
{state.get("revenue_model", {})}

Pricing:
{state.get("pricing_strategy", {})}

Economics:
{state.get("unit_economics_model", {})}

Decision:
{state.get("viability_decision", {})}

Return ONLY JSON:
{{
 "plain_english_summary": "",
 "key_strengths": [],
 "key_risks": [],
 "recommended_next_action": ""
}}
"""
    result = llm.invoke(prompt)
    return {"explainability": safe_json_parse(result)}