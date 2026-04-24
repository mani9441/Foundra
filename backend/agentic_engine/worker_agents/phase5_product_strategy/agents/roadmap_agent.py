# ============================================================
# File: phase5_product_strategy/agents/roadmap_agent.py
# Build realistic execution roadmap
# ============================================================

from ..tools.medium import run_roadmap_planner


def run_roadmap_agent(state):
    constraints = state["constraints"]
    prioritized = state["prioritized_features"]

    roadmap = run_roadmap_planner(
        features=prioritized,
        timeline_weeks=constraints.get("timeline_weeks", 6),
        developers=constraints.get("engineering_capacity", 2),
        budget=constraints.get("budget", 50000)
    )

    state["roadmap"] = roadmap
    state["logs"].append("Roadmap Agent completed.")

    return state