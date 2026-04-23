# ============================================================
# File: phase2_validation/utils/json_parser.py
# ============================================================

import json
import re


def extract_json(text: str):
    """
    Safe JSON extraction from LLM output.
    """

    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return {"raw_output": text}