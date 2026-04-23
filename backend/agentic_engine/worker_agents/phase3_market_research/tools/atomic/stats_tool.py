# ============================================================
# File: phase3_market_research/tools/stats_tool.py
# Atomic Numeric Helper Tools
# ============================================================

from langchain.tools import tool


@tool
def calculate_percentage(base: float, percent: float) -> float:
    """
    Calculate percentage of a number.
    """
    return base * (percent / 100.0)


@tool
def estimate_som(sam: float, capture_percent: float) -> float:
    """
    Estimate Obtainable Market from SAM.
    """
    return sam * (capture_percent / 100.0)