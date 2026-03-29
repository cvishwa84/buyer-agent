from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_recommendations_endpoint_happy_path() -> None:
    payload = {
        "item_name": "Industrial Ball Bearings",
        "quantity": 1000,
        "budget_per_unit": 12.0,
        "delivery_days_max": 20,
        "destination_country": "US",
        "quality_min_score": 75,
        "required_certifications": ["ISO9001"],
    }
    response = client.post("/buyer-agent/recommendations", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "strategy_summary" in data
    assert len(data["recommendations"]) >= 1
    assert data["recommendations"][0]["score"]["total_score"] >= data["recommendations"][-1]["score"][
        "total_score"
    ]


def test_recommendations_endpoint_validation_error() -> None:
    invalid_payload = {
        "item_name": "",
        "quantity": 0,
        "budget_per_unit": -1,
        "delivery_days_max": 0,
        "destination_country": "U",
    }
    response = client.post("/buyer-agent/recommendations", json=invalid_payload)
    assert response.status_code == 422
