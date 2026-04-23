# ============================================================
# File: phase2_validation/tools_atomic/test_real_tools_part1.py
# ============================================================

from pprint import pprint

from ..atomic.web_trend_fetch import web_trend_fetch_tool
from ..atomic.domain_lookup import domain_lookup_tool
from ..atomic.competitor_scraper import competitor_scraper_tool
from ..atomic.pricing_lookup import pricing_lookup_tool


if __name__ == "__main__":

    pprint(
        web_trend_fetch_tool.invoke(
            "startup idea validation"
        )
    )

    pprint(
        domain_lookup_tool.invoke(
            "Foundra"
        )
    )

    pprint(
        competitor_scraper_tool.invoke(
            "https://typeform.com"
        )
    )

    pprint(
        pricing_lookup_tool.invoke(
            "https://typeform.com/pricing"
        )
    )