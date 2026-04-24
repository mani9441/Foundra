from .competitor_research import run_competitor_research
from .demand_signal import run_demand_signal
from .segment_analyzer import run_segment_analyzer
from .benchmark_analyzer import run_benchmark_analyzer


def run_research_bundle(inputs: dict):
    niche = inputs.get("reachable_niche_segment", "")
    keyword = inputs.get("problem_keyword", niche)
    industry = inputs.get("industry", "saas")

    competitor = run_competitor_research(niche)
    demand = run_demand_signal(keyword)
    segment = run_segment_analyzer(inputs)
    benchmark = run_benchmark_analyzer(industry)

    return {
        "competitor_research": competitor,
        "demand_signal": demand,
        "segment_analysis": segment,
        "benchmarks": benchmark
    }