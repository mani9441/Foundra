# ============================================================
# File: phase3_market_research/agents/final_verdict_agent.py
# Final Investment Style Verdict Agent
# ============================================================

from langchain.chat_models import init_chat_model
from ..state import MarketResearchState

from ..llm import get_llm
llm =  get_llm()


def run_final_verdict_agent(state: MarketResearchState):

    prompt = f"""
You are a venture capitalist evaluating startup market attractiveness.

Inputs:

TAM/SAM/SOM:
{state.get("tam_sam_som")}

Competitors:
{state.get("competitor_map")}

Niche:
{state.get("niche_segment")}

Pricing:
{state.get("pricing_benchmarks")}

Differentiation:
{state.get("differentiation_opportunity")}

Return JSON:
{{
 "decision": "PROCEED / PIVOT / REJECT",
 "confidence": 0.0,
 "reason": "...",
 "best_entry_strategy": "...",
 "key_risks": [],
 "next_action": "..."
}}
"""

    result = llm.invoke(prompt).content
    state["final_decision"] = {"raw": result}

    return state