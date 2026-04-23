from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()

def extract_keywords(text: str):
    prompt = f"""
Extract only important business keywords from:

{text}

Return comma separated only.
"""
    response = llm.invoke(prompt)
    return response.content