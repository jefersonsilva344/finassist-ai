from src.agent.sufficiency import check_budget_sufficiency


def test_budget_is_sufficient():

    result = check_budget_sufficiency(
        {
            "income": 4000,
            "expenses": 3000,
        }
    )

    assert result.sufficient is True
    assert result.missing_information == []


def test_budget_missing_expenses():

    result = check_budget_sufficiency(
        {
            "income": 4000,
            "expenses": None,
        }
    )

    assert result.sufficient is False
    assert "despesas mensais" in result.missing_information


def test_budget_missing_income():

    result = check_budget_sufficiency(
        {
            "income": None,
            "expenses": 3000,
        }
    )

    assert result.sufficient is False
    assert "renda mensal" in result.missing_information


def test_budget_without_data():

    result = check_budget_sufficiency(None)

    assert result.sufficient is False
    assert "renda mensal" in result.missing_information
    assert "despesas mensais" in result.missing_information