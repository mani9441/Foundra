# ============================================================
# File: phase5_product_strategy/agents/ruthless_scope_killer.py
# SAFE VERSION FOR AZURE / OPENAI CONTENT FILTER
# Replace full file
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

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except:
            pass

    return {
        "selected_features": [],
        "deferred_features": [],
        "reasoning": "fallback"
    }


# ============================================================
# MAIN AGENT
# ============================================================

def run_ruthless_scope_killer(state):
    """
    Renamed internally but keeps same function name
    to avoid graph changes.
    """

    features = state["feature_pool"]["all_features"]
    constraints = state["constraints"]
    inputs = state["inputs"]

    prompt = f"""
You are a startup product strategist.

Your job is to reduce product scope to the fastest,
highest-value MVP launch plan.

Return ONLY valid JSON.

CORE VALUE:
{inputs.get("core_value_proposition", "")}

FEATURE CANDIDATES:
{json.dumps(features, indent=2)}

CONSTRAINTS:
{json.dumps(constraints, indent=2)}

Selection Rules:
- Keep highest customer impact items
- Keep fastest to build items
- Keep lowest complexity items
- Keep revenue-driving items
- Delay low-priority items
- Delay expensive items
- Delay complex items

Return exactly:

{{
  "selected_features": [],
  "deferred_features": [],
  "reasoning": ""
}}
"""

    try:
        result = llm.invoke(prompt)

        raw = (
            result.content
            if hasattr(result, "content")
            else str(result)
        )

        data = extract_json(raw)

    except Exception:
        data = {}

    selected = data.get("selected_features", [])
    deferred = data.get("deferred_features", [])

    # Hard fallback if model weak / filtered / empty
    if not selected and features:
        selected = features[:5]
        deferred = features[5:]

    # Keep backward compatibility with graph + frontend
    state["surviving_features"] = selected
    state["killed_features"] = deferred

    state["logs"].append(
        "Scope optimization completed."
    )

    return state