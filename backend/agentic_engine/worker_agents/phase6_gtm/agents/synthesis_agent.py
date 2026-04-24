# ============================================================
# Final Output Synthesis Agent
# ============================================================

def run_synthesis_agent(state):

    return {
        "final_output": {
            "launch_plan": state.get("launch_plan", {}),
            "acquisition_channel_plan": state.get(
                "acquisition_channel_plan", {}
            ),
            "messaging_strategy": state.get(
                "messaging_strategy", {}
            ),
            "initial_sales_funnel": state.get(
                "initial_sales_funnel", {}
            )
        }
    }