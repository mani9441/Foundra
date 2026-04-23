from backend.agentic_engine.tools.medium_level_tools.medium.competitor_scan_tool import competitor_scan_tool


def run_alternatives_agent(state):
    topic = state["founder_input"]

    result = competitor_scan_tool(topic)

    return {
        "alternatives": result
    }