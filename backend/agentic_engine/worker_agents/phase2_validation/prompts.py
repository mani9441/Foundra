# ============================================================
# File: phase2_validation/prompts.py
# ============================================================

SYSTEM_ANALYST = """
You are a world-class startup validation strategist.
Think like founder + VC + product expert + growth marketer.

Rules:
- Use evidence
- Be skeptical
- No fluff
- JSON only
"""

SOLUTION_VALIDATOR_PROMPT = """
Validate whether this startup solution solves the stated pain strongly.

Problem:
{problem}

Users:
{users}

Pain Evidence:
{pain}

Founder Ideas:
{ideas}

Competitors:
{competitors}

Return JSON:
{{
  "best_solution_concept":"",
  "why_now":"",
  "feasibility_score":0,
  "pain_solution_fit_score":0,
  "uniqueness_score":0,
  "risks":[]
}}
"""

ICP_PROMPT = """
Find best ICP.

Problem: {problem}
Users: {users}
Pain: {pain}

Return JSON:
{{
 "persona_name":"",
 "industry":"",
 "company_size":"",
 "buyer_role":"",
 "urgent_needs":[],
 "budget_power":"",
 "adoption_probability":0
}}
"""

VALUE_PROP_PROMPT = """
Create strongest value proposition.

Problem: {problem}
Pain: {pain}
Alternatives: {alts}
Solution: {solution}

Return JSON:
{{
 "headline":"",
 "one_liner":"",
 "why_better_than_alternatives":[],
 "top_3_benefits":[]
}}
"""

DECISION_PROMPT = """
You are an investment committee.

Inputs:
Solution: {solution}
ICP: {icp}
Demand: {demand}
ValueProp: {vp}

Return JSON:
{{
 "decision":"PROCEED/PIVOT/REJECT",
 "confidence":0,
 "reasons":[],
 "next_actions":[]
}}
"""