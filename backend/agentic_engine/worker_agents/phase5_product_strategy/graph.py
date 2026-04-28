# ============================================================
# File: phase5_product_strategy/graph.py
# Replace full file
# Final Graph + Save Output Node
# ============================================================

from langgraph.graph import StateGraph, END
import os
import json

from .state import ProductStrategyState

# Agents
from .agents.constraint_agent import run_constraint_agent
from .agents.feature_discovery_agent import run_feature_discovery_agent
from .agents.ruthless_scope_killer import run_ruthless_scope_killer
from .agents.mvp_scope_agent import run_mvp_scope_agent
from .agents.prioritization_agent import run_prioritization_agent
from .agents.roadmap_agent import run_roadmap_agent
from .agents.build_spec_agent import run_build_spec_agent


# ============================================================
# HELPERS
# ============================================================

def clean_json(obj):
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, list):
        return [clean_json(x) for x in obj]

    if isinstance(obj, dict):
        return {str(k): clean_json(v) for k, v in obj.items()}

    if hasattr(obj, "content"):
        return str(obj.content)

    return str(obj)


def save_output_node(state):
    """
    Final save node
    """

   

    payload = {
        "mvp_scope": state.get("mvp_scope", {}),
        "prioritized_features": state.get(
            "prioritized_features", {}
        ),
        "product_roadmap": state.get("roadmap", {}),
        "build_specification": state.get(
            "build_specification", {}
        ),

        "meta": {
            "surviving_features": state.get(
                "surviving_features", []
            ),
            "killed_features": state.get(
                "killed_features", []
            ),
            "logs": state.get("logs", []),
            "errors": state.get("errors", [])
        }
    }

    filename = state["filename"]

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            clean_json(payload),
            f,
            indent=2,
            ensure_ascii=False
        )

    return {
        "saved_file": filename
    }


# ============================================================
# GRAPH
# ============================================================

def build_phase5_graph():
    graph = StateGraph(ProductStrategyState)

    # Nodes
    graph.add_node(
        "constraints",
        run_constraint_agent
    )

    graph.add_node(
        "feature_discovery",
        run_feature_discovery_agent
    )

    graph.add_node(
        "scope_killer",
        run_ruthless_scope_killer
    )

    graph.add_node(
        "mvp_scope",
        run_mvp_scope_agent
    )

    graph.add_node(
        "prioritization",
        run_prioritization_agent
    )

    graph.add_node(
        "roadmap",
        run_roadmap_agent
    )

    graph.add_node(
        "build_spec",
        run_build_spec_agent
    )

    graph.add_node(
        "save_output",
        save_output_node
    )

    # Entry
    graph.set_entry_point("constraints")

    # Flow
    graph.add_edge(
        "constraints",
        "feature_discovery"
    )

    graph.add_edge(
        "feature_discovery",
        "scope_killer"
    )

    graph.add_edge(
        "scope_killer",
        "mvp_scope"
    )

    graph.add_edge(
        "mvp_scope",
        "prioritization"
    )

    graph.add_edge(
        "prioritization",
        "roadmap"
    )

    graph.add_edge(
        "roadmap",
        "build_spec"
    )

    graph.add_edge(
        "build_spec",
        END
    )

    # graph.add_edge(
    #     "save_output",
    #     END
    # )

    return graph.compile()