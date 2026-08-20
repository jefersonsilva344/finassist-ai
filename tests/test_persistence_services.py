from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.persistence.database import Base
from src.persistence.models import User
from src.persistence.services import (
    SessionService,
    UserService,
)



def test_user_service_creates_user(db_session):
    session = db_session
    """
    O serviço deve criar e persistir um usuário.
    """

    service = UserService(session)

    user = service.create_user(
        external_id="test-user-001"
    )

    assert user.id is not None
    assert user.external_id == "test-user-001"



def test_user_service_recovers_user(db_session):
    session = db_session
    """
    O serviço deve recuperar um usuário
    previamente persistido.
    """

    service = UserService(session)

    created_user = service.create_user(
        external_id="test-user-001"
    )

    recovered_user = service.get_user(
        created_user.id
    )

    assert recovered_user is not None
    assert recovered_user.id == created_user.id



def test_session_service_creates_session(db_session):
    session = db_session
    """
    O serviço deve criar uma sessão vinculada
    a um usuário existente.
    """

    user_service = UserService(session)
    session_service = SessionService(session)

    user = user_service.create_user(
        external_id="test-user-001"
    )

    user_session = session_service.start_session(
        user.id
    )

    assert user_session.id is not None
    assert user_session.user_id == user.id
    assert user_session.created_at is not None
    assert user_session.last_activity_at is not None



def test_session_service_recovers_session(db_session):
    session = db_session
    """
    O serviço deve recuperar uma sessão
    previamente persistida.
    """

    user_service = UserService(session)
    session_service = SessionService(session)

    user = user_service.create_user(
        external_id="test-user-001"
    )

    created_session = session_service.start_session(
        user.id
    )

    recovered_session = session_service.get_session(
        created_session.id
    )

    assert recovered_session is not None
    assert recovered_session.id == created_session.id
    assert recovered_session.user_id == user.id



def test_session_service_lists_user_sessions(db_session):
    session = db_session
    """
    O serviço deve retornar todas as sessões
    pertencentes ao usuário.
    """

    user_service = UserService(session)
    session_service = SessionService(session)

    user = user_service.create_user(
        external_id="test-user-001"
    )

    first = session_service.start_session(user.id)
    second = session_service.start_session(user.id)

    sessions = session_service.list_user_sessions(
        user.id
    )

    session_ids = {
        item.id
        for item in sessions
    }

    assert first.id in session_ids
    assert second.id in session_ids
    assert len(sessions) == 2
