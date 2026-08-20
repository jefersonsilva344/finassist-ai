from .session import SessionState


# ==========================================================
# CONSULTAS DE ORÇAMENTO
# ==========================================================

FOLLOW_UP_KEYWORDS = {
    "saldo": "balance",
    "sobra": "balance",
    "quanto sobra": "balance",

    "taxa de economia": "savings_rate",
    "economizo": "savings_rate",
    "economia": "savings_rate",

    "comprometimento": "commitment",
    "comprometimento da renda": "commitment",
}


def detect_follow_up(
    message: str,
    session: SessionState,
) -> str | None:
    """
    Identifica perguntas de continuação relacionadas
    ao orçamento geral.

    Exemplos:

    "Quanto sobra?"
    -> "balance"

    "Qual minha taxa de economia?"
    -> "savings_rate"

    "Qual meu comprometimento?"
    -> "commitment"
    """

    if session.income is None or session.expenses is None:
        return None

    text = message.lower().strip()

    for keyword, action in FOLLOW_UP_KEYWORDS.items():
        if keyword in text:
            return action

    return None


# ==========================================================
# CATEGORIAS FINANCEIRAS
# ==========================================================

CATEGORY_QUERY_KEYWORDS = {
    "aluguel": "moradia",
    "moradia": "moradia",
    "casa": "moradia",

    "alimentação": "alimentação",
    "alimentacao": "alimentação",
    "comida": "alimentação",

    "transporte": "transporte",
    "ônibus": "transporte",
    "onibus": "transporte",
    "uber": "transporte",

    "contas": "contas",
    "luz": "contas",
    "água": "contas",
    "agua": "contas",
    "internet": "contas",

    "dívida": "dívidas",
    "divida": "dívidas",
    "dívidas": "dívidas",

    "lazer": "lazer",
}


# ==========================================================
# CONSULTA DE VALOR POR CATEGORIA
# ==========================================================

def detect_category_query(
    message: str,
    session: SessionState,
) -> str | None:
    """
    Identifica consultas sobre o valor gasto
    em uma categoria financeira.

    Exemplos:

    "Quanto gasto com aluguel?"
    -> "moradia"

    "Quanto gasto com alimentação?"
    -> "alimentação"

    "Quanto gastei com transporte?"
    -> "transporte"
    """

    if not session.expense_categories:
        return None

    text = message.lower().strip()

    query_indicators = (
        "quanto gasto",
        "quanto eu gasto",
        "quanto gastei",
        "quanto tenho gasto",
        "qual o valor gasto",
        "qual valor gasto",
        "quanto custa",
    )

    if not any(
        indicator in text
        for indicator in query_indicators
    ):
        return None

    for keyword, category in CATEGORY_QUERY_KEYWORDS.items():

        if keyword in text:
            return category

    return None


# ==========================================================
# CONSULTA DE PERCENTUAL POR CATEGORIA
# ==========================================================

def detect_category_percentage_query(
    message: str,
    session: SessionState,
) -> str | None:
    """
    Identifica consultas sobre quanto uma categoria
    representa da renda mensal.

    Exemplos:

    "Quanto da minha renda gasto com alimentação?"
    -> "alimentação"

    "Quanto o aluguel representa da minha renda?"
    -> "moradia"

    "Qual percentual gasto com transporte?"
    -> "transporte"
    """

    if not session.expense_categories:
        return None

    if session.income is None:
        return None

    text = message.lower().strip()

    percentage_indicators = (
        "quanto da minha renda",
        "quanto da renda",
        "representa da minha renda",
        "representa da renda",
        "qual percentual",
        "qual porcentagem",
        "qual percentual gasto",
        "qual porcentagem gasto",
        "percentual gasto",
        "porcentagem gasto",
    )

    if not any(
        indicator in text
        for indicator in percentage_indicators
    ):
        return None

    for keyword, category in CATEGORY_QUERY_KEYWORDS.items():

        if keyword in text:
            return category

    return None


# ==========================================================
# RESUMO DE CATEGORIAS
# ==========================================================

def detect_category_summary_query(
    message: str,
    session: SessionState,
) -> bool:
    """
    Identifica solicitações de resumo das despesas
    categorizadas.

    Exemplos:

    "Como estão minhas despesas?"
    -> True

    "Mostre minhas despesas por categoria"
    -> True

    "Quais são meus maiores gastos?"
    -> True
    """

    if not session.expense_categories:
        return False

    text = message.lower().strip()

    summary_indicators = (
        "como estão minhas despesas",
        "como estao minhas despesas",
        "minhas despesas por categoria",
        "despesas por categoria",
        "gastos por categoria",
        "resumo das despesas",
        "resumo dos gastos",
        "resumo financeiro",
        "maiores gastos",
        "maiores despesas",
        "onde estou gastando",
        "onde gasto mais",
        "como estou gastando",
    )

    return any(
        indicator in text
        for indicator in summary_indicators
    )