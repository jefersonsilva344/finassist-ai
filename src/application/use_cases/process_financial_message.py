from src.application.dto import (
    FinancialMessageInput,
    FinancialMessageOutput,
)
from src.application.financial_flow import FinancialFlow
from src.application.services.financial_app_service import (
    FinancialAppService,
)


class ProcessFinancialMessage:
    """
    Caso de uso responsável por processar
    uma mensagem financeira.
    """

    def __init__(
        self,
        flow: FinancialFlow,
    ) -> None:

        self.service = FinancialAppService(
            flow=flow,
        )

    def execute(
        self,
        data: FinancialMessageInput,
    ) -> FinancialMessageOutput:

        return self.service.process_message(
            data
        )