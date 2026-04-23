# ============================================================
# File: phase2_validation/utils/json_parser.py
# Robust JSON extractor for LLM outputs
# ============================================================

import json
import re
from typing import Any, Dict


def _clean_json_string(text: str) -> str:
    """
    Clean common LLM formatting issues.
    """

    text = text.strip()

    # remove markdown code fences
    text = re.sub(r"^```json", "", text.strip(), flags=re.IGNORECASE)
    text = re.sub(r"^```", "", text.strip())
    text = re.sub(r"```$", "", text.strip())

    # smart quotes
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")

    return text.strip()


def _find_json_block(text: str) -> str:
    """
    Finds first valid-looking JSON object or array block.
    """

    # object
    obj = re.search(r"\{.*\}", text, re.DOTALL)

    if obj:
        return obj.group(0)

    # array
    arr = re.search(r"\[.*\]", text, re.DOTALL)

    if arr:
        return arr.group(0)

    return text


def extract_json(text: str) -> Any:
    """
    Main parser used across all agents/tools.

    Handles:
    - raw json
    - markdown fenced json
    - extra text around json
    - malformed fallback
    """

    if text is None:
        return {}

    if not isinstance(text, str):
        return text

    cleaned = _clean_json_string(text)

    # try direct parse
    try:
        return json.loads(cleaned)
    except:
        pass

    # try extracting block
    block = _find_json_block(cleaned)

    try:
        return json.loads(block)
    except:
        pass

    # remove trailing commas
    block2 = re.sub(r",\s*([\]}])", r"\1", block)

    try:
        return json.loads(block2)
    except:
        pass

    # final fallback
    return {
        "raw_output": text,
        "parse_error": True
    }