from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialMessageOutput:
    """
    Resultado produzido pela camada de aplicação
    após o processamento de uma mensagem financeira.
    """

    response: str