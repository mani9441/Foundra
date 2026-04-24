from datetime import datetime


def run_log_agent(state):
    logs = state.get("logs", [])

    logs.append(
        f"{datetime.now().isoformat()} | pipeline_completed"
    )

    return {"logs": logs}