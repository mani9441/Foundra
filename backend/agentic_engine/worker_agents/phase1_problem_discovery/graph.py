import os
import json

from langgraph.graph import StateGraph, END

from .state import DiscoveryState

# Agents
from .agents.pain_evidence_agent import run_pain_evidence_agent
from .agents.target_user_agent import run_target_user_agent
from .agents.problem_statement_agent import run_problem_statement_agent
from .agents.alternatives_agent import run_alternatives_agent
from .agents.objective_agent import run_objective_agent
from .agents.judge_agent import run_judge_agent


# -------------------------
# NODE WRAPPERS
# -------------------------

def pain_node(state):
    print("Running Pain Evidence Agent...")
    return run_pain_evidence_agent(state)


def user_node(state):
    print("Running Target User Agent...")
    return run_target_user_agent(state)


def problem_node(state):
    print("Running Problem Statement Agent...")
    return run_problem_statement_agent(state)


def alternatives_node(state):
    print("Running Alternatives Agent...")
    return run_alternatives_agent(state)


def objective_node(state):
    print("Running Objective Agent...")
    return run_objective_agent(state)


def judge_node(state):
    print("Running Judge Agent...")
    return run_judge_agent(state)


# -------------------------
# CONDITIONAL LOGIC
# -------------------------

def retry_or_end(state):
    result = str(state["final_decision"]).lower()

    if "reject" in result:
        return "retry"

    if "pivot" in result:
        return "retry"

    return "end"


# -------------------------
# BUILD GRAPH
# -------------------------

def build_graph():
    workflow = StateGraph(DiscoveryState)

    workflow.add_node("pain", pain_node)
    workflow.add_node("users", user_node)
    workflow.add_node("problem", problem_node)
    workflow.add_node("alternatives", alternatives_node)
    workflow.add_node("objective", objective_node)
    workflow.add_node("judge", judge_node)

    workflow.set_entry_point("pain")

    workflow.add_edge("pain", "users")
    workflow.add_edge("users", "problem")
    workflow.add_edge("problem", "alternatives")
    workflow.add_edge("alternatives", "objective")
    workflow.add_edge("objective", "judge")

    workflow.add_conditional_edges(
        "judge",
        retry_or_end,
        {
            "retry": "pain",
            "end": END
        }
    )

    return workflow.compile()


# -------------------------
# SAVE OUTPUT
# -------------------------

def save_output(result,filename):
    os.makedirs("outputs", exist_ok=True)

    with open(filename, "w") as f:
        json.dump(result, f, indent=2)


# -------------------------
# MAIN RUNNER
# -------------------------

def run_phase1(founder_input: str):
    app = build_graph()

    initial_state = {
        "founder_input": founder_input,
        "search_results": [],
        "complaints": [],
        "problem_statement": "",
        "target_users": [],
        "pain_evidence": {},
        "alternatives": {},
        "objective": "",
        "final_decision": {}
    }

    result = app.invoke(initial_state)

    #save_output(result,filename)

    return result


# -------------------------
# CLI TEST
# -------------------------

# if __name__ == "__main__":
#     founder_idea = input("Enter startup area or idea: ")

#     result = run_phase1(founder_idea)

#     print("\n=== FINAL OUTPUT ===\n")
#     print(json.dumps(result, indent=2))