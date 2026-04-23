# ============================================================
# File: phase2_validation/tools_medium/traction_score_tool.py
# Pure scoring tool
# ============================================================

from typing import Dict, Any


def run_traction_score(
    pain: int,
    urgency: int,
    willingness_to_pay: int,
    reachability: int
) -> Dict[str, Any]:
    """
    Score out of 100
    """

    raw = pain * urgency * willingness_to_pay * reachability
    score = min(100, int(raw / 100))

    return {
        "traction_score": score,
        "formula": "pain x urgency x WTP x reachability / 100"
    }