"""Gemini AI API endpoints."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import ActiveUserDep
from app.schemas.ai import AIGenerateRequest, AIGenerateResponse, AIModelInfoResponse
from app.services.gemini_service import gemini_service

router = APIRouter(prefix="/ai", tags=["Gemini AI"])


class ConfigureKeyRequest(BaseModel):
    """Payload to update Gemini API Key directly from Web UI."""

    api_key: str = Field(min_length=10, description="Mã Google Gemini API Key")


@router.get(
    "/info",
    response_model=AIModelInfoResponse,
    summary="Get Gemini Model & Module Info",
)
async def get_gemini_info() -> AIModelInfoResponse:
    """Return status and configuration of the active Gemini 3.8 Flash module."""
    return gemini_service.get_info()


@router.post(
    "/configure-key",
    summary="Configure Gemini API Key and persist to .env",
)
async def configure_key(payload: ConfigureKeyRequest):
    """Save Gemini API Key to .env and immediately activate in memory."""
    success = gemini_service.save_api_key(payload.api_key)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Không thể ghi vào file .env",
        )
    return {
        "success": True,
        "message": "Đã lưu Gemini API Key vào file .env thành công và kích hoạt ngay lập tức!",
        "model": "gemini-3.8-flash",
    }


@router.post(
    "/generate",
    response_model=AIGenerateResponse,
    summary="Generate content with Gemini 3.8 Flash (Low)",
)
async def generate_content(
    req: AIGenerateRequest,
    current_user: ActiveUserDep,
) -> AIGenerateResponse:
    """Generate completion using Gemini 3.8 Flash model. Requires user authentication."""
    return await gemini_service.generate(req)
