# ============================================================
# File: phase5_product_strategy/agents/feature_discovery_agent.py
# Discover all possible useful features
# ============================================================

from ..tools.medium import run_feature_research


def run_feature_discovery_agent(state):
    inputs = state["inputs"]

    solution = inputs.get("validated_solution_concept", "")
    icp = inputs.get("icp", "")
    value_prop = inputs.get("core_value_proposition", "")

    research = run_feature_research(
        solution_concept=solution,
        icp=icp,
        value_proposition=value_prop
    )

    all_features = []

    for group in research.values():
        if isinstance(group, list):
            all_features.extend(group)

    # dedupe
    all_features = list(dict.fromkeys(all_features))

    state["feature_pool"] = {
        "research": research,
        "all_features": all_features
    }

    state["logs"].append("Feature Discovery Agent completed.")

    return state