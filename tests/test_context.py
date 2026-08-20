from src.agent.context import detect_follow_up
from src.agent.session import SessionState
from src.agent.memory import add_expense

from src.agent.context import (
    detect_follow_up,
    detect_category_query,
    detect_category_percentage_query,
    detect_category_summary_query,
)


def create_complete_session() -> SessionState:
    session = SessionState()

    session.update_income(4000)
    session.update_expenses(3000)

    return session


def test_detect_balance_follow_up():
    session = create_complete_session()

    result = detect_follow_up(
        "Quanto sobra?",
        session,
    )

    assert result == "balance"


def test_detect_savings_rate_follow_up():
    session = create_complete_session()

    result = detect_follow_up(
        "Qual minha taxa de economia?",
        session,
    )

    assert result == "savings_rate"


def test_detect_commitment_follow_up():
    session = create_complete_session()

    result = detect_follow_up(
        "Qual meu comprometimento?",
        session,
    )

    assert result == "commitment"


def test_follow_up_requires_complete_session():
    session = SessionState()

    session.update_income(4000)

    result = detect_follow_up(
        "Quanto sobra?",
        session,
    )

    assert result is None


def test_unknown_follow_up_returns_none():
    session = create_complete_session()

    result = detect_follow_up(
        "Qual é a capital do Brasil?",
        session,
    )

    assert result is None


def test_detect_category_query():
    session = SessionState()

    session.add_expense_category(
        "moradia",
        1500,
    )

    result = detect_category_query(
        "Quanto gasto com aluguel?",
        session,
    )

    assert result == "moradia"


def test_detect_food_category_query():
    session = SessionState()

    session.add_expense_category(
        "alimentação",
        600,
    )

    result = detect_category_query(
        "Quanto gasto com alimentação?",
        session,
    )

    assert result == "alimentação"


def test_category_query_without_categories_returns_none():
    session = SessionState()

    result = detect_category_query(
        "Quanto gasto com aluguel?",
        session,
    )

    assert result is None

    # ==========================================================
# TESTES DE CONSULTA DE PERCENTUAL POR CATEGORIA
# ==========================================================

def test_detect_category_percentage_query():
    session = SessionState()

    session.update_income(4000)

    add_expense(
        session,
        "alimentação",
        600,
    )

    result = detect_category_percentage_query(
        "Quanto da minha renda gasto com alimentação?",
        session,
    )

    assert result == "alimentação"


def test_detect_rent_percentage_query():
    session = SessionState()

    session.update_income(4000)

    add_expense(
        session,
        "aluguel",
        1500,
    )

    result = detect_category_percentage_query(
        "Quanto o aluguel representa da minha renda?",
        session,
    )

    assert result == "moradia"


def test_category_percentage_query_without_income_returns_none():
    session = SessionState()

    add_expense(
        session,
        "alimentação",
        600,
    )

    result = detect_category_percentage_query(
        "Quanto da minha renda gasto com alimentação?",
        session,
    )

    assert result is None


# ==========================================================
# TESTES DE RESUMO DAS CATEGORIAS
# ==========================================================

def test_detect_category_summary_query():
    session = SessionState()

    add_expense(
        session,
        "alimentação",
        600,
    )

    result = detect_category_summary_query(
        "Como estão minhas despesas?",
        session,
    )

    assert result is True


def test_detect_expenses_by_category_query():
    session = SessionState()

    add_expense(
        session,
        "alimentação",
        600,
    )

    result = detect_category_summary_query(
        "Mostre minhas despesas por categoria",
        session,
    )

    assert result is True


def test_category_summary_without_categories_returns_false():
    session = SessionState()

    result = detect_category_summary_query(
        "Como estão minhas despesas?",
        session,
    )

    assert result is False