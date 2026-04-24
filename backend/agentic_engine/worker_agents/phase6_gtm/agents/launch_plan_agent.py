# ============================================================
# Launch Plan Agent
# ============================================================

import json

from ..tools.medium.launch_calendar_tool import launch_calendar_tool


def run_launch_plan_agent(state):

    mvp_scope = json.dumps(state.get("mvp_scope", {}))
    budget = json.dumps(state.get("marketing_budget", {}))
    channels = json.dumps(
        state.get("market_intelligence", {}).get("channel_research", {})
    )

    result = launch_calendar_tool(
        product=mvp_scope,
        budget=budget,
        channels=channels
    )

    return {
        "launch_plan": result
    }