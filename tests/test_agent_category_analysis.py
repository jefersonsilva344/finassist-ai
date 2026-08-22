from unittest.mock import MagicMock, patch

from src.agent.agent import FinAssistAgent


# ==========================================================
# TESTE: CONSULTA DE VALOR POR CATEGORIA
# ==========================================================

def test_agent_handles_category_value_query():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    agent.session.add_expense_category(
        "aluguel",
        1500,
    )

    result = agent._handle_category_query(
        "Quanto gasto com aluguel?"
    )

    assert result is not None
    assert "R$ 1.500,00" in result
    assert "moradia" in result


# ==========================================================
# TESTE: PERCENTUAL SEM RESULTADO
# ==========================================================

def test_agent_category_percentage_returns_none_when_percentage_is_missing():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    agent.session.add_expense_category(
        "aluguel",
        1500,
    )

    with patch(
        "src.agent.agent.detect_category_percentage_query",
        return_value="aluguel",
    ), patch.object(
        agent.session,
        "get_category_expense",
        return_value=1500,
    ), patch(
        "src.agent.agent.calculate_category_percentages",
        return_value={},
    ):

        result = agent._handle_category_percentage_query(
            "Quanto da minha renda gasto com aluguel?"
        )

    assert result is None


# ==========================================================
# TESTE: RESUMO DAS CATEGORIAS
# ==========================================================

def test_agent_handles_category_summary():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    agent.session.add_expense_category(
        "aluguel",
        1500,
    )

    agent.session.add_expense_category(
        "alimentação",
        600,
    )

    agent.session.add_expense_category(
        "transporte",
        300,
    )

    result = agent._handle_category_summary(
        "Como estão minhas despesas?"
    )

    assert result is not None

    assert "Moradia" in result
    assert "R$ 1.500,00" in result
    assert "37.50%" in result

    assert "Alimentação" in result
    assert "R$ 600,00" in result
    assert "15.00%" in result

    assert "Transporte" in result
    assert "R$ 300,00" in result
    assert "7.50%" in result


# ==========================================================
# TESTE: ORDEM DOS MAIORES GASTOS
# ==========================================================

def test_agent_category_summary_is_sorted():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    agent.session.add_expense_category(
        "transporte",
        300,
    )

    agent.session.add_expense_category(
        "aluguel",
        1500,
    )

    agent.session.add_expense_category(
        "alimentação",
        600,
    )

    result = agent._handle_category_summary(
        "Quais são meus maiores gastos?"
    )

    assert result is not None

    position_moradia = result.index(
        "Moradia"
    )

    position_alimentacao = result.index(
        "Alimentação"
    )

    position_transporte = result.index(
        "Transporte"
    )

    assert position_moradia < position_alimentacao
    assert position_alimentacao < position_transporte


# ==========================================================
# TESTE: CONSULTA DE CATEGORIA NÃO DETECTADA
# ==========================================================

def test_agent_returns_none_when_category_query_cannot_be_detected():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    result = agent._handle_category_query(
        "Quanto gasto com aluguel?"
    )

    assert result is None


# ==========================================================
# TESTE: CONSULTA DE PERCENTUAL NÃO DETECTADA
# ==========================================================

def test_agent_returns_none_when_category_percentage_query_cannot_be_detected():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    result = agent._handle_category_percentage_query(
        "Quanto da minha renda gasto com aluguel?"
    )

    assert result is None


# ==========================================================
# TESTE: RESUMO NÃO DETECTADO
# ==========================================================

def test_agent_returns_none_when_category_summary_cannot_be_detected():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    result = agent._handle_category_summary(
        "Como estão minhas despesas?"
    )

    assert result is None


# ==========================================================
# TESTE: CONSULTA SEM DESPESA REGISTRADA
# ==========================================================

def test_agent_handles_category_query_without_registered_expense():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    with patch(
        "src.agent.agent.detect_category_query",
        return_value="aluguel",
    ):

        result = agent._handle_category_query(
            "Quanto gasto com aluguel?"
        )

    assert result is not None
    assert "Não encontrei despesas registradas" in result
    assert "aluguel" in result


# ==========================================================
# TESTE: PERCENTUAL SEM DESPESA REGISTRADA
# ==========================================================

def test_agent_handles_category_percentage_without_registered_expense():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    with patch(
        "src.agent.agent.detect_category_percentage_query",
        return_value="aluguel",
    ):

        result = agent._handle_category_percentage_query(
            "Quanto da minha renda gasto com aluguel?"
        )

    assert result is not None
    assert "Não encontrei despesas registradas" in result
    assert "aluguel" in result


# ==========================================================
# TESTE: RESUMO DE CATEGORIAS VAZIO
# ==========================================================

def test_agent_handles_empty_category_summary():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    with patch(
        "src.agent.agent.detect_category_summary_query",
        return_value=True,
    ):

        result = agent._handle_category_summary(
            "Como estão minhas despesas?"
        )

    assert result == (
        "Ainda não existem despesas categorizadas registradas."
    )