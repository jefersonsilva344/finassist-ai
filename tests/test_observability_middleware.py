import logging

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.observability.middleware import (
    observability_middleware,
)


def create_test_app() -> FastAPI:
    app = FastAPI()

    app.middleware("http")(
        observability_middleware
    )

    @app.get("/test")
    def test_route():
        return {"status": "ok"}

    return app


def test_middleware_adds_request_id_header():
    app = create_test_app()

    client = TestClient(app)

    response = client.get("/test")

    assert response.status_code == 200

    request_id = response.headers.get(
        "X-Request-ID"
    )

    assert request_id is not None
    assert len(request_id) == 36


def test_middleware_logs_request_completion(
    caplog,
):
    app = create_test_app()

    client = TestClient(app)

    with caplog.at_level(
        logging.INFO,
        logger="finassist.api",
    ):
        response = client.get("/test")

    assert response.status_code == 200

    messages = [
        record.message
        for record in caplog.records
        if record.name == "finassist.api"
    ]

    assert any(
        "HTTP request started" in message
        for message in messages
    )

    assert any(
        "HTTP request completed" in message
        for message in messages
    )