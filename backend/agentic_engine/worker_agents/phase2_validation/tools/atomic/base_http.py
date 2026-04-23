# ============================================================
# File: phase2_validation/tools_atomic/base_http.py
# REAL TOOL INFRA - requests session + retry + timeout
# ============================================================

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def get_session() -> requests.Session:
    """
    Shared resilient HTTP session.
    """

    session = requests.Session()

    retry = Retry(
        total=3,
        read=3,
        connect=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "HEAD", "OPTIONS"],
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    session.headers.update(
        {
            "User-Agent":
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 Chrome/122 Safari/537.36"
        }
    )

    return session


SESSION = get_session()