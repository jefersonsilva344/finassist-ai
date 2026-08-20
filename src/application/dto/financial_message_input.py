from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialMessageInput:
    """
    Dados necessários para processar uma mensagem financeira.
    """

    external_user_id: str
    message: str