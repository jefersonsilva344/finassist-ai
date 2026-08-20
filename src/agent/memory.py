from .session import SessionState
from .category import normalize_category


def add_expense(
    session: SessionState,
    category: str,
    amount: float,
) -> None:
    """
    Adiciona uma despesa categorizada à sessão.

    A soma das categorias é a fonte de verdade
    para o total de despesas.
    """

    normalized_category = normalize_category(
        category
    )

    current_amount = session.expense_categories.get(
        normalized_category,
        0.0,
    )

    session.expense_categories[
        normalized_category
    ] = current_amount + amount

    session.expenses = sum(
        session.expense_categories.values()
    )