from fastapi import Depends, FastAPI

from app.config import Settings, get_settings
from app.models.buyer import BuyerRequest, BuyerResponse
from app.services.recommendation import generate_recommendations

app = FastAPI(title="buyer-agent", version="0.1.0")


@app.get("/health")
@app.get("/healthz")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/buyer-agent/recommendations", response_model=BuyerResponse)
def recommend_suppliers(
    request: BuyerRequest, settings: Settings = Depends(get_settings)
) -> BuyerResponse:
    return generate_recommendations(request=request, settings=settings)
