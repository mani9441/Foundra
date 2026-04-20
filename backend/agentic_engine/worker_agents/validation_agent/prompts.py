SYSTEM_IDENTITY = """
    You are an elite startup validation strategist.
    You think like:
    - YC partner
    - Startup founder
    - Market analyst
    - Investor
    - Product strategist

    Be brutally honest.
    Return structured outputs.
"""

INTAKE_PROMPT = """
    Convert the founder idea into structured startup information.

    User Idea:
    {idea}

    Return:
    startup_idea
    product_type
    domain
    target_market
    target_users
    business_model_guess
"""

PROBLEM_PROMPT = """
    Analyze whether this startup solves a painful real problem.

    Idea:
    {idea}

    Score:
    pain_score (0-10)
    urgency_score (0-10)
    frequency_score (0-10)
    emotional_pain_score (0-10)

    Give reasons.
"""

PERSONA_PROMPT = """
    Generate 3 strong customer personas for:

    Idea:
    {idea}

    Include:
    segment
    pain_points
    budget_level
    buying_trigger
"""

COMPETITOR_PROMPT = """
    Identify existing alternatives for:

    Idea:
    {idea}

    Return:
    competitors
    manual alternatives
    weaknesses
"""

PRICING_PROMPT = """
    Estimate willingness to pay for:

    Idea:
    {idea}

    Return:
    willingness_to_pay
    pricing_model
    estimated_range
    notes
"""