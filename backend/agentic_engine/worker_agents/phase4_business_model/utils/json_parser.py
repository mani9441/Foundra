# ============================================================
# FIX FILE: phase4_business_model/utils/json_parser.py
# Replace full file
# ============================================================

import json
import re
from typing import Any, Dict


def to_text(value):
    """
    Convert LLM outputs like AIMessage safely to text.
    """

    if value is None:
        return ""

    # LangChain AIMessage
    if hasattr(value, "content"):
        return str(value.content)

    return str(value)


def extract_json_block(text: str) -> str:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return text.strip()


def repair_common_json(text: str) -> str:
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")

    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)

    return text.strip()


def safe_json_parse(value: Any) -> Dict[str, Any]:
    """
    Handles:
    - AIMessage
    - raw strings
    - dict
    """

    if isinstance(value, dict):
        return value

    text = to_text(value)

    if not text:
        return {}

    try:
        return json.loads(text)
    except:
        pass

    try:
        block = extract_json_block(text)
        block = repair_common_json(block)
        return json.loads(block)
    except:
        return {
            "raw_text": text,
            "parsed": False
        }