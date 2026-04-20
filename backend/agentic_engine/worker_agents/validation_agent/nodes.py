from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser, PydanticOutputParser

from .llm import get_llm
from .prompts import SYSTEM_IDENTITY, INTAKE_PROMPT, PROBLEM_PROMPT, PERSONA_PROMPT, COMPETITOR_PROMPT, PRICING_PROMPT
from .utils import add_error
from .schemas import ParsedIdeaSchema, ProblemAnalysisSchema, PricingSchema

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser




def intake_node(state):
    try:
        parser = PydanticOutputParser(pydantic_object=ParsedIdeaSchema)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_IDENTITY),
                ("human", INTAKE_PROMPT + "\n\n{format_instructions}")
            ]
        )

        chain = prompt | get_llm() | parser

        result = chain.invoke(
            {
                "idea": state["user_input"],
                "format_instructions": parser.get_format_instructions(),
            }
        )

        state["parsed_idea"] = result.model_dump()
        return state

    except Exception as e:
        return add_error(state, f"intake_node failed: {str(e)}")


###############################################################


def problem_node(state):
    try:
        parser = PydanticOutputParser(pydantic_object=ProblemAnalysisSchema)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_IDENTITY),
                ("human", PROBLEM_PROMPT + "\n\n{format_instructions}")
            ]
        )

        chain = prompt | get_llm() | parser

        result = chain.invoke(
            {
                "idea": state["parsed_idea"]["startup_idea"],
                "format_instructions": parser.get_format_instructions(),
            }
        )

        state["problem_analysis"] = result.model_dump()
        return state

    except Exception as e:
        return add_error(state, f"problem_node failed: {str(e)}")
    

##########################################################


def persona_node(state):
    try:
        parser = JsonOutputParser()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_IDENTITY),
                ("human", PERSONA_PROMPT)
            ]
        )

        chain = prompt | get_llm() | parser

        result = chain.invoke(
            {
                "idea": state["parsed_idea"]["startup_idea"],
            }
        )

        state["personas"] = result if isinstance(result, list) else []
        return state

    except Exception as e:
        return add_error(state, f"persona_node failed: {str(e)}")


##############################################################

def competitor_node(state):
    try:
        parser = JsonOutputParser()

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_IDENTITY),
                ("human", COMPETITOR_PROMPT)
            ]
        )

        chain = prompt | get_llm() | parser

        result = chain.invoke(
            {
                "idea": state["parsed_idea"]["startup_idea"],
            }
        )

        state["competitors"] = result if isinstance(result, list) else []
        return state

    except Exception as e:
        return add_error(state, f"competitor_node failed: {str(e)}")


################################################################

def pricing_node(state):
    try:
        parser = PydanticOutputParser(pydantic_object=PricingSchema)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", SYSTEM_IDENTITY),
                ("human", PRICING_PROMPT + "\n\n{format_instructions}")
            ]
        )

        chain = prompt | get_llm() | parser

        result = chain.invoke(
            {
                "idea": state["parsed_idea"]["startup_idea"],
                "format_instructions": parser.get_format_instructions(),
            }
        )

        state["pricing_analysis"] = result.model_dump()
        return state

    except Exception as e:
        return add_error(state, f"pricing_node failed: {str(e)}")
    

#####################################################################



def gap_node(state):
    try:
        prompt = ChatPromptTemplate.from_template("""
Find whitespace opportunities for this startup.

Idea:
{idea}

Competitors:
{competitors}

Return JSON array of market gaps.
""")

        chain = prompt | get_llm() | JsonOutputParser()

        result = chain.invoke({
            "idea": state["parsed_idea"]["startup_idea"],
            "competitors": state.get("competitors", [])
        })

        state["market_gaps"] = result if isinstance(result, list) else []
        return state

    except Exception as e:
        return add_error(state, f"gap_node failed: {str(e)}")


######################################################################

def skeptic_node(state):
    try:
        prompt = ChatPromptTemplate.from_template("""
            Act like a skeptical investor.

            Startup Idea:
            {idea}

            Pain Analysis:
            {pain}

            Pricing:
            {pricing}

            Competitors:
            {competitors}

            Return JSON array of brutal concerns.
        """)

        chain = prompt | get_llm() | JsonOutputParser()

        result = chain.invoke({
            "idea": state["parsed_idea"]["startup_idea"],
            "pain": state.get("problem_analysis", {}),
            "pricing": state.get("pricing_analysis", {}),
            "competitors": state.get("competitors", [])
        })

        state["skeptic_notes"] = result if isinstance(result, list) else []
        return state

    except Exception as e:
        return add_error(state, f"skeptic_node failed: {str(e)}")

#########################################################


def uvp_node(state):
    try:
        prompt = ChatPromptTemplate.from_template("""
            Create a sharp Unique Value Proposition.

            Idea:
            {idea}

            Pain:
            {pain}

            Market Gaps:
            {gaps}

            Return only final UVP sentence.
        """)

        chain = prompt | get_llm() | StrOutputParser()

        result = chain.invoke({
            "idea": state["parsed_idea"]["startup_idea"],
            "pain": state.get("problem_analysis", {}),
            "gaps": state.get("market_gaps", [])
        })

        state["uvp"] = result.strip()
        return state

    except Exception as e:
        return add_error(state, f"uvp_node failed: {str(e)}")


###########################################################


def judge_node(state):
    try:
        pain = state.get("problem_analysis", {}).get("pain_score", 0)
        urgency = state.get("problem_analysis", {}).get("urgency_score", 0)
        freq = state.get("problem_analysis", {}).get("frequency_score", 0)
        wtp = state.get("pricing_analysis", {}).get("willingness_to_pay", 0)

        score = (
            pain * 0.35 +
            urgency * 0.20 +
            freq * 0.15 +
            wtp * 0.30
        ) * 10

        score = int(score)

        if score >= 75:
            verdict = "PROCEED"
        elif score >= 60:
            verdict = "NICHE DOWN"
        elif score >= 40:
            verdict = "PIVOT"
        else:
            verdict = "REJECT"

        state["confidence_score"] = score
        state["verdict"] = verdict

        recs = []

        if verdict == "PROCEED":
            recs.append("Begin customer interviews immediately")
            recs.append("Build MVP quickly")
        elif verdict == "NICHE DOWN":
            recs.append("Target narrower segment")
        elif verdict == "PIVOT":
            recs.append("Rework customer or pain point")
        else:
            recs.append("Do not build yet")

        state["recommendations"] = recs

        return state

    except Exception as e:
        return add_error(state, f"judge_node failed: {str(e)}")


#########################################################

def report_node(state):
    try:
        state["final_report"] = {
            "idea": state["parsed_idea"]["startup_idea"],
            "problem_analysis": state.get("problem_analysis", {}),
            "personas": state.get("personas", []),
            "competitors": state.get("competitors", []),
            "pricing": state.get("pricing_analysis", {}),
            "market_gaps": state.get("market_gaps", []),
            "skeptic_notes": state.get("skeptic_notes", []),
            "uvp": state.get("uvp", ""),
            "confidence_score": state.get("confidence_score", 0),
            "verdict": state.get("verdict", ""),
            "recommendations": state.get("recommendations", []),
            "errors": state.get("errors", [])
        }

        return state

    except Exception as e:
        return add_error(state, f"report_node failed: {str(e)}")