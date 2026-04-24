from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class RevenueModelSchema(BaseModel):
    primary_model: str
    secondary_model: Optional[str] = None
    rationale: str
    confidence: float = 0.0


class PricingTier(BaseModel):
    name: str
    price: str
    features: List[str] = []


class PricingStrategySchema(BaseModel):
    pricing_model: str
    tiers: List[PricingTier]
    launch_strategy: str
    rationale: str
    confidence: float = 0.0


class UnitEconomicsSchema(BaseModel):
    cac: str
    ltv: str
    ltv_cac_ratio: str
    gross_margin: str
    payback_period: str
    assumptions: List[str] = []


class ViabilitySchema(BaseModel):
    decision: str
    confidence: float
    risks: List[str]
    opportunities: List[str]
    rationale: str


class ExecutiveOpinionSchema(BaseModel):
    role: str
    stance: str
    reasoning: str
    confidence: float


class FinalDecisionSchema(BaseModel):
    verdict: str
    summary: str
    next_steps: List[str]
    confidence: float


class ResearchSchema(BaseModel):
    competitors: List[Dict[str, Any]] = []
    benchmarks: Dict[str, Any] = {}
    notes: List[str] = []