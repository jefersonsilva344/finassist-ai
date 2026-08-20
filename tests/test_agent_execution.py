from types import SimpleNamespace
from unittest.mock import MagicMock

from src.agent.agent import FinAssistAgent

import pytest

from src.agent import agent as agent_module


def create_agent() -> FinAssistAgent:
    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)
    agent.session.update_expenses(3000)

    return agent


def test_check_information_for_budget_analysis():

    agent = create_agent()

    result = agent._check_information(
        intent="budget_analysis",
        user_message="Analise meu orçamento",
    )

    assert result is not None
    assert result.sufficient is True


def test_execute_tools_returns_empty_when_tool_is_not_required():

    agent = create_agent()

    decision = SimpleNamespace(
        intent="budget_analysis",
        requires_tool=False,
    )

    result = agent._execute_tools(
        decision=decision,
        user_message="Analise meu orçamento",
    )

    assert result == ""


def test_execute_tools_returns_empty_for_non_budget_intent():

    agent = create_agent()

    decision = SimpleNamespace(
        intent="investment",
        requires_tool=True,
    )

    result = agent._execute_tools(
        decision=decision,
        user_message="Quero investir",
    )

    assert result == ""


def test_execute_tools_returns_empty_when_budget_is_insufficient():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent.session.update_income(4000)

    decision = SimpleNamespace(
        intent="budget_analysis",
        requires_tool=True,
    )

    result = agent._execute_tools(
        decision=decision,
        user_message="Analise meu orçamento",
    )

    assert result == ""


def test_execute_tools_calculates_complete_budget():

    agent = create_agent()

    decision = SimpleNamespace(
        intent="budget_analysis",
        requires_tool=True,
    )

    result = agent._execute_tools(
        decision=decision,
        user_message="Analise meu orçamento",
    )

    assert "CÁLCULO FINANCEIRO DETERMINÍSTICO:" in result
    assert "Receita: R$ 4000.00" in result
    assert "Despesas: R$ 3000.00" in result
    assert "Saldo: R$ 1000.00" in result
    assert "Taxa de economia: 25.00%" in result
    assert "Comprometimento da renda: 75.00%" in result


def test_answer_returns_category_percentage_before_llm():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent._update_session = MagicMock()
    agent._handle_follow_up = MagicMock(
        return_value=None
    )
    agent._handle_category_percentage_query = MagicMock(
        return_value="percentual"
    )
    agent._handle_category_query = MagicMock(
        return_value=None
    )
    agent._handle_category_summary = MagicMock(
        return_value=None
    )

    result = agent.answer(
        "consulta"
    )

    assert result == "percentual"
    agent.client.responses.create.assert_not_called()


def test_answer_returns_category_before_llm():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent._update_session = MagicMock()
    agent._handle_follow_up = MagicMock(
        return_value=None
    )
    agent._handle_category_percentage_query = MagicMock(
        return_value=None
    )
    agent._handle_category_query = MagicMock(
        return_value="categoria"
    )
    agent._handle_category_summary = MagicMock(
        return_value=None
    )

    result = agent.answer(
        "consulta"
    )

    assert result == "categoria"
    agent.client.responses.create.assert_not_called()


def test_answer_returns_category_summary_before_llm():

    agent = FinAssistAgent(
        client=MagicMock()
    )

    agent._update_session = MagicMock()
    agent._handle_follow_up = MagicMock(
        return_value=None
    )
    agent._handle_category_percentage_query = MagicMock(
        return_value=None
    )
    agent._handle_category_query = MagicMock(
        return_value=None
    )
    agent._handle_category_summary = MagicMock(
        return_value="resumo"
    )

    result = agent.answer(
        "consulta"
    )

    assert result == "resumo"
    agent.client.responses.create.assert_not_called()


def test_answer_includes_deterministic_results_in_llm_context(
    monkeypatch,
):

    agent = FinAssistAgent(
        client=MagicMock()
    )

    response = MagicMock()
    response.output_text = "Resposta final"

    agent.client.responses.create.return_value = response

    agent._update_session = MagicMock()
    agent._handle_follow_up = MagicMock(
        return_value=None
    )
    agent._handle_category_percentage_query = MagicMock(
        return_value=None
    )
    agent._handle_category_query = MagicMock(
        return_value=None
    )
    agent._handle_category_summary = MagicMock(
        return_value=None
    )

    monkeypatch.setattr(
        agent_module,
        "classify_intent",
        lambda message: "budget_analysis",
    )

    monkeypatch.setattr(
        agent_module,
        "retrieve_knowledge",
        lambda message: "contexto financeiro",
    )

    monkeypatch.setattr(
        agent_module,
        "make_decision",
        lambda **kwargs: SimpleNamespace(
            intent="budget_analysis",
            reason="Analisar orçamento",
            requires_knowledge=False,
            requires_tool=True,
        ),
    )

    sufficiency = SimpleNamespace(
        sufficient=True,
        missing_information=[],
        reason="Todos os dados estão disponíveis.",
    )

    agent._check_information = MagicMock(
        return_value=sufficiency
    )

    agent._execute_tools = MagicMock(
        return_value=(
            "CÁLCULO FINANCEIRO DETERMINÍSTICO:\n"
            "Saldo: R$ 1000.00"
        )
    )

    result = agent.answer(
        "Analise meu orçamento"
    )

    assert result == "Resposta final"

    call = agent.client.responses.create.call_args

    assert call is not None

    input_text = call.kwargs["input"]

    assert "CÁLCULO FINANCEIRO DETERMINÍSTICO:" in input_text
    assert "Saldo: R$ 1000.00" in input_text
    assert "INFORMAÇÕES SUFICIENTES." in input_text


def test_answer_includes_missing_information_in_llm_context(
    monkeypatch,
):

    agent = FinAssistAgent(
        client=MagicMock()
    )

    response = MagicMock()
    response.output_text = "Preciso de mais informações."

    agent.client.responses.create.return_value = response

    agent._update_session = MagicMock()
    agent._handle_follow_up = MagicMock(
        return_value=None
    )
    agent._handle_category_percentage_query = MagicMock(
        return_value=None
    )
    agent._handle_category_query = MagicMock(
        return_value=None
    )
    agent._handle_category_summary = MagicMock(
        return_value=None
    )

    monkeypatch.setattr(
        agent_module,
        "classify_intent",
        lambda message: "budget_analysis",
    )

    monkeypatch.setattr(
        agent_module,
        "retrieve_knowledge",
        lambda message: "",
    )

    monkeypatch.setattr(
        agent_module,
        "make_decision",
        lambda **kwargs: SimpleNamespace(
            intent="budget_analysis",
            reason="Orçamento incompleto",
            requires_knowledge=False,
            requires_tool=True,
        ),
    )

    sufficiency = SimpleNamespace(
        sufficient=False,
        missing_information=["expenses"],
        reason="As despesas não foram informadas.",
    )

    agent._check_information = MagicMock(
        return_value=sufficiency
    )

    agent._execute_tools = MagicMock(
        return_value=""
    )

    result = agent.answer(
        "Recebo R$ 4000"
    )

    assert result == "Preciso de mais informações."

    call = agent.client.responses.create.call_args

    input_text = call.kwargs["input"]

    assert "INFORMAÇÕES INSUFICIENTES." in input_text
    assert "Dados ausentes: expenses" in input_text
    assert "As despesas não foram informadas." in input_text