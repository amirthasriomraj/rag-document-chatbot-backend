from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from app.schemas.error import ErrorResponse
from app.core.logging import logger


async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            message=exc.detail,
            status_code=exc.status_code
        ).model_dump()
    )

async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            message="Internal server error",
            status_code=500
        ).model_dump()
    )