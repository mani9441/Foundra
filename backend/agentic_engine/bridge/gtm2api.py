# ============================================================
# LangChain Agent for PhaseLaunchPage
# Input File: phase_launch.json
# Output: launchData (frontend-ready)
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

class ChannelItem(BaseModel):
    name: str
    value: int

class GrowthItem(BaseModel):
    week: str
    users: int

class TaskItem(BaseModel):
    title: str
    team: str
    day: int

class FunnelItem(BaseModel):
    value: int
    name: str

class LaunchOutput(BaseModel):

    readiness: int
    description: str

    channels_title: str
    channels_allocation: list[ChannelItem]

    growth_title: str
    growth_forecast: list[GrowthItem]

    warroom_title: str
    warroom_tasks: list[TaskItem]

    funnel_title: str
    funnel_stages: list[FunnelItem]

    footer_sub: str


parser = PydanticOutputParser(pydantic_object=LaunchOutput)

# ============================================================
# 3. Prompt
# ============================================================

prompt = ChatPromptTemplate.from_template("""
You are a startup go-to-market strategist.

Analyze startup launch planning content and generate ONLY frontend-ready
variables for a Launch Dashboard.

Rules:

1. readiness = 0-100 launch readiness score.
2. description = concise GTM summary.

3. Channel allocation must include exactly:
- SEO
- Ads
- Email
- Social

Total should equal 100.

4. Growth forecast must include:
W1, W2, W3, W4, W5, W6

Users should grow realistically.

5. War room tasks = exactly 4 launch milestones.
Fields:
title, team, day

6. Funnel must include exactly:
Awareness
Consideration
Evaluation
Bookings

Use descending realistic values.

7. Footer = sharp operator insight.

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

def generate_phase_launch(content: str):

    raw = chain.run(
        content=content,
        format_instructions=parser.get_format_instructions()
    )

    structured = parser.parse(raw)

    frontend = {
        "readiness": structured.readiness,
        "description": structured.description,

        "channels": {
            "title": structured.channels_title,
            "allocation": [c.dict() for c in structured.channels_allocation]
        },

        "growth": {
            "title": structured.growth_title,
            "forecast": [g.dict() for g in structured.growth_forecast]
        },

        "warRoom": {
            "title": structured.warroom_title,
            "tasks": [t.dict() for t in structured.warroom_tasks]
        },

        "funnel": {
            "title": structured.funnel_title,
            "stages": [f.dict() for f in structured.funnel_stages]
        },

        "footer": {
            "sub": structured.footer_sub
        }
    }

    return frontend

# ============================================================
# 5. Load File
# ============================================================

# with open("phase_launch.json", "r", encoding="utf-8") as f:
#     content = f.read()

# result = generate_phase_launch(content)

# print(json.dumps(result, indent=2))