import logging

from fastapi.testclient import TestClient

from src.api.main import app


def test_financial_request_contains_request_id():
    client = TestClient(app)

    response = client.post(
        "/financial/messages",
        json={
            "external_user_id": "observability-user",
            "message": "Minha renda é R$ 5000.",
        },
    )

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None
    assert len(request_id) > 0


def test_financial_request_is_logged(caplog):
    client = TestClient(app)

    with caplog.at_level(
        logging.INFO,
        logger="finassist.api",
    ):
        response = client.post(
            "/financial/messages",
            json={
                "external_user_id": "observability-user",
                "message": "Minha renda é R$ 5000.",
            },
        )

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