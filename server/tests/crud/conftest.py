import pytest

from services.dependencies import get_pg


@pytest.fixture()
def session():
    yield from get_pg()
