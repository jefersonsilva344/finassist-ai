import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.persistence.database import Base


@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    Base.metadata.create_all(engine)

    try:
        yield engine
    finally:
        Base.metadata.drop_all(engine)
        engine.dispose()


@pytest.fixture
def db_session_factory(db_engine):
    return sessionmaker(
        bind=db_engine,
        autoflush=False,
        autocommit=False,
    )


@pytest.fixture
def db_session(db_session_factory):
    session = db_session_factory()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(scope="session", autouse=True)
def setup_application_database():
    """
    Garante que o banco utilizado pela aplicação
    tenha suas tabelas criadas antes dos testes.
    """

    from src.persistence.config import DEFAULT_DATABASE_PATH
    from src.persistence.database import init_db

    DEFAULT_DATABASE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    init_db()

    yield


@pytest.fixture(scope="session", autouse=True)
def dispose_application_engine():
    yield

    from src.persistence.database import engine

    engine.dispose()