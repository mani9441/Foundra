from google import genai
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


def clean_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()
    return text

from backend.agentic_engine.worker_agents.market_reseacrh_agent.llm import llm

def call_llm(prompt):
    return llm(prompt)


def pricing_analysis(competitors):
    prompt = f"""
    You are a startup market analyst.

    Based on the competitor data below, estimate pricing models.

    Competitors:
    {competitors}

    For each competitor, identify:
    - pricing_model (subscription, freemium, one-time, etc.)
    - price_range (approx)
    - tier (low / mid / premium)

    Return STRICT JSON:
    [
      {{
        "name": "",
        "pricing_model": "",
        "price_range": "",
        "tier": ""
      }}
    ]
    """

    response = call_llm(prompt)

    if not response:
        return {"error": "LLM failed"}

    try:
        cleaned = clean_json(response)
        return json.loads(cleaned)
    except:
        return {"error": response}