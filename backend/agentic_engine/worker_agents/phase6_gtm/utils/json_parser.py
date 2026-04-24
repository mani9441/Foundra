# ============================================================
# File: phase6_gtm/utils/json_parser.py
# Shared Robust JSON Parser
# ============================================================

import json
import re


def parse_llm_json(raw, fallback=None):

    if fallback is None:
        fallback = {}

    if raw is None:
        return fallback

    if hasattr(raw, "content"):
        raw = raw.content

    raw = str(raw).strip()

    if not raw:
        return fallback

    raw = raw.replace(
        "```json", ""
    ).replace(
        "```", ""
    ).strip()

    try:
        return json.loads(raw)
    except:
        pass

    match = re.search(
        r"\{.*\}",
        raw,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(
                match.group(0)
            )
        except:
            pass

    match = re.search(
        r"\[.*\]",
        raw,
        re.DOTALL
    )

    if match:
        try:
            return json.loads(
                match.group(0)
            )
        except:
            pass

    return fallback