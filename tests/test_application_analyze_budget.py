from unittest.mock import MagicMock

from src.application.dto import BudgetAnalysisOutput
from src.application.use_cases.analyze_budget import AnalyzeBudget


def test_analyze_budget_returns_output():
    service = MagicMock()

    service.analyze.return_value = {
        "balance": 1000,
        "savings_rate": 25,
        "commitment": 75,
    }

    use_case = AnalyzeBudget(
        service=service,
    )

    result = use_case.execute(
        income=4000,
        expenses=3000,
    )

    assert isinstance(
        result,
        BudgetAnalysisOutput,
    )

    assert result.balance == 1000
    assert result.savings_rate == 25
    assert result.commitment == 75

    service.analyze.assert_called_once_with(
        income=4000,
        expenses=3000,
    )