from backend.agentic_engine.tools.medium_level_tools.medium.complaint_research_tool import complaint_research_tool
from backend.agentic_engine.tools.medium_level_tools.medium.pain_ranker_tool import pain_ranker_tool


def run_pain_evidence_agent(state):
    topic = state["founder_input"]

    research = complaint_research_tool(topic)
    ranking = pain_ranker_tool(research["summary"])

    return {
        "pain_evidence": {
            "summary": research["summary"],
            "sentiment": research["sentiment"],
            "ranking": ranking,
            "sources": research["raw_sources"]
        }
    }