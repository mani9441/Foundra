# ============================================================
# File: phase5_product_strategy/run_phase5_from_phase4.py
# Reads Phase 4 JSON output and converts into Phase 5 inputs
# Input file example:
# Pasted code.json
# ============================================================

import json
from typing import Dict, Any

from .graph import build_phase5_graph


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


# ============================================================
# EXTRACT PHASE 4 -> PHASE 5
# ============================================================

def extract_phase4_to_phase5(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Phase 4 output into Phase 5 required schema
    """

    # ------------------------------------------------
    # Revenue Model
    # ------------------------------------------------
    revenue_model = data.get("revenue_model", {})
    revenue_model_text = safe_text(revenue_model)

    # ------------------------------------------------
    # Pricing Strategy
    # ------------------------------------------------
    pricing_strategy = data.get("pricing_strategy", {})
    pricing_strategy_text = safe_text(pricing_strategy)

    # ------------------------------------------------
    # Best Segment => ICP
    # ------------------------------------------------
    research = data.get("research", {})
    segment_analysis = research.get("segment_analysis", {})

    icp = {
        "target_segment": segment_analysis.get("best_segment", ""),
        "segment_size": segment_analysis.get("segment_size", ""),
        "pain_level": segment_analysis.get("pain_level", ""),
        "ability_to_pay": segment_analysis.get("ability_to_pay", ""),
        "why_best": segment_analysis.get("why_best", "")
    }

    # ------------------------------------------------
    # Validated Solution Concept
    # ------------------------------------------------
    validated_solution_concept = (
        segment_analysis.get("best_segment", "") +
        " booking / workflow / marketplace platform"
    )

    # ------------------------------------------------
    # Core Value Proposition
    # ------------------------------------------------
    viability = data.get("viability_decision", {})

    opportunities = viability.get("opportunities", [])

    core_value_proposition = " | ".join(
        safe_list(opportunities)
    )

    if not core_value_proposition.strip():
        core_value_proposition = (
            "Solve major pain point faster and cheaper"
        )

    # ------------------------------------------------
    # Risk Signals -> technical constraints
    # ------------------------------------------------
    unit_economics = data.get("unit_economics_model", {})
    risk_flags = unit_economics.get("risk_flags", [])

    technical_constraints = safe_list(risk_flags)

    # ------------------------------------------------
    # Budget Guessing by Viability Confidence
    # ------------------------------------------------
    confidence = float(data.get("confidence_score", 0.6))

    if confidence < 0.45:
        budget = 50000
    elif confidence < 0.70:
        budget = 100000
    else:
        budget = 250000

    # ------------------------------------------------
    # Final Payload
    # ------------------------------------------------
    payload = {
        "validated_solution_concept": validated_solution_concept,
        "icp": icp,
        "core_value_proposition": core_value_proposition,
        "revenue_model": revenue_model_text,
        "pricing_strategy": pricing_strategy_text,

        # external runtime assumptions
        "team_skills": [
            "python",
            "fastapi",
            "react",
            "postgresql"
        ],
        "engineering_capacity": 2,
        "budget": budget,
        "time_constraints_weeks": 6,
        "technical_constraints": technical_constraints,

        # carry forward context
        "phase4_decision": viability,
        "phase4_confidence_score": confidence
    }

    return payload


# ============================================================
# MAIN RUNNER
# ============================================================

def run_from_phase4_file(file_path: str):
    """
    Reads phase4 json and runs phase5
    """

    with open(file_path, "r", encoding="utf-8") as f:
        phase4_data = json.load(f)

    phase5_input = extract_phase4_to_phase5(phase4_data)

    app = build_phase5_graph()

    result = app.invoke({
        "inputs": phase5_input,
        "logs": [],
        "errors": []
    })

    print(json.dumps(result, indent=2, ensure_ascii=False))


# ============================================================
# CLI
# ============================================================

# if __name__ == "__main__":
#     run_from_phase4_file("Pasted code.json")