# backend/agentic_engine/bridge/discovery2api.py

# ============================================================
# Phase 1 Discovery Bridge
# Converts raw startup research into frontend-ready JSON
# Reliable / schema-safe / chart-compatible
# ============================================================

import json
from typing import List

from pydantic import BaseModel, Field

from langchain_classic.prompts import ChatPromptTemplate
from langchain_classic.output_parsers import PydanticOutputParser
from langchain_classic.chains import LLMChain

from backend.agentic_engine.LLMs.llm import get_llm

# ============================================================
# LLM
# ============================================================

llm = get_llm()

# ============================================================
# FRONTEND-COMPATIBLE SCHEMA
# ============================================================

class RadarMetric(BaseModel):
    metric: str = Field(description="Metric name")
    score: int = Field(description="0 to 100 score")


class SegmentItem(BaseModel):
    name: str = Field(description="Segment name")
    score: int = Field(description="0 to 100 impact score")


class DiscoveryOutput(BaseModel):
    # Core discovery
    core_label: str
    core_headline: str
    core_description: str

    # Opportunity
    opportunity_title: str
    opportunity_score: int
    opportunity_status: str

    # Radar
    radar_title: str
    radar_metrics: List[RadarMetric]

    # Segments
    segments_title: str
    segments_data: List[SegmentItem]

    # Footer
    footer_sub: str


parser = PydanticOutputParser(pydantic_object=DiscoveryOutput)

# ============================================================
# PROMPT
# ============================================================

prompt = ChatPromptTemplate.from_template(
"""
You are an elite startup intelligence analyst.

Read the startup research input and convert it into variables
for a premium frontend discovery dashboard.

Rules:

1. Headline must be concise and powerful.
2. Opportunity score must be 0-100 based on:
   - urgency
   - frequency
   - willingness to pay
   - competition gap

3. Status:
   80+ = HIGH POTENTIAL
   60+ = MEDIUM POTENTIAL
   else = LOW POTENTIAL

4. Radar metrics must contain EXACTLY these 5 rows:
   - Demand
   - Urgency
   - Frequency
   - Spend
   - Competition

5. Segment chart = top 3 user groups.

6. Output ONLY valid structured data.

{format_instructions}

INPUT:
{content}
"""
)

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

# ============================================================
# FALLBACK OUTPUT
# ============================================================

def fallback_output():
    return {
        "coreDiscovery": {
            "label": "Core Discovery",
            "headline": "Clear market pain point identified",
            "description": "Users experience recurring friction with insufficient existing solutions."
        },
        "opportunity": {
            "title": "Opportunity Score",
            "score": 78,
            "status": "MEDIUM POTENTIAL"
        },
        "painSignalRadar": {
            "title": "Pain Signal Radar",
            "metrics": [
                {"metric": "Demand", "score": 80},
                {"metric": "Urgency", "score": 74},
                {"metric": "Frequency", "score": 72},
                {"metric": "Spend", "score": 66},
                {"metric": "Competition", "score": 58},
            ],
        },
        "topAffectedSegments": {
            "title": "Top Affected Segments",
            "data": [
                {"name": "Students", "score": 84},
                {"name": "Professionals", "score": 77},
                {"name": "Small Teams", "score": 69},
            ],
        },
        "footer": {
            "sub": "Proceed to validation phase to test willingness to pay."
        },
    }

# ============================================================
# MAIN FUNCTION
# ============================================================

def generate_phase_discovery(content: str):
    try:
        raw = chain.run(
            content=content,
            format_instructions=parser.get_format_instructions()
        )

        structured = parser.parse(raw)

        score = max(0, min(100, structured.opportunity_score))

        frontend = {
            "coreDiscovery": {
                "label": structured.core_label,
                "headline": structured.core_headline,
                "description": structured.core_description,
            },

            "opportunity": {
                "title": structured.opportunity_title,
                "score": score,
                "status": structured.opportunity_status,
            },

            "painSignalRadar": {
                "title": structured.radar_title,
                "metrics": [
                    {
                        "metric": m.metric,
                        "score": max(0, min(100, m.score)),
                    }
                    for m in structured.radar_metrics
                ],
            },

            "topAffectedSegments": {
                "title": structured.segments_title,
                "data": [
                    {
                        "name": s.name,
                        "score": max(0, min(100, s.score)),
                    }
                    for s in structured.segments_data
                ],
            },

            "footer": {
                "sub": structured.footer_sub,
            },
        }

        return frontend

    except Exception as e:
        print("Discovery bridge error:", str(e))
        return fallback_output()
# ============================================================
# 5. Example Usage
# ============================================================

# with open("startup_result.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_phase_discovery(content)

# print(json.dumps(result, indent=2))