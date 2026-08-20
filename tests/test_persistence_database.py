from pathlib import Path

from sqlalchemy import inspect

from src.persistence.database import Base, engine


def test_database_engine_is_configured():
    """
    O engine do banco deve estar configurado.
    """

    assert engine is not None
    assert engine.url is not None


def test_database_uses_sqlite_by_default():
    """
    O ambiente padrão do projeto deve utilizar SQLite.
    """

    assert engine.url.get_backend_name() == "sqlite"


def test_persistence_base_contains_models():
    """
    Os modelos de persistência devem estar registrados
    na Base centralizada.
    """

    table_names = set(Base.metadata.tables.keys())

    expected_tables = {
        "users",
        "sessions",
        "financial_periods",
        "expenses",
        "conversation_messages",
    }

    assert expected_tables.issubset(table_names)


def test_database_schema_can_be_inspected():
    """
    O schema registrado no engine deve ser inspecionável.
    """

    inspector = inspect(engine)

    assert inspector is not None