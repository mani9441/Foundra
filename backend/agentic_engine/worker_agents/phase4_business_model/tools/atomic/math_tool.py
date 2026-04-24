def ltv(arpu_monthly: float, churn_rate_monthly: float):
    if churn_rate_monthly <= 0:
        return 0
    return round(arpu_monthly / churn_rate_monthly, 2)


def ltv_cac_ratio(ltv_value: float, cac_value: float):
    if cac_value <= 0:
        return 0
    return round(ltv_value / cac_value, 2)


def gross_margin(revenue: float, cogs: float):
    if revenue <= 0:
        return 0
    return round((revenue - cogs) / revenue, 4)


def payback_months(cac_value: float, gross_profit_monthly: float):
    if gross_profit_monthly <= 0:
        return 0
    return round(cac_value / gross_profit_monthly, 2)