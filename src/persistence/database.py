from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.pool import StaticPool

from src.persistence.config import get_database_url


DATABASE_URL = get_database_url()


class Base(DeclarativeBase):
    """
    Classe base para os modelos SQLAlchemy.
    """

    pass


connect_args = {}
engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

    if DATABASE_URL == "sqlite:///:memory:":
        engine_kwargs["poolclass"] = StaticPool


engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    **engine_kwargs,
)


SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def register_models() -> None:
    """
    Importa os modelos ORM para garantir que suas
    tabelas sejam registradas no metadata da Base.
    """

    from src.persistence import models  # noqa: F401


def init_db() -> None:
    """
    Cria as tabelas registradas nos modelos.
    """

    register_models()

    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Cria uma sessão de banco e garante seu fechamento.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()