import pytest

from cutting_board_drawers_optimizer.optimizer import CuttingBoard


@pytest.fixture
def get_cutting_board():
    return CuttingBoard(65, 24, 2560, 2590)

def test_that_cutting_board_constructor_raises_value_error_if_length_is_less_than_1(get_cutting_board):
    with pytest.raises(ValueError, match=r'.*length.*'):
        CuttingBoard(0, 24, 2560, 2590)

def test_that_cutting_board_constructor_raises_value_error_if_width_is_less_than_1(get_cutting_board):
    with pytest.raises(ValueError, match=r'.*width.*'):
        CuttingBoard(65, 0, 2560, 2590)

def test_that_cutting_board_constructor_raises_value_error_if_weight_is_less_than_1(get_cutting_board):
    with pytest.raises(ValueError, match=r'.*weight.*'):
        CuttingBoard(65, 24, 0, 2590)

def test_that_cutting_board_constructor_raises_value_error_if_price_is_less_than_1(get_cutting_board):
    with pytest.raises(ValueError, match=r'.*price.*'):
        CuttingBoard(65, 24, 2560, 0)

def test_that_get_price_in_chf_returns_correct_float(get_cutting_board):
    assert get_cutting_board.get_price_in_chf() == '25.90'

def test_that_get_price_in_chf_returns_correct_float_length(get_cutting_board):
    price = str(get_cutting_board.get_price_in_chf())
    decimal_chars = len(price.split('.')[1])
    assert decimal_chars == 2