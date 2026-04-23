from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def run_problem_statement_agent(state):
    founder_input = state["founder_input"]
    pain_summary = state["pain_evidence"]["summary"]
    users = state["target_users"]

    prompt = f"""
Create a strong startup-grade problem statement.

Founder Idea:
{founder_input}

Pain Evidence:
{pain_summary}

Target Users:
{users}

Return only final problem statement.
"""

    response = llm.invoke(prompt)

    return {
        "problem_statement": response.content.strip()
    }