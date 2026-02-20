import pytest
from cutting_board_drawers_optimizer.optimizer import Optimizer, Drawer, CuttingBoard


def test_optimizer_initialization():
    drawers = [Drawer("Drawer 1", 60, 50, 10000, 5)]
    cutting_boards = [CuttingBoard("Board 1", 40, 30, 2000, 5039)]
    max_budget = 10000
    cutting_board_amount = 3

    optimizer = Optimizer(drawers, cutting_boards, max_budget, cutting_board_amount)

    assert optimizer.drawers == drawers
    assert optimizer.cutting_boards == cutting_boards
    assert optimizer.max_budget == max_budget
    assert optimizer.cutting_board_amount == cutting_board_amount


def test_optimizer_properties_read_only():
    drawers: list[Drawer] = []
    cutting_boards: list[CuttingBoard] = []
    max_budget = 5000
    cutting_board_amount = 2

    optimizer = Optimizer(drawers, cutting_boards, max_budget, cutting_board_amount)

    with pytest.raises(AttributeError):
        optimizer.drawers = []  # type: ignore[misc]
    
    with pytest.raises(AttributeError):
        optimizer.cutting_boards = []  # type: ignore[misc]

    with pytest.raises(AttributeError):
        optimizer.max_budget = 1000  # type: ignore[misc]

    with pytest.raises(AttributeError):
        optimizer.cutting_board_amount = 5  # type: ignore[misc]
