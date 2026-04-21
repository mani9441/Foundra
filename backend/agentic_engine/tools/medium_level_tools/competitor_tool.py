"""

INPUT niche / idea
   ↓
search web
   ↓
identify competitor names
   ↓
summarize offerings
   ↓
extract weaknesses
   ↓
detect market gaps
   ↓
return structured report

"""

from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, START, END

from ..low_level_tools.basic_tools import *


# ==========================================
# STATE
# ==========================================

class CompetitorState(TypedDict, total=False):
    niche: str
    search_results: str
    summary: str
    competitors: str
    weaknesses: str
    market_gaps: str
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

        query = f"best companies startups tools for {niche}"

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

        state["summary"] = result
        return state

    except Exception as e:
        return add_error(state, f"summary_node: {str(e)}")


# ==========================================
# NODE 3: COMPETITORS
# ==========================================

def competitor_extract_node(state):
    try:
        prompt = f"""
Extract likely competitors from this market summary.

Return:
- names
- short description
- pricing clues if visible

Text:
{state["summary"]}
"""

        result = extract_key_points.invoke(prompt)

        state["competitors"] = result
        return state

    except Exception as e:
        return add_error(
            state,
            f"competitor_extract_node: {str(e)}"
        )


# ==========================================
# NODE 4: WEAKNESSES
# ==========================================

def weakness_node(state):
    try:
        prompt = f"""
Based on these competitors, infer common weaknesses.

Competitors:
{state["competitors"]}

Return bullet points.
"""

        result = extract_key_points.invoke(prompt)

        state["weaknesses"] = result
        return state

    except Exception as e:
        return add_error(state, f"weakness_node: {str(e)}")


# ==========================================
# NODE 5: MARKET GAPS
# ==========================================

def gap_node(state):
    try:
        prompt = f"""
Find whitespace market opportunities.

Competitors:
{state["competitors"]}

Weaknesses:
{state["weaknesses"]}

Return opportunities where new startup can win.
"""

        result = extract_key_points.invoke(prompt)

        state["market_gaps"] = result
        return state

    except Exception as e:
        return add_error(state, f"gap_node: {str(e)}")


# ==========================================
# NODE 6: REPORT
# ==========================================

def report_node(state):
    state["final_report"] = {
        "niche": state.get("niche", ""),
        "competitors": state.get("competitors", ""),
        "weaknesses": state.get("weaknesses", ""),
        "market_gaps": state.get("market_gaps", ""),
        "raw_results": state.get("search_results", ""),
        "errors": state.get("errors", [])
    }

    return state


# ==========================================
# BUILD GRAPH
# ==========================================

def build_graph():
    graph = StateGraph(CompetitorState)

    graph.add_node("search", search_node)
    graph.add_node("summary", summary_node)
    graph.add_node("extract", competitor_extract_node)
    graph.add_node("weakness", weakness_node)
    graph.add_node("gap", gap_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "summary")
    graph.add_edge("summary", "extract")
    graph.add_edge("extract", "weakness")
    graph.add_edge("weakness", "gap")
    graph.add_edge("gap", "report")
    graph.add_edge("report", END)

    return graph.compile()


competitor_tool = build_graph()


def run_competitor_tool(niche: str):
    return competitor_tool.invoke(
        {
            "niche": niche
        }
    )