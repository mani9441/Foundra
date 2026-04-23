from ...low_level_tools.google_search import google_search
from ...low_level_tools.summarize_tool import summarize_text
from  backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def competitor_scan_tool(topic: str):
    results = google_search(f"best tools apps software for {topic}")

    text = "\n".join(results)

    prompt = f"""
Analyze competitors in this market.

Data:
{text}

Return JSON style:

competitors: []
weaknesses: []
market_maturity: low/medium/high
"""

    response = llm.invoke(prompt)

    return {
        "raw_sources": results,
        "analysis": response.content
    }