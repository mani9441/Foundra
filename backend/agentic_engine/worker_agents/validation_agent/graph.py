
from langgraph.graph import StateGraph, START, END

from .state import ValidationState

# Core Nodes
from .nodes import *




# ==========================================
# CONDITIONAL ROUTING
# ==========================================

def route_after_problem(state: ValidationState):
    """
    If pain too weak, skip most work and judge early.
    """
    pain = state.get("problem_analysis", {}).get("pain_score", 0)

    if pain <= 3:
        return "judge"

    return "persona"


def route_after_judge(state: ValidationState):
    """
    Always go to report now.
    Future:
    route to niche_finder / pivot_agent etc.
    """
    return "report"


# ==========================================
# BUILD GRAPH
# ==========================================

def build_validation_graph():
    graph = StateGraph(ValidationState)

    # --------------------------------------
    # Register Nodes
    # --------------------------------------

    graph.add_node("intake", intake_node)
    graph.add_node("problem", problem_node)
    graph.add_node("persona", persona_node)
    graph.add_node("competitor", competitor_node)
    graph.add_node("pricing", pricing_node)

    graph.add_node("gap", gap_node)
    graph.add_node("skeptic", skeptic_node)
    graph.add_node("uvp", uvp_node)
    graph.add_node("judge", judge_node)
    graph.add_node("report", report_node)

    # --------------------------------------
    # Start Flow
    # --------------------------------------

    graph.add_edge(START, "intake")
    graph.add_edge("intake", "problem")

    # --------------------------------------
    # Conditional after problem
    # --------------------------------------

    graph.add_conditional_edges(
        "problem",
        route_after_problem,
        {
            "persona": "persona",
            "judge": "judge",
        }
    )

    # --------------------------------------
    # Main Sequential + Parallel Style Chain
    # --------------------------------------

    # persona -> competitor
    graph.add_edge("persona", "competitor")

    # competitor -> pricing
    graph.add_edge("competitor", "pricing")

    # pricing -> gap
    graph.add_edge("pricing", "gap")

    # gap -> skeptic
    graph.add_edge("gap", "skeptic")

    # skeptic -> uvp
    graph.add_edge("skeptic", "uvp")

    # uvp -> judge
    graph.add_edge("uvp", "judge")

    # --------------------------------------
    # Judge Routing
    # --------------------------------------

    graph.add_conditional_edges(
        "judge",
        route_after_judge,
        {
            "report": "report"
        }
    )

    # --------------------------------------
    # End
    # --------------------------------------

    graph.add_edge("report", END)

    return graph.compile()


# ==========================================
# EXPORTED APP INSTANCE
# ==========================================

validation_app = build_validation_graph()


# ==========================================
# OPTIONAL STREAMING RUNNER EXAMPLE
# ==========================================

def stream_validation(user_input: str):
    """
    Streams node-by-node updates.
    """

    state = {
        "user_input": user_input
    }

    for event in validation_app.stream(state):
        print(event)


# ==========================================
# OPTIONAL STANDARD RUNNER EXAMPLE
# ==========================================

def run_validation(user_input: str):
    """
    Single invoke mode
    """

    state = {
        "user_input": user_input
    }

    result = validation_app.invoke(state)
    return result



# ==========================================
# HOW FLOW WORKS
# ==========================================

"""
START
 ↓
intake
 ↓
problem
 ↓ (if weak pain)
judge
 ↓
report
 ↓
END


NORMAL PATH:

START
 ↓
intake
 ↓
problem
 ↓
persona
 ↓
competitor
 ↓
pricing
 ↓
gap
 ↓
skeptic
 ↓
uvp
 ↓
judge
 ↓
report
 ↓
END
"""

# ==========================================
# WHY THIS IS PRODUCTION GRADE
# ==========================================

"""
✓ Conditional routing
✓ Modular nodes
✓ Easy to add tools
✓ Replaceable models
✓ Streaming support
✓ Deterministic flow
✓ Clean maintainable architecture
✓ Easy to attach memory/checkpoints later
"""

# ==========================================
# NEXT = PART 5
# run.py
# CLI runner
# test cases
# pretty print report
# debug mode
# benchmark ideas
# ==========================================