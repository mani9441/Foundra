# ============================================================
# File: phase2_validation/tools_atomic/domain_lookup.py
# REAL TOOL - WHOIS + DNS check
# ============================================================

from typing import Dict, Any
from langchain.tools import tool
import socket


@tool("domain_lookup_tool")
def domain_lookup_tool(name: str) -> Dict[str, Any]:
    """
    Checks common startup domains.
    """

    try:
        import whois
    except:
        return {
            "error": "python-whois package missing"
        }

    brand = name.lower().replace(" ", "")

    tlds = [".com", ".ai", ".io"]

    results = []

    for tld in tlds:
        domain = brand + tld

        available = False

        try:
            info = whois.whois(domain)

            if not info.domain_name:
                available = True

        except:
            available = True

        # DNS fallback
        try:
            socket.gethostbyname(domain)
            dns_live = True
        except:
            dns_live = False

        results.append(
            {
                "domain": domain,
                "available": available,
                "dns_live": dns_live
            }
        )

    return {
        "brand": name,
        "domains": results
    }