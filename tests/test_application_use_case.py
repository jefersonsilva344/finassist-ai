from unittest.mock import MagicMock

from src.application.dto import (
    FinancialMessageInput,
    FinancialMessageOutput,
)
from src.application.use_cases.process_financial_message import (
    ProcessFinancialMessage,
)


def test_process_financial_message_delegates_to_service():

    flow = MagicMock()

    use_case = ProcessFinancialMessage(
        flow=flow,
    )

    use_case.service = MagicMock()

    use_case.service.process_message.return_value = (
        FinancialMessageOutput(
            response="Resposta financeira."
        )
    )

    data = FinancialMessageInput(
        external_user_id="user-001",
        message="Quanto sobra?",
    )

    result = use_case.execute(data)

    assert result.response == (
        "Resposta financeira."
    )

    use_case.service.process_message.assert_called_once_with(
        data
    )