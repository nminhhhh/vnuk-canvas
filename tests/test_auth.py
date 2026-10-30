"""Authentication and user management integration tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import init_db
from app.main import app


@pytest.mark.asyncio
async def test_auth_workflow():
    """Comprehensive test covering user registration, login, and profile access."""
    # Ensure database tables exist
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Register a new user
        reg_payload = {
            "email": "testuser@example.com",
            "password": "StrongPassword123!",
            "full_name": "Test User",
        }
        reg_res = await client.post("/api/v1/auth/register", json=reg_payload)
        assert reg_res.status_code == 201
        user_data = reg_res.json()
        assert user_data["email"] == reg_payload["email"]
        assert user_data["full_name"] == reg_payload["full_name"]
        assert "id" in user_data
        assert "hashed_password" not in user_data

        # 2. Duplicate registration should return 409 Conflict
        dup_res = await client.post("/api/v1/auth/register", json=reg_payload)
        assert dup_res.status_code == 409

        # 3. Login with correct credentials
        login_payload = {
            "email": "testuser@example.com",
            "password": "StrongPassword123!",
        }
        login_res = await client.post("/api/v1/auth/login", json=login_payload)
        assert login_res.status_code == 200
        token_data = login_res.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"
        token = token_data["access_token"]

        # 4. Login with wrong password should return 401
        bad_login = await client.post(
            "/api/v1/auth/login",
            json={"email": "testuser@example.com", "password": "WrongPassword"},
        )
        assert bad_login.status_code == 401

        # 5. Access /me with valid Bearer token
        headers = {"Authorization": f"Bearer {token}"}
        me_res = await client.get("/api/v1/auth/me", headers=headers)
        assert me_res.status_code == 200
        me_data = me_res.json()
        assert me_data["email"] == "testuser@example.com"
        assert me_data["full_name"] == "Test User"

        # 6. Access /me without token should return 401
        unauth_res = await client.get("/api/v1/auth/me")
        assert unauth_res.status_code == 401
