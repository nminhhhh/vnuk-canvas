"""Canvas LMS VNUK integration tests."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.core.database import init_db
from app.main import app


@pytest.mark.asyncio
async def test_canvas_lms_workflow():
    """Verify Canvas LMS authentication, courses, modules and assignments."""
    await init_db()

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Connect Canvas (Demo token)
        conn_res = await client.post(
            "/api/v1/canvas/connect",
            json={"canvas_url": "https://canvas.vnuk.edu.vn", "access_token": "DEMO_VNUK"},
        )
        assert conn_res.status_code == 200
        assert conn_res.json()["success"] is True

        headers = {
            "x-canvas-token": "DEMO_VNUK",
            "x-canvas-url": "https://canvas.vnuk.edu.vn",
        }

        # 2. Get Courses
        courses_res = await client.get("/api/v1/canvas/courses", headers=headers)
        assert courses_res.status_code == 200
        courses = courses_res.json()
        assert len(courses) >= 1
        first_course_id = courses[0]["id"]

        # 3. Get Course Modules
        modules_res = await client.get(
            f"/api/v1/canvas/courses/{first_course_id}/modules",
            headers=headers,
        )
        assert modules_res.status_code == 200
        modules = modules_res.json()
        assert len(modules) >= 1

        # 4. Get Assignments
        assign_res = await client.get(
            f"/api/v1/canvas/courses/{first_course_id}/assignments",
            headers=headers,
        )
        assert assign_res.status_code == 200
        assignments = assign_res.json()
        assert len(assignments) >= 1

        # 5. Get Upcoming Todos / Deadlines
        todos_res = await client.get("/api/v1/canvas/todos", headers=headers)
        assert todos_res.status_code == 200
        todos = todos_res.json()
        assert len(todos) >= 1
