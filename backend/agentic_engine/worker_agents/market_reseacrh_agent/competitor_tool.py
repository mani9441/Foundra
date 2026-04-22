from tavily import TavilyClient
from google import genai
import os
from dotenv import load_dotenv
import json
import time

load_dotenv("backend/agentic_engine/worker_agents/market_reseacrh_agent/.env")

# Init APIs
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))



def clean_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text

from backend.agentic_engine.worker_agents.market_reseacrh_agent.llm import llm


#  NEW: Retry + fallback LLM call
def call_llm_with_retry(prompt):
    return llm(prompt)

    


def competitor_research(idea: str):
    queries = [
        f"top companies like {idea}",
        f"apps similar to {idea}",
        f"startups in {idea} market",
        f"alternatives to {idea}",
        f"best {idea} apps 2025"
    ]

    all_results = []

    # Multi-query search
    for query in queries:
        search_results = tavily.search(query=query, max_results=3)

        for result in search_results["results"]:
            all_results.append(
                f"{result['title']}: {result['content']}"
            )

    raw_data = "\n".join(all_results)

    # Gemini analysis
    prompt = f"""
    You are a startup market analyst.

    From the data below, identify TRUE competitors.

    IMPORTANT:
    - Only include real product companies or apps
    - Exclude service providers and agencies
    - Focus on direct competitors
    - Prefer well-known products

    DATA:
    {raw_data}

    Return STRICT JSON:
    {{
      "competitors": [
        {{
          "name": "",
          "description": "",
          "strength": "",
          "weakness": ""
        }}
      ]
    }}
    """

    #  Use retry function
    response_text = call_llm_with_retry(prompt)

    if not response_text:
        return {"error": "LLM failed completely"}

    try:
        cleaned = clean_json(response_text)
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": str(e),
            "raw_output": response_text
        }