from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse

llm = get_llm()


REQUIRED_KEYS = [
    "reachable_niche_segment",
    "industry",
    "cost_assumptions",
    "sales_motion_assumptions"
]


def run_missing_data_agent(state):
    inputs = state["inputs"]

    missing = [k for k in REQUIRED_KEYS if k not in inputs]

    if not missing:
        return {"inputs": inputs}

    prompt = f"""
Infer realistic startup defaults.

Current Inputs:
{inputs}

Missing Keys:
{missing}

Return ONLY JSON object containing missing keys only.
"""

    result = llm.invoke(prompt)
    inferred = safe_json_parse(result)

    merged = {**inputs, **inferred}

    return {"inputs": merged}