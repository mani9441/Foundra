from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def pain_ranker_tool(research_text: str):
    prompt = f"""
Based on this pain research:

{research_text}

Score from 1-10:

urgency:
frequency:
willingness_to_pay:
emotional_pain:

Also give final opportunity score.
"""

    response = llm.invoke(prompt)
    return response.content