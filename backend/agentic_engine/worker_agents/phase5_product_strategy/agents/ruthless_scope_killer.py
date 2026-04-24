# ============================================================
# File: phase5_product_strategy/agents/ruthless_scope_killer.py
# Replace full file
# Fix: robust LLM JSON parsing
# ============================================================

import json
import re

from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


# ============================================================
# HELPERS
# ============================================================

def extract_json(text: str):
    if not text:
        return {}

    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    return {
        "surviving_features": [],
        "killed_features": [],
        "reasoning": "fallback"
    }


# ============================================================
# MAIN AGENT
# ============================================================

def run_ruthless_scope_killer(state):
    features = state["feature_pool"]["all_features"]
    constraints = state["constraints"]
    inputs = state["inputs"]

    prompt = f"""
You are a ruthless startup advisor.

Return ONLY valid JSON.

PRIMARY VALUE:
{inputs.get("core_value_proposition","")}

FEATURES:
{json.dumps(features, indent=2)}

CONSTRAINTS:
{json.dumps(constraints, indent=2)}

Kill:
- nice to have
- slow to build
- expensive
- low impact
- vanity features

Return:

{{
  "surviving_features": [],
  "killed_features": [],
  "reasoning": ""
}}
"""

    result = llm.invoke(prompt)

    raw = (
        result.content
        if hasattr(result, "content")
        else str(result)
    )

    data = extract_json(raw)

    surviving = data.get("surviving_features", [])
    killed = data.get("killed_features", [])

    # hard fallback if model weak
    if not surviving and features:
        surviving = features[:5]
        killed = features[5:]

    state["surviving_features"] = surviving
    state["killed_features"] = killed

    state["logs"].append(
        "Ruthless Scope Killer completed."
    )

    return state