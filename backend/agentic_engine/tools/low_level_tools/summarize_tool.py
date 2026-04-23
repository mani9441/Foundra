from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()

def summarize_text(text: str):
    prompt = f"""
Summarize the following research into concise bullet points.

{text}
"""
    response = llm.invoke(prompt)
    return response.content