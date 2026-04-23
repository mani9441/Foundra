import json

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


########## Phase 1 ############

# from backend.agentic_engine.worker_agents.phase1_problem_discovery.graph import run_phase1


# founder_idea = input("Enter startup area or idea: ")

# result = run_phase1(founder_idea)

# print("\n=== FINAL OUTPUT ===\n")
# print(json.dumps(result, indent=2))


########## Phase 2 ############


from backend.agentic_engine.worker_agents.phase2_validation.run_phase2_from_phase1 import run_from_phase1_file



output = run_from_phase1_file(r"outputs/phase1_result.json")
print(json.dumps(output, indent=2))