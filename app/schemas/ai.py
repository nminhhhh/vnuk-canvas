"""Gemini AI schemas."""
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field


class AIGenerateRequest(BaseModel):
    """Payload for generating text with Gemini 3.8 Flash."""

    prompt: Annotated[str, Field(min_length=1, max_length=10000, description="Nội dung prompt")]
    system_instruction: Annotated[str | None, Field(default=None, max_length=2000)] = None
    temperature: Annotated[float, Field(default=0.7, ge=0.0, le=2.0)] = 0.7
    max_output_tokens: Annotated[int, Field(default=1024, ge=1, le=8192)] = 1024


class AIGenerateResponse(BaseModel):
    """Response containing Gemini generated content."""

    content: str
    model: str
    mode: str
    created_at: datetime
    metadata: dict[str, Any] = {}


class AIModelInfoResponse(BaseModel):
    """System information on the active Gemini module."""

    active_model: str
    mode: str
    is_api_key_configured: bool
    status: str
