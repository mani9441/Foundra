def generate_final_report(
    competitors,
    matrix,
    pricing,
    market,
    trends,
    geography,
    swot,
    segments,
    strategy
):
    return {
        "competitors": competitors,
        "matrix": matrix,
        "pricing": pricing,
        "market_size": market,
        "trends": trends,
        "geography": geography,
        "swot": swot,
        "segments": segments,
        "strategy": strategy
    }