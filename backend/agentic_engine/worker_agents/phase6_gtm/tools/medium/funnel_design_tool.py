# ============================================================
# Funnel Design Tool
# Creates sales funnel
# ============================================================

from backend.agentic_engine.LLMs.llm import get_llm
from ...utils.json_parser import parse_llm_json

llm = get_llm()


def funnel_design_tool(
    product: str,
    price: str,
    channels: str,
    icp: str
):
    prompt = f"""
You are a revenue systems strategist.

Product:
{product}

Price:
{price}

Channels:
{channels}

ICP:
{icp}

Return JSON:

{{
  "funnel_stages": [],
  "lead_capture_strategy": [],
  "followup_sequence": [],
  "close_method": [],
  "retention_plan": [],
  "kpis": {{}}
}}
"""

    raw = llm.invoke(prompt)

    return parse_llm_json(
        raw,
        {
            "funnel_stages": [],
            "lead_capture_strategy": [],
            "followup_sequence": [],
            "close_method": [],
            "retention_plan": [],
            "kpis": {}
        }
    )