from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def user_persona_builder(problem_text: str):
    prompt = f"""
Given this startup problem:

{problem_text}

Identify top 3 customer segments suffering most.

For each include:
- user type
- why they suffer
- likely budget
"""

    response = llm.invoke(prompt)
    return response.content