from ..atomic.math_tool import (
    ltv,
    ltv_cac_ratio,
    gross_margin,
    payback_months
)


def run_economics_engine(
    monthly_price: float,
    churn_rate: float,
    cac: float,
    cogs_monthly: float
):
    lifetime_value = ltv(monthly_price, churn_rate)
    ratio = ltv_cac_ratio(lifetime_value, cac)

    gm = gross_margin(monthly_price, cogs_monthly)

    gross_profit = monthly_price - cogs_monthly
    payback = payback_months(cac, gross_profit)

    return {
        "monthly_price": monthly_price,
        "cac": cac,
        "ltv": lifetime_value,
        "ltv_cac_ratio": ratio,
        "gross_margin": gm,
        "payback_months": payback
    }