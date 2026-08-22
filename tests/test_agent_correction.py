from src.agent.agent import FinAssistAgent
from src.llm.client import LLMClient


class FakeLLMClient:
    def generate(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        return "fake response"


def test_agent_uses_corrected_expenses_in_follow_up():

    agent = FinAssistAgent(
        client=FakeLLMClient()
    )

    agent.answer(
        "Minha renda é R$ 5000 e gasto R$ 4000"
    )

    assert agent.session.income == 5000.0
    assert agent.session.expenses == 4000.0

    agent.answer(
        "Na verdade minhas despesas são R$ 2000"
    )

    assert agent.session.income == 5000.0
    assert agent.session.expenses == 2000.0

    response = agent.answer(
        "Quanto é meu saldo?"
    )

    assert agent.session.income == 5000.0
    assert agent.session.expenses == 2000.0

    assert "R$ 3.000,00" in response