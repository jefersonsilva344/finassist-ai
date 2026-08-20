from unittest.mock import MagicMock

from src.application.dto import FinancialMessageInput
from src.application.services.financial_app_service import (
    FinancialAppService,
)


def test_financial_app_service_processes_message():

    flow = MagicMock()

    flow.process_message.return_value = (
        "Seu saldo mensal é de R$ 1.000,00."
    )

    service = FinancialAppService(
        flow=flow,
    )

    data = FinancialMessageInput(
        external_user_id="user-001",
        message="Recebo R$ 4.000 e gasto R$ 3.000",
    )

    result = service.process_message(data)

    assert result.response == (
        "Seu saldo mensal é de R$ 1.000,00."
    )

    flow.process_message.assert_called_once_with(
        external_user_id="user-001",
        message="Recebo R$ 4.000 e gasto R$ 3.000",
    )