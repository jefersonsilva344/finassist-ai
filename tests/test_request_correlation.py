import logging

from fastapi.testclient import TestClient

from src.api.main import app


def test_financial_logs_contain_same_request_id(caplog):
    client = TestClient(app)

    with caplog.at_level(
        logging.INFO,
        logger="finassist.api",
    ):
        response = client.post(
            "/financial/messages",
            json={
                "external_user_id": "correlation-user",
                "message": "Minha renda é R$ 5000.",
            },
        )

    assert response.status_code == 200

    request_id = response.headers.get("X-Request-ID")

    assert request_id is not None

    messages = [
        record.message
        for record in caplog.records
        if record.name == "finassist.api"
    ]

    started = [
        message
        for message in messages
        if "Financial message processing started" in message
    ]

    completed = [
        message
        for message in messages
        if "Financial message processing completed" in message
    ]

    assert started
    assert completed

    assert request_id in started[0]
    assert request_id in completed[0]