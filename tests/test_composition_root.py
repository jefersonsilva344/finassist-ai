from src.agent.agent import FinAssistAgent
from src.application.financial_flow import FinancialFlow
from src.bootstrap.container import (
    ApplicationContainer,
    build_container,
)


def test_build_container_creates_application_graph(
    db_session,
):
    container = build_container(
        db_session
    )

    assert isinstance(
        container,
        ApplicationContainer,
    )

    assert isinstance(
        container.financial_flow,
        FinancialFlow,
    )

    assert isinstance(
        container.financial_flow.agent,
        FinAssistAgent,
    )


def test_financial_flow_receives_persistence_dependencies(
    db_session,
):
    container = build_container(
        db_session
    )

    flow = container.financial_flow

    assert flow.context_service is not None
    assert flow.financial_persistence is not None


def test_agent_receives_openai_client(
    db_session,
):
    container = build_container(
        db_session
    )

    agent = container.financial_flow.agent

    assert agent.client is not None


def test_financial_flow_uses_injected_dependencies(
    db_session,
):
    context_service = object()
    financial_persistence = object()
    agent = object()

    flow = FinancialFlow(
        agent=agent,
        context_service=context_service,
        financial_persistence=financial_persistence,
    )

    assert flow.agent is agent
    assert flow.context_service is context_service
    assert (
        flow.financial_persistence
        is financial_persistence
    )