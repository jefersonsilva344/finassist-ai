from src.application.dto import (
    FinancialMessageInput,
    FinancialMessageOutput,
)
from src.application.financial_flow import FinancialFlow


class FinancialAppService:
    """
    Serviço de aplicação responsável por processar
    uma mensagem financeira.

    As dependências são injetadas pelo Composition Root.
    """

    def __init__(
        self,
        flow: FinancialFlow,
    ) -> None:
        self.flow = flow

    def process_message(
        self,
        data: FinancialMessageInput,
    ) -> FinancialMessageOutput:

        response = self.flow.process_message(
            external_user_id=data.external_user_id,
            message=data.message,
        )

        return FinancialMessageOutput(
            response=response,
        )