"""
Workflow

INPUT topic
   ↓
web search
   ↓
collect sources
   ↓
optional scrape top URLs
   ↓
summarize evidence
   ↓
extract insights
   ↓
return structured report

"""

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, START, END

# Reusable atomic tools
from ..low_level_tools.basic_tools import *



# ==========================================
# STATE
# ==========================================

class ResearchState(TypedDict, total=False):
    topic: str
    search_results: str
    raw_sources: List[str]
    summary: str
    key_points: str
    final_report: Dict[str, Any]
    errors: List[str]


# ==========================================
# HELPERS
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
        topic = state["topic"]

        result = web_search.invoke(topic)

        state["search_results"] = result
        return state

    except Exception as e:
        return add_error(state, f"search_node: {str(e)}")


# ==========================================
# NODE 2: SUMMARIZE
# ==========================================

def summarize_node(state):
    try:
        text = state.get("search_results", "")

        result = summarize_text.invoke(text)

        state["summary"] = result
        return state

    except Exception as e:
        return add_error(state, f"summarize_node: {str(e)}")


# ==========================================
# NODE 3: EXTRACT INSIGHTS
# ==========================================

def insights_node(state):
    try:
        text = state.get("summary", "")

        result = extract_key_points.invoke(text)

        state["key_points"] = result
        return state

    except Exception as e:
        return add_error(state, f"insights_node: {str(e)}")


# ==========================================
# NODE 4: REPORT
# ==========================================

def report_node(state):
    state["final_report"] = {
        "topic": state.get("topic", ""),
        "summary": state.get("summary", ""),
        "key_points": state.get("key_points", ""),
        "raw_results": state.get("search_results", ""),
        "errors": state.get("errors", [])
    }

    return state


# ==========================================
# BUILD GRAPH
# ==========================================

def build_research_graph():
    graph = StateGraph(ResearchState)

    graph.add_node("search", search_node)
    graph.add_node("summarize", summarize_node)
    graph.add_node("insights", insights_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "summarize")
    graph.add_edge("summarize", "insights")
    graph.add_edge("insights", "report")
    graph.add_edge("report", END)

    return graph.compile()


# ==========================================
# EXPORTED TOOL
# ==========================================

research_tool = build_research_graph()


# ==========================================
# SIMPLE WRAPPER
# ==========================================

def run_research(topic: str):
    return research_tool.invoke(
        {
            "topic": topic
        }
    )