from __future__ import annotations

from typing import Dict, List

from app.models.buyer import BuyerRequest, Recommendation, ScoreBreakdown, SupplierOption


# Mock supplier data for v1; replace with real data/provider integration.
MOCK_SUPPLIERS: List[SupplierOption] = [
    SupplierOption(
        supplier_id="sup-001",
        supplier_name="Atlas Components Ltd.",
        unit_price=9.75,
        lead_time_days=7,
        quality_score=86,
        reliability_score=90,
        certifications=["ISO9001", "RoHS"],
        country="DE",
    ),
    SupplierOption(
        supplier_id="sup-002",
        supplier_name="Pacific Industrial Supply",
        unit_price=8.95,
        lead_time_days=12,
        quality_score=79,
        reliability_score=82,
        certifications=["ISO9001"],
        country="CN",
    ),
    SupplierOption(
        supplier_id="sup-003",
        supplier_name="Northstar Manufacturing",
        unit_price=10.25,
        lead_time_days=5,
        quality_score=91,
        reliability_score=88,
        certifications=["ISO9001", "RoHS", "REACH"],
        country="PL",
    ),
]


def _clamp_0_100(value: float) -> float:
    return max(0.0, min(100.0, value))


def _price_score(unit_price: float, budget_per_unit: float) -> float:
    # Score declines linearly as quote exceeds budget.
    if budget_per_unit <= 0:
        return 0.0
    ratio = unit_price / budget_per_unit
    if ratio <= 1:
        return 100.0 - (ratio * 20.0)
    return _clamp_0_100(80.0 - ((ratio - 1.0) * 120.0))


def _lead_time_score(lead_time_days: int, delivery_days_max: int) -> float:
    if delivery_days_max <= 0:
        return 0.0
    ratio = lead_time_days / delivery_days_max
    if ratio <= 1:
        return 100.0 - (ratio * 25.0)
    return _clamp_0_100(75.0 - ((ratio - 1.0) * 140.0))


def _compliance_score(
    supplier_certifications: List[str], required_certifications: List[str]
) -> float:
    if not required_certifications:
        return 100.0
    supplier_set = {cert.lower() for cert in supplier_certifications}
    required_set = {cert.lower() for cert in required_certifications}
    if not required_set:
        return 100.0
    matched = len(supplier_set.intersection(required_set))
    return (matched / len(required_set)) * 100.0


def score_supplier(supplier: SupplierOption, request: BuyerRequest) -> ScoreBreakdown:
    price = _price_score(supplier.unit_price, request.budget_per_unit)
    lead = _lead_time_score(supplier.lead_time_days, request.delivery_days_max)
    quality = _clamp_0_100(supplier.quality_score)
    reliability = _clamp_0_100(supplier.reliability_score)
    compliance = _compliance_score(supplier.certifications, request.required_certifications)

    # Weights sum to 1.0 for transparent ranking.
    total = (
        (price * 0.30)
        + (lead * 0.25)
        + (quality * 0.20)
        + (reliability * 0.15)
        + (compliance * 0.10)
    )

    return ScoreBreakdown(
        price_score=round(price, 2),
        lead_time_score=round(lead, 2),
        quality_score=round(quality, 2),
        reliability_score=round(reliability, 2),
        compliance_score=round(compliance, 2),
        total_score=round(total, 2),
    )


def _build_risks(
    supplier: SupplierOption, request: BuyerRequest, score: ScoreBreakdown
) -> List[str]:
    risks: List[str] = []
    if supplier.unit_price > request.budget_per_unit:
        risks.append("Quoted unit price is above budget target.")
    if supplier.lead_time_days > request.delivery_days_max:
        risks.append("Lead time exceeds requested delivery window.")
    if supplier.quality_score < request.quality_min_score:
        risks.append("Quality score falls below requested minimum.")
    if score.compliance_score < 100:
        risks.append("Missing one or more required certifications.")
    return risks


def _build_rationale(
    supplier: SupplierOption, score: ScoreBreakdown, risks: List[str]
) -> str:
    strengths: List[str] = []
    if score.price_score >= 80:
        strengths.append("competitive pricing")
    if score.lead_time_score >= 80:
        strengths.append("fast lead time")
    if score.quality_score >= 85:
        strengths.append("strong quality profile")
    if score.reliability_score >= 85:
        strengths.append("high reliability")
    if score.compliance_score == 100:
        strengths.append("full certification match")

    if not strengths:
        strengths.append("balanced sourcing profile")
    risk_text = " Risks: " + "; ".join(risks) if risks else ""
    return (
        f"{supplier.supplier_name} is recommended due to "
        f"{', '.join(strengths)}.{risk_text}"
    )


def build_recommendations(request: BuyerRequest, top_k: int = 3) -> List[Recommendation]:
    scored: List[Dict[str, object]] = []
    for supplier in MOCK_SUPPLIERS:
        score = score_supplier(supplier, request)
        risks = _build_risks(supplier, request, score)
        rationale = _build_rationale(supplier, score, risks)
        scored.append(
            {
                "supplier": supplier,
                "score": score,
                "risks": risks,
                "rationale": rationale,
            }
        )

    ranked = sorted(
        scored, key=lambda item: item["score"].total_score, reverse=True  # type: ignore[arg-type]
    )[:top_k]

    return [
        Recommendation(
            supplier=item["supplier"],  # type: ignore[arg-type]
            score=item["score"],  # type: ignore[arg-type]
            rationale=item["rationale"],  # type: ignore[arg-type]
            risks=item["risks"],  # type: ignore[arg-type]
        )
        for item in ranked
    ]
