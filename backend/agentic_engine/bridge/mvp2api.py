# ============================================================
# LangChain Agent for PhaseMVPPage
# Input File: phase_mvp.json
# Output: mvpData (frontend-ready)
# ============================================================

# pip install langchain langchain-openai pydantic python-dotenv

import os
import json
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import PydanticOutputParser
from langchain_classic.chains import LLMChain

load_dotenv()

# ============================================================
# 1. LLM
# ============================================================

from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()

# ============================================================
# 2. Schema
# ============================================================

class RoadmapItem(BaseModel):
    week: str
    value: int

class MatrixMetric(BaseModel):
    subject: str
    value: int

class MVPOutput(BaseModel):

    confidence: int
    coreProblem: str

    scope_title: str
    scope_mustHave: list[str]

    roadmap_title: str
    roadmap_data: list[RoadmapItem]

    readiness_title: str
    readiness_metrics: list[MatrixMetric]

    techdebt_title: str
    techdebt_items: list[str]

    footer_sub: str


parser = PydanticOutputParser(pydantic_object=MVPOutput)

# ============================================================
# 3. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a startup product strategist.

Analyze startup MVP planning content and generate ONLY frontend-ready
variables for an MVP Dashboard.

Rules:

1. confidence = 0-100 execution confidence.
2. coreProblem = one-line core startup pain.

3. MVP scope must include exactly 4 must-have features.

4. Roadmap must contain:
W1, W2, W3, W4, W5, W6
Each value = cumulative progress %

5. Readiness Matrix must include exactly:
- Speed
- Scope
- Retention
- Monetization
- Execution
- UX

Each score = 0-100

6. Tech debt = 1 to 3 realistic shortcuts / deferred items.

7. Footer = sharp founder insight.

{format_instructions}

INPUT CONTENT:
{content}
""")

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# ============================================================
# 4. Main Function
# ============================================================

def generate_phase_mvp(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = parser.parse(raw)

    frontend = {
        "confidence": structured.confidence,
        "coreProblem": structured.coreProblem,

        "scope": {
            "title": structured.scope_title,
            "mustHave": structured.scope_mustHave
        },

        "roadmap": {
            "title": structured.roadmap_title,
            "data": [r.dict() for r in structured.roadmap_data]
        },

        "readinessMatrix": {
            "title": structured.readiness_title,
            "metrics": [m.dict() for m in structured.readiness_metrics]
        },

        "techDebt": {
            "title": structured.techdebt_title,
            "items": structured.techdebt_items
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend

# ============================================================
# 5. Load File
# ============================================================

# with open("phase_mvp.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_phase_mvp(content)

# print(json.dumps(result, indent=2))