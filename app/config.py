from functools import lru_cache
from typing import Optional
import os

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_name: str = "buyer-agent"
    openai_api_key: Optional[str] = Field(default=None)
    openai_model: str = Field(default="gpt-4o-mini")
    llm_timeout_seconds: float = Field(default=20.0)
    http_timeout_seconds: float = Field(default=10.0)
    log_prompts: bool = Field(default=True)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        llm_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "20")),
        http_timeout_seconds=float(os.getenv("HTTP_TIMEOUT_SECONDS", "10")),
        log_prompts=os.getenv("LOG_PROMPTS", "true").lower() == "true",
    )
