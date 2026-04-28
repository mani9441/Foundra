# ============================================================
# LangChain Agent for PhaseValidationPage
# Input File: validation_output.json
# Output: validationData (frontend-ready)
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
# 2. Structured Schema
# ============================================================

class ReadinessItem(BaseModel):
    label: str
    value: int

class RiskItem(BaseModel):
    name: str
    severity: int
    likelihood: int

class BoardMember(BaseModel):
    role: str
    mood: str
    text: str

class ValidationOutput(BaseModel):

    summary: str
    confidence: int

    readiness_title: str
    readiness_items: list[ReadinessItem]

    risks_title: str
    risks_data: list[RiskItem]

    verdict_label: str
    verdict: str

    confidence_label: str
    executive_confidence: str

    board_title: str
    board_members: list[BoardMember]

    footer_sub: str


parser = PydanticOutputParser(pydantic_object=ValidationOutput)

# ============================================================
# 3. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a venture validation analyst.

Your job is to analyze startup validation results and return only
frontend-ready variables for a validation dashboard.

Rules:

1. Confidence = 0-100 score.
2. Summary = short executive summary.
3. Readiness ladder must contain exactly:
- ICP Validated
- Pain Severity
- MVP Feasible
- Revenue Potential

4. Risks matrix must contain exactly:
- Adoption
- Pricing
- Trust
- Competition

Each risk gets:
severity (0-100)
likelihood (0-100)

5. Verdict should be one of:
Proceed
Proceed with Caution
Hold
Reject

6. Board members must simulate startup executives:
CEO
CFO
CTO
CMO

Mood examples:
Bullish, Cautious, Neutral, Concerned

7. Footer = sharp investor-style insight.

{format_instructions}

INPUT CONTENT:
{content}
""")

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# ============================================================
# 4. Main Agent Function
# ============================================================

def generate_phase_validation(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = parser.parse(raw)

    frontend = {
        "summary": structured.summary,
        "confidence": structured.confidence,

        "readiness": {
            "title": structured.readiness_title,
            "items": [i.dict() for i in structured.readiness_items]
        },

        "risks": {
            "title": structured.risks_title,
            "data": [r.dict() for r in structured.risks_data]
        },

        "executive": {
            "verdictLabel": structured.verdict_label,
            "verdict": structured.verdict,
            "confidenceLabel": structured.confidence_label,
            "confidence": structured.executive_confidence
        },

        "board": {
            "title": structured.board_title,
            "members": [m.dict() for m in structured.board_members]
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend

# ============================================================
# 5. Load validation_output.json
# ============================================================

# with open("validation_output.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_phase_validation(content)

# print(json.dumps(result, indent=2))