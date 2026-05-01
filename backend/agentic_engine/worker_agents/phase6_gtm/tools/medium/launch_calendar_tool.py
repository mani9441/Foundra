# ============================================================
# Launch Calendar Tool
# 30 day launch plan
# ============================================================

from ...llm import get_llm
from ...utils.json_parser import parse_llm_json

llm = get_llm()


def launch_calendar_tool(
    product: str,
    budget: str,
    channels: str
):
    prompt = f"""
You are a startup launch manager.

Product:
{product}

Budget:
{budget}

Channels:
{channels}

Create a realistic 30 day launch execution calendar.

Return JSON:

{{
  "week_1": [],
  "week_2": [],
  "week_3": [],
  "week_4": [],
  "launch_day": [],
  "success_metrics": []
}}
"""

    raw = llm.invoke(prompt)

    return parse_llm_json(
        raw,
        {
            "week_1": [],
            "week_2": [],
            "week_3": [],
            "week_4": [],
            "launch_day": [],
            "success_metrics": []
        }
    )