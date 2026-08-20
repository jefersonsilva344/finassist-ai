from fastapi import Request
from fastapi.responses import JSONResponse

from src.api.errors.exceptions import FinAssistError


async def finassist_error_handler(
    request: Request,
    exc: FinAssistError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
        },
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": (
                "Ocorreu um erro interno ao processar a solicitação."
            ),
        },
    )