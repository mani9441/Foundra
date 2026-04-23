from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()

def classify_problem(text: str):
    prompt = f"""
Classify startup problem category:

{text}

Choose:
B2B SaaS
Consumer
Healthcare
Finance
Marketplace
AI Tool
Productivity
Other
"""
    response = llm.invoke(prompt)
    return response.content.strip()