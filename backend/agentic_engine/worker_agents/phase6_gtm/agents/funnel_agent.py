# ============================================================
# Funnel Agent
# ============================================================

import json

from ..tools.medium.funnel_design_tool import funnel_design_tool


def run_funnel_agent(state):

    product = json.dumps(state.get("mvp_scope", {}))
    price = json.dumps(state.get("pricing_strategy", {}))

    channels = json.dumps(
        state.get("acquisition_channel_plan", {})
    )

    icp = json.dumps(state.get("icp", {}))

    result = funnel_design_tool(
        product=product,
        price=price,
        channels=channels,
        icp=icp
    )

    return {
        "initial_sales_funnel": result
    }