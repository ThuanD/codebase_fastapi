from fastapi import APIRouter

from app.api import auth, healthcheck, users

router = APIRouter()

router.include_router(auth.router, tags=["authentication"], prefix="/auth")
router.include_router(healthcheck.router, tags=["healthcheck"], prefix="/healthcheck")
router.include_router(users.router, tags=["users"], prefix="/users")
