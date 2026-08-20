from fastapi.testclient import TestClient

from src.api.main import app


def test_health_check_returns_ok():

    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "ok",
        "service": "finassist-ai",
    }