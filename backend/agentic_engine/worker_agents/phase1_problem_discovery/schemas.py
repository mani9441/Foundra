from pydantic import BaseModel, Field
from typing import List


class ProblemStatementOutput(BaseModel):
    problem_statement: str = Field(...)


class TargetUserOutput(BaseModel):
    target_users: List[str]


class PainEvidenceOutput(BaseModel):
    evidence_points: List[str]
    urgency_score: int
    frequency_score: int


class AlternativesOutput(BaseModel):
    competitors: List[str]
    weaknesses: List[str]


class ObjectiveOutput(BaseModel):
    objective: str


class JudgeOutput(BaseModel):
    decision: str
    confidence: int
    reasons: List[str]