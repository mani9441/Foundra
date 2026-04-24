from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


def run_pricing_agent(state):
    inputs = state["inputs"]
    research = state.get("research", {})
    revenue = state.get("revenue_model", {})

    prompt = f"""
You are a world-class pricing strategist.

Inputs:
{inputs}

Research:
{research}

Revenue Model:
{revenue}

Return ONLY JSON:
{{
 "pricing_model": "",
 "tiers": [
   {{"name":"","price":"","features":[]}}
 ],
 "launch_offer": "",
 "upsell_strategy": "",
 "logic": "",
 "confidence": 0.0
}}
"""
    result = llm.invoke(prompt)
    return {"pricing_strategy": safe_json_parse(result)}