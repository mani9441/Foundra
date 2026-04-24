from backend.agentic_engine.LLMs.llm import get_llm
from ..atomic.search_tool import search_web
from ...utils.json_parser import safe_json_parse

llm = get_llm()


def run_demand_signal(problem_keyword: str):
    search = search_web(problem_keyword, max_results=8)

    prompt = f"""
You are a market demand analyst.

Signals:
{search}

Estimate demand strength.

Return ONLY JSON:
{{
 "demand_score": 0,
 "urgency_score": 0,
 "trend_direction": "",
 "buying_intent_score": 0,
 "reasoning": []
}}
"""

    result = llm.invoke(prompt)
    return safe_json_parse(result)