CATEGORY_ALIASES = {
    "aluguel": "moradia",
    "casa": "moradia",
    "moradia": "moradia",

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


def normalize_category(category: str) -> str:
    """
    Normaliza o nome de uma categoria financeira.

    Exemplos:
        aluguel -> moradia
        casa -> moradia
        alimentacao -> alimentação
        uber -> transporte
    """

    normalized = category.strip().lower()

    return CATEGORY_ALIASES.get(
        normalized,
        normalized,
    )