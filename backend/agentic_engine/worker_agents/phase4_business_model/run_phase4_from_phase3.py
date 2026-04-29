# ============================================================
# File: phase4_business_model/run_phase4_from_phase3.py
# Reads Phase 3 JSON output and converts into Phase 4 inputs
# Input file example:
# Pasted code.json
# ============================================================

import json
from typing import Dict, Any

from .run import run_phase4


# ============================================================
# HELPERS
# ============================================================

def safe_text(value):
    """
    Convert any type into string safely.
    """
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)

    if isinstance(value, list):
        return ", ".join([str(v) for v in value])

    return str(value)


def safe_list(value):
    """
    Convert any type into list safely.
    """
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return [json.dumps(value, ensure_ascii=False)]

    if isinstance(value, str):
        return [value]

    return [str(value)]


def try_extract_json(raw_value):
    """
    If phase output contains {"raw": "...json text..."}
    return parsed json when possible.
    """
    if isinstance(raw_value, dict) and "raw" in raw_value:
        txt = raw_value["raw"]

        start = txt.find("{")
        end = txt.rfind("}")

        if start != -1 and end != -1 and end > start:
            block = txt[start:end + 1]

            try:
                return json.loads(block)
            except:
                return raw_value

    return raw_value


# ============================================================
# CORE CONVERTER
# ============================================================

def extract_phase3_to_phase4(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Phase 3 output into Phase 4 schema.
    """

    # ------------------------------------------------
    # Niche Segment
    # ------------------------------------------------
    niche_raw = data.get("niche_segment", {})
    niche_segment = safe_text(
        niche_raw.get("raw", niche_raw)
        if isinstance(niche_raw, dict)
        else niche_raw
    )

    # ------------------------------------------------
    # Pricing Benchmarks
    # ------------------------------------------------
    pricing_raw = data.get("pricing_benchmarks", {})
    pricing_parsed = try_extract_json(pricing_raw)

    # ------------------------------------------------
    # Differentiation Opportunity
    # ------------------------------------------------
    diff_raw = data.get("differentiation_opportunity", {})
    differentiation_opportunity = safe_text(
        diff_raw.get("raw", diff_raw)
        if isinstance(diff_raw, dict)
        else diff_raw
    )

    # ------------------------------------------------
    # Market Size Estimate
    # ------------------------------------------------
    market_raw = data.get("tam_sam_som", {})
    market_size_estimate = safe_text(
        market_raw.get("raw", market_raw)
        if isinstance(market_raw, dict)
        else market_raw
    )

    # ------------------------------------------------
    # Final Decision / Entry Strategy
    # ------------------------------------------------
    decision_raw = data.get("final_decision", {})
    final_decision = safe_text(
        decision_raw.get("raw", decision_raw)
        if isinstance(decision_raw, dict)
        else decision_raw
    )

    # ------------------------------------------------
    # Competitor Context
    # ------------------------------------------------
    competitor_raw = data.get("competitor_map", {})
    competitor_context = safe_text(
        competitor_raw.get("raw", competitor_raw)
        if isinstance(competitor_raw, dict)
        else competitor_raw
    )

    # ------------------------------------------------
    # Build Phase 4 Inputs
    # ------------------------------------------------
    payload = {
        # Required Previous Outputs
        "reachable_niche_segment": niche_segment,

        "pricing_benchmarks": pricing_parsed,

        "differentiation_opportunity":
            differentiation_opportunity,

        "market_size_estimate":
            market_size_estimate,

        # Derived Operational Inputs
        "cost_assumptions": {
            "platform_ops": "medium",
            "customer_support": "medium",
            "vendor_onboarding": "high",
            "marketing": "medium-high"
        },

        "delivery_model_options": [
            "mobile marketplace",
            "managed marketplace",
            "subscription membership",
            "lead generation commission"
        ],

        "industry_margin_norms": {
            "marketplace": "20%-45%",
            "subscription": "60%+",
            "services": "15%-35%"
        },

        "sales_motion_assumptions": {
            "primary_channel": "performance marketing",
            "secondary_channel": "partnerships",
            "retention_channel": "membership loyalty"
        },

        # Extra Context
        "industry": "marketplace",
        "problem_keyword":
            "car repair mechanic booking app",

        "competitor_context":
            competitor_context,

        "phase3_decision":
            final_decision
    }

    return payload


# ============================================================
# MAIN RUNNER
# ============================================================

def run_from_phase3_file(file_path: str):
    """
    Reads phase3 json and runs phase4.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        phase3_data = json.load(f)

    phase4_input = extract_phase3_to_phase4(phase3_data)

    result = run_phase4(phase4_input)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result


# ============================================================
# CLI
# ============================================================

# if __name__ == "__main__":
#     run_from_phase3_file("Pasted code.json")