import pytest

from cutting_board_drawers_optimizer.optimizer import Drawer


@pytest.fixture
def get_drawer() -> Drawer:
    return Drawer(120, 80, 15_670)

def test_that_drawer_constructor_raises_value_error_if_length_is_less_than_1():
    with pytest.raises(ValueError, match=r'.*length.*'):
        Drawer(0, 80, 15_670)

def test_that_drawer_constructor_raises_value_error_if_width_is_less_than_1():
    with pytest.raises(ValueError, match=r'.*width.*'):
        Drawer(120, 0, 15_670)

def test_that_drawer_constructor_raises_value_error_if_max_load_is_less_than_1():
    with pytest.raises(ValueError, match=r'.*max_load.*'):
        Drawer(120, 80, 0)

def test_that_get_length_in_centimeters_returns_correct_float(get_drawer):
    assert get_drawer.get_length_in_centimeters() == 120

def test_that_get_width_in_centimeters_returns_correct_float(get_drawer):
    assert get_drawer.get_width_in_centimeters() == 80

def test_that_get_max_load_in_grams_returns_correct_float(get_drawer):
    assert get_drawer.get_max_load_in_grams() == 15_670