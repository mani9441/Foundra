from google import genai
import os
from dotenv import load_dotenv
import json
import time




def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return text

from backend.agentic_engine.worker_agents.market_reseacrh_agent.llm import llm

def call_llm(prompt):
    return llm(prompt)


def swot_analysis(matrix, pricing, market):
    prompt = f"""
    You are a startup strategy expert.

    Based on the following data:

    Competitor Matrix:
    {json.dumps(matrix, indent=2)}

    Pricing Data:
    {json.dumps(pricing, indent=2)}

    Market Size:
    {json.dumps(market, indent=2)}

    Generate a SWOT analysis for a new startup entering this market.

    Return STRICT JSON:
    {{
      "strengths": [],
      "weaknesses": [],
      "opportunities": [],
      "threats": []
    }}
    """

    response = call_llm(prompt)

    if not response:
        return {"error": "LLM failed"}

    try:
        cleaned = clean_json(response)
        return json.loads(cleaned)
    except:
        return {"error": response}