import json
from typing import Any


def safe_json(data: Any):
    try:
        return json.loads(data)
    except:
        return data


def add_error(state, message: str):
    if "errors" not in state:
        state["errors"] = []
    state["errors"].append(message)
    return state
