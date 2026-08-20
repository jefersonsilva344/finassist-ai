from collections.abc import Generator
from typing import Callable

from fastapi import Depends
from sqlalchemy.orm import Session

from src.persistence.database import SessionLocal


SessionFactory = Callable[[], Session]


def get_session_factory() -> SessionFactory:
    return SessionLocal


def get_db_session(
    session_factory: SessionFactory = Depends(
        get_session_factory,
    ),
) -> Generator[Session, None, None]:
    """
    Fornece uma sessão do banco de dados.

    A sessão é criada no início do ciclo,
    permanece disponível durante a operação
    e é sempre encerrada ao final.

    A SessionFactory permanece injetável para testes,
    sem ser exposta como parâmetro HTTP no OpenAPI.
    """

    session = session_factory()

    try:
        yield session
    finally:
        session.close()


def commit_session(session: Session) -> None:
    """
    Confirma a transação atual.

    Em caso de erro, desfaz a transação
    e propaga a exceção.
    """

    try:
        session.commit()

    except Exception:
        session.rollback()
        raise