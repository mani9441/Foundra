# ============================================================
# File: phase2_validation/tools_atomic/pricing_lookup.py
# REAL TOOL - scrape pricing page
# ============================================================

import re
from typing import Dict, Any
from langchain.tools import tool
from bs4 import BeautifulSoup

from ..atomic.base_http import SESSION


@tool("pricing_lookup_tool")
def pricing_lookup_tool(url: str) -> Dict[str, Any]:
    """
    Input:
        pricing page URL
    """

    try:
        r = SESSION.get(url, timeout=8)

        soup = BeautifulSoup(r.text[:300000], "html.parser")

        text = soup.get_text(" ", strip=True)

        prices = re.findall(
            r'[$₹€]\s?\d+(?:\.\d{1,2})?',
            text
        )

        unique_prices = list(dict.fromkeys(prices))[:10]

        return {
            "url": url,
            "prices_found": unique_prices,
            "pricing_detected": len(unique_prices) > 0
        }

    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }