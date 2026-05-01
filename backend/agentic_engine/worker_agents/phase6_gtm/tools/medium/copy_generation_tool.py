# ============================================================
# Copy Generation Tool
# Messaging / ad copy / CTA
# ============================================================

from ...llm import get_llm
from ...utils.json_parser import parse_llm_json

llm = get_llm()


def copy_generation_tool(
    product: str,
    icp: str,
    value_prop: str,
    audience_insights: str
):
    prompt = f"""
You are an elite conversion copywriter.

Product:
{product}

ICP:
{icp}

Value Proposition:
{value_prop}

Audience Insights:
{audience_insights}

Return JSON:

{{
  "headlines": [],
  "pain_based_hooks": [],
  "trust_builders": [],
  "cta_lines": [],
  "cold_outreach_lines": [],
  "landing_page_copy": []
}}
"""

    raw = llm.invoke(prompt)

    return parse_llm_json(
        raw,
        {
            "headlines": [],
            "pain_based_hooks": [],
            "trust_builders": [],
            "cta_lines": [],
            "cold_outreach_lines": [],
            "landing_page_copy": []
        }
    )