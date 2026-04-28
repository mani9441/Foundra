# ============================================================
# File: phase3_market_research/graph.py
# Full Market Research LangGraph
# Final node saves result to outputs/phase3_result.json
# ============================================================

import os
import json

from langgraph.graph import StateGraph, END
from .state import MarketResearchState

from .agents.tam_sam_som_agent import run_tam_sam_som_agent
from .agents.competitor_map_agent import run_competitor_map_agent
from .agents.niche_segment_agent import run_niche_segment_agent
from .agents.pricing_benchmark_agent import run_pricing_benchmark_agent
from .agents.differentiation_agent import run_differentiation_agent
from .agents.final_verdict_agent import run_final_verdict_agent


def save_results_node(state: MarketResearchState):
    """
    Save final Phase 3 outputs to outputs/phase3_result.json
    """


    final_payload = {
        "tam_sam_som": state.get("tam_sam_som", {}),
        "competitor_map": state.get("competitor_map", {}),
        "niche_segment": state.get("niche_segment", {}),
        "pricing_benchmarks": state.get("pricing_benchmarks", {}),
        "differentiation_opportunity": state.get(
            "differentiation_opportunity", {}
        ),
        "final_decision": state.get("final_decision", {})
    }

    filename = state["filename"]

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(final_payload, f, indent=4, ensure_ascii=False)

    print(f"Saved: {filename}")

    return state


def build_market_graph():

    graph = StateGraph(MarketResearchState)

    graph.add_node("tam", run_tam_sam_som_agent)
    graph.add_node("competitor", run_competitor_map_agent)
    graph.add_node("niche", run_niche_segment_agent)
    graph.add_node("pricing", run_pricing_benchmark_agent)
    graph.add_node("differentiate", run_differentiation_agent)
    graph.add_node("verdict", run_final_verdict_agent)
    graph.add_node("save", save_results_node)

    graph.set_entry_point("tam")

    graph.add_edge("tam", "competitor")
    graph.add_edge("competitor", "niche")
    graph.add_edge("niche", "pricing")
    graph.add_edge("pricing", "differentiate")
    graph.add_edge("differentiate", "verdict")
    graph.add_edge("verdict", END)
    #graph.add_edge("save", END)

    return graph.compile()