from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def evidence_validator(claims_text: str):
    prompt = f"""
Check if these startup discovery claims are strong or weak.

Claims:
{claims_text}

Return:

Strong Evidence:
Weak Evidence:
Missing Proof:
Confidence Score /100
"""

    response = llm.invoke(prompt)
    return response.content