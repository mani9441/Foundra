# ============================================================
# File: phase2_validation/agents/value_prop_agent.py
# ============================================================

from typing import Dict, Any

from backend.agentic_engine.LLMs.llm import get_llm
from ..prompts import SYSTEM_ANALYST, VALUE_PROP_PROMPT
from ..utils.json_parser import extract_json

from ..tools.medium.value_prop_testing_tool import run_value_prop_testing


def run_value_prop_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Output:
    state["core_value_proposition"]
    """

    llm = get_llm()

    solution = state["validated_solution_concept"].get(
        "best_solution_concept",
        str(state["founder_solution_ideas"][0])
    )

    tests = run_value_prop_testing(
        state["problem_statement"],
        solution,
        state["existing_alternatives"]
    )

    prompt = VALUE_PROP_PROMPT.format(
        problem=state["problem_statement"],
        pain=state["pain_evidence"],
        alts=state["existing_alternatives"],
        solution=solution
    )

    result = llm.invoke(
        [
            ("system", SYSTEM_ANALYST),
            ("human", prompt)
        ]
    )

    data = extract_json(result.content)
    data["message_tests"] = tests

    state["core_value_proposition"] = data
    return state