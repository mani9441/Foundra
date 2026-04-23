from .google_search import google_search


def trends_tool(topic: str):
    q = f"{topic} market trends demand rising search trend"
    return google_search(q)