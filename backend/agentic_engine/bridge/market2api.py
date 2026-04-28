# ============================================================
# LangChain Agent for PhaseMarketPage
# Input File: phase_market.json
# Output: marketData (frontend-ready)
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

class MarketSizeItem(BaseModel):
    label: str
    value: str

class WeaknessMetric(BaseModel):
    metric: str
    value: int

class MarketOutput(BaseModel):

    description: str
    readiness: int

    market_items: list[MarketSizeItem]

    weakness_title: str
    weakness_metrics: list[WeaknessMetric]

    strategy_title: str
    strategy_text: str

    opportunities_title: str
    opportunities_items: list[str]

    footer_sub: str


parser = PydanticOutputParser(pydantic_object=MarketOutput)

# ============================================================
# 3. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a startup market intelligence strategist.

Analyze the provided startup market research and generate ONLY
frontend-ready variables for a Market Dashboard.

Rules:

1. description = concise market summary.
2. readiness = 0-100 score for market attractiveness.

3. market size must include exactly:
- TAM
- SAM
- SOM

Use realistic values with $ and M/B notation.

4. competitor weakness radar must include exactly:
- Transparency
- Coverage
- UX
- Trust
- Speed

Values are 0-100 weakness scores.

5. strategy = short market entry thesis.

6. opportunities = top 3 whitespace gaps in competitors.

7. footer = sharp investor insight.

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

def generate_phase_market(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = parser.parse(raw)

    frontend = {
        "description": structured.description,
        "readiness": structured.readiness,

        "marketSize": {
            "items": [i.dict() for i in structured.market_items]
        },

        "competitorWeakness": {
            "title": structured.weakness_title,
            "metrics": [m.dict() for m in structured.weakness_metrics]
        },

        "strategy": {
            "title": structured.strategy_title,
            "text": structured.strategy_text
        },

        "opportunities": {
            "title": structured.opportunities_title,
            "items": structured.opportunities_items
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend

# ============================================================
# 5. Load phase_market.json
# ============================================================

# with open("phase_market.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_phase_market(content)

# print(json.dumps(result, indent=2))