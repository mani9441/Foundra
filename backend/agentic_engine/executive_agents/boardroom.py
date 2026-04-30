import json
import operator
from typing import Annotated, Dict, List, TypedDict, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

# ===============================================================
# 1. THE BRAIN: EXECUTIVE AGENT DEFINITION
# ===============================================================

class ExecutiveReview(BaseModel):
    comment: str = Field(description="The actual spoken words in the meeting.")
    vote: Literal["APPROVE", "REVISE", "REJECT"]
    confidence: int = Field(ge=1, le=10)
    refinement_orders: str = Field(default="")

# ===============================================================
# 2. THE STATE: SHARED MEMORY (The "Transcript")
# ===============================================================

class BoardroomState(TypedDict):
    phase: str
    report: str
    # 'history' stores the actual transcript of the debate
    history: Annotated[List[BaseMessage], operator.add] 
    iteration: int
    final_decision: str

# ===============================================================
# 3. THE AGENT LOGIC (Real LLM Calls)
# ===============================================================
from backend.agentic_engine.LLMs.llm import get_llm

def executive_node(state: BoardroomState, role: str, bias: str):
    llm = get_llm()
    structured_llm = llm.with_structured_output(ExecutiveReview)
    
    # 1. Format the transcript safely
    if not state['history']:
        transcript = "The meeting has just started. No one has spoken yet."
    else:
        transcript = "\n".join([f"{m.type}: {m.content}" for m in state['history']])
    
    # 2. Build the message list correctly
    # We must provide a SYSTEM message for the persona and a HUMAN message for the task
    system_msg = SystemMessage(content=f"""
        You are the {role} of a startup. 
        Your Bias: {bias}.
        RULES: React to the debate history and the report. Output JSON only.
    """)
    
    human_msg = HumanMessage(content=f"""
        Phase: {state['phase']}
        Report to Analyze: {state['report']}
        
        Transcript so far:
        {transcript}
        
        Give your executive response:
    """)
    
    # 3. Invoke with a list of messages
    # This prevents the 'contents are required' error
    review = structured_llm.invoke([system_msg, human_msg])
    
    return {
        "history": [HumanMessage(content=f"[{role}]: {review.comment} (Vote: {review.vote})")],
        "final_decision": review.refinement_orders if review.vote == "REVISE" else ""
    }
# ===============================================================
# 4. THE CEO SYNTHESIS (The Final Hammer)
# ===============================================================

def ceo_final_node(state: BoardroomState):
    """The CEO hears the bickering and makes the final call."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.2)
    
    prompt = f"""
    You are the CEO. You've heard the debate:
    {state['history']}
    
    Summarize the consensus. If there is a deadlock, you make the final executive decision.
    If you need a redo, output the specific 'Operational Redo Instructions'.
    """
    
    response = llm.invoke(prompt)
    return {"final_decision": response.content}

# ===============================================================
# 5. GRAPH CONSTRUCTION (The Workflow)
# ===============================================================

workflow = StateGraph(BoardroomState)

# Define nodes with pre-set personas
workflow.add_node("CEO_Opening", lambda s: executive_node(s, "CEO", "Growth & Vision"))
workflow.add_node("CTO_Rebuttal", lambda s: executive_node(s, "CTO", "Technical Stability"))
workflow.add_node("CFO_Check", lambda s: executive_node(s, "CFO", "Runway & Burn Rate"))
workflow.add_node("Synthesis", ceo_final_node)

# THE REAL BOARDROOM FLOW: CEO -> CTO -> CFO -> CEO Summary
workflow.add_edge(START, "CEO_Opening")
workflow.add_edge("CEO_Opening", "CTO_Rebuttal")
workflow.add_edge("CTO_Rebuttal", "CFO_Check")
workflow.add_edge("CFO_Check", "Synthesis")
workflow.add_edge("Synthesis", END)

startup_engine = workflow.compile()


# 1. Prepare the Input (The Initial State)
initial_input = {
    "phase": "Phase 4: Product Strategy (MVP)",
    "report": """
        Idea: Startup Mechanics on mobile. 
        Pain Score: 9. 
        Current Plan: Launch full feature set in 30 days. 
        Runway: 4 months. 
        Tech Stack: React Native + FastAPI.
    """,
    "history": [], # Starts empty, will be populated by agents
    "iteration": 0,
    "final_decision": ""
}

# from backend.agentic_engine.executive_agents.boardroom import startup_engine
# # 2. Run the Graph
# # We use .invoke() for a final result, or .stream() to see the debate live
# print("--- BOARD MEETING STARTING ---\n")

# result = startup_engine.invoke(initial_input)

# # 3. Display the Transcript (The "Real" Debate)
# print("## MEETING TRANSCRIPT ##")
# for message in result['history']:
#     # Each message is a HumanMessage object added during the graph run
#     print(f"\n{message.content}")

# print("\n" + "="*30)
# print("## FINAL EXECUTIVE DECREE ##")
# print(result['final_decision'])