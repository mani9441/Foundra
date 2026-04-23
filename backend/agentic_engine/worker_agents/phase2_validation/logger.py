# ============================================================
# File: phase2_validation/utils/logger.py
# ============================================================

from datetime import datetime


def log(state: dict, message: str):
    if "logs" not in state:
        state["logs"] = []

    ts = datetime.utcnow().isoformat()
    state["logs"].append(f"{ts} | {message}")
    return state