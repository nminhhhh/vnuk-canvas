"""Gemini AI module integration tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import init_db
from app.main import app


@pytest.mark.asyncio
async def test_gemini_info_and_generation():
    """Verify Gemini AI module info and completion generation endpoint."""
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Info endpoint (public)
        info_res = await client.get("/api/v1/ai/info")
        assert info_res.status_code == 200
        info_data = info_res.json()
        assert info_data["active_model"] == "gemini-3.8-flash"
        assert info_data["mode"] == "low"
        assert "status" in info_data

        # 2. Authentication for generate endpoint
        user_payload = {
            "email": "aiuser@example.com",
            "password": "Password123!",
            "full_name": "AI Tester",
        }
        await client.post("/api/v1/auth/register", json=user_payload)
        login_res = await client.post(
            "/api/v1/auth/login",
            json={"email": user_payload["email"], "password": user_payload["password"]},
        )
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Generate completion
        gen_payload = {
            "prompt": "Tóm tắt ưu điểm của mô hình kiến trúc Clean Architecture trong 1 câu.",
            "temperature": 0.5,
        }
        gen_res = await client.post("/api/v1/ai/generate", json=gen_payload, headers=headers)
        assert gen_res.status_code == 200
        gen_data = gen_res.json()
        assert "content" in gen_data
        assert gen_data["model"] == "gemini-3.8-flash"
        assert gen_data["mode"] == "low"
