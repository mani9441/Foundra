from ..tools.medium.research_bundle import run_research_bundle


def run_research_agent(state):
    inputs = state["inputs"]

    research = run_research_bundle(inputs)

    return {"research": research}