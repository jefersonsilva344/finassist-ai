class FinAssistError(Exception):
    """Exceção base da aplicação."""

    status_code = 500
    error_code = "internal_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class InvalidFinancialRequestError(FinAssistError):
    """Erro relacionado a uma solicitação financeira inválida."""

    status_code = 400
    error_code = "invalid_financial_request"


class ExternalServiceError(FinAssistError):
    """Erro relacionado a uma dependência externa."""

    status_code = 503
    error_code = "external_service_unavailable"