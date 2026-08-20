from src.agent.session import SessionState


def calculate_category_percentages(
    session: SessionState,
) -> dict[str, float]:
    """
    Calcula o percentual de cada categoria
    em relação à renda mensal.
    """

    if session.income is None:
        return {}

    if session.income <= 0:
        raise ValueError(
            "A renda deve ser maior que zero."
        )

    return {
        category: (amount / session.income) * 100
        for category, amount
        in session.expense_categories.items()
    }


def get_category_summary(
    session: SessionState,
) -> list[dict[str, float | str]]:
    """
    Retorna um resumo das despesas categorizadas,
    ordenado do maior para o menor valor.
    """

    percentages = calculate_category_percentages(
        session
    )

    summary = []

    for category, amount in (
        session.expense_categories.items()
    ):
        summary.append(
            {
                "category": category,
                "amount": amount,
                "percentage": percentages[category],
            }
        )

    return sorted(
        summary,
        key=lambda item: item["amount"],
        reverse=True,
    )