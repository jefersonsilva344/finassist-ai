from sqlalchemy.orm import Session

from src.bootstrap.container import (
    ApplicationContainer,
    build_container,
)
from src.llm.client import LLMClient


def build_application(
    db: Session,
    llm_client: LLMClient | None = None,
) -> ApplicationContainer:
    """
    Factory principal da aplicação.

    Mantém a criação do grafo de dependências
    fora da camada HTTP.
    """

    return build_container(
        db=db,
        llm_client=llm_client,
    )