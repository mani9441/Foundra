from typing import TypedDict, List, Dict, Any


class DiscoveryState(TypedDict):
    founder_input: str

    search_results: List[str]
    complaints: List[str]

    problem_statement: str
    target_users: List[str]

    pain_evidence: Dict[str, Any]
    alternatives: Dict[str, Any]

    objective: str

    final_decision: Dict[str, Any]

    retry_count: int
    max_retries: int