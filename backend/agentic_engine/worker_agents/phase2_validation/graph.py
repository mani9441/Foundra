# ============================================================
# File: phase2_validation/graph.py
# PART 5 - LangGraph Orchestration Engine
# Final output = JSON only
# ============================================================

import json
from typing import Dict, Any
import os

from langgraph.graph import StateGraph, END

from .state import ValidationState

from .agents.solution_validator import run_solution_validator
from .agents.icp_agent import run_icp_agent
from .agents.demand_signal_agent import run_demand_signal_agent
from .agents.value_prop_agent import run_value_prop_agent
from .agents.debate_moderator import run_debate_moderator
from .agents.decision_agent import run_decision_agent


# ============================================================
# NODE WRAPPERS
# ============================================================

def node_solution(state: ValidationState) -> ValidationState:
    return run_solution_validator(state)


def node_icp(state: ValidationState) -> ValidationState:
    return run_icp_agent(state)


def node_demand(state: ValidationState) -> ValidationState:
    return run_demand_signal_agent(state)


def node_value_prop(state: ValidationState) -> ValidationState:
    return run_value_prop_agent(state)


def node_debate(state: ValidationState) -> ValidationState:
    return run_debate_moderator(state)


def node_decision(state: ValidationState) -> ValidationState:
    return run_decision_agent(state)


# ============================================================
# FINAL JSON PACKER
# ============================================================

def node_finalize(state: ValidationState) -> ValidationState:
    """
    Final node:
    - build final JSON
    - save to outputs/phase2_result.json
    """

    final_json = {
        "validated_solution_concept": state.get(
            "validated_solution_concept", {}
        ),
        "ICP": state.get("icp", {}),
        "demand_signals": state.get("demand_signals", {}),
        "core_value_proposition": state.get(
            "core_value_proposition", {}
        ),
        "board_debate": state.get("board_debate", {}),
        "decision": state.get("proceed_pivot_reject", {}),
    }

    # ensure folder exists
    os.makedirs("outputs", exist_ok=True)

    file_path = os.path.join(
        "outputs",
        "phase2_result.json"
    )

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(
            final_json,
            f,
            indent=2,
            ensure_ascii=False
        )

    state["final_json"] = final_json
    state["saved_file"] = file_path

    return state


# ============================================================
# BUILD GRAPH
# ============================================================

def build_phase2_graph():
    graph = StateGraph(ValidationState)

    # nodes
    graph.add_node("solution", node_solution)
    graph.add_node("icp", node_icp)
    graph.add_node("demand", node_demand)
    graph.add_node("value_prop", node_value_prop)
    graph.add_node("debate", node_debate)
    graph.add_node("decision", node_decision)
    graph.add_node("finalize", node_finalize)

    # flow
    graph.set_entry_point("solution")

    graph.add_edge("solution", "icp")
    graph.add_edge("icp", "demand")
    graph.add_edge("demand", "value_prop")
    graph.add_edge("value_prop", "debate")
    graph.add_edge("debate", "decision")
    graph.add_edge("decision", "finalize")
    graph.add_edge("finalize", END)

    return graph.compile()


# ============================================================
# RUNNER
# ============================================================

def run_phase2(inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Safe runner for Phase 2 graph.
    """

    app = build_phase2_graph()

    result = app.invoke(inputs)

    # If finalize node worked normally
    if "final_json" in result:
        return result["final_json"]

    # Fallback protection if LangGraph merge issue happens
    final_json = {
        "validated_solution_concept":
            result.get("validated_solution_concept", {}),

        "ICP":
            result.get("icp", {}),

        "demand_signals":
            result.get("demand_signals", {}),

        "core_value_proposition":
            result.get("core_value_proposition", {}),

        "board_debate":
            result.get("board_debate", {}),

        "decision":
            result.get("proceed_pivot_reject", {}),

        "warning":
            "final_json key missing. Fallback response used."
    }

    # also save file again for safety
    os.makedirs("outputs", exist_ok=True)

    with open(
        os.path.join("outputs", "phase2_result.json"),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            final_json,
            f,
            indent=2,
            ensure_ascii=False
        )

    return final_json

# ============================================================
# CLI TEST
# ============================================================

# if __name__ == "__main__":

#     sample = {
#         "problem_statement":
#             "Small startups struggle to validate ideas quickly.",

#         "target_user_segment":
#             "Early stage founders",

#         "pain_evidence": [
#             "Waste months building wrong products",
#             "No structured validation process",
#             "No customer feedback loop"
#         ],

#         "existing_alternatives": [
#             "Consultants",
#             "Google Forms",
#             "Guesswork"
#         ],

#         "founder_solution_ideas": [
#             "AI startup validation engine"
#         ],

#         "team_constraints": [
#             "2 engineers",
#             "low budget",
#             "4 week MVP"
#         ],

#         "basic_market_context":
#             "Growing AI SaaS market",

#         "prototype_mockup_capability":
#             "Strong backend weak frontend"
#     }

#     output = run_phase2(sample)

#     print(json.dumps(output, indent=2))