# ============================================================
# File: phase2_validation/tools_atomic/reddit_search.py
# Atomic Tool
# ============================================================

from typing import Dict, Any
from langchain.tools import tool

from ...config import settings


@tool("reddit_search_tool")
def reddit_search_tool(query: str) -> Dict[str, Any]:
    """
    Search Reddit pain discussions.
    """

    try:
        import praw

        reddit = praw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent=settings.REDDIT_USER_AGENT,
        )

        posts = []

        for submission in reddit.subreddit("all").search(query, limit=5):
            posts.append(
                {
                    "title": submission.title,
                    "score": submission.score,
                    "url": submission.url,
                    "subreddit": str(submission.subreddit),
                }
            )

        return {"query": query, "posts": posts}

    except Exception as e:
        return {
            "query": query,
            "posts": [],
            "error": str(e),
        }