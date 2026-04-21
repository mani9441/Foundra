from langchain.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
import requests
from bs4 import BeautifulSoup
from ...worker_agents.validation_agent.llm import get_llm

#### web search tool
search = TavilySearchResults(k=5)


@tool
def web_search(query: str) -> str:
    """
    Search the web for latest information.
    """
    results = search.invoke({"query": query})
    return str(results)


#### web scrape tool

@tool
def scrape_url(url: str) -> str:
    """
    Extract readable text from a webpage.
    """
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")

        for tag in soup(["script", "style"]):
            tag.extract()

        text = soup.get_text(separator=" ", strip=True)

        return text[:5000]  # prevent overload

    except Exception as e:
        return f"scrape_url error: {str(e)}"



#### Summarize tool

@tool
def summarize_text(text: str) -> str:
    """
    Summarize large text into key insights.
    """
    try:
        llm = get_llm()

        prompt = f"""
            Summarize the following content into concise insights:

            {text}
        """

        return llm.invoke(prompt).content

    except Exception as e:
        return f"summarize_text error: {str(e)}"



### Extraction tool

@tool
def extract_key_points(text: str) -> str:
    """
    Extract important structured points from text.
    """
    try:
        llm = get_llm()

        prompt = f"""
            Extract the most important points:

            {text}
        """

        return llm.invoke(prompt).content

    except Exception as e:
        return f"extract_key_points error: {str(e)}"
    

### Classify tool

@tool
def classify_text(text: str, labels: str) -> str:
    """
    Classify text into given labels.
    labels = comma separated string
    """
    try:
        llm = get_llm()

        prompt = f"""
        Classify the following text into one of these labels:

        Labels: {labels}

        Text:
        {text}

        Return only label.
    """

        return llm.invoke(prompt).content.strip()

    except Exception as e:
        return f"classify_text error: {str(e)}"
    

### Compare tool

@tool
def compare_items(item_a: str, item_b: str) -> str:
    """
    Compare two items and highlight differences.
    """
    try:
        llm = get_llm()

        prompt = f"""
            Compare these two items:

            A:
            {item_a}

            B:
            {item_b}

            Return key differences.
        """

        return llm.invoke(prompt).content

    except Exception as e:
        return f"compare_items error: {str(e)}"
    

### Sentiment tool

@tool
def sentiment_analysis(text: str) -> str:
    """
    Analyze sentiment and detect frustration/pain signals.
    """
    try:
        llm = get_llm()

        prompt = f"""
            Analyze sentiment and detect pain level:

            Text:
            {text}

            Return:
            - sentiment (positive/neutral/negative)
            - pain level (low/medium/high)
            - reason
        """

        return llm.invoke(prompt).content

    except Exception as e:
        return f"sentiment_analysis error: {str(e)}"
    


