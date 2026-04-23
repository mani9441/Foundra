from langchain_community.tools.tavily_search import TavilySearchResults
#from langchain_tavily import TavilySearch



MAX_SEARCH_RESULTS = 5

def google_search(query: str, max_results: int = MAX_SEARCH_RESULTS):
    """
    Performs a search with a configurable number of results.
    Defaults to the value in config.py if not specified.
    """
    try:
        # Re-initialize the tool with the dynamic limit
        tool = TavilySearchResults(max_results=max_results)
        
        results = tool.invoke(query)
        cleaned = []

        for r in results:
            # Using .strip() to clean up formatting
            title = r.get('title', 'No Title').strip()
            content = r.get('content', 'No Content').strip()
            cleaned.append(f"{title} | {content}")

        return cleaned

    except Exception as e:
        return [f"Search failed: {str(e)}"]