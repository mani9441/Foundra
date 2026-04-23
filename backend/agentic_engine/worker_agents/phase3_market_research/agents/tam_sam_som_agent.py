# ============================================================
# File: phase3_market_research/agents/tam_sam_som_agent.py
# Market Size Estimation Agent
# ============================================================

from langchain.chat_models import init_chat_model
from ..state import MarketResearchState
from ..tools.atomic.search_tool import web_search

from backend.agentic_engine.LLMs.llm import get_llm
llm =  get_llm()


def run_tam_sam_som_agent(state: MarketResearchState):

    concept = state["validated_solution_concept"]
    geography = state.get("geography", "Global")

    search_results = web_search.invoke(
        f"{concept} software market size CAGR industry report {geography}"
    )

    context = "\n".join(
        [f"{r['title']} | {r['snippet']}" for r in search_results]
    )

    prompt = f"""
You are a top startup market analyst.

Startup Idea:
{concept}

Geography:
{geography}

Research Data:
{context}

Estimate:
1. TAM
2. SAM
3. SOM

Return JSON:
{{
 "tam": "...",
 "sam": "...",
 "som": "...",
 "logic": "...",
 "confidence": 0.0
}}
"""

    result = llm.invoke(prompt).content
    state["tam_sam_som"] = {"raw": result}

    return state