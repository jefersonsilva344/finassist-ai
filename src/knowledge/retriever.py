from .loader import load_knowledge


KEYWORDS_BY_DOCUMENT = {
    "fundamentos_financeiros.md": {
        "receita",
        "despesa",
        "orçamento",
        "orcamento",
        "juros",
        "inflação",
        "inflacao",
        "liquidez",
        "rentabilidade",
        "risco",
    },

    "orcamento_pessoal.md": {
        "orçamento",
        "orcamento",
        "receita",
        "despesa",
        "gasto",
        "saldo",
        "comprometimento",
    },

    "reserva_emergencia.md": {
        "reserva",
        "emergência",
        "emergencia",
        "despesas essenciais",
    },

    "investimentos.md": {
        "investimento",
        "investimentos",
        "renda fixa",
        "renda variável",
        "renda variavel",
        "fundos",
        "títulos",
        "titulos",
        "liquidez",
        "risco",
        "diversificação",
        "diversificacao",
        "rentabilidade",
        "retorno",
        "volatilidade",
    },

    "criptomoedas.md": {
        "cripto",
        "criptomoeda",
        "criptomoedas",
        "bitcoin",
        "custódia",
        "custodia",
        "chave privada",
        "seed phrase",
    },

    "seguranca_financeira.md": {
        "golpe",
        "phishing",
        "senha",
        "cvv",
        "token",
        "segurança",
        "seguranca",
        "fraude",
        "credencial",
        "credenciais",
    },
}


def retrieve_knowledge(
    query: str,
    max_documents: int = 2,
) -> str:
    """
    Recupera documentos relevantes com base em palavras-chave.
    """

    documents = load_knowledge()

    query_lower = query.lower().strip()

    scores: list[tuple[int, str]] = []

    for document_name, keywords in KEYWORDS_BY_DOCUMENT.items():
        score = sum(
            1
            for keyword in keywords
            if keyword.lower() in query_lower
        )

        if score > 0 and document_name in documents:
            scores.append((score, document_name))

    scores.sort(
        key=lambda item: (-item[0], item[1])
    )

    selected_documents = [
        document_name
        for _, document_name in scores[:max_documents]
    ]

    if not selected_documents:
        return ""

    context_parts = []

    for document_name in selected_documents:
        context_parts.append(
            f"# Documento: {document_name}\n\n"
            f"{documents[document_name]}"
        )

    return "\n\n---\n\n".join(context_parts)