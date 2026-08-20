from src.agent.agent import FinAssistAgent
from src.agent.session import SessionState

from unittest.mock import patch


def create_agent() -> FinAssistAgent:
    agent = FinAssistAgent.__new__(
        FinAssistAgent
    )

    agent.session = SessionState()

    return agent


def test_agent_handles_balance_follow_up():
    agent = create_agent()

    agent.session.update_income(4000)
    agent.session.update_expenses(3000)

    result = agent._handle_follow_up(
        "Quanto sobra?"
    )

    assert result is not None
    assert "R$ 1.000,00" in result


def test_agent_handles_savings_follow_up():
    agent = create_agent()

    agent.session.update_income(4000)
    agent.session.update_expenses(3000)

    result = agent._handle_follow_up(
        "Qual minha taxa de economia?"
    )

    assert result is not None
    assert "25.00%" in result


def test_agent_handles_commitment_follow_up():
    agent = create_agent()

    agent.session.update_income(4000)
    agent.session.update_expenses(3000)

    result = agent._handle_follow_up(
        "Qual meu comprometimento?"
    )

    assert result is not None
    assert "75.00%" in result


def test_agent_follow_up_returns_none_with_incomplete_session():

    agent = create_agent()

    agent.session.update_income(4000)

    result = agent._handle_follow_up(
        "Quanto sobra?"
    )

    assert result is None


def test_agent_follow_up_returns_none_when_action_exists_but_session_is_incomplete():

    agent = create_agent()

    agent.session.update_income(4000)

    with patch(
        "src.agent.agent.detect_follow_up",
        return_value="balance",
    ):

        result = agent._handle_follow_up(
            "Quanto sobra?"
        )

    assert result is None


def test_agent_follow_up_returns_none_for_unknown_action():

    agent = create_agent()

    agent.session.update_income(4000)
    agent.session.update_expenses(3000)

    with patch(
        "src.agent.agent.detect_follow_up",
        return_value="unknown_action",
    ):

        result = agent._handle_follow_up(
            "Pergunta desconhecida"
        )

    assert result is None