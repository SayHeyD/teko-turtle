import pytest

from drawer import Drawer


@pytest.fixture
def get_drawer():
    return Drawer(2000, 1500, 5300)


def test_that_drawer_returns_correct_length(get_drawer):
    assert get_drawer.get_length() == 2000


def test_that_drawer_returns_correct_width(get_drawer):
    assert get_drawer.get_width() == 1500


def test_that_drawer_returns_correct_max_load(get_drawer):
    assert get_drawer.get_max_load() == 5300
