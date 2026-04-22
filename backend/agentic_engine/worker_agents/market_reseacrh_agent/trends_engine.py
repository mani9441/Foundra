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


def analyze_trends(idea: str):
    prompt = f"""
    You are a startup market trend analyst.

    Analyze the industry trends for the startup idea:
    "{idea}"

    Provide:
    - trend_direction (growing / stable / declining)
    - market_stage (emerging / growth / mature / saturated)
    - key_trends (list)
    - technological_drivers (list)
    - risks (list)
    - timing_score (1-10)
    - recommendation (is it a good time to enter?)

    Return STRICT JSON:
    {{
      "trend_direction": "",
      "market_stage": "",
      "key_trends": [],
      "technological_drivers": [],
      "risks": [],
      "timing_score": "",
      "recommendation": ""
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