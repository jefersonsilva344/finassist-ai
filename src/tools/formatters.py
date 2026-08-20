def format_brl(value: float) -> str:
    """
    Formata um valor numérico como moeda brasileira.

    Exemplos:
        2300.0 -> "R$ 2.300,00"
        1500.5 -> "R$ 1.500,50"
        5000.0 -> "R$ 5.000,00"
    """

    formatted = f"{value:,.2f}"

    formatted = (
        formatted
        .replace(",", "_")
        .replace(".", ",")
        .replace("_", ".")
    )

    return f"R$ {formatted}"