# ============================================================
# File: phase5_product_strategy/tools/atomic/cost_estimator_tool.py
# Startup MVP Rough Cost Estimator
# ============================================================

def estimate_cost(
    developers: int,
    weeks: int,
    infra_scale: str = "small"
):
    dev_cost = developers * weeks * 15000

    infra_map = {
        "small": 5000,
        "medium": 15000,
        "large": 50000
    }

    infra = infra_map.get(infra_scale, 5000)

    total = dev_cost + infra

    return {
        "developer_cost_estimate": dev_cost,
        "infrastructure_estimate": infra,
        "total_estimated_cost": total
    }