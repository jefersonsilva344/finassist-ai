from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_DATABASE_PATH = BASE_DIR / "data" / "finassist.db"


def get_database_url() -> str:
    """
    Retorna a URL de conexão com o banco de dados.

    A variável de ambiente DATABASE_URL pode sobrescrever
    o banco padrão utilizado pela aplicação.
    """

    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return database_url

    return f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"