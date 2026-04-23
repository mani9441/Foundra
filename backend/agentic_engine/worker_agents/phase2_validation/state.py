# ============================================================
# File: phase2_validation/state.py
# ============================================================

from typing import TypedDict, List, Dict, Any, Optional


class ValidationState(TypedDict, total=False):
    # INPUTS
    problem_statement: str
    target_user_segment: str
    pain_evidence: List[str]
    existing_alternatives: List[str]

    founder_solution_ideas: List[str]
    team_constraints: List[str]
    basic_market_context: str
    prototype_mockup_capability: str

    # RESEARCH OUTPUTS
    market_research: Dict[str, Any]
    competitor_analysis: Dict[str, Any]
    demand_validation: Dict[str, Any]

    # AGENT OUTPUTS
    validated_solution_concept: Dict[str, Any]
    icp: Dict[str, Any]
    demand_signals: Dict[str, Any]
    core_value_proposition: Dict[str, Any]

    board_debate: List[Dict[str, Any]]

    # FINAL
    proceed_pivot_reject: Dict[str, Any]

    # META
    errors: List[str]
    logs: List[str]

    # IMPORTANT ADD THESE
    final_json: Dict[str, Any]
    saved_file: str