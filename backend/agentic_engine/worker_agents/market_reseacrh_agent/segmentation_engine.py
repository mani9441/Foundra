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


def segment_market(matrix, pricing, market, swot):
    prompt = f"""
    You are a startup market strategist.

    Based on the following data:

    Competitor Matrix:
    {json.dumps(matrix, indent=2)}

    Pricing Data:
    {json.dumps(pricing, indent=2)}

    Market Size:
    {json.dumps(market, indent=2)}

    SWOT Analysis:
    {json.dumps(swot, indent=2)}

    Identify target customer segments.

    For each segment provide:
    - name
    - description
    - needs
    - willingness_to_pay (low / medium / high)
    - preferred_features

    Return STRICT JSON:
    {{
      "segments": [
        {{
          "name": "",
          "description": "",
          "needs": "",
          "willingness_to_pay": "",
          "preferred_features": ""
        }}
      ]
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