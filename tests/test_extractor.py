from src.tools.extractor import extract_budget_values

from src.tools.extractor import (
    extract_categorized_expense,
)


def test_extract_budget_values():
    result = extract_budget_values(
        "Recebo 4000 e gasto 3200"
    )

    assert result == {
        "income": 4000.0,
        "expenses": 3200.0,
    }


def test_extract_budget_values_brazilian_format():
    result = extract_budget_values(
        "Recebo R$ 4.000 e tenho despesas de R$ 3.200"
    )

    assert result == {
        "income": 4000.0,
        "expenses": 3200.0,
    }


def test_extract_budget_values_with_decimal():
    result = extract_budget_values(
        "Minha renda é 4000,50 e minhas despesas são 3200,25"
    )

    assert result == {
        "income": 4000.50,
        "expenses": 3200.25,
    }


def test_extract_budget_values_returns_none_when_no_financial_data():
    result = extract_budget_values(
        "Olá, tudo bem?"
    )

    assert result is None


def test_extract_budget_values_with_income_only():
    result = extract_budget_values(
        "Recebo R$ 4000"
    )

    assert result == {
        "income": 4000.0,
        "expenses": None,
    }


def test_extract_budget_values_with_expenses_only():
    result = extract_budget_values(
        "Gasto R$ 3000"
    )

    assert result == {
        "income": None,
        "expenses": 3000.0,
    }



def test_extract_rent_expense():
    result = extract_categorized_expense(
        "Gasto R$ 1500 de aluguel"
    )

    assert result == (
        "aluguel",
        1500,
    )


def test_extract_food_expense():
    result = extract_categorized_expense(
        "Gastei R$ 600 com alimentação"
    )

    assert result == (
        "alimentação",
        600,
    )


def test_extract_transport_expense():
    result = extract_categorized_expense(
        "Gasto R$ 400 com transporte"
    )

    assert result == (
        "transporte",
        400,
    )


def test_extract_multiple_categorized_expenses():
    from src.tools.extractor import (
        extract_categorized_expenses,
    )

    message = (
        "Minha renda é R$ 5.000, "
        "pago R$ 1.500 de aluguel, "
        "R$ 800 com alimentação "
        "e R$ 400 com transporte."
    )

    result = extract_categorized_expenses(
        message
    )

    assert result == [
        ("aluguel", 1500.0),
        ("alimentação", 800.0),
        ("transporte", 400.0),
    ]
    

def test_extract_multiple_categorized_expenses_category_first():
    from src.tools.extractor import (
        extract_categorized_expenses,
    )

    message = (
        "aluguel R$ 1500, "
        "alimentação R$ 800, "
        "transporte R$ 400"
    )

    result = extract_categorized_expenses(
        message
    )

    assert result == [
        ("aluguel", 1500.0),
        ("alimentação", 800.0),
        ("transporte", 400.0),
    ]