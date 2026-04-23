#from backend.agentic_engine.graph import graph

# result = graph.invoke({
#     "user_input": "AI startup helping students prepare for exams",
#     "startup_name": "",
#     "industry": "",
#     "worker_reports": {},
#     "executive_reviews": {},
#     "board_decision": "",
#     "final_report": {},
#     "logs": []
# })

# print(result["final_report"])

##########################################################################################

# from backend.agentic_engine.worker_agents.validation_agent.graph import run_validation

# val = run_validation("Startup Mechanics on mobile")
# print(val)

# #########################################################################################

# from backend.agentic_engine.worker_agents.market_reseacrh_agent.agent_test import market_research_agent
# import json
# # Run
# result = market_research_agent(val)

# print("\nFinal Output:\n")
# print(json.dumps(result, indent=2))

###########################################################
from backend.agentic_engine.boardroom.engine import run_phase_gate

import json

# Open the file and load the content into the variable
with open('bin/pahse2_out.json', 'r') as file:
    phase_output = json.load(file)

metrics = {
    "runway_months": 4,
    "competitor_pressure": True,
    "growth_rate": 10
}

result = run_phase_gate(
    startup_name="Foundra",
    startup_stage="Pre-seed",
    phase="validation",
    report=phase_output,
    metrics=metrics
)

print(result.__dict__)