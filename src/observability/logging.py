import logging
import os


LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
).upper()


def configure_logging() -> None:
    """
    Configura o sistema de logging da aplicação.

    A configuração é centralizada para que todos os módulos
    utilizem o mesmo padrão de logs.
    """

    level = getattr(
        logging,
        LOG_LEVEL,
        logging.INFO,
    )

    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        force=True,
    )