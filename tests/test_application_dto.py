from src.application.dto import (
    FinancialMessageInput,
    FinancialMessageOutput,
)


def test_financial_message_input_stores_data():
    data = FinancialMessageInput(
        external_user_id="user-001",
        message="Recebo R$ 4.000",
    )

    assert data.external_user_id == "user-001"
    assert data.message == "Recebo R$ 4.000"


def test_financial_message_output_stores_response():
    output = FinancialMessageOutput(
        response="Seu saldo mensal é de R$ 1.000,00."
    )

    assert output.response == (
        "Seu saldo mensal é de R$ 1.000,00."
    )


def test_financial_message_input_is_immutable():
    data = FinancialMessageInput(
        external_user_id="user-001",
        message="Teste",
    )

    try:
        data.message = "Alterado"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "FinancialMessageInput deveria ser imutável."
        )


def test_financial_message_output_is_immutable():
    output = FinancialMessageOutput(
        response="Resposta"
    )

    try:
        output.response = "Alterado"
    except AttributeError:
        pass
    else:
        raise AssertionError(
            "FinancialMessageOutput deveria ser imutável."
        )