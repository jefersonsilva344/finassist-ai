from dataclasses import dataclass

from openai import OpenAI
from sqlalchemy.orm import Session

from src.agent.agent import FinAssistAgent
from src.application.financial_flow import FinancialFlow
from src.config.settings import OPENAI_API_KEY
from src.persistence.services.context_service import ContextService
from src.persistence.services.financial_service import (
    FinancialPersistenceService,
)


@dataclass
class ApplicationContainer:
    """
    Composition root do FinAssist AI.

    Responsável por construir e conectar
    as dependências da aplicação.
    """

    financial_flow: FinancialFlow


def build_container(
    db: Session,
    openai_client=None,
) -> ApplicationContainer:
    """
    Monta todas as dependências da aplicação.

    Dependências externas podem ser injetadas
    para facilitar testes.
    """

    # ------------------------------------------------------
    # Infrastructure / Persistence
    # ------------------------------------------------------

    context_service = ContextService(
        db
    )

    financial_persistence = (
        FinancialPersistenceService(
            db
        )
    )

    # ------------------------------------------------------
    # External client
    # ------------------------------------------------------

    if openai_client is None:
        openai_client = OpenAI(
            api_key=OPENAI_API_KEY,
        )

    # ------------------------------------------------------
    # Agent
    # ------------------------------------------------------

    agent = FinAssistAgent(
        client=openai_client,
    )

    # ------------------------------------------------------
    # Application
    # ------------------------------------------------------

    financial_flow = FinancialFlow(
        agent=agent,
        context_service=context_service,
        financial_persistence=financial_persistence,
    )

    return ApplicationContainer(
        financial_flow=financial_flow,
    )