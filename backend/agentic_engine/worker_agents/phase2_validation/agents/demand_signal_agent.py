# ============================================================
# File: phase2_validation/agents/demand_signal_agent.py
# ============================================================

from typing import Dict, Any

from ..tools.medium.demand_validation_tool import run_demand_validation


def run_demand_signal_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Output:
    state["demand_signals"]
    """

    demand = run_demand_validation(
        state["problem_statement"]
    )

    state["demand_validation"] = demand
    state["demand_signals"] = demand

    return state