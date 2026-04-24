import requests
from bs4 import BeautifulSoup
from ...config import settings


def scrape_url(url: str) -> str:
    try:
        headers = {"User-Agent": settings.USER_AGENT}
        res = requests.get(
            url,
            headers=headers,
            timeout=settings.REQUEST_TIMEOUT
        )

        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style", "noscript"]):
            tag.extract()

        text = soup.get_text(" ", strip=True)
        return text[:settings.MAX_CONTENT_CHARS]

    except:
        return ""