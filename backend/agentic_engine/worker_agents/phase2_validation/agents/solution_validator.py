# ============================================================
# File: phase2_validation/agents/solution_validator.py
# ============================================================

from typing import Dict, Any

from ..llm import get_llm
from ..prompts import SYSTEM_ANALYST, SOLUTION_VALIDATOR_PROMPT
from ..utils.json_parser import extract_json

from ..tools.medium.market_research_tool import run_market_research
from ..tools.medium.competitor_analysis_tool import run_competitor_analysis


def run_solution_validator(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Output:
    state["validated_solution_concept"]
    """

    llm = get_llm()

    market = run_market_research(
        state["problem_statement"],
        state["target_user_segment"]
    )

    competitors = run_competitor_analysis(
        state["existing_alternatives"]
    )

    prompt = SOLUTION_VALIDATOR_PROMPT.format(
        problem=state["problem_statement"],
        users=state["target_user_segment"],
        pain=state["pain_evidence"],
        ideas=state["founder_solution_ideas"],
        competitors=competitors
    )

    result = llm.invoke(
        [
            ("system", SYSTEM_ANALYST),
            ("human", prompt)
        ]
    )

    data = extract_json(result.content)

    state["market_research"] = market
    state["competitor_analysis"] = competitors
    state["validated_solution_concept"] = data

    return state