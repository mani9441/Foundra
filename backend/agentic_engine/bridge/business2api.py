# ============================================================
# FILE: backend/agentic_engine/bridge/business2api.py
# FIXED + PRODUCTION SAFE VERSION
# ============================================================

import os
import json
import re
from dotenv import load_dotenv

from pydantic import BaseModel
from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import PydanticOutputParser
from langchain_classic.chains import LLMChain

load_dotenv()

# ============================================================
# LLM
# ============================================================

from backend.agentic_engine.LLMs.llm import get_llm

llm = get_llm()

# ============================================================
# SCHEMA
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
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a startup monetization strategist.

Analyze the startup business model content and return ONLY
valid JSON object matching required format.

STRICT RULES:

1. Return ONLY raw JSON.
2. Do NOT return markdown.
3. Do NOT return schema.
4. Do NOT wrap response inside "data".
5. No explanation.

Rules:

description = concise revenue model summary.
readiness = score from 0 to 100.

pricing tiers must include EXACTLY:
- Basic
- Premium
- Pro

Margins must contain EXACTLY:
- M1
- M2
- M3
- M4

Economics must contain EXACTLY:
- CAC
- LTV
- LTV:CAC
- Payback

{format_instructions}

INPUT CONTENT:
{content}
""")

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# ============================================================
# UNIVERSAL SAFE PARSER
# ============================================================

def extract_json(raw: str):
    """
    Extract first valid JSON object from model response
    """
    raw = raw.strip()

    # direct parse
    try:
        return json.loads(raw)
    except:
        pass

    # extract json block
    match = re.search(r"\{.*\}", raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    raise ValueError("No valid JSON found in model output")


def safe_parse(raw: str) -> BusinessOutput:
    """
    Handles:
    1. normal JSON
    2. wrapped {"data": {...}}
    3. schema + data
    4. parser fallback
    """

    try:
        data = extract_json(raw)

        # if wrapped inside data
        if "data" in data and isinstance(data["data"], dict):
            data = data["data"]

        return BusinessOutput.model_validate(data)

    except Exception:
        # final fallback
        return parser.parse(raw)

# ============================================================
# MAIN FUNCTION
# ============================================================

def generate_business_model(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = safe_parse(raw)

    frontend = {
        "description": structured.description,
        "readiness": structured.readiness,

        "pricing": {
            "title": structured.pricing_title,
            "tiers": [t.model_dump() for t in structured.pricing_tiers]
        },

        "margins": {
            "title": structured.margins_title,
            "data": [m.model_dump() for m in structured.margins_data]
        },

        "economics": {
            "title": structured.economics_title,
            "items": [i.model_dump() for i in structured.economics_items]
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend