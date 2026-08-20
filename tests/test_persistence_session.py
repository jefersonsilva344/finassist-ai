from unittest.mock import MagicMock

from src.persistence.session import (
    commit_session,
    get_db_session,
)


def test_session_factory_is_configured(
        db_session_factory,
):
    """
    A fábrica de sessões deve estar configurada.
    """

    session = db_session_factory()

    try:
        assert session is not None
    finally:
        session.close()


def test_get_db_session_provides_session(
        db_session_factory,
):
    """
    get_db_session deve fornecer uma sessão SQLAlchemy.
    """

    generator = get_db_session(
        db_session_factory,
    )
    session = next(generator)

    try:
        assert session is not None
    finally:
        generator.close()


def test_get_db_session_closes_session(
        db_session_factory,
):
    """
    A sessão deve ser encerrada ao finalizar o ciclo.
    """

    generator = get_db_session(
        db_session_factory,
    )
    session = next(generator)

    session.close = MagicMock()

    generator.close()

    session.close.assert_called_once()


def test_commit_session_commits_transaction():
    """
    Uma operação bem-sucedida deve executar commit.
    """

    session = MagicMock()

    commit_session(session)

    session.commit.assert_called_once()
    session.rollback.assert_not_called()


def test_commit_session_rolls_back_on_error():
    """
    Uma falha no commit deve executar rollback
    e propagar a exceção.
    """

    session = MagicMock()

    session.commit.side_effect = RuntimeError("database error")

    try:
        commit_session(session)
    except RuntimeError as exc:
        assert str(exc) == "database error"
    else:
        raise AssertionError(
            "A exceção deveria ter sido propagada."
        )

    session.rollback.assert_called_once()