from typing import TypedDict, Dict, List, Any

class FoundraState(TypedDict):
    user_input: str
    startup_name: str
    industry: str
    
    worker_reports: Dict[str, Any]
    executive_reviews: Dict[str, Any]
    
    board_decision: str
    final_report: Dict[str, Any]
    
    logs: List[str]

    