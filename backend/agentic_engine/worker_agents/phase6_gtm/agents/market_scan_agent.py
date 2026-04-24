# ============================================================
# Market Scan Agent
# Builds shared market intelligence
# ============================================================

import json

from ..tools.medium.competitor_research_tool import competitor_research_tool
from ..tools.medium.channel_research_tool import channel_research_tool
from ..tools.medium.audience_research_tool import audience_research_tool


def run_market_scan_agent(state):

    mvp_scope = state.get("mvp_scope", {})
    icp = state.get("icp", {})
    value_prop = state.get("core_value_proposition", {})

    niche = json.dumps(mvp_scope)
    icp_text = json.dumps(icp)
    product = json.dumps(value_prop)

    competitor_data = competitor_research_tool(niche)
    channel_data = channel_research_tool(product, icp_text)
    audience_data = audience_research_tool(icp_text)

    return {
        "market_intelligence": {
            "competitor_research": competitor_data,
            "channel_research": channel_data,
            "audience_research": audience_data
        }
    }