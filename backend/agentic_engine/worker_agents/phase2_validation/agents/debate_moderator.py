from typing import Dict, Any
from ..llm import get_llm
from ..utils.json_parser import extract_json


def run_debate_moderator(state: Dict[str, Any]) -> Dict[str, Any]:

    llm = get_llm()

    prompt = f"""
You are an executive board.

Return ONLY valid JSON.
No markdown.
No explanation.
No intro text.

Inputs:
Solution: {state["validated_solution_concept"]}
ICP: {state["icp"]}
Demand: {state["demand_signals"]}
Value Prop: {state["core_value_proposition"]}

Return:

{{
 "bull_case":[...],
 "skeptic_case":[...],
 "pivot_case":[...],
 "consensus_summary":""
}}
"""

    result = llm.invoke(prompt)

    state["board_debate"] = extract_json(result.content)

    return state