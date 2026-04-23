# ============================================================
# File: phase2_validation/tools_atomic/google_search.py
# FREE VERSION (No SerpAPI Key Required)
# Uses DuckDuckGo Search via duckduckgo-search package
# pip install duckduckgo-search
# ============================================================

from typing import Dict, Any
from langchain.tools import tool

@tool("google_search_tool")
def google_search_tool(query: str) -> Dict[str, Any]:
    """
    Free search tool replacement using DuckDuckGo.
    """
    try:
        # The library now prefers importing DDGS directly 
        from duckduckgo_search import DDGS

        results = []
        # Initializing without the 'with' block is often more stable 
        # in newer versions, but the context manager still works.
        with DDGS() as ddgs:
            # 'keywords' is the correct argument for query strings
            search_results = ddgs.text(
                keywords=query,
                region='wt-wt', # Optional: Global region
                safesearch='moderate',
                max_results=5
            )

            for r in search_results:
                results.append({
                    "title": r.get("title", ""),
                    "link": r.get("href", ""),
                    "snippet": r.get("body", ""),
                })

        return {
            "query": query,
            "results": results
        }

    except Exception as e:
        return {
            "query": query,
            "results": [],
            "error": str(e)
        }