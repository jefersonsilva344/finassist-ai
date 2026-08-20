from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.routes.financial import router as financial_router
from src.api.routes.health import router as health_router
from src.observability.logging import configure_logging
from src.observability.middleware import observability_middleware


configure_logging()


def create_app() -> FastAPI:
    app = FastAPI(
        title="FinAssist AI",
        description="API de educação e organização financeira pessoal.",
        version="1.0.0",
    )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error.",
            },
        )

    app.middleware("http")(observability_middleware)

    app.include_router(health_router)
    app.include_router(financial_router)

    return app


app = create_app()