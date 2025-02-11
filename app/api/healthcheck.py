from fastapi import APIRouter

from app.schemas.health import HealthCheckSchema

router = APIRouter()


@router.get("", response_model=HealthCheckSchema)
async def get():
    return {"status": "healthy"}
