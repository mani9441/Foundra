from google import genai
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()


from backend.agentic_engine.worker_agents.market_reseacrh_agent.llm import llm

def call_llm(prompt):
    return llm(prompt)


# NEW: Clean JSON before parsing
def clean_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    return text


def market_sizing(idea: str):
    prompt = f"""
    You are a startup market analyst.

    For the startup idea: {idea}

    Estimate:
    - TAM (Total Addressable Market)
    - SAM (Serviceable Available Market)
    - SOM (Serviceable Obtainable Market)

    Give:
    - approximate values in USD
    - short reasoning

    Return STRICT JSON:
    {{
      "TAM": "",
      "SAM": "",
      "SOM": "",
      "reasoning": ""
    }}
    """

    response = call_llm(prompt)

    if not response:
        return {"error": "LLM failed completely"}

    try:
        cleaned = clean_json(response)  
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": str(e),
            "raw_output": response
        }