from src.agent.intent import classify_intent


def test_phishing_is_security():
    result = classify_intent(
        "Recebi um link de phishing."
    )

    assert result == "financial_security"


def test_password_request_is_security():
    result = classify_intent(
        "Como proteger minha senha bancária?"
    )

    assert result == "financial_security"


def test_cvv_request_is_security():
    result = classify_intent(
        "Onde devo informar meu CVV?"
    )

    assert result == "financial_security"