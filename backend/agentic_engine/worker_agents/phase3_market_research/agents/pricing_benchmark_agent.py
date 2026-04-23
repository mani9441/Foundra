# ============================================================
# File: phase3_market_research/agents/pricing_benchmark_agent.py
# Pricing Intelligence Agent
# ============================================================

from langchain.chat_models import init_chat_model
from ..state import MarketResearchState
from ..tools.atomic.search_tool import web_search

from backend.agentic_engine.LLMs.llm import get_llm
llm =  get_llm()


def run_pricing_benchmark_agent(state: MarketResearchState):

    concept = state["validated_solution_concept"]

    search_results = web_search.invoke(
        f"{concept} pricing plans SaaS pricing competitors"
    )

    context = "\n".join(
        [f"{r['title']} | {r['snippet']}" for r in search_results]
    )

    prompt = f"""
You are a SaaS pricing strategist.

Startup Idea:
{concept}

Market Pricing Data:
{context}

Generate JSON:
{{
 "pricing_models": [],
 "benchmark_range": "...",
 "recommended_entry_price": "...",
 "freemium_needed": true,
 "logic": "..."
}}
"""

    result = llm.invoke(prompt).content
    state["pricing_benchmarks"] = {"raw": result}

    return state