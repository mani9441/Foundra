# ============================================================
# LangChain Agent for PhaseDiscoveryPage Dynamic Variables
# Input: large startup analysis content (your JSON / text output)
# Output: discoveryData object for frontend
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
# 2. Structured Output Schema
# ============================================================

class RadarMetric(BaseModel):
    subject: str
    value: int
    fullMark: int = 10

class SegmentItem(BaseModel):
    name: str
    pain: int

class DiscoveryOutput(BaseModel):

    # Core Discovery
    core_label: str = Field(description="Short label like Core Discovery")
    core_headline: str = Field(description="Strong single-line pain headline")
    core_description: str = Field(description="2 line summary")

    # Opportunity
    opportunity_title: str = Field(description="Title like Opportunity Rating")
    opportunity_score: int = Field(description="0-100 score")
    opportunity_status: str = Field(description="High / Medium / Low")

    # Radar
    radar_title: str
    radar_metrics: list[RadarMetric]

    # Segments
    segments_title: str
    segments_data: list[SegmentItem]

    # Footer
    footer_sub: str


parser = PydanticOutputParser(pydantic_object=DiscoveryOutput)

# ============================================================
# 3. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_template("""
    You are a startup intelligence analyst.

    Your task is to read startup research content and generate ONLY the
    variables needed for a frontend discovery page.

    Use smart reasoning.

    Rules:

    1. Headline must be sharp and emotional.
    2. Opportunity score should be based on:
    - pain urgency
    - frequency
    - willingness to pay
    - market gap

    3. Status:
    score >=80 => High
    score >=60 => Medium
    else Low

    4. Radar metrics must include exactly:
    Urgency
    Frequency
    WTP
    Emotion
    Gap

    5. Segment chart = top 3 affected users.

    6. Footer should be short insight sentence.

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

def generate_phase_discovery(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = parser.parse(raw)

    frontend = {
        "coreDiscovery": {
            "label": structured.core_label,
            "headline": structured.core_headline,
            "description": structured.core_description
        },

        "opportunity": {
            "title": structured.opportunity_title,
            "score": structured.opportunity_score,
            "status": structured.opportunity_status
        },

        "painSignalRadar": {
            "title": structured.radar_title,
            "metrics": [m.dict() for m in structured.radar_metrics]
        },

        "topAffectedSegments": {
            "title": structured.segments_title,
            "data": [s.dict() for s in structured.segments_data]
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend

# ============================================================
# 5. Example Usage
# ============================================================

# with open("startup_result.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_phase_discovery(content)

# print(json.dumps(result, indent=2))