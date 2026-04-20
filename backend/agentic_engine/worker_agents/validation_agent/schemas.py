from pydantic import BaseModel, Field
from typing import List, Dict, Optional


class ParsedIdeaSchema(BaseModel):
    startup_idea: str
    product_type: Optional[str] = None
    domain: Optional[str] = None
    target_market: Optional[str] = None
    target_users: Optional[str] = None
    business_model_guess: Optional[str] = None


class ProblemAnalysisSchema(BaseModel):
    pain_score: int = Field(..., ge=0, le=10)
    urgency_score: int = Field(..., ge=0, le=10)
    frequency_score: int = Field(..., ge=0, le=10)
    emotional_pain_score: int = Field(..., ge=0, le=10)
    reasons: List[str]


class PersonaSchema(BaseModel):
    segment: str
    pain_points: List[str]
    budget_level: str
    buying_trigger: str


class CompetitorSchema(BaseModel):
    name: str
    type: str
    weakness: str


class PricingSchema(BaseModel):
    willingness_to_pay: int = Field(..., ge=0, le=10)
    pricing_model: str
    estimated_range: str
    notes: List[str]


class FinalVerdictSchema(BaseModel):
    verdict: str
    confidence_score: int
    recommendations: List[str]
