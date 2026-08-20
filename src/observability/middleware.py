import time
import uuid

from fastapi import Request

from src.observability.logger import logger


async def observability_middleware(
    request: Request,
    call_next,
):
    request_id = str(uuid.uuid4())

    request.state.request_id = request_id

    start_time = time.perf_counter()

    logger.info(
        "HTTP request started | "
        "method=%s path=%s request_id=%s",
        request.method,
        request.url.path,
        request_id,
    )

    try:
        response = await call_next(request)

    except Exception:
        duration_ms = (
            time.perf_counter() - start_time
        ) * 1000

        logger.exception(
            "HTTP request failed | "
            "method=%s path=%s duration_ms=%.2f request_id=%s",
            request.method,
            request.url.path,
            duration_ms,
            request_id,
        )

        raise

    duration_ms = (
        time.perf_counter() - start_time
    ) * 1000

    response.headers["X-Request-ID"] = request_id

    logger.info(
        "HTTP request completed | "
        "method=%s path=%s status=%s "
        "duration_ms=%.2f request_id=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request_id,
    )

    return response