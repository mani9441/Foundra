from .google_search import google_search

def reddit_search(query: str):
    q = f"Reddit discussions complaints {query}"
    return google_search(q)