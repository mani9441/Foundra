# ============================================================
# File: phase5_product_strategy/tools/atomic/json_utils.py
# Shared Utility Helpers
# ============================================================

import json
import os


def safe_json_load(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_json_save(path: str, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)