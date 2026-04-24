from phase4_business_model import run_phase4_pretty


inputs = {
    "reachable_niche_segment": "small ecommerce brands needing AI customer support",
    "pricing_benchmarks": "competitors charge $19-$99 monthly",
    "differentiation_opportunity": "24/7 multilingual AI with WhatsApp integration",
    "market_size_estimate": "large and growing SMB ecommerce segment",

    "cost_assumptions": {
        "llm_cost_per_customer": 8,
        "infra": 3
    },

    "delivery_model_options": [
        "self serve SaaS",
        "agency assisted onboarding"
    ],

    "industry": "saas",

    "sales_motion_assumptions": {
        "channel": "content + outbound",
        "avg_cac": 55
    },

    "estimated_cac": 55,
    "monthly_churn_rate": 0.06,
    "monthly_cogs": 11,

    "problem_keyword": "AI ecommerce support software"
}

run_phase4_pretty(inputs)