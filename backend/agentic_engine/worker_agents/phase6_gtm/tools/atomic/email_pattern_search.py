# ============================================================
# File: phase6_gtm/tools/atomic/email_pattern_search.py
# Search winning cold email templates/patterns
# ============================================================

from .web_search import web_search


def email_pattern_search(audience: str, max_results: int = 8):
    """
    Example:
    SaaS founders cold email examples
    """

    query = f"{audience} cold email examples templates best performing"

    return web_search(query=query, max_results=max_results)