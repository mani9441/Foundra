from backend.agentic_engine.LLMs.llm import get_llm
from ..utils.json_parser import safe_json_parse
from ..tools.medium.economics_engine import run_economics_engine

llm = get_llm()


def run_unit_economics_agent(state):
    pricing = state.get("pricing_strategy", {})
    inputs = state["inputs"]

    monthly_price = 29.0
    cac = float(inputs.get("estimated_cac", 40))
    churn = float(inputs.get("monthly_churn_rate", 0.05))
    cogs = float(inputs.get("monthly_cogs", 8))

    econ = run_economics_engine(
        monthly_price=monthly_price,
        churn_rate=churn,
        cac=cac,
        cogs_monthly=cogs
    )

    prompt = f"""
You are a startup CFO.

Raw Economics:
{econ}

Inputs:
{inputs}

Pricing:
{pricing}

Return ONLY JSON:
{{
 "cac": "",
 "ltv": "",
 "ltv_cac_ratio": "",
 "gross_margin": "",
 "payback_period": "",
 "risk_flags": [],
 "confidence": 0.0
}}
"""
    result = llm.invoke(prompt)
    parsed = safe_json_parse(result)

    parsed["raw_calculation"] = econ

    return {"unit_economics_model": parsed}