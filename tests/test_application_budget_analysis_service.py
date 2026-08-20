from src.application.services.budget_analysis_service import (
    BudgetAnalysisService,
)


def test_budget_analysis_returns_balance():
    service = BudgetAnalysisService()

    result = service.analyze(
        income=4000,
        expenses=3000,
    )

    assert result["balance"] == 1000
    assert result["savings_rate"] == 25
    assert result["commitment"] == 75


def test_budget_analysis_rejects_zero_income():
    service = BudgetAnalysisService()

    try:
        service.analyze(
            income=0,
            expenses=3000,
        )
    except ValueError as exc:
        assert str(exc) == "A receita deve ser maior que zero."
    else:
        raise AssertionError(
            "Deveria rejeitar receita igual a zero."
        )


def test_budget_analysis_rejects_negative_income():
    service = BudgetAnalysisService()

    try:
        service.analyze(
            income=-1000,
            expenses=500,
        )
    except ValueError as exc:
        assert str(exc) == "A receita deve ser maior que zero."
    else:
        raise AssertionError(
            "Deveria rejeitar receita negativa."
        )