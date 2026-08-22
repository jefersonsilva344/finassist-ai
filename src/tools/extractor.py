import re


def extract_budget_values(
    message: str,
) -> dict[str, float | None] | None:
    """
    Extrai renda e despesas genéricas de uma mensagem.

    Exemplos:

    "Recebo R$ 4000"
    -> {"income": 4000.0, "expenses": None}

    "Gasto R$ 3000"
    -> {"income": None, "expenses": 3000.0}

    "Recebo R$ 4000 e gasto R$ 3000"
    -> {"income": 4000.0, "expenses": 3000.0}
    """

    text = message.lower()

    income_patterns = [
        r"(?:recebo|receita|renda|salário|salario)"
        r"\s*(?:é|e|de|:)?\s*"
        r"r?\$?\s*([\d.,]+)",

        r"(?:ganho|ganha)\s*"
        r"r?\$?\s*([\d.,]+)",
    ]

    expense_patterns = [
        r"(?:gasto|gastos|despesa|despesas)"
        r"\s*(?:é|são|sao|de|:)?\s*"
        r"r?\$?\s*([\d.,]+)",
    ]

    income = _extract_first(
        text,
        income_patterns,
    )

    expenses = _extract_first(
        text,
        expense_patterns,
    )

    if income is None and expenses is None:
        return None

    return {
        "income": income,
        "expenses": expenses,
    }


def _extract_first(
    text: str,
    patterns: list[str],
) -> float | None:
    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return _parse_number(
                match.group(1)
            )

    return None


def _parse_number(value: str) -> float:
    """
    Converte formatos brasileiros e internacionais.

    Exemplos:

    4000
    4.000
    4.000,50
    4000,50
    """

    value = value.strip()

    if "," in value and "." in value:
        value = value.replace(".", "")
        value = value.replace(",", ".")

    elif "," in value:
        value = value.replace(",", ".")

    elif "." in value:
        parts = value.split(".")

        if (
            len(parts) == 2
            and len(parts[1]) == 3
        ):
            value = value.replace(".", "")

    return float(value)


def extract_categorized_expense(
    message: str,
) -> tuple[str, float] | None:
    """
    Extrai uma única despesa categorizada.

    Exemplos:

    "Gasto R$ 1500 de aluguel"
    -> ("aluguel", 1500.0)

    "Gastei R$ 600 com alimentação"
    -> ("alimentação", 600.0)

    Caso nenhuma despesa categorizada seja encontrada:
    -> None
    """

    expenses = extract_categorized_expenses(message)

    if not expenses:
        return None

    return expenses[0]


def extract_categorized_expenses(
    message: str,
) -> list[tuple[str, float]]:
    """
    Extrai múltiplas despesas categorizadas
    de uma única mensagem.

    Exemplos:

    "pago R$ 1500 de aluguel,
     R$ 800 com alimentação
     e R$ 400 com transporte"

    retorna:

    [
        ("aluguel", 1500.0),
        ("alimentação", 800.0),
        ("transporte", 400.0),
    ]
    """

    text = message.lower().strip()

    expenses: list[tuple[str, float]] = []

    # ======================================================
    # VALOR PRIMEIRO
    #
    # R$ 1500 de aluguel
    # R$ 800 com alimentação
    # R$ 400 em transporte
    # ======================================================

    pattern_amount_first = (
        r"r?\$?\s*([\d.,]+)"
        r"\s+"
        r"(?:de|com|em)"
        r"\s+"
        r"(aluguel|moradia|alimentação|alimentacao|"
        r"comida|transporte|ônibus|onibus|uber|"
        r"contas|luz|água|agua|internet|"
        r"dívida|divida|dívidas|dividas|lazer)"
        r"\b"
    )

    for match in re.finditer(
        pattern_amount_first,
        text,
    ):
        amount = _parse_number(
            match.group(1)
        )

        category = match.group(2).strip()

        expenses.append(
            (
                category,
                amount,
            )
        )

    # ======================================================
    # CATEGORIA PRIMEIRO
    #
    # aluguel R$ 1500
    # alimentação R$ 800
    # transporte R$ 400
    # ======================================================

    pattern_category_first = (
        r"\b"
        r"(aluguel|moradia|alimentação|alimentacao|"
        r"comida|transporte|ônibus|onibus|uber|"
        r"contas|luz|água|agua|internet|"
        r"dívida|divida|dívidas|dividas|lazer)"
        r"\s+"
        r"r?\$?\s*([\d.,]+)"
    )

    for match in re.finditer(
        pattern_category_first,
        text,
    ):
        category = match.group(1).strip()

        amount = _parse_number(
            match.group(2)
        )

        expenses.append(
            (
                category,
                amount,
            )
        )

    return expenses