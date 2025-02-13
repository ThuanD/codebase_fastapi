from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user, get_db
from app.models.user import User
from app.schemas.auth import (
    RefreshTokenRequest,
    RegisterRequest,
    RegisterResponse,
    TokenResponse,
)
from app.services.auth import AuthService

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
async def register(
    register_data: RegisterRequest, db: Session = Depends(get_db)
) -> User:
    """Register new user."""
    auth_service = AuthService(db)
    return auth_service.register(register_data)


@router.post("/login", response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> TokenResponse:
    auth_service = AuthService(db)
    return auth_service.login(
        email=form_data.username,  # OAuth2 form uses username field for email
        password=form_data.password,
    )


@router.post("/refresh")
async def refresh_token(
    refresh_data: RefreshTokenRequest, db: Session = Depends(get_db)
) -> TokenResponse:
    """Refresh access token."""
    auth_service = AuthService(db)
    return auth_service.refresh_token(refresh_token=refresh_data.refresh_token)


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)
):
    auth_service = AuthService(db)
    return auth_service.logout(current_user)


@router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
