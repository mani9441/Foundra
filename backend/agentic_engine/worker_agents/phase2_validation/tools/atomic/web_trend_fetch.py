# ============================================================
# File: phase2_validation/tools_atomic/web_trend_fetch.py
# REAL TOOL - Google Trends via pytrends
# ============================================================

from typing import Dict, Any
from langchain.tools import tool


@tool("web_trend_fetch_tool")
def web_trend_fetch_tool(keyword: str) -> Dict[str, Any]:
    """
    Real Google Trends fetch.
    """

    try:
        from pytrends.request import TrendReq

        pytrends = TrendReq(hl="en-US", tz=330)

        pytrends.build_payload(
            kw_list=[keyword],
            timeframe="today 12-m"
        )

        df = pytrends.interest_over_time()

        if df.empty:
            return {
                "keyword": keyword,
                "trend_direction": "unknown",
                "interest_score": 0,
                "history": []
            }

        values = df[keyword].tolist()

        latest = values[-1]
        first = values[0]

        direction = "stable"

        if latest > first + 5:
            direction = "rising"
        elif latest < first - 5:
            direction = "declining"

        related = pytrends.related_queries()

        top_queries = []
        try:
            top_df = related[keyword]["top"]
            if top_df is not None:
                top_queries = top_df.head(5)["query"].tolist()
        except:
            pass

        return {
            "keyword": keyword,
            "trend_direction": direction,
            "interest_score": int(sum(values) / len(values)),
            "history": values[-12:],
            "top_related_queries": top_queries
        }

    except Exception as e:
        return {
            "keyword": keyword,
            "error": str(e)
        }