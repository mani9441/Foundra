from typing import Any, Dict


def safe_get(d: Dict[str, Any], key: str, default=None):
    if not isinstance(d, dict):
        return default
    return d.get(key, default)


def clamp(value, low=0.0, high=1.0):
    try:
        value = float(value)
        return max(low, min(high, value))
    except:
        return low


def short_text(text: str, n: int = 300):
    if not text:
        return ""
    return text[:n]