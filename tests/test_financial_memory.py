from src.agent.session import SessionState
from src.agent.category import normalize_category


def test_session_starts_without_categories():
    session = SessionState()

    assert session.expense_categories == {}


def test_add_expense_category():
    session = SessionState()

    session.add_expense_category(
        "aluguel",
        1500,
    )

    assert session.expense_categories[
        "moradia"
    ] == 1500


def test_same_category_is_accumulated():
    session = SessionState()

    session.add_expense_category(
        "aluguel",
        1500,
    )

    session.add_expense_category(
        "aluguel",
        500,
    )

    assert session.expense_categories[
        "moradia"
    ] == 2000


def test_expenses_are_updated():
    session = SessionState()

    session.add_expense_category(
        "alimentação",
        600,
    )

    session.add_expense_category(
        "transporte",
        400,
    )

    assert session.get_total_categorized_expenses() == 1000


def test_category_alias():
    assert normalize_category(
        "aluguel"
    ) == "moradia"

    assert normalize_category(
        "uber"
    ) == "transporte"

    assert normalize_category(
        "comida"
    ) == "alimentação"


def test_expenses_sync_with_categories():
    """
    O total de despesas deve ser igual à soma
    das despesas categorizadas.
    """

    session = SessionState()

    session.add_expense_category(
        "aluguel",
        1500,
    )

    session.add_expense_category(
        "alimentação",
        600,
    )

    session.add_expense_category(
        "transporte",
        300,
    )

    assert session.expenses == 2400


def test_expense_categories_are_source_of_truth():
    """
    Uma atualização genérica de despesas não deve
    sobrescrever o total quando existem categorias.
    """

    session = SessionState()

    session.add_expense_category(
        "aluguel",
        1500,
    )

    session.add_expense_category(
        "alimentação",
        600,
    )

    session.update_expenses(9999)

    assert session.expenses == 2100


def test_has_categorized_expenses():
    """
    Verifica se a sessão identifica corretamente
    a existência de despesas categorizadas.
    """

    session = SessionState()

    assert (
        session.has_categorized_expenses()
        is False
    )

    session.add_expense_category(
        "transporte",
        300,
    )

    assert (
        session.has_categorized_expenses()
        is True
    )