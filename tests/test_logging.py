import logging

from src.observability.logging import configure_logging

def test_configure_logging_sets_default_level():
    configure_logging()

    logger = logging.getLogger()

    assert logger.level == logging.INFO

def test_application_logger_has_expected_name():
    from src.observability.logger import logger

    assert logger.name == "finassist.api"