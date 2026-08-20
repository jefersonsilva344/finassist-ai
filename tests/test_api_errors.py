import asyncio
import json

from fastapi.testclient import TestClient

from src.api.errors.exceptions import (
    ExternalServiceError,
    FinAssistError,
    InvalidFinancialRequestError,
)
from src.api.errors.handlers import (
    finassist_error_handler,
    unexpected_error_handler,
)
from src.api.main import create_app


def test_unexpected_error_returns_safe_response():
    app = create_app()

    @app.get("/test-error")
    def failing_endpoint():
        raise RuntimeError("internal secret")

    client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = client.get("/test-error")

    assert response.status_code == 500

    assert response.json() == {
        "detail": "Internal server error.",
    }


def test_finassist_error_preserves_message():
    error = FinAssistError("Erro interno")

    assert error.message == "Erro interno"
    assert str(error) == "Erro interno"
    assert error.status_code == 500
    assert error.error_code == "internal_error"


def test_invalid_financial_request_error_has_expected_configuration():
    error = InvalidFinancialRequestError(
        "Solicitação financeira inválida"
    )

    assert error.message == "Solicitação financeira inválida"
    assert str(error) == "Solicitação financeira inválida"
    assert error.status_code == 400
    assert error.error_code == "invalid_financial_request"


def test_external_service_error_has_expected_configuration():
    error = ExternalServiceError(
        "Serviço externo indisponível"
    )

    assert error.message == "Serviço externo indisponível"
    assert str(error) == "Serviço externo indisponível"
    assert error.status_code == 503
    assert error.error_code == "external_service_unavailable"


def test_finassist_error_handler_returns_expected_response():
    error = InvalidFinancialRequestError(
        "Dados financeiros inválidos"
    )

    response = asyncio.run(
        finassist_error_handler(
            request=None,
            exc=error,
        )
    )

    assert response.status_code == 400

    assert json.loads(response.body) == {
        "error": "invalid_financial_request",
        "message": "Dados financeiros inválidos",
    }


def test_external_service_error_handler_returns_expected_response():
    error = ExternalServiceError(
        "Serviço financeiro indisponível"
    )

    response = asyncio.run(
        finassist_error_handler(
            request=None,
            exc=error,
        )
    )

    assert response.status_code == 503

    assert json.loads(response.body) == {
        "error": "external_service_unavailable",
        "message": "Serviço financeiro indisponível",
    }


def test_unexpected_error_handler_returns_safe_response():
    error = RuntimeError("internal secret")

    response = asyncio.run(
        unexpected_error_handler(
            request=None,
            exc=error,
        )
    )

    assert json.loads(response.body) == {
        "error": "internal_error",
        "message": (
            "Ocorreu um erro interno ao processar a solicitação."
        ),
    }