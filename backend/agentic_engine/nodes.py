


def input_node(state):
    state["logs"].append("Input captured")
    
    text = state["user_input"]

    state["startup_name"] = "Untitled Startup"
    state["industry"] = "AI SaaS"

    return state


def worker_agents_node(state):

    reports = {}

    reports["idea_validation"] = {
        "score": 8,
        "summary": "Problem seems real and painful."
    }

    reports["market_research"] = {
        "market_size": "Large",
        "competition": "Medium"
    }

    reports["business_model"] = {
        "model": "Freemium + Subscription"
    }

    reports["product_strategy"] = {
        "mvp": ["Core feature A", "Core feature B"]
    }

    reports["gtm_strategy"] = {
        "channels": ["Instagram", "Communities", "SEO"]
    }

    state["worker_reports"] = reports
    state["logs"].append("Worker agents completed")

    return state


def executive_room_node(state):

    worker = state["worker_reports"]

    reviews = {}

    reviews["CEO"] = "Strong opportunity. Worth testing."
    reviews["CFO"] = "Low-cost start possible."
    reviews["CTO"] = "Can build MVP in 4 weeks."
    reviews["CMO"] = "Need niche positioning."
    reviews["CPO"] = "Focus user pain deeply."

    state["executive_reviews"] = reviews
    state["board_decision"] = "APPROVED FOR MVP"

    state["logs"].append("Executive board completed")

    return state


def final_output_node(state):

    state["final_report"] = {
        "startup_name": state["startup_name"],
        "industry": state["industry"],
        "workers": state["worker_reports"],
        "executives": state["executive_reviews"],
        "decision": state["board_decision"]
    }

    state["logs"].append("Final report generated")

    return state