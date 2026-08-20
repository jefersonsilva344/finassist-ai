from src.persistence.context import PersistenceContext
from src.persistence.services.context_service import (
    ContextService,
)


def test_context_creates_user_and_session(db_session):
    service = ContextService(db_session)

    context = service.create_context(
        "test-user-001"
    )

    assert isinstance(
        context,
        PersistenceContext,
    )

    assert context.user_id is not None
    assert context.session_id is not None

def test_context_reuses_existing_user(db_session):
    service = ContextService(db_session)

    first_context = service.create_context(
        "user-001"
    )

    db_session.commit()

    second_context = service.create_context(
        "user-001"
    )

    assert (
        second_context.user_id
        == first_context.user_id
    )

    assert (
        second_context.session_id
        != first_context.session_id
    )

def test_context_isolates_users(db_session):
    service = ContextService(db_session)

    user_1 = service.create_context(
        "user-001"
    )

    user_2 = service.create_context(
        "user-002"
    )

    assert user_1.user_id != user_2.user_id
    assert user_1.session_id != user_2.session_id


def test_get_or_create_context_creates_when_missing(db_session):
    service = ContextService(db_session)

    context = service.get_or_create_context(
        "user-context-001"
    )

    assert isinstance(
        context,
        PersistenceContext,
    )

    assert context.user_id is not None
    assert context.session_id is not None


def test_get_or_create_context_reuses_existing_session(db_session):
    service = ContextService(db_session)

    first_context = service.get_or_create_context(
        "user-context-002"
    )

    second_context = service.get_or_create_context(
        "user-context-002"
    )

    assert (
        second_context.user_id
        == first_context.user_id
    )

    assert (
        second_context.session_id
        == first_context.session_id
    )


def test_get_or_create_context_isolates_users(db_session):
    service = ContextService(db_session)

    user_1 = service.get_or_create_context(
        "user-context-A"
    )

    user_2 = service.get_or_create_context(
        "user-context-B"
    )

    assert user_1.user_id != user_2.user_id
    assert user_1.session_id != user_2.session_id