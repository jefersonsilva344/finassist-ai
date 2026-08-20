from src.agent.session import SessionState
from src.agent.memory import add_expense
from src.tools.category_report import (
    build_category_report,
)


def test_category_report():
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

    result = build_category_report(
        session
    )

    assert "moradia: R$ 1500.00" in result
    assert "alimentação: R$ 600.00" in result
    assert "transporte: R$ 300.00" in result

    assert "Total categorizado: R$ 2400.00" in result

    assert (
        "Saldo considerando despesas "
        "categorizadas: R$ 1600.00"
    ) in result


def test_category_report_without_categories():
    session = SessionState()

    result = build_category_report(
        session
    )

    assert (
        "Não existem despesas categorizadas"
        in result
    )