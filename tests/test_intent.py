from src.agent.intent import classify_intent


def test_financial_education_intent():
    result = classify_intent(
        "O que é uma reserva de emergência?"
    )

    assert result == "financial_education"


def test_budget_analysis_intent():
    result = classify_intent(
        "Recebo 4000 e tenho 3200 de despesas."
    )

    assert result == "budget_analysis"


def test_investment_intent():
    result = classify_intent(
        "O que é renda fixa?"
    )

    assert result == "investment_education"


def test_security_intent():
    result = classify_intent(
        "Recebi uma mensagem de phishing."
    )

    assert result == "financial_security"


def test_inflation_is_financial_education():
    result = classify_intent(
        "Me explique inflação."
    )

    assert result == "financial_education"


def test_fixed_income_is_investment():
    result = classify_intent(
        "O que é renda fixa?"
    )

    assert result == "investment_education"


def test_monthly_income_is_budget():
    result = classify_intent(
        "Minha renda mensal é R$ 5.000."
    )

    assert result == "budget_analysis"


def test_financial_goal():
    result = classify_intent(
        "Quero juntar dinheiro para comprar uma casa."
    )

    assert result == "financial_goal"


def test_security_has_priority():
    result = classify_intent(
        "Recebi um golpe e pediram minha senha."
    )

    assert result == "financial_security"