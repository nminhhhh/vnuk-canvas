"""Authentication and user account endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import ActiveUserDep, SessionDep
from app.core.security import create_access_token
from app.models.user import User
from app.schemas.user import LoginRequest, Token, UserCreate, UserResponse
from app.services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register_user(
    user_in: UserCreate,
    db: SessionDep,
) -> User:
    """Register a new user account with unique email verification."""
    existing_user = await user_service.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email address already exists.",
        )
    new_user = await user_service.create(db, user_in=user_in)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="User Login (JSON body)",
)
async def login_json(
    credentials: LoginRequest,
    db: SessionDep,
) -> Token:
    """Authenticate with email and password via JSON payload and return JWT access token."""
    user = await user_service.authenticate(
        db,
        email=credentials.email,
        password=credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account",
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/login-form",
    response_model=Token,
    summary="User Login (OAuth2 Form / Swagger UI)",
)
async def login_form(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
) -> Token:
    """OAuth2 compatible token login for Swagger UI interactive testing."""
    user = await user_service.authenticate(
        db,
        email=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account",
        )

    access_token = create_access_token(subject=user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get Current User Profile",
)
async def get_me(
    current_user: ActiveUserDep,
) -> User:
    """Return profile details for currently authenticated user."""
    return current_user
