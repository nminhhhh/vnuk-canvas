"""Dashboard endpoint integration test."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import init_db
from app.main import app


@pytest.mark.asyncio
async def test_dashboard_routes():
    """Verify that dashboard SPA is successfully rendered at / and /dashboard."""
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Root route
        res_root = await client.get("/")
        assert res_root.status_code == 200
        assert "FastAPI + Gemini 3.8 Flash Dashboard" in res_root.text
        assert "Gemini 3.8 Flash (Low)" in res_root.text

        # 2. /dashboard route
        res_dash = await client.get("/dashboard")
        assert res_dash.status_code == 200
        assert "FastAPI + Gemini 3.8 Flash Dashboard" in res_dash.text
