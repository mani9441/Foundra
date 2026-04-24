# ============================================================
# FILE: phase4_business_model/graph.py
# Replace full file
# ============================================================

from langgraph.graph import StateGraph, END
import os
import json

from .state import BusinessModelState

# Core Agents
from .agents.missing_data_agent import run_missing_data_agent
from .agents.research_agent import run_research_agent
from .agents.revenue_model_agent import run_revenue_model_agent
from .agents.pricing_agent import run_pricing_agent
from .agents.unit_economics_agent import run_unit_economics_agent
from .agents.viability_agent import run_viability_agent

# Quality Agents
from .agents.critic_agent import run_critic_agent
from .agents.repair_agent import run_repair_agent
from .agents.confidence_agent import run_confidence_agent
from .agents.explainability_agent import run_explainability_agent
from .agents.log_agent import run_log_agent

# Router
from .agents.router import should_repair


# ============================================================
# HELPERS
# ============================================================

def increment_retry(state):
    retries = state.get("retries", 0) + 1
    return {"retries": retries}


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
    os.makedirs("outputs", exist_ok=True)

    payload = {
        "revenue_model": state.get("revenue_model", {}),
        "pricing_strategy": state.get("pricing_strategy", {}),
        "unit_economics_model": state.get("unit_economics_model", {}),
        "viability_decision": state.get("viability_decision", {}),
        "confidence_score": state.get("confidence_score", 0.0),
        "research": state.get("research", {}),
        "critic_report": state.get("critic_report", {}),
        "explainability": state.get("explainability", {}),
        "logs": state.get("logs", [])
    }

    with open("outputs/phase4_result.json", "w", encoding="utf-8") as f:
        json.dump(clean_json(payload), f, indent=2, ensure_ascii=False)

    return {
        "saved_file": "outputs/phase4_result.json"
    }


# ============================================================
# GRAPH
# ============================================================

def build_graph():
    graph = StateGraph(BusinessModelState)

    # Nodes
    graph.add_node("missing_data", run_missing_data_agent)
    graph.add_node("research", run_research_agent)

    graph.add_node("revenue_model", run_revenue_model_agent)
    graph.add_node("pricing", run_pricing_agent)
    graph.add_node("economics", run_unit_economics_agent)
    graph.add_node("viability", run_viability_agent)

    graph.add_node("critic", run_critic_agent)
    graph.add_node("repair", run_repair_agent)
    graph.add_node("retry_counter", increment_retry)

    graph.add_node("confidence", run_confidence_agent)
    graph.add_node("explainability", run_explainability_agent)
    graph.add_node("logger", run_log_agent)

    # Final save node
    graph.add_node("save_output", save_output_node)

    # Entry
    graph.set_entry_point("missing_data")

    # Main Flow
    graph.add_edge("missing_data", "research")

    graph.add_edge("research", "revenue_model")
    graph.add_edge("revenue_model", "pricing")
    graph.add_edge("pricing", "economics")
    graph.add_edge("economics", "viability")

    graph.add_edge("viability", "critic")

    # Repair Loop
    graph.add_conditional_edges(
        "critic",
        should_repair,
        {
            "repair": "repair",
            "approved": "confidence"
        }
    )

    graph.add_edge("repair", "retry_counter")
    graph.add_edge("retry_counter", "critic")

    # Final Flow
    graph.add_edge("confidence", "explainability")
    graph.add_edge("explainability", "logger")
    graph.add_edge("logger", "save_output")
    graph.add_edge("save_output", END)

    return graph.compile()