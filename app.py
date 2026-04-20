from backend.agentic_engine.graph import graph

result = graph.invoke({
    "user_input": "AI startup helping students prepare for exams",
    "startup_name": "",
    "industry": "",
    "worker_reports": {},
    "executive_reviews": {},
    "board_decision": "",
    "final_report": {},
    "logs": []
})

print(result["final_report"])

from backend.agentic_engine.worker_agents.validation_agent.graph import run_validation

val = run_validation("Startup Mechanics on mobile")
print(val)