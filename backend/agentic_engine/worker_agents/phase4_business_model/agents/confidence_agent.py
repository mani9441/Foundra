def run_confidence_agent(state):
    critic = state.get("critic_report", {})

    score = critic.get("score", 0.65)

    try:
        score = float(score)
    except:
        score = 0.65

    return {
        "confidence_score": max(0.0, min(score, 1.0))
    }