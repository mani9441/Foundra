from langgraph.graph import StateGraph, END

from backend.agentic_engine.state import FoundraState

from backend.agentic_engine.nodes import *

builder = StateGraph(FoundraState)


builder.add_node("input", input_node)
builder.add_node("workers", worker_agents_node)
builder.add_node("executives", executive_room_node)
builder.add_node("final", final_output_node)

builder.set_entry_point("input")

builder.add_edge("input", "workers")
builder.add_edge("workers", "executives")
builder.add_edge("executives", "final")
builder.add_edge("final", END)

graph = builder.compile()