from src.agent.agent import FinAssistAgent
from src.agent.intent import classify_intent


def test_budget_complete_has_correct_intent():

    message = "Recebo R$ 4000 e gasto R$ 3000"

    assert classify_intent(message) == "budget_analysis"


def test_budget_incomplete_has_correct_intent():

    message = "Recebo R$ 4000"

    assert classify_intent(message) == "budget_analysis"