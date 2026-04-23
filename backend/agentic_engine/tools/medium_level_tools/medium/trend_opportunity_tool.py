from ...low_level_tools.trends_tool import trends_tool
from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()


def trend_opportunity_tool(topic: str):
    trend_data = trends_tool(topic)

    text = "\n".join(trend_data)

    prompt = f"""
Analyze these market trend signals:

{text}

Return:
- Is demand growing?
- Why now?
- Opportunity score /10
"""

    response = llm.invoke(prompt)
    return response.content