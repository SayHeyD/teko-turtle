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


def test_optimizer_fit_check():
    # Drawer: 60x50
    drawer1 = Drawer("Drawer 1", 60, 50, 10000, 5)
    # Drawer: 40x40
    drawer2 = Drawer("Drawer 2", 40, 40, 10000, 5)
    
    # Fits in both orientations in Drawer 1, doesn't fit in Drawer 2
    board1 = CuttingBoard("Board 1", 45, 30, 1000, 2000)
    # Fits in Drawer 1 only when rotated (55x45 vs 60x50), doesn't fit in Drawer 2
    board2 = CuttingBoard("Board 2", 55, 45, 1000, 2000)
    # Fits in both drawers (30x20)
    board3 = CuttingBoard("Board 3", 30, 20, 1000, 2000)
    # Fits in Drawer 2 only when rotated (40x35 vs 40x40), also fits in Drawer 1
    board4 = CuttingBoard("Board 4", 40, 35, 1000, 2000)
    # Fits in none (70x60)
    board5 = CuttingBoard("Board 5", 70, 60, 1000, 2000)

    drawers = [drawer1, drawer2]
    cutting_boards = [board1, board2, board3, board4, board5]
    
    optimizer = Optimizer(drawers, cutting_boards, 10000, 5)
    fits = optimizer.fit_check()

    assert drawer1 in fits[board1]
    assert drawer2 not in fits[board1]

    assert drawer1 in fits[board2]
    assert drawer2 not in fits[board2]

    assert drawer1 in fits[board3]
    assert drawer2 in fits[board3]

    assert drawer1 in fits[board4]
    assert drawer2 in fits[board4]

    assert len(fits[board5]) == 0
