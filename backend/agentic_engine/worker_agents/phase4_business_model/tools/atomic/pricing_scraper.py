import re
from .scrape_tool import scrape_url


PRICE_REGEX = r'(\$|₹|€|£)\s?\d+(?:\.\d{1,2})?'


def scrape_pricing(url: str):
    text = scrape_url(url)

    prices = re.findall(PRICE_REGEX, text)
    amounts = re.findall(r'(\$|₹|€|£)\s?\d+(?:\.\d{1,2})?', text)

    return {
        "url": url,
        "sample_text": text[:1500],
        "prices_found": amounts[:20],
        "has_pricing": len(amounts) > 0
    }