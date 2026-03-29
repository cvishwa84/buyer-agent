from app.config import Settings
from app.models.buyer import BuyerRequest, BuyerResponse
from app.services.llm import generate_strategy_summary
from app.services.sourcing import build_recommendations


def generate_recommendations(request: BuyerRequest, settings: Settings) -> BuyerResponse:
    strategy_summary = generate_strategy_summary(request=request, settings=settings)
    recommendations = build_recommendations(request=request)
    return BuyerResponse(strategy_summary=strategy_summary, recommendations=recommendations)
