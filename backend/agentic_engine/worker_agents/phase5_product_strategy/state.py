# ============================================================
# File: phase5_product_strategy/state.py
# Final Production State Schema
# ============================================================

from typing import TypedDict, Dict, Any, List


class ProductStrategyState(TypedDict, total=False):
    # incoming
    inputs: Dict[str, Any]

    # processed
    constraints: Dict[str, Any]

    # research
    feature_pool: Dict[str, Any]

    # refined
    killed_features: List[str]
    surviving_features: List[str]

    # outputs
    mvp_scope: Dict[str, Any]
    prioritized_features: Dict[str, Any]
    roadmap: Dict[str, Any]
    build_specification: Dict[str, Any]

    # meta
    logs: List[str]
    errors: List[str]