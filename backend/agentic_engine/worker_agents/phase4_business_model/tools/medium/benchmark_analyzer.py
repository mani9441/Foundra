from ..atomic.benchmark_tool import get_benchmark


def run_benchmark_analyzer(industry: str):
    b = get_benchmark(industry)

    return {
        "industry": industry,
        "gross_margin_target": b["gross_margin"],
        "ltv_cac_target": b["ltv_cac_good"],
        "payback_target_months": b["payback_good_months"]
    }