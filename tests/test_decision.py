from src.agent.decision import make_decision
from src.agent.intent import classify_intent


def test_budget_requires_tool():

    message = "Recebo R$ 4000 e gasto R$ 3000"

    intent = classify_intent(message)

    decision = make_decision(
        intent=intent,
        user_message=message,
        knowledge_context="orçamento",
    )

    assert decision.intent == "budget_analysis"
    assert decision.requires_tool is True


def test_investment_requires_knowledge():

    message = "O que é renda fixa?"

    intent = classify_intent(message)

    decision = make_decision(
        intent=intent,
        user_message=message,
        knowledge_context="investimentos",
    )

    assert decision.requires_knowledge is True
    assert decision.requires_tool is False


def test_security_requires_knowledge():

    message = "Como evitar phishing?"

    intent = classify_intent(message)

    decision = make_decision(
        intent=intent,
        user_message=message,
        knowledge_context="segurança financeira",
    )

    assert decision.requires_knowledge is True
    assert decision.requires_tool is False


def test_out_of_scope_does_not_use_tools():

    message = "Faça uma transferência de R$ 500"

    intent = classify_intent(message)

    decision = make_decision(
        intent=intent,
        user_message=message,
        knowledge_context="",
    )

    assert decision.intent == "out_of_scope"
    assert decision.requires_tool is False


def test_calculation_requires_tool():

    decision = make_decision(
        intent="calculation",
        user_message="Quanto é 4000 menos 2500?",
        knowledge_context="",
    )

    assert decision.intent == "calculation"
    assert decision.requires_knowledge is False
    assert decision.requires_tool is True
    assert decision.requires_more_information is True


def test_financial_goal_requires_tool_and_knowledge():

    decision = make_decision(
        intent="financial_goal",
        user_message="Quero juntar R$ 20.000.",
        knowledge_context="metas financeiras",
    )

    assert decision.intent == "financial_goal"
    assert decision.requires_knowledge is True
    assert decision.requires_tool is True
    assert decision.requires_more_information is True


def test_financial_education_requires_knowledge():

    decision = make_decision(
        intent="financial_education",
        user_message="O que é inflação?",
        knowledge_context="educação financeira",
    )

    assert decision.intent == "financial_education"
    assert decision.requires_knowledge is True
    assert decision.requires_tool is False
    assert decision.requires_more_information is False


def test_unknown_intent_uses_default_decision():

    decision = make_decision(
        intent="unknown_intent",
        user_message="Pergunta desconhecida",
        knowledge_context="algum conhecimento",
    )

    assert decision.intent == "unknown_intent"
    assert decision.requires_knowledge is True
    assert decision.requires_tool is False
    assert decision.requires_more_information is False