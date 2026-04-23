from ...low_level_tools.google_search import google_search
from ...low_level_tools.reddit_search import reddit_search
from ...low_level_tools.summarize_tool import summarize_text
from ...low_level_tools.sentiment_tool import detect_sentiment


def complaint_research_tool(topic: str):
    search_results = google_search(f"{topic} user complaints frustrations problems")
    reddit_results = reddit_search(topic)

    merged = "\n".join(search_results + reddit_results)

    summary = summarize_text(merged)
    sentiment = detect_sentiment(merged)

    return {
        "raw_sources": search_results + reddit_results,
        "summary": summary,
        "sentiment": sentiment
    }