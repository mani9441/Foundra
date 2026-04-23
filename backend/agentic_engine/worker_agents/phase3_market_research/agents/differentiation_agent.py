# ============================================================
# File: phase3_market_research/agents/differentiation_agent.py
# Market Gap / Differentiation Agent
# ============================================================

from langchain.chat_models import init_chat_model
from ..state import MarketResearchState

from backend.agentic_engine.LLMs.llm import get_llm
llm =  get_llm()


def run_differentiation_agent(state: MarketResearchState):

    concept = state["validated_solution_concept"]
    competitor_map = state.get("competitor_map", {})
    niche = state.get("niche_segment", {})

    prompt = f"""
You are a startup positioning expert.

Startup Idea:
{concept}

Competitor Data:
{competitor_map}

Niche Segment:
{niche}

Find whitespace opportunities.

Return JSON:
{{
 "positioning_statement": "...",
 "unique_angles": [],
 "market_gaps": [],
 "defensibility_score": 0.0
}}
"""

    result = llm.invoke(prompt).content
    state["differentiation_opportunity"] = {"raw": result}

    return state