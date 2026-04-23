from backend.agentic_engine.tools.medium_level_tools.medium.user_persona_builder import user_persona_builder


def run_target_user_agent(state):
    founder_input = state["founder_input"]

    personas = user_persona_builder(founder_input)

    return {
        "target_users": personas
    }