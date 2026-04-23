import json
import os

MEMORY_FILE = "outputs/discovery_memory.json"


def save_memory(data):
    os.makedirs("outputs", exist_ok=True)

    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r") as f:
        return json.load(f)