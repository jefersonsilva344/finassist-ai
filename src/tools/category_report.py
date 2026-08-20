from src.agent.session import SessionState
from src.tools.category_analyzer import (
    get_category_summary,
)


def build_category_report(
    session: SessionState,
) -> str:
    """
    Gera um relatório determinístico das despesas
    categorizadas.
    """

    if not session.expense_categories:
        return (
            "Não existem despesas categorizadas "
            "registradas na sessão."
        )

    summary = get_category_summary(
        session
    )

    lines = [
        "ANÁLISE DE DESPESAS POR CATEGORIA:"
    ]

    for item in summary:

        category = item["category"]
        amount = item["amount"]
        percentage = item["percentage"]

        lines.append(
            f"{category}: "
            f"R$ {amount:.2f} "
            f"({percentage:.2f}% da renda)"
        )

    total = session.get_total_categorized_expenses()

    lines.append(
        f"Total categorizado: R$ {total:.2f}"
    )

    if session.income is not None:

        balance = (
            session.income - total
        )

        lines.append(
            f"Saldo considerando despesas "
            f"categorizadas: R$ {balance:.2f}"
        )

    return "\n".join(lines)