def calculate_balance(
    income: float,
    expenses: float,
) -> float:
    return income - expenses


def calculate_savings_rate(
    income: float,
    expenses: float,
) -> float:
    if income <= 0:
        raise ValueError(
            "A receita deve ser maior que zero."
        )

    return ((income - expenses) / income) * 100


def calculate_income_commitment(
    income: float,
    expenses: float,
) -> float:
    if income <= 0:
        raise ValueError(
            "A receita deve ser maior que zero."
        )

    return (expenses / income) * 100


def calculate_compound_growth(
    principal: float,
    annual_rate: float,
    years: int,
) -> float:
    """
    Calcula o valor futuro utilizando crescimento composto.

    annual_rate deve ser informado como decimal.
    Exemplo:
        10% = 0.10
    """

    if principal < 0:
        raise ValueError(
            "O valor inicial não pode ser negativo."
        )

    if years < 0:
        raise ValueError(
            "O período não pode ser negativo."
        )

    return principal * (
        1 + annual_rate
    ) ** years


def calculate_compound_profit(
    principal: float,
    annual_rate: float,
    years: int,
) -> float:
    final_value = calculate_compound_growth(
        principal,
        annual_rate,
        years,
    )

    return final_value - principal