"""Canvas LMS API Endpoints."""
from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, status

from app.schemas.canvas import (
    CanvasAssignment,
    CanvasConnectRequest,
    CanvasCourse,
    CanvasModule,
    CanvasTodo,
)
from app.services.canvas_service import canvas_service

router = APIRouter(prefix="/canvas", tags=["Canvas LMS VNUK"])


@router.post(
    "/connect",
    summary="Connect and verify Canvas LMS Account",
)
async def connect_canvas(payload: CanvasConnectRequest):
    """Verify Canvas API Token and connect user's VNUK Canvas account."""
    result = await canvas_service.verify_connection(
        canvas_url=payload.canvas_url,
        access_token=payload.access_token,
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result.get("error", "Không thể xác thực Canvas Access Token"),
        )
    return result


@router.get(
    "/courses",
    response_model=list[CanvasCourse],
    summary="List enrolled Canvas courses",
)
async def get_courses(
    x_canvas_token: Annotated[str, Header(description="Canvas Personal Access Token")],
    x_canvas_url: Annotated[str, Header(description="Canvas LMS URL")] = "https://canvas.vnuk.edu.vn",
) -> list[CanvasCourse]:
    """Retrieve all enrolled courses from VNUK Canvas LMS."""
    return await canvas_service.get_courses(x_canvas_url, x_canvas_token)


@router.get(
    "/courses/{course_id}/modules",
    response_model=list[CanvasModule],
    summary="Get learning modules & materials for a course",
)
async def get_course_modules(
    course_id: int,
    x_canvas_token: Annotated[str, Header(description="Canvas Personal Access Token")],
    x_canvas_url: Annotated[str, Header(description="Canvas LMS URL")] = "https://canvas.vnuk.edu.vn",
) -> list[CanvasModule]:
    """Retrieve all weekly modules, slides, and lessons of a specific course."""
    return await canvas_service.get_course_modules(x_canvas_url, x_canvas_token, course_id)


@router.get(
    "/courses/{course_id}/assignments",
    response_model=list[CanvasAssignment],
    summary="Get assignments & homework for a course",
)
async def get_course_assignments(
    course_id: int,
    x_canvas_token: Annotated[str, Header(description="Canvas Personal Access Token")],
    x_canvas_url: Annotated[str, Header(description="Canvas LMS URL")] = "https://canvas.vnuk.edu.vn",
) -> list[CanvasAssignment]:
    """Retrieve assignments, due dates and submission status for a specific course."""
    return await canvas_service.get_course_assignments(x_canvas_url, x_canvas_token, course_id)


@router.get(
    "/todos",
    response_model=list[CanvasTodo],
    summary="Get upcoming deadlines across all Canvas courses",
)
async def get_upcoming_todos(
    x_canvas_token: Annotated[str, Header(description="Canvas Personal Access Token")],
    x_canvas_url: Annotated[str, Header(description="Canvas LMS URL")] = "https://canvas.vnuk.edu.vn",
) -> list[CanvasTodo]:
    """Retrieve all pending deadlines and assignments sorted by due date."""
    return await canvas_service.get_upcoming_todos(x_canvas_url, x_canvas_token)
