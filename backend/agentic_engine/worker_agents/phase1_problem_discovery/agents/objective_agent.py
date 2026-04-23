from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def run_objective_agent(state):
    problem = state["problem_statement"]

    prompt = f"""
Create a clear startup mission objective based on:

{problem}

Return one concise sentence.
"""

    response = llm.invoke(prompt)

    return {
        "objective": response.content.strip()
    }