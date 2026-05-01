# ============================================================
# File: phase3_market_research/agents/competitor_map_agent.py
# Competitor Discovery Agent
# ============================================================

from langchain.chat_models import init_chat_model
from ..state import MarketResearchState
from ..tools.atomic.search_tool import web_search

from ..llm import get_llm
llm =  get_llm()


def run_competitor_map_agent(state: MarketResearchState):

    concept = state["validated_solution_concept"]

    search_results = web_search.invoke(
        f"best startups companies tools like {concept}"
    )

    context = "\n".join(
        [f"{r['title']} | {r['snippet']}" for r in search_results]
    )

    prompt = f"""
You are a market intelligence analyst.

Startup Idea:
{concept}

Search Data:
{context}

Find:
1. Direct competitors
2. Indirect competitors
3. Emerging startups
4. Their common weaknesses

Return JSON.
"""

    result = llm.invoke(prompt).content
    state["competitor_map"] = {"raw": result}

    return state