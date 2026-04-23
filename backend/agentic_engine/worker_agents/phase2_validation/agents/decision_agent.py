# ============================================================
# File: phase2_validation/agents/decision_agent.py
# ============================================================

from typing import Dict, Any

from backend.agentic_engine.LLMs.llm import get_llm
from ..prompts import SYSTEM_ANALYST, DECISION_PROMPT
from ..utils.json_parser import extract_json


def run_decision_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Final Proceed / Pivot / Reject
    """

    llm = get_llm()

    prompt = DECISION_PROMPT.format(
        solution=state["validated_solution_concept"],
        icp=state["icp"],
        demand=state["demand_signals"],
        vp=state["core_value_proposition"]
    )

    result = llm.invoke(
        [
            ("system", SYSTEM_ANALYST),
            ("human", prompt)
        ]
    )

    state["proceed_pivot_reject"] = extract_json(result.content)
    return state