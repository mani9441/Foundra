# ============================================================
# File: phase6_gtm/graph.py
# LangGraph Orchestration Engine
# ============================================================

import os
import json

from langgraph.graph import StateGraph, END

from .state import GTMState

from .agents.market_scan_agent import run_market_scan_agent
from .agents.launch_plan_agent import run_launch_plan_agent
from .agents.channel_strategy_agent import run_channel_strategy_agent
from .agents.messaging_agent import run_messaging_agent
from .agents.funnel_agent import run_funnel_agent
from .agents.synthesis_agent import run_synthesis_agent


# ============================================================
# Helpers
# ============================================================

def clean_json(obj):
    """
    Ensure JSON serializable output
    """

    if isinstance(obj, dict):
        return {
            str(k): clean_json(v)
            for k, v in obj.items()
        }

    elif isinstance(obj, list):
        return [clean_json(x) for x in obj]

    elif obj is None:
        return {}

    return obj


# ============================================================
# Save Output Node
# ============================================================

def save_output_node(state):
    """
    Final save node
    """

  

    payload = {
        "launch_plan": state.get(
            "launch_plan", {}
        ),

        "acquisition_channel_plan": state.get(
            "acquisition_channel_plan", {}
        ),

        "messaging_strategy": state.get(
            "messaging_strategy", {}
        ),

        "initial_sales_funnel": state.get(
            "initial_sales_funnel", {}
        ),

        "meta": {
            "market_intelligence": state.get(
                "market_intelligence", {}
            )
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
# Graph Build
# ============================================================

builder = StateGraph(GTMState)

# Nodes
builder.add_node(
    "market_scan",
    run_market_scan_agent
)

builder.add_node(
    "launch_plan",
    run_launch_plan_agent
)

builder.add_node(
    "channel_strategy",
    run_channel_strategy_agent
)

builder.add_node(
    "messaging",
    run_messaging_agent
)

builder.add_node(
    "funnel",
    run_funnel_agent
)

builder.add_node(
    "synthesis",
    run_synthesis_agent
)

builder.add_node(
    "save_output",
    save_output_node
)


# ============================================================
# Flow
# ============================================================

builder.set_entry_point("market_scan")

# after research -> parallel workers
builder.add_edge(
    "market_scan",
    "launch_plan"
)

builder.add_edge(
    "market_scan",
    "channel_strategy"
)

builder.add_edge(
    "market_scan",
    "messaging"
)

# funnel depends on channel strategy
builder.add_edge(
    "channel_strategy",
    "funnel"
)

# workers -> synthesis
builder.add_edge(
    "launch_plan",
    "synthesis"
)

builder.add_edge(
    "messaging",
    "synthesis"
)

builder.add_edge(
    "funnel",
    "synthesis"
)

# final save
builder.add_edge(
    "synthesis",
    END
)

# builder.add_edge(
#     "save_output",
#     END
# )

# Compile
graph = builder.compile()


# ============================================================
# Runner
# ============================================================

def run_phase6(inputs: dict):
    """
    Run full Phase 6 system
    """

    return graph.invoke(inputs)