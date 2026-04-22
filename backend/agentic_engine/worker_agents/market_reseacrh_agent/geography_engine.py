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


def analyze_geography(idea: str):
    prompt = f"""
    You are a global market strategist.

    For the startup idea: "{idea}"

    Identify demand geography:

    Provide:
    - top_markets (countries with highest demand)
    - emerging_markets (fast-growing regions)
    - low_penetration_opportunities (untapped regions)
    - region_characteristics (brief explanation per region)
    - recommended_launch_regions

    Return STRICT JSON:
    {{
      "top_markets": [],
      "emerging_markets": [],
      "low_penetration_opportunities": [],
      "region_characteristics": [],
      "recommended_launch_regions": []
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