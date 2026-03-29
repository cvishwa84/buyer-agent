import logging
from typing import Any, Dict

from app.config import Settings
from app.models.buyer import BuyerRequest

logger = logging.getLogger(__name__)


SENSITIVE_KEYS = {"openai_api_key", "api_key", "authorization", "token", "password"}


def _redact(value: Any) -> Any:
    if isinstance(value, dict):
        redacted: Dict[str, Any] = {}
        for k, v in value.items():
            if k.lower() in SENSITIVE_KEYS:
                redacted[k] = "[REDACTED]"
            else:
                redacted[k] = _redact(v)
        return redacted
    if isinstance(value, list):
        return [_redact(item) for item in value]
    return value


def generate_strategy_summary(request: BuyerRequest, settings: Settings) -> str:
    """
    Lightweight strategy generator.
    In v1, keep deterministic behavior; later this can call OpenAI/LangChain.
    """
    prompt_payload = {
        "role": "procurement_analyst",
        "item_name": request.item_name,
        "quantity": request.quantity,
        "budget_per_unit": request.budget_per_unit,
        "delivery_days_max": request.delivery_days_max,
        "destination_country": request.destination_country,
        "quality_min_score": request.quality_min_score,
        "required_certifications": request.required_certifications,
        "notes": request.notes,
        "openai_api_key": settings.openai_api_key,
    }
    if settings.log_prompts:
        logger.info("buyer_agent.strategy_input=%s", _redact(prompt_payload))

    cert_text = (
        ", ".join(request.required_certifications)
        if request.required_certifications
        else "no mandatory certifications"
    )
    summary = (
        f"Source {request.quantity} units of {request.item_name} with target unit price <= "
        f"{request.budget_per_unit:.2f}, lead time <= {request.delivery_days_max} days to "
        f"{request.destination_country}. Prioritize suppliers with quality >= "
        f"{request.quality_min_score:.0f} and {cert_text}. Rank by blended cost, speed, "
        "quality, reliability, and compliance risk."
    )
    if settings.log_prompts:
        logger.info("buyer_agent.strategy_output=%s", summary)
    return summary
