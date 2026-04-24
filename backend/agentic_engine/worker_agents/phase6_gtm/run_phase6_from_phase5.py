# ============================================================
# File: phase6_gtm/run_phase6_from_phase5.py
# Reads Phase 5 JSON Output and converts into Phase 6 inputs
# Then runs Phase 6 Graph
# ============================================================

import json
from typing import Dict, Any

from .graph import run_phase6


# ============================================================
# Helpers
# ============================================================

def safe_dict(value):
    """
    Ensure dictionary
    """

    if isinstance(value, dict):
        return value

    return {}


def safe_list(value):
    """
    Ensure list
    """

    if isinstance(value, list):
        return value

    return []


def estimate_budget(mvp_scope: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimate realistic GTM budget from product size
    """

    features = safe_list(
        mvp_scope.get("mvp_scope", [])
    )

    count = len(features)

    if count <= 3:
        monthly = 300

    elif count <= 6:
        monthly = 800

    else:
        monthly = 1500

    return {
        "monthly_budget_usd": monthly,
        "notes": "Auto-estimated from MVP scope size"
    }


def build_channel_access() -> Dict[str, Any]:

    return {
        "organic_channels": [
            "SEO",
            "LinkedIn",
            "Reddit",
            "Email Outreach",
            "Communities"
        ],
        "paid_channels": [
            "Google Ads",
            "Meta Ads"
        ],
        "status": "default available"
    }


def build_sales_resources() -> Dict[str, Any]:

    return {
        "founder_led_sales": True,
        "sales_team_size": 0,
        "automation_tools_allowed": True
    }


def build_brand_assets(build_spec: Dict[str, Any]) -> Dict[str, Any]:

    frontend = safe_dict(
        build_spec.get("frontend", {})
    )

    framework = frontend.get(
        "framework",
        "Web App"
    )

    return {
        "website_ready": True,
        "frontend_framework": framework,
        "landing_page_possible": True,
        "design_assets_status": "basic"
    }


def build_partnerships() -> Dict[str, Any]:

    return {
        "existing_partnerships": [],
        "strategic_targets": [
            "Local communities",
            "Influencers",
            "Affiliate partners"
        ]
    }


# ============================================================
# Phase 5 -> Phase 6 Mapping
# ============================================================

def convert_phase5_to_phase6(
    data: Dict[str, Any]
) -> Dict[str, Any]:

    mvp_scope = safe_dict(
        data.get("mvp_scope", {})
    )

    build_spec = safe_dict(
        data.get("build_specification", {})
    )

    pricing_strategy = {
        "recommended_model": "Freemium + Transaction Fee",
        "basis": "Auto-generated based on marketplace/booking style MVP"
    }

    icp = {
        "primary_users": mvp_scope.get(
            "core_problem",
            ""
        ),
        "success_metric": mvp_scope.get(
            "success_metric",
            ""
        )
    }

    core_value_proposition = {
        "statement":
        "Fast, reliable and convenient transportation booking for busy commuters."
    }

    phase6_inputs = {

        # Previous phase outputs
        "mvp_scope": mvp_scope,
        "icp": icp,
        "core_value_proposition":
        core_value_proposition,
        "pricing_strategy":
        pricing_strategy,

        # New external inputs
        "marketing_budget":
        estimate_budget(mvp_scope),

        "channel_access":
        build_channel_access(),

        "sales_resources":
        build_sales_resources(),

        "brand_assets":
        build_brand_assets(build_spec),

        "partnerships":
        build_partnerships()
    }

    return phase6_inputs


# ============================================================
# Runner
# ============================================================

def run_from_phase5_file(
    filepath: str = "outputs/phase5_result.json"
):
    """
    Read Phase 5 output file and run Phase 6
    """

    with open(
        filepath,
        "r",
        encoding="utf-8"
    ) as f:
        phase5_data = json.load(f)

    phase6_inputs = convert_phase5_to_phase6(
        phase5_data
    )

    result = run_phase6(
        phase6_inputs
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )

    return result