from backend.agentic_engine.tools.medium_level_tools.medium.evidence_validator import evidence_validator
from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def run_judge_agent(state):
    text = f"""
Problem:
{state['problem_statement']}

Users:
{state['target_users']}

Pain:
{state['pain_evidence']['summary']}

Alternatives:
{state['alternatives']['analysis']}

Objective:
{state['objective']}
"""

    evidence = evidence_validator(text)

    prompt = f"""
You are startup investment judge.

Evaluate this opportunity.

{text}

Evidence Check:
{evidence}

Return:

decision: Proceed / Pivot / Reject
confidence: %
reasons: bullet points
"""

    response = llm.invoke(prompt)

    return {
        "final_decision": response.content
    }