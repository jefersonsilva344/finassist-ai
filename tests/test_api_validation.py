from fastapi.testclient import TestClient

from src.api.main import app
from src.api.routes.financial import get_container


class FakeFinancialFlow:

    def process_message(
        self,
        external_user_id: str,
        message: str,
    ) -> str:

        return "Resposta simulada."


class FakeApplicationContainer:

    def __init__(self):
        self.financial_flow = FakeFinancialFlow()


def client() -> TestClient:

    app.dependency_overrides[get_container] = (
        lambda: FakeApplicationContainer()
    )

    return TestClient(app)


def test_financial_message_rejects_empty_external_user_id():

    test_client = client()

    try:
        response = test_client.post(
            "/financial/messages",
            json={
                "external_user_id": "",
                "message": "Minha renda é R$ 5.000",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()


def test_financial_message_rejects_empty_message():

    test_client = client()

    try:
        response = test_client.post(
            "/financial/messages",
            json={
                "external_user_id": "user-001",
                "message": "",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()


def test_financial_message_requires_external_user_id():

    test_client = client()

    try:
        response = test_client.post(
            "/financial/messages",
            json={
                "message": "Minha renda é R$ 5.000",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()


def test_financial_message_requires_message():

    test_client = client()

    try:
        response = test_client.post(
            "/financial/messages",
            json={
                "external_user_id": "user-001",
            },
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()


def test_financial_message_requires_json_body():

    test_client = client()

    try:
        response = test_client.post(
            "/financial/messages",
            json={},
        )

        assert response.status_code == 422

    finally:
        app.dependency_overrides.clear()