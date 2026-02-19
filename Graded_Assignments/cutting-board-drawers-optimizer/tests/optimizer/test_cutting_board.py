import pytest

from cutting_board_drawers_optimizer.optimizer import CuttingBoard


@pytest.fixture
def get_cutting_board() -> CuttingBoard:
    return CuttingBoard("Test Board", 65, 24, 2560, 2590)


def test_that_cutting_board_constructor_raises_value_error_if_length_is_less_than_1():
    with pytest.raises(ValueError, match=r".*length.*"):
        CuttingBoard("Test Board", 0, 24, 2560, 2590)


def test_that_cutting_board_constructor_raises_value_error_if_width_is_less_than_1():
    with pytest.raises(ValueError, match=r".*width.*"):
        CuttingBoard("Test Board", 65, 0, 2560, 2590)


def test_that_cutting_board_constructor_raises_value_error_if_weight_is_less_than_1():
    with pytest.raises(ValueError, match=r".*weight.*"):
        CuttingBoard("Test Board", 65, 24, 0, 2590)


def test_that_cutting_board_constructor_raises_value_error_if_price_is_less_than_1():
    with pytest.raises(ValueError, match=r".*price.*"):
        CuttingBoard("Test Board", 65, 24, 2560, 0)


def test_that_get_price_in_chf_returns_correct_float(get_cutting_board):
    assert get_cutting_board.get_price_in_chf() == "25.90"


def test_that_get_price_in_chf_returns_correct_float_length(get_cutting_board):
    price = str(get_cutting_board.get_price_in_chf())
    decimal_chars = len(price.split(".")[1])
    assert decimal_chars == 2


def test_that_get_price_in_centime_returns_correct_value(get_cutting_board):
    price = get_cutting_board.get_price_in_centime()
    assert price == 2590


def test_that_get_length_in_centimeters_returns_correct_float(get_cutting_board):
    assert get_cutting_board.get_length_in_centimeters() == 65


def test_that_get_width_in_centimeters_returns_correct_float(get_cutting_board):
    assert get_cutting_board.get_width_in_centimeters() == 24


def test_that_get_weight_in_grams_returns_correct_float(get_cutting_board):
    assert get_cutting_board.get_weight_in_grams() == 2560


def test_that_area_returns_correct_value(get_cutting_board):
    assert get_cutting_board.area == 65 * 24
