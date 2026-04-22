from competitor_tool import competitor_research
from competitor_matrix import generate_competitor_matrix
from report_generator import generate_final_report
from google import genai
import os
from dotenv import load_dotenv
import json
import time




# ==============================
#  LLM WRAPPER
# ==============================
from backend.agentic_engine.worker_agents.market_reseacrh_agent.llm import llm

def llm(prompt):
    return llm(prompt)


# ==============================
#  ROBUST JSON PARSER
# ==============================
def parse_json(text):
    try:
        if not text:
            return {}

        text = text.strip()

        if "```" in text:
            parts = text.split("```")
            text = parts[1] if len(parts) > 1 else text
            if text.startswith("json"):
                text = text[4:]

        start = text.find("{")
        end = text.rfind("}") + 1

        return json.loads(text[start:end])

    except Exception as e:
        print("[Parse Error]:", e)
        print("RAW OUTPUT:\n", text)
        return {}


# ==============================
#  MAIN AGENT
# ==============================
def market_research_agent(user_input):

    print("\n[Agent] Starting...")

    # ======================
    # CALL 1 — COMPETITORS
    # ======================
    print("[Agent] Fetching competitors...")
    competitors = competitor_research(user_input)

    print("[Agent] Building competitor matrix...")
    matrix = generate_competitor_matrix(competitors)

    print("\nCompetitor Matrix:\n")
    for row in matrix:
        print(row)

    # ======================
    # CALL 2 — MARKET INTELLIGENCE (DEEP)
    # ======================
    print("\n[Agent] Running market intelligence...")

    market_prompt = f"""
You are a senior market intelligence analyst.

You must think step-by-step like separate expert modules.

Startup:
{user_input}

Competitors:
{json.dumps(matrix, indent=2)}

---

### TASK 1: PRICING ENGINE
- Identify pricing tiers across competitors
- Classify: low / mid / premium
- Detect pricing strategy
- Identify pricing gaps
- Infer willingness to pay

---

### TASK 2: MARKET SIZING ENGINE
- Estimate TAM, SAM, SOM realistically
- Explain assumptions clearly

---

### TASK 3: TRENDS ENGINE
- Identify macro trends
- Identify technological drivers
- Identify risks
- Determine market stage
- Give timing score (1–10)

---

### TASK 4: GEOGRAPHY ENGINE
- Identify top markets
- Identify emerging markets
- Identify underserved regions
- Explain WHY each matters

---

### RULES:
- No generic answers
- No vague buzzwords
- Be specific and analytical

---

RETURN STRICT JSON:

{{
  "pricing": [],
  "market_size": {{
    "TAM": "",
    "SAM": "",
    "SOM": "",
    "reasoning": ""
  }},
  "trends": {{
    "trend_direction": "",
    "market_stage": "",
    "key_trends": [],
    "technological_drivers": [],
    "risks": [],
    "timing_score": "",
    "recommendation": ""
  }},
  "geography": {{
    "top_markets": [],
    "emerging_markets": [],
    "low_penetration_opportunities": [],
    "region_characteristics": [],
    "recommended_launch_regions": []
  }}
}}
"""

    market_response = llm(market_prompt)
    print("\n[DEBUG] Market RAW OUTPUT:\n", market_response)

    market_data = parse_json(market_response)

    # ======================
    # CALL 3 — STRATEGIC INTELLIGENCE (DEEP)
    # ======================
    print("\n[Agent] Running strategic intelligence...")

    strategy_prompt = f"""
You are a startup strategy consultant.

Think like:
- investor
- product strategist
- growth expert

Startup:
{user_input}

Competitors:
{json.dumps(matrix, indent=2)}

Market Data:
{json.dumps(market_data, indent=2)}

---

### TASK 1: SWOT ENGINE
- Strengths (internal advantages)
- Weaknesses (real constraints)
- Opportunities (market gaps)
- Threats (competition + risks)

---

### TASK 2: SEGMENTATION ENGINE
- Identify 2–3 segments
- Define:
  - behavior
  - pain points
  - willingness to pay
  - needs

---

### TASK 3: STRATEGY ENGINE
Provide:

1. Market positioning
2. Differentiation strategy
3. Best target segment (with reason)
4. Pricing strategy
5. Growth strategy

---

### RULES:
- No generic startup advice
- Must be actionable
- Must be realistic

---

RETURN STRICT JSON:

{{
  "swot": {{
    "strengths": [],
    "weaknesses": [],
    "opportunities": [],
    "threats": []
  }},
  "segments": {{
    "segments": []
  }},
  "strategy": ""
}}
"""

    strategy_response = llm(strategy_prompt)
    print("\n[DEBUG] Strategy RAW OUTPUT:\n", strategy_response)

    strategy_data = parse_json(strategy_response)

    # ======================
    # FINAL REPORT
    # ======================
    final_report = generate_final_report(
        competitors,
        matrix,
        market_data.get("pricing"),
        market_data.get("market_size"),
        market_data.get("trends"),
        market_data.get("geography"),
        strategy_data.get("swot"),
        strategy_data.get("segments"),
        strategy_data.get("strategy")
    )

    return final_report


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    user_input = input("Enter your startup idea: ")
    result = market_research_agent(user_input)

    print("\nFinal Output:\n")
    print(json.dumps(result, indent=2))