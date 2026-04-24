from typing import TypedDict, Dict, Any, List


class BusinessModelState(TypedDict, total=False):
    # Raw Inputs
    inputs: Dict[str, Any]

    # External / Research Outputs
    research: Dict[str, Any]
    competitors: List[Dict[str, Any]]
    pricing_benchmarks: Dict[str, Any]
    economics_benchmarks: Dict[str, Any]

    # Specialist Agent Outputs
    revenue_model: Dict[str, Any]
    pricing_strategy: Dict[str, Any]
    unit_economics_model: Dict[str, Any]
    viability_decision: Dict[str, Any]

    # Executive Debate
    executive_opinions: Dict[str, Any]
    final_decision: Dict[str, Any]

    # Diagnostics
    confidence_score: float
    warnings: List[str]
    errors: List[str]
    logs: List[str]

    # Retry Control
    retries: int
    max_retries: int