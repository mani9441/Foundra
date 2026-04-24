from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


def run_revenue_model_agent(state):
    inputs = state["inputs"]
    research = state.get("research", {})

    prompt = f"""
You are an elite startup monetization strategist.

Inputs:
{inputs}

Research:
{research}

Choose best revenue model.

Return ONLY JSON:
{{
 "primary_model": "",
 "secondary_model": "",
 "collection_method": "",
 "expansion_paths": [],
 "rationale": "",
 "confidence": 0.0
}}
"""
    result = llm.invoke(prompt)
    return {"revenue_model": safe_json_parse(result)}