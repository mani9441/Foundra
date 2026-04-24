from .search_tool import search_web


def find_companies(niche: str, limit: int = 5):
    query = f"{niche} companies startups software pricing"
    results = search_web(query, max_results=limit)

    companies = []

    for r in results:
        companies.append({
            "name": r["title"],
            "url": r["url"],
            "snippet": r["snippet"]
        })

    return companies