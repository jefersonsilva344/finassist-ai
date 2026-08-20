OUT_OF_SCOPE_PATTERNS = {
    # Acesso a dados reais
    "consulte meus investimentos",
    "consultar meus investimentos",
    "consulte meu saldo",
    "consultar meu saldo",
    "saldo da minha conta",
    "acesse minha conta",
    "acessar minha conta",
    "consulte minha conta",
    "consultar minha conta",

    # Execução de operações
    "faça uma transferência",
    "fazer uma transferência",
    "realize uma transferência",
    "realizar uma transferência",

    "faça um investimento",
    "realize um investimento",

    # Execução de compra/venda
    "compre uma ação para mim",
    "compre ações para mim",
    "venda uma ação para mim",
    "venda ações para mim",

    "compre bitcoin para mim",
    "venda bitcoin para mim",
}


INTENT_KEYWORDS = {
    "financial_security": {
        "golpe",
        "phishing",
        "senha",
        "cvv",
        "token",
        "fraude",
        "segurança",
        "seguranca",
        "código de autenticação",
        "codigo de autenticacao",
        "credencial",
        "credenciais",
        "chave privada",
        "seed phrase",
    },

    "investment_education": {
        "investimento",
        "investimentos",
        "investir",
        "renda fixa",
        "renda variável",
        "renda variavel",
        "fundo de investimento",
        "fundos",
        "ação",
        "acoes",
        "ações",
        "criptomoeda",
        "criptomoedas",
        "bitcoin",
        "diversificação",
        "diversificacao",
        "liquidez",
        "rentabilidade",
        "volatilidade",
    },

    "financial_goal": {
        "meta financeira",
        "objetivo financeiro",
        "juntar dinheiro",
        "economizar dinheiro",
        "guardar dinheiro",
        "quero juntar",
        "quero economizar",
        "quero guardar",
    },

    "budget_analysis": {
        "recebo",
        "salário",
        "salario",
        "renda mensal",
        "gasto",
        "gastos",
        "despesa",
        "despesas",
        "orçamento",
        "orcamento",
        "dívida",
        "divida",
        "cartão de crédito",
        "cartao de credito",
    },

    "calculation": {
        "calcule",
        "calcular",
        "cálculo",
        "calculo",
        "porcentagem",
        "percentual",
        "quanto é",
        "quanto e",
        "quanto vou ganhar",
        "quanto vou receber",
        "quanto terei",
        "qual será o valor",
        "qual sera o valor",
    },

    "financial_education": {
        "o que é",
        "o que e",
        "o que significa",
        "explique",
        "conceito",
        "inflação",
        "inflacao",
        "juros",
        "educação financeira",
        "educacao financeira",
        "reserva de emergência",
        "reserva de emergencia",
        "planejamento financeiro",
    },
}


INTENT_PRIORITY = [
    "financial_security",
    "calculation",
    "investment_education",
    "financial_goal",
    "budget_analysis",
    "financial_education",
]


def classify_intent(message: str) -> str:
    text = message.lower().strip()

    # ---------------------------------------------------------
    # 1. FORA DO ESCOPO
    # Somente operações/acessos que o sistema realmente não possui.
    # ---------------------------------------------------------

    for pattern in OUT_OF_SCOPE_PATTERNS:
        if pattern in text:
            return "out_of_scope"

    # ---------------------------------------------------------
    # 2. CALCULA SCORES
    # ---------------------------------------------------------

    scores: dict[str, int] = {}

    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(
            1
            for keyword in keywords
            if keyword.lower() in text
        )

        if score:
            scores[intent] = score

    # ---------------------------------------------------------
    # 3. NENHUMA INTENÇÃO
    # ---------------------------------------------------------

    if not scores:
        return "out_of_scope"

    # ---------------------------------------------------------
    # 4. MAIOR SCORE
    # ---------------------------------------------------------

    max_score = max(scores.values())

    candidates = {
        intent
        for intent, score in scores.items()
        if score == max_score
    }

    # ---------------------------------------------------------
    # 5. DESEMPATE POR PRIORIDADE
    # ---------------------------------------------------------

    for intent in INTENT_PRIORITY:
        if intent in candidates:
            return intent

    return "out_of_scope"