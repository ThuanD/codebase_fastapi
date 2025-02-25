from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.schemas.user import User as UserSchema
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register(register_data: RegisterRequest,
                   db: AsyncSession = Depends(get_db)) -> User:
    """Register a new user."""
    auth_service = AuthService(db)
    return await auth_service.register(register_data)


@router.post("/login", response_model=TokenResponse)
async def login(login_data: LoginRequest,
                db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Login user and return access token."""
    auth_service = AuthService(db)
    return await auth_service.login(login_data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_data: RefreshTokenRequest,
                        db: AsyncSession = Depends(get_db)) -> TokenResponse:
    """Refresh access token."""
    auth_service = AuthService(db)
    return await auth_service.refresh_token(refresh_data.refresh_token)


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_active_user),
                 db: AsyncSession = Depends(get_db)) -> dict:
    """Logout current user."""
    auth_service = AuthService(db)
    return await auth_service.logout(current_user)


@router.get("/me")
async def read_users_me(
        current_user: User = Depends(get_current_active_user)) -> UserSchema:
    """Get current user information."""
    return current_user
