from backend.agentic_engine.LLMs.llm import get_llm
import time

def llm(prompt):

    try:
        llm = get_llm()
        response = llm.invoke(prompt).content
        return response
    except Exception as e:
        print(f"[LLM] Failed {e}")
        time.sleep(2)

    return "LLM failed "