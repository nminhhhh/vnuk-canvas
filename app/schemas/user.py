"""Pydantic DTO schemas for User & Authentication.
Zero third-party optional dependency on email-validator.
"""
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    """Base user attributes."""

    email: Annotated[str, Field(min_length=3, max_length=255, description="Địa chỉ email")]
    full_name: Annotated[str | None, Field(default=None, max_length=255)] = None
    is_active: bool = True


class UserCreate(BaseModel):
    """Schema for registering a new user."""

    email: Annotated[str, Field(min_length=3, max_length=255, description="Địa chỉ email")]
    password: Annotated[str, Field(min_length=6, max_length=128)]
    full_name: Annotated[str | None, Field(default=None, max_length=255)] = None


class UserUpdate(BaseModel):
    """Schema for updating user details."""

    email: Annotated[str | None, Field(default=None, min_length=3, max_length=255)] = None
    password: Annotated[str | None, Field(default=None, min_length=6, max_length=128)] = None
    full_name: Annotated[str | None, Field(default=None, max_length=255)] = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """Public user response schema."""

    id: int
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """OAuth2 / JWT Token schema."""

    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """Decoded JWT payload data."""

    sub: str | None = None
    exp: int | None = None


class LoginRequest(BaseModel):
    """Direct JSON body login request schema."""

    email: Annotated[str, Field(min_length=3, max_length=255)]
    password: str
