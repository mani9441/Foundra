# validation_agent/nodes.py

from .utils import add_error

# Reusable workflow tools
from ...tools.medium_level_tools.research_tool import run_research
from ...tools.medium_level_tools.competitor_tool import run_competitor_tool
from ...tools.medium_level_tools.pain_signal_tool import run_pain_signal
from ...tools.medium_level_tools.pricing_tool import run_pricing_tool

# ==========================================
# INTAKE NODE (keep simple)
# ==========================================

def intake_node(state):
    try:
        state["parsed_idea"] = {
            "startup_idea": state["user_input"]
        }
        return state

    except Exception as e:
        return add_error(state, str(e))


# ==========================================
# RESEARCH NODE
# ==========================================

def research_node(state):
    try:
        topic = state["parsed_idea"]["startup_idea"]

        result = run_research(topic)

        state["market_research"] = result["final_report"]
        return state

    except Exception as e:
        return add_error(state, f"research_node: {str(e)}")


# ==========================================
# PROBLEM NODE
# ==========================================

def problem_node(state):
    try:
        topic = state["parsed_idea"]["startup_idea"]

        result = run_pain_signal(topic)

        report = result["final_report"]

        state["problem_analysis"] = {
            "pain_score": report["severity_score"],
            "reasons": report["pain_points"],
            "sentiment": report["sentiment"]
        }

        return state

    except Exception as e:
        return add_error(state, f"problem_node: {str(e)}")


# ==========================================
# COMPETITOR NODE
# ==========================================

def competitor_node(state):
    try:
        topic = state["parsed_idea"]["startup_idea"]

        result = run_competitor_tool(topic)

        state["competitor_analysis"] = \
            result["final_report"]

        return state

    except Exception as e:
        return add_error(state, f"competitor_node: {str(e)}")


# ==========================================
# PRICING NODE
# ==========================================

def pricing_node(state):
    try:
        topic = state["parsed_idea"]["startup_idea"]

        result = run_pricing_tool(topic)

        report = result["final_report"]

        state["pricing_analysis"] = {
            "pricing_models":
                report["pricing_models"],
            "estimated_range":
                report["estimated_range"],
            "willingness_to_pay":
                report["monetization_score"]
        }

        return state

    except Exception as e:
        return add_error(state, f"pricing_node: {str(e)}")
    
    
# ==========================================
# JUDGE NODE
# ==========================================

def judge_node(state):
    try:
        problem = state.get("problem_analysis", {})
        pricing = state.get("pricing_analysis", {})
        comp = str(state.get("competitor_analysis", "")).lower()
        skeptic = str(state.get("skeptic_notes", "")).lower()

        pain = problem.get("pain_score", 0)
        monetization = pricing.get("willingness_to_pay", 0)

        # Derived Scores
        competition_window = 7
        if "crowded" in comp:
            competition_window = 4
        elif "gap" in comp:
            competition_window = 8

        execution_risk = 7
        if "hard" in skeptic or "risk" in skeptic:
            execution_risk = 5

        # Weighted Total
        total = (
            pain * 0.35 +
            monetization * 0.25 +
            competition_window * 0.20 +
            execution_risk * 0.20
        )

        score = int(total * 10)

        if score >= 80:
            verdict = "PROCEED"
        elif score >= 65:
            verdict = "NICHE DOWN"
        elif score >= 45:
            verdict = "PIVOT"
        else:
            verdict = "REJECT"

        state["confidence_score"] = score
        state["verdict"] = verdict

        state["judge_summary"] = {
            "pain": pain,
            "monetization": monetization,
            "competition_window": competition_window,
            "execution_risk": execution_risk
        }

        return state

    except Exception as e:
        return add_error(state, f"judge_node: {str(e)}")
    

# ==========================================
# REPORT NODE
# ==========================================

def report_node(state):
    state["final_report"] = {
        "idea": state["user_input"],
        "verdict": state.get("verdict", ""),
        "confidence_score": state.get("confidence_score", 0),

        "scores": state.get("judge_summary", {}),

        "pain_analysis": state.get("problem_analysis", {}),
        "personas": state.get("personas", ""),
        "competition": state.get("competitor_analysis", {}),
        "pricing": state.get("pricing_analysis", {}),
        "market_gaps": state.get("market_gaps", ""),
        "uvp": state.get("uvp", ""),
        "risks": state.get("skeptic_notes", ""),

        "next_actions": self_actions(
            state.get("verdict", "")
        ),

        "errors": state.get("errors", [])
    }

    return state


def self_actions(verdict):
    if verdict == "PROCEED":
        return [
            "Run 10 customer interviews",
            "Build MVP",
            "Test landing page"
        ]
    elif verdict == "NICHE DOWN":
        return [
            "Choose smaller target segment",
            "Refine offer"
        ]
    elif verdict == "PIVOT":
        return [
            "Change customer or pain point"
        ]
    else:
        return [
            "Do not build yet",
            "Try new problem area"
        ]
    

    
### persona node

def persona_node(state):
    try:
        idea = state["parsed_idea"]["startup_idea"]

        pain = str(state.get("problem_analysis", {}))
        comp = str(state.get("competitor_analysis", {}))

        from ...LLMs.llm import get_llm
        llm = get_llm()

        prompt = f"""
            Based on this startup idea, pain signals, and competitors:

            Idea:
            {idea}

            Pain:
            {pain}

            Competitors:
            {comp}

            Generate 2-3 realistic customer personas.

            Include:
            - segment
            - main pain
            - willingness to pay
            - why they care
        """

        result = llm.invoke(prompt).content

        state["personas"] = result
        return state

    except Exception as e:
        return add_error(state, f"persona_node: {str(e)}")
    

### Gap node 

def gap_node(state):
    try:
        comp = str(state.get("competitor_analysis", {}))

        from ...LLMs.llm import get_llm
        llm = get_llm()

        prompt = f"""
From this competitor analysis:

{comp}

Extract:
- real market gaps
- underserved users
- pricing gaps
- UX gaps
"""

        result = llm.invoke(prompt).content

        state["market_gaps"] = result
        return state

    except Exception as e:
        return add_error(state, f"gap_node: {str(e)}")
    

### skeptic node 

def skeptic_node(state):
    try:
        idea = state["parsed_idea"]["startup_idea"]

        pain = str(state.get("problem_analysis", {}))
        pricing = str(state.get("pricing_analysis", {}))
        comp = str(state.get("competitor_analysis", {}))

        from ...LLMs.llm import get_llm
        llm = get_llm()

        prompt = f"""
Act like a harsh investor.

Idea:
{idea}

Pain:
{pain}

Pricing:
{pricing}

Competitors:
{comp}

List critical risks:
- why this might fail
- market risks
- execution risks
"""

        result = llm.invoke(prompt).content

        state["skeptic_notes"] = result
        return state

    except Exception as e:
        return add_error(state, f"skeptic_node: {str(e)}")
    

### UVP node

def uvp_node(state):
    try:
        idea = state["parsed_idea"]["startup_idea"]
        gaps = str(state.get("market_gaps", ""))
        pain = str(state.get("problem_analysis", {}))

        from ...LLMs.llm import get_llm
        llm = get_llm()

        prompt = f"""
Create a strong startup UVP.

Idea:
{idea}

Pain:
{pain}

Market Gaps:
{gaps}

Return:
1 clear powerful positioning statement.
"""

        result = llm.invoke(prompt).content

        state["uvp"] = result.strip()
        return state

    except Exception as e:
        return add_error(state, f"uvp_node: {str(e)}")