from sqlalchemy.orm import Session

from src.bootstrap.container import (
    ApplicationContainer,
    build_container,
)


def build_application(
    db: Session,
) -> ApplicationContainer:
    """
    Factory principal da aplicação.

    Mantém a criação do grafo de dependências
    fora da camada HTTP.
    """

    return build_container(
        db=db,
    )