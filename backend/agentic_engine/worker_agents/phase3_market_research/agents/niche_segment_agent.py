# ============================================================
# File: phase3_market_research/agents/niche_segment_agent.py
# Reachable Niche Segment Agent
# ============================================================

from langchain.chat_models import init_chat_model
from ..state import MarketResearchState

from ..llm import get_llm
llm =  get_llm()


def run_niche_segment_agent(state: MarketResearchState):

    icp = state["icp"]
    concept = state["validated_solution_concept"]
    demand = state["demand_signals"]

    prompt = f"""
You are a startup GTM strategist.

Startup Idea:
{concept}

ICP:
{icp}

Demand Signals:
{demand}

Find the most reachable niche segment
to dominate first.

Return JSON:
{{
 "best_niche": "...",
 "why": "...",
 "acquisition_channels": [],
 "difficulty": "low/medium/high"
}}
"""

    result = llm.invoke(prompt).content
    state["niche_segment"] = {"raw": result}

    return state