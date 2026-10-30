"""Health check endpoints."""
from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="System Health Status")
async def health_check() -> dict[str, Any]:
    """Check API server health status and timestamp."""
    return {
        "status": "healthy",
        "service": "fastapi-core",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "orchestrated_by": "Antigravity Master Orchestrator",
    }
