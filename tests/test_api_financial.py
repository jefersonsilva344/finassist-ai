from fastapi.testclient import TestClient

from src.api.main import app
from src.api.routes.financial import get_container


class FakeFinancialFlow:

    def process_message(
        self,
        external_user_id: str,
        message: str,
    ) -> str:

        assert external_user_id == "user-001"
        assert message == "Recebo R$ 4.000 e gasto R$ 3.000"

        return "Seu saldo mensal é de R$ 1.000,00."


class FakeApplicationContainer:

    def __init__(self):
        self.financial_flow = FakeFinancialFlow()


def test_process_financial_message_returns_response():

    app.dependency_overrides[get_container] = (
        lambda: FakeApplicationContainer()
    )

    try:
        client = TestClient(app)

        response = client.post(
            "/financial/messages",
            json={
                "external_user_id": "user-001",
                "message": "Recebo R$ 4.000 e gasto R$ 3.000",
            },
        )

        assert response.status_code == 200

        assert response.json() == {
            "response": "Seu saldo mensal é de R$ 1.000,00."
        }

    finally:
        app.dependency_overrides.clear()