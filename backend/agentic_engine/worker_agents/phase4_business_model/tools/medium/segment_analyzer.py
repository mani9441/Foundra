from ...llm import get_llm
from ...utils.json_parser import safe_json_parse

llm = get_llm()


def run_segment_analyzer(inputs: dict):
    prompt = f"""
You are a GTM strategist.

Inputs:
{inputs}

Return ONLY JSON:
{{
 "best_segment": "",
 "segment_size": "",
 "pain_level": "",
 "ability_to_pay": "",
 "why_best": ""
}}
"""

    result = llm.invoke(prompt)
    return safe_json_parse(result)