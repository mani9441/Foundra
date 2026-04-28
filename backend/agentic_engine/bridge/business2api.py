# ============================================================
# LangChain Agent for BusinessModelPage
# Input File: business_model.json
# Output: businessData (frontend-ready)
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

class PricingTier(BaseModel):
    name: str
    price: float

class MarginRow(BaseModel):
    month: str
    margin: float

class EconomicItem(BaseModel):
    label: str
    value: str

class BusinessOutput(BaseModel):

    description: str
    readiness: int

    pricing_title: str
    pricing_tiers: list[PricingTier]

    margins_title: str
    margins_data: list[MarginRow]

    economics_title: str
    economics_items: list[EconomicItem]

    footer_sub: str


parser = PydanticOutputParser(pydantic_object=BusinessOutput)

# ============================================================
# 3. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a startup monetization strategist.

Analyze the startup business model content and return ONLY
frontend-ready variables for a Business Model dashboard.

Rules:

1. description = concise revenue model summary.
2. readiness = 0-100 monetization readiness score.

3. pricing tiers must include exactly:
- Basic
- Premium
- Pro

Use realistic prices.

4. margin forecast must contain exactly:
M1, M2, M3, M4

Margins are percentages.

5. unit economics must include exactly:
- CAC
- LTV
- LTV:CAC
- Payback

6. Footer = investor-grade insight.

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

def generate_business_model(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = parser.parse(raw)

    frontend = {
        "description": structured.description,
        "readiness": structured.readiness,

        "pricing": {
            "title": structured.pricing_title,
            "tiers": [t.dict() for t in structured.pricing_tiers]
        },

        "margins": {
            "title": structured.margins_title,
            "data": [m.dict() for m in structured.margins_data]
        },

        "economics": {
            "title": structured.economics_title,
            "items": [i.dict() for i in structured.economics_items]
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend

# ============================================================
# 5. Load File
# ============================================================

# with open("business_model.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_business_model(content)

# print(json.dumps(result, indent=2))