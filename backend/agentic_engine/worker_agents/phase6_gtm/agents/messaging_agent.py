# ============================================================
# Messaging Strategy Agent
# ============================================================

import json

from ..tools.medium.copy_generation_tool import copy_generation_tool


def run_messaging_agent(state):

    product = json.dumps(state.get("mvp_scope", {}))
    icp = json.dumps(state.get("icp", {}))
    value_prop = json.dumps(state.get("core_value_proposition", {}))

    audience = json.dumps(
        state.get("market_intelligence", {}).get("audience_research", {})
    )

    result = copy_generation_tool(
        product=product,
        icp=icp,
        value_prop=value_prop,
        audience_insights=audience
    )

    return {
        "messaging_strategy": result
    }