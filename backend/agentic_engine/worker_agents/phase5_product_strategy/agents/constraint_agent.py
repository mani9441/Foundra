# ============================================================
# File: phase5_product_strategy/agents/constraint_agent.py
# Analyze budget / skills / capacity / constraints
# ============================================================

import math


def run_constraint_agent(state):
    inputs = state["inputs"]

    team_skills = inputs.get("team_skills", [])
    engineering_capacity = int(inputs.get("engineering_capacity", 2))
    budget = int(inputs.get("budget", 50000))
    time_weeks = int(inputs.get("time_constraints_weeks", 6))
    technical_constraints = inputs.get("technical_constraints", [])

    if budget < 50000:
        budget_level = "very_low"
    elif budget < 150000:
        budget_level = "low"
    elif budget < 500000:
        budget_level = "medium"
    else:
        budget_level = "high"

    weekly_capacity_points = engineering_capacity * 10
    total_capacity_points = weekly_capacity_points * time_weeks

    constraints = {
        "team_skills": team_skills,
        "engineering_capacity": engineering_capacity,
        "budget": budget,
        "budget_level": budget_level,
        "timeline_weeks": time_weeks,
        "technical_constraints": technical_constraints,
        "weekly_capacity_points": weekly_capacity_points,
        "total_capacity_points": total_capacity_points
    }

    state["constraints"] = constraints
    state["logs"].append("Constraint Agent completed.")

    return state