from ...llm import get_llm
from ...utils.json_parser import safe_json_parse

llm = get_llm()


def run_pricing_research(inputs: dict, competitor_data: dict):
    prompt = f"""
You are a SaaS pricing strategist.

Inputs:
{inputs}

Competitor Insights:
{competitor_data}

Determine best pricing opportunities.

Return ONLY JSON:
{{
  "recommended_model": "",
  "starter_range": "",
  "pro_range": "",
  "enterprise_range": "",
  "pricing_logic": [],
  "discount_strategy": []
}}
"""

    result = llm.invoke(prompt)
    return safe_json_parse(result)