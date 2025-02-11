from fastapi import Request
from fastapi.responses import JSONResponse

from app.errors.exception import BaseError


async def http_exception_handler(_request: Request, exc: BaseError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.to_dict())
