from src.agent.session import SessionState
from src.agent.memory import add_expense
from src.tools.category_analyzer import (
    calculate_category_percentages,
    get_category_summary,
)


def test_calculate_category_percentages():
    session = SessionState()

    session.update_income(4000)

    add_expense(
        session,
        "aluguel",
        1500,
    )

    add_expense(
        session,
        "alimentação",
        600,
    )

    add_expense(
        session,
        "transporte",
        300,
    )

    result = calculate_category_percentages(
        session
    )

    assert result["moradia"] == 37.5
    assert result["alimentação"] == 15.0
    assert result["transporte"] == 7.5


def test_category_summary_is_sorted_by_amount():
    session = SessionState()

    session.update_income(4000)

    add_expense(
        session,
        "transporte",
        300,
    )

    add_expense(
        session,
        "aluguel",
        1500,
    )

    add_expense(
        session,
        "alimentação",
        600,
    )

    result = get_category_summary(
        session
    )

    assert result[0]["category"] == "moradia"
    assert result[1]["category"] == "alimentação"
    assert result[2]["category"] == "transporte"