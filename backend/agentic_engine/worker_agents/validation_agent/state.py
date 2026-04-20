from typing import TypedDict, List, Dict, Any, Optional


class ValidationState(TypedDict, total=False):
    # Raw Input
    user_input: str

    # Parsed
    parsed_idea: Dict[str, Any]
    assumptions: Dict[str, Any]

    # Worker Outputs
    problem_analysis: Dict[str, Any]
    personas: List[Dict[str, Any]]
    competitors: List[Dict[str, Any]]
    pricing_analysis: Dict[str, Any]
    market_gaps: List[str]
    interview_questions: List[str]
    skeptic_notes: List[str]
    uvp: str

    # Final
    scores: Dict[str, float]
    verdict: str
    confidence_score: int
    recommendations: List[str]

    # Export
    final_report: Dict[str, Any]

    # Runtime
    errors: List[str]