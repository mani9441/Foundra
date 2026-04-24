import json
from .graph import build_graph


def build_initial_state(inputs: dict):
    return {
        "inputs": inputs,

        "research": {},
        "competitors": [],
        "pricing_benchmarks": {},
        "economics_benchmarks": {},

        "revenue_model": {},
        "pricing_strategy": {},
        "unit_economics_model": {},
        "viability_decision": {},

        "confidence_score": 0.0,
        "warnings": [],
        "errors": [],
        "logs": [],

        "retries": 0,
        "max_retries": 2
    }


def normalize_output(result: dict):
    return {
        "revenue_model": result.get("revenue_model", {}),
        "pricing_strategy": result.get("pricing_strategy", {}),
        "unit_economics_model": result.get("unit_economics_model", {}),
        "viability_decision": result.get("viability_decision", {}),
        "confidence_score": result.get("confidence_score", 0.0),
        "research": result.get("research", {}),
        "critic_report": result.get("critic_report", {}),
        "explainability": result.get("explainability", {}),
        "logs": result.get("logs", [])
    }


def run_phase4(inputs: dict):
    graph = build_graph()
    state = build_initial_state(inputs)
    result = graph.invoke(state)
    return normalize_output(result)


def run_phase4_pretty(inputs: dict):
    result = run_phase4(inputs)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result