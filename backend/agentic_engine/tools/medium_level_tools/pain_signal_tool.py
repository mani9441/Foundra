"""

INPUT problem/topic
   ↓
search complaints online
   ↓
collect frustration signals
   ↓
summarize recurring pain
   ↓
score severity
   ↓
return structured pain report

"""


from typing import TypedDict, Dict, Any, List
from langgraph.graph import StateGraph, START, END

from ..low_level_tools.basic_tools import *

# ==========================================
# STATE
# ==========================================

class PainState(TypedDict, total=False):
    topic: str
    search_results: str
    complaints_summary: str
    pain_points: str
    sentiment_report: str
    severity_score: int
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
# NODE 1: SEARCH COMPLAINTS
# ==========================================

def search_node(state):
    try:
        topic = state["topic"]

        query = (
            f"{topic} problems complaints frustrating "
            f"reddit review issues users hate"
        )

        result = web_search.invoke(query)

        state["search_results"] = result
        return state

    except Exception as e:
        return add_error(state, f"search_node: {str(e)}")


# ==========================================
# NODE 2: SUMMARIZE COMPLAINTS
# ==========================================

def summary_node(state):
    try:
        result = summarize_text.invoke(
            state["search_results"]
        )

        state["complaints_summary"] = result
        return state

    except Exception as e:
        return add_error(state, f"summary_node: {str(e)}")


# ==========================================
# NODE 3: EXTRACT PAIN THEMES
# ==========================================

def pain_extract_node(state):
    try:
        prompt = f"""
Extract recurring user pain points.

Text:
{state["complaints_summary"]}

Return:
- repeated complaints
- emotional frustrations
- workflow pain
- unmet needs
"""

        result = extract_key_points.invoke(prompt)

        state["pain_points"] = result
        return state

    except Exception as e:
        return add_error(
            state,
            f"pain_extract_node: {str(e)}"
        )


# ==========================================
# NODE 4: SENTIMENT / PAIN LEVEL
# ==========================================

def sentiment_node(state):
    try:
        result = sentiment_analysis.invoke(
            state["pain_points"]
        )

        state["sentiment_report"] = result
        return state

    except Exception as e:
        return add_error(
            state,
            f"sentiment_node: {str(e)}"
        )


# ==========================================
# NODE 5: SCORE
# ==========================================

def score_node(state):
    try:
        text = (
            state.get("pain_points", "") +
            " " +
            state.get("sentiment_report", "")
        ).lower()

        score = 4

        if "high" in text:
            score += 3

        if "repeated" in text:
            score += 1

        if "frustrat" in text:
            score += 1

        if "urgent" in text:
            score += 1

        if score > 10:
            score = 10

        state["severity_score"] = score
        return state

    except Exception as e:
        return add_error(
            state,
            f"score_node: {str(e)}"
        )


# ==========================================
# NODE 6: REPORT
# ==========================================

def report_node(state):
    state["final_report"] = {
        "topic": state.get("topic", ""),
        "pain_points": state.get("pain_points", ""),
        "sentiment": state.get(
            "sentiment_report", ""
        ),
        "severity_score": state.get(
            "severity_score", 0
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
    graph = StateGraph(PainState)

    graph.add_node("search", search_node)
    graph.add_node("summary", summary_node)
    graph.add_node("extract", pain_extract_node)
    graph.add_node("sentiment", sentiment_node)
    graph.add_node("score", score_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "search")
    graph.add_edge("search", "summary")
    graph.add_edge("summary", "extract")
    graph.add_edge("extract", "sentiment")
    graph.add_edge("sentiment", "score")
    graph.add_edge("score", "report")
    graph.add_edge("report", END)

    return graph.compile()


pain_signal_tool = build_graph()


def run_pain_signal(topic: str):
    return pain_signal_tool.invoke(
        {
            "topic": topic
        }
    )