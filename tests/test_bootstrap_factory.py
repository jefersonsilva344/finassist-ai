from unittest.mock import Mock

from src.bootstrap.container import ApplicationContainer
from src.bootstrap.factory import build_application


def test_build_application_returns_application_container():
    db = Mock()

    container = build_application(db)

    assert isinstance(container, ApplicationContainer)