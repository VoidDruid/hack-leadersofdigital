# Example tests, for basic stuff from this project

from services.api import extra


def test_responses():
    assert len(extra) == 1
    assert 400 in extra  # default error response


def test_extra_responses():
    extra = extra.extra(['permissions', 'not_found'])
    assert len(extra) == 3
    assert 400 in extra
    assert 403 in extra
    assert 404 in extra
