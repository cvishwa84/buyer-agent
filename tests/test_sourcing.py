from app.models.buyer import BuyerRequest
from app.models.buyer import SupplierOption
from app.services.sourcing import build_recommendations, score_supplier


def test_score_supplier_includes_compliance_penalty_when_missing_cert() -> None:
    request = BuyerRequest(
        item_name="Industrial Pump",
        quantity=50,
        budget_per_unit=110.0,
        delivery_days_max=14,
        destination_country="US",
        quality_min_score=80,
        required_certifications=["ISO9001"],
    )
    supplier = SupplierOption(
        supplier_id="x",
        supplier_name="No Cert Co",
        unit_price=90.0,
        lead_time_days=10,
        quality_score=86.0,
        reliability_score=80.0,
        certifications=[],
        country="US",
    )

    score = score_supplier(supplier, request)
    assert score.compliance_score == 0.0
    assert score.total_score < 90.0


def test_build_recommendations_returns_ranked_suppliers() -> None:
    request = BuyerRequest(
        item_name="Industrial Pump",
        quantity=20,
        budget_per_unit=120.0,
        delivery_days_max=12,
        destination_country="US",
        quality_min_score=75,
        required_certifications=["ISO9001"],
    )
    recommendations = build_recommendations(request)

    assert len(recommendations) > 0
    totals = [r.score.total_score for r in recommendations]
    assert totals == sorted(totals, reverse=True)
