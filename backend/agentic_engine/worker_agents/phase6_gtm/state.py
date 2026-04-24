# ============================================================
# File: phase6_gtm/state.py
# LangGraph Shared State
# ============================================================

from typing import TypedDict, Dict, Any


class GTMState(TypedDict, total=False):

    # Inputs from previous phase
    mvp_scope: Dict[str, Any]
    icp: Dict[str, Any]
    core_value_proposition: Dict[str, Any]
    pricing_strategy: Dict[str, Any]

    # External Inputs
    marketing_budget: Dict[str, Any]
    channel_access: Dict[str, Any]
    sales_resources: Dict[str, Any]
    brand_assets: Dict[str, Any]
    partnerships: Dict[str, Any]

    # Shared Research Memory
    market_intelligence: Dict[str, Any]

    # Outputs
    launch_plan: Dict[str, Any]
    acquisition_channel_plan: Dict[str, Any]
    messaging_strategy: Dict[str, Any]
    initial_sales_funnel: Dict[str, Any]

    # Final
    final_output: Dict[str, Any]