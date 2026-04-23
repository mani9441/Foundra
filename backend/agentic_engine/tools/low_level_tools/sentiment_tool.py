from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()

def detect_sentiment(text: str):
    prompt = f"""
Analyze sentiment of the following customer statements.

Return:
Negative %, Neutral %, Positive %

{text}
"""
    response = llm.invoke(prompt)
    return response.content