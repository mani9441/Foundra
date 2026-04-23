# ============================================================
# File: phase3_market_research/run_phase3_from_phase2.py
# Reads Phase 2 JSON output and converts into Phase 3 inputs
# Input file example:
# Pasted code.json
# ============================================================

import json
from typing import Dict, Any

from .graph import build_market_graph


# ============================================================
# HELPERS
# ============================================================

def safe_list(value):
    """
    Convert strings/dicts/lists into list safely.
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


def extract_phase2_to_phase3(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Phase 2 output format into Phase 3 required schema.
    """

    # ------------------------------------------------
    # Validated Solution Concept
    # ------------------------------------------------
    solution_block = data.get("validated_solution_concept", {})

    if isinstance(solution_block, dict):
        validated_solution_concept = solution_block.get(
            "best_solution_concept",
            ""
        )
    else:
        validated_solution_concept = safe_text(solution_block)

    # ------------------------------------------------
    # ICP
    # ------------------------------------------------
    icp = data.get("ICP", {})

    # ------------------------------------------------
    # Demand Signals
    # ------------------------------------------------
    demand_obj = data.get("demand_signals", {})

    demand_signals = []

    if isinstance(demand_obj, dict):
        for _, v in demand_obj.items():
            if isinstance(v, list):
                demand_signals.extend(
                    [safe_text(x) for x in v]
                )
            else:
                demand_signals.append(
                    safe_text(v)
                )
    else:
        demand_signals = safe_list(demand_obj)

    # ------------------------------------------------
    # Core Value Proposition
    # ------------------------------------------------
    cvp = data.get("core_value_proposition", {})

    if isinstance(cvp, dict):
        headline = cvp.get("headline", "")
        one_liner = cvp.get("one_liner", "")

        benefits = cvp.get("top_3_benefits", [])

        core_value_proposition = " | ".join(
            [headline, one_liner] + safe_list(benefits)
        )

    else:
        core_value_proposition = safe_text(cvp)

    # ------------------------------------------------
    # Geography
    # ------------------------------------------------
    geography = "Global"

    demo = (
        icp.get("persona_model", {})
        .get("demographics", {})
    )

    if isinstance(demo, dict):
        geography = demo.get("location", "Global")

    # ------------------------------------------------
    # Final Payload
    # ------------------------------------------------
    payload = {
        "validated_solution_concept":
            validated_solution_concept,

        "icp":
            icp,

        "demand_signals":
            demand_signals,

        "core_value_proposition":
            core_value_proposition,

        "geography":
            geography,

        # extra carry-forward context
        "phase2_decision":
            data.get("decision", {}),

        "phase2_warning":
            data.get("warning", "")
    }

    return payload


# ============================================================
# MAIN RUNNER
# ============================================================

def run_from_phase2_file(file_path: str):
    """
    Reads phase2 json and runs phase3.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        phase2_data = json.load(f)

    phase3_input = extract_phase2_to_phase3(phase2_data)

    app = build_market_graph()

    result = app.invoke(phase3_input)

    print(json.dumps(result, indent=2, ensure_ascii=False))


# ============================================================
# CLI
# ============================================================

# if __name__ == "__main__":
#     run_from_phase2_file("Pasted code.json")