import pytest

from cutting_board import CuttingBoard

@pytest.fixture
def get_cutting_board():
    return CuttingBoard(100, 200, 2000, 3500)

def test_that_cutting_board_returns_correct_length(get_cutting_board):
    assert get_cutting_board.get_length() == 100

def test_that_cutting_board_returns_correct_width(get_cutting_board):
    assert get_cutting_board.get_width() == 200

def test_that_cutting_board_returns_correct_price(get_cutting_board):
    assert get_cutting_board.get_price() == 2000

def test_that_cutting_board_returns_correct_weight(get_cutting_board):
    assert get_cutting_board.get_weight() == 3500

