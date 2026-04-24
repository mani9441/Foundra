# ============================================================
# File: phase6_gtm/tools/atomic/scrape_url.py
# Read webpage text content
# pip install requests beautifulsoup4
# ============================================================

import requests
from bs4 import BeautifulSoup


def scrape_url(url: str, timeout: int = 10):
    """
    Extract readable webpage text
    """

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:12000]

    except Exception as e:
        return f"Failed scraping {url}: {str(e)}"