from typing import List, Optional

from pydantic import BaseModel, Field


class BuyerRequest(BaseModel):
    item_name: str = Field(..., min_length=1, description="Name of the item to source.")
    quantity: int = Field(..., ge=1, description="Number of units requested.")
    budget_per_unit: float = Field(..., gt=0, description="Target max budget per unit.")
    delivery_days_max: int = Field(..., ge=1, description="Maximum acceptable lead time.")
    destination_country: str = Field(..., min_length=2)
    quality_min_score: float = Field(default=70, ge=0, le=100)
    required_certifications: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class SupplierOption(BaseModel):
    supplier_id: str
    supplier_name: str
    unit_price: float
    lead_time_days: int
    quality_score: float
    reliability_score: float
    certifications: List[str]
    country: str


class ScoreBreakdown(BaseModel):
    price_score: float
    lead_time_score: float
    quality_score: float
    reliability_score: float
    compliance_score: float
    total_score: float


class Recommendation(BaseModel):
    supplier: SupplierOption
    score: ScoreBreakdown
    rationale: str
    risks: List[str]


class BuyerResponse(BaseModel):
    strategy_summary: str
    recommendations: List[Recommendation]
