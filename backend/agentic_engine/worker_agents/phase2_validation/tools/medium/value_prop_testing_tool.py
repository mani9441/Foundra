# ============================================================
# File: phase2_validation/tools_medium/value_prop_testing_tool.py
# ============================================================

from typing import Dict, Any

from ...llm import get_llm
from ...utils.json_parser import extract_json


def run_value_prop_testing(
    problem: str,
    solution: str,
    alternatives: list
) -> Dict[str, Any]:
    """
    Generate multiple value props and rank.
    """

    llm = get_llm()

    prompt = f"""
Create 5 startup value proposition angles.

Problem:
{problem}

Solution:
{solution}

Alternatives:
{alternatives}

Return JSON:
{{
 "angles":[
   {{"headline":"","score":0}},
   {{"headline":"","score":0}}
 ],
 "winner":"",
 "reason":""
}}
"""

    result = llm.invoke(prompt)
    return extract_json(result.content)