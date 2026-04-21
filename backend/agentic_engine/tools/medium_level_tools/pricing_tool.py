"""

INPUT niche
   ↓
search pricing pages
   ↓
summarize pricing signals
   ↓
extract common models
   ↓
estimate realistic pricing
   ↓
return structured report

"""


from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, START, END

from ..low_level_tools.basic_tools import *

# ==========================================
# STATE
# ==========================================

class PricingState(TypedDict, total=False):
    niche: str
    search_results: str
    pricing_summary: str
    pricing_models: str
    estimated_range: str
    monetization_score: int
    final_report: Dict[str, Any]
    errors: List[str]


# ==========================================
# HELPER
# ==========================================

def add_error(state, msg):
    if "errors" not in state:
        state["errors"] = []
    state["errors"].append(msg)
    return state


# ==========================================
# NODE 1: SEARCH
# ==========================================

def search_node(state):
    try:
        niche = state["niche"]

        query = (
            f"{niche} pricing plans subscription "
            f"software cost SaaS pricing"
        )

        result = web_search.invoke(query)

        state["search_results"] = result
        return state

    except Exception as e:
        return add_error(state, f"search_node: {str(e)}")


# ==========================================
# NODE 2: SUMMARY
# ==========================================

def summary_node(state):
    try:
        result = summarize_text.invoke(
            state["search_results"]
        )

        state["pricing_summary"] = result
        return state

    except Exception as e:
        return add_error(state, f"summary_node: {str(e)}")


# ==========================================
# NODE 3: EXTRACT MODELS
# ==========================================

def models_node(state):
    try:
        prompt = f"""
Analyze this pricing summary.

Return:
- common pricing models
- free vs paid patterns
- seat based vs subscription
- enterprise pricing clues

Text:
{state['pricing_summary']}
"""

        result = extract_key_points.invoke(prompt)

        state["pricing_models"] = result
        return state

    except Exception as e:
        return add_error(state, f"models_node: {str(e)}")


# ==========================================
# NODE 4: ESTIMATE RANGE
# ==========================================

def range_node(state):
    try:
        prompt = f"""
Based on this niche and pricing patterns,
estimate realistic startup pricing ranges.

Niche:
{state['niche']}

Patterns:
{state['pricing_models']}

Return:
- freemium possible?
- starter plan range
- pro plan range
- enterprise possible?
"""

        result = extract_key_points.invoke(prompt)

        state["estimated_range"] = result
        return state

    except Exception as e:
        return add_error(state, f"range_node: {str(e)}")


# ==========================================
# NODE 5: SCORE
# ==========================================

def score_node(state):
    try:
        text = (
            state.get("pricing_models", "") +
            " " +
            state.get("estimated_range", "")
        ).lower()

        score = 5

        if "subscription" in text:
            score += 2

        if "enterprise" in text:
            score += 2

        if "freemium" in text:
            score += 1

        if score > 10:
            score = 10

        state["monetization_score"] = score
        return state

    except Exception as e:
        return add_error(state, f"score_node: {str(e)}")


# ==========================================
# NODE 6: REPORT
# ==========================================

def report_node(state):
    state["final_report"] = {
        "niche": state.get("niche", ""),
        "pricing_models": state.get(
            "pricing_models", ""
        ),
        "estimated_range": state.get(
            "estimated_range", ""
        ),
        "monetization_score": state.get(
            "monetization_score", 0
        ),
        "raw_results": state.get(
            "search_results", ""
        ),
        "errors": state.get("errors", [])
    }

    return state


# ==========================================
# BUILD GRAPH
# ==========================================

def build_graph():
    graph = StateGraph(PricingState)

    graph.add_node("search", search_node)
    graph.add_node("summary", summary_node)
    graph.add_node("models", models_node)
    graph.add_node("range", range_node)
    graph.add_node("score", score_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "summary")
    graph.add_edge("summary", "models")
    graph.add_edge("models", "range")
    graph.add_edge("range", "score")
    graph.add_edge("score", "report")
    graph.add_edge("report", END)

    return graph.compile()


pricing_tool = build_graph()


def run_pricing_tool(niche: str):
    return pricing_tool.invoke(
        {
            "niche": niche
        }
    )