"""Pydantic schemas for Canvas LMS Integration."""
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field, HttpUrl


class CanvasConnectRequest(BaseModel):
    """Payload to connect user's Canvas account."""

    canvas_url: Annotated[str, Field(default="https://canvas.vnuk.edu.vn", description="Địa chỉ hệ thống Canvas LMS")] = "https://canvas.vnuk.edu.vn"
    access_token: Annotated[str, Field(min_length=10, description="Canvas Personal Access Token")]


class CanvasModuleItem(BaseModel):
    """Individual item/lesson material in a module."""

    id: int
    title: str
    type: str  # File, Page, Assignment, ExternalUrl
    html_url: str | None = None
    content_id: int | None = None


class CanvasModule(BaseModel):
    """Learning unit / week module in a course."""

    id: int
    name: str
    items_count: int = 0
    items: list[CanvasModuleItem] = []


class CanvasAssignment(BaseModel):
    """Assignment with due dates and submission tracking."""

    id: int
    name: str
    description: str | None = None
    due_at: str | None = None
    points_possible: float | None = None
    has_submitted: bool = False
    html_url: str | None = None


class CanvasCourse(BaseModel):
    """Enrolled course in Canvas LMS."""

    id: int
    name: str
    course_code: str
    term: str | None = None
    enrollment_type: str | None = "student"
    workflow_state: str = "available"
    modules: list[CanvasModule] = []
    assignments: list[CanvasAssignment] = []


class CanvasTodo(BaseModel):
    """Upcoming deadline or assignment item."""

    type: str
    assignment: CanvasAssignment
    course_name: str
    due_at: str | None = None
