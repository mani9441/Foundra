# ============================================================
# File: phase2_validation/run_phase2_from_phase1.py
# Reads Phase 1 JSON output and converts into Phase 2 inputs
# Input file example:
# Pasted code.json
# ============================================================

import json
from typing import Dict, Any

from .graph import run_phase2


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


def extract_phase1_to_phase2(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Phase 1 output format into Phase 2 required schema.
    """

    # pain evidence can be nested dict in your sample
    pain_obj = data.get("pain_evidence", {})

    pain_evidence = []

    if isinstance(pain_obj, dict):
        for _, v in pain_obj.items():
            if isinstance(v, list):
                pain_evidence.extend(v)
            else:
                pain_evidence.append(str(v))
    else:
        pain_evidence = safe_list(pain_obj)

    # alternatives can be nested dict
    alts = data.get("alternatives", {})

    alternatives = []

    if isinstance(alts, dict):
        raw = alts.get("competitors")

        if raw:
            alternatives = safe_list(raw)
        else:
            alternatives = safe_list(alts.get("analysis", alts))
    else:
        alternatives = safe_list(alts)

    # founder solution ideas
    founder_idea = data.get("founder_input", "")

    payload = {
        "problem_statement":
            data.get("problem_statement", ""),

        "target_user_segment":
            data.get("target_users", ""),

        "pain_evidence":
            pain_evidence,

        "existing_alternatives":
            alternatives,

        "founder_solution_ideas":
            [founder_idea] if founder_idea else [],

        "team_constraints": [
            "Unknown team size",
            "Unknown budget"
        ],

        "basic_market_context":
            "Imported from Phase 1 output",

        "prototype_mockup_capability":
            "Unknown",

        # carry extra context if needed
        "phase1_objective":
            data.get("objective", ""),

        "phase1_final_decision":
            data.get("final_decision", "")
    }

    return payload


# ============================================================
# MAIN RUNNER
# ============================================================

def run_from_phase1_file(file_path: str):
    """
    Reads phase1 json and runs phase2.
    """

    with open(file_path, "r", encoding="utf-8") as f:
        phase1_data = json.load(f)

    phase2_input = extract_phase1_to_phase2(phase1_data)

    result = run_phase2(phase2_input)

    print(json.dumps(result, indent=2, ensure_ascii=False))


# ============================================================
# CLI
# ============================================================

# if __name__ == "__main__":
#     run_from_phase1_file("Pasted code.json")