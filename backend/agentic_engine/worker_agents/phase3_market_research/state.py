# ============================================================
# File: phase3_market_research/state.py
# Shared LangGraph State
# ============================================================

from typing import TypedDict, Dict, Any, List, Optional


class MarketResearchState(TypedDict, total=False):
    # Inputs from previous phase
    validated_solution_concept: str
    icp: Dict[str, Any]
    demand_signals: List[str]
    core_value_proposition: str
    geography: str

    # Intermediate data
    raw_search_results: List[Dict[str, Any]]
    scraped_pages: List[Dict[str, Any]]
    market_sources: List[Dict[str, Any]]

    # Final outputs
    tam_sam_som: Dict[str, Any]
    competitor_map: Dict[str, Any]
    niche_segment: Dict[str, Any]
    pricing_benchmarks: Dict[str, Any]
    differentiation_opportunity: Dict[str, Any]

    final_decision: Dict[str, Any]