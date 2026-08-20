import logging

from fastapi.testclient import TestClient

from src.api.main import app


def test_financial_flow_logs_processing(caplog):
    client = TestClient(app)

    with caplog.at_level(
        logging.INFO,
        logger="finassist.api",
    ):
        response = client.post(
            "/financial/messages",
            json={
                "external_user_id": "logging-user",
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
        "Financial message processing started" in message
        for message in messages
    )

    assert any(
        "Financial message processing completed" in message
        for message in messages
    )