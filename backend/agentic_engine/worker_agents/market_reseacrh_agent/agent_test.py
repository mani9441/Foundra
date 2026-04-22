from .competitor_tool import competitor_research
from .competitor_matrix import generate_competitor_matrix
import time
from .market_sizing import market_sizing   
from .pricing_engine import pricing_analysis
import json
from .swot_engine import swot_analysis
from .segmentation_engine import segment_market
from .report_generator import generate_final_report
from .trends_engine import analyze_trends
from .geography_engine import analyze_geography


from backend.agentic_engine.worker_agents.market_reseacrh_agent.llm import llm


def market_research_agent(user_input):
    print("\n[Agent] Understanding request...")

    # Step 1: Competitor analysis
    print("[Agent] Fetching competitors...")
    competitors = competitor_research(user_input)

    time.sleep(2)  

    # Step 2: Build matrix
    print("[Agent] Building competitor matrix...")
    matrix = generate_competitor_matrix(competitors)

    print("\nCompetitor Matrix:\n")
    for row in matrix:
        print(row)

    print("\n[Agent] Analyzing pricing...")
    pricing = pricing_analysis(matrix)#
    time.sleep(2)
    print("\nPricing Data:\n", pricing)#
    
    # Step 3: Market sizing
    print("\n[Agent] Calculating market size...")
    market = market_sizing(user_input)

    time.sleep(2)   
    print("\nMarket Size:\n", market)

    print("\n[Agent] Analyzing industry trends...")
    trends = analyze_trends(user_input)

    time.sleep(2)

    print("\nIndustry Trends:\n", trends)


    print("\n[Agent] Analyzing demand geography...")
    geography = analyze_geography(user_input)

    time.sleep(2)

    print("\nGeography Insights:\n", geography)

    print("\n[Agent] Generating SWOT analysis...")
    swot = swot_analysis(matrix, pricing, market)

    time.sleep(2)

    print("\nSWOT Analysis:\n", swot)
    # Step 4: Final reasoning
    print("\n[Agent] Analyzing data...")
    

    print("\n[Agent] Segmenting market...")
    segments = segment_market(matrix, pricing, market, swot)

    time.sleep(2)

    print("\nTarget Segments:\n", segments)


    if "error" in pricing or "error" in market or "error" in swot:
        print("[Warning] Some components failed, results may be incomplete")


    final_prompt = f"""
    You are a startup market research expert.

    User request:
    {user_input}

    Competitor Matrix:
    {json.dumps(matrix, indent=2)}

    Market Size:
    {json.dumps(market, indent=2)}

    Pricing Data:
    {json.dumps(pricing, indent=2)}

    SWOT Analysis:
    {json.dumps(swot, indent=2)}

    Target Segments:
    {json.dumps(segments, indent=2)}

    Industry Trends:
    {json.dumps(trends, indent=2)}

    Geography Insights:
    {json.dumps(geography, indent=2)}

    Do:
    - Explain competitors clearly
    - Highlight key players
    - Identify gaps in market
    - Comment on market opportunity

    - Provide strategic insights based on SWOT
    - Recommend best target segment to focus on
    - Evaluate market timing and trends
    - Recommend best regions to launch
    Provide a clear, concise, and actionable strategy.
    Use bullet points where possible.
    """

    strategy = llm(final_prompt)
    final_report = generate_final_report(
        competitors,
        matrix,
        pricing,
        market,
        trends,
        geography,
        swot,
        segments,
        strategy
    )
    return final_report

# # Run
# result = market_research_agent("Find competitors for an AI fitness app")

# print("\nFinal Output:\n")
# print(json.dumps(result, indent=2))