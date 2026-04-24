def should_repair(state):
    critic = state.get("critic_report", {})
    retries = state.get("retries", 0)
    max_retries = state.get("max_retries", 2)

    approved = critic.get("approved", True)

    if approved:
        return "approved"

    if retries >= max_retries:
        return "approved"

    return "repair"