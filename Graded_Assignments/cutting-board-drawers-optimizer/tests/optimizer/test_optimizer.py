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


def test_optimizer_optimize_basic():
    # Drawer: 60x50, max load 10kg, max 2 boards
    drawer = Drawer("Drawer 1", 60, 50, 10000, 2)
    # Board 1: 40x30, 2kg, 20 CHF (2000 cents), area 1200
    board1 = CuttingBoard("Board 1", 40, 30, 2000, 2000)
    # Board 2: 40x30, 2kg, 30 CHF (3000 cents), area 1200
    board2 = CuttingBoard("Board 2", 41, 31, 2000, 3000)
    # Board 3: 40x30, 2kg, 25 CHF (2500 cents), area 1200
    board3 = CuttingBoard("Board 3", 42, 32, 2000, 2500)

    # Max budget: 50 CHF (5000 cents)
    # Max boards: 3
    # Target: Should pick Board 3 twice (Total area 1344*2 = 2688, cost 5000)
    # Before it would pick Board 1 and Board 3 because it couldn't pick same board twice.

    optimizer = Optimizer([drawer], [board1, board2, board3], 5000, 3)
    result = optimizer.optimize()

    assigned_boards = result[drawer]
    assert len(assigned_boards) == 2
    assert assigned_boards.count(board3) == 2


def test_optimizer_optimize_constraints():
    # Drawer 1: 30x20, load 1000g, max 1 board
    drawer1 = Drawer("D1", 30, 20, 1000, 1)
    # Drawer 2: 50x40, load 5000g, max 5 boards
    drawer2 = Drawer("D2", 50, 40, 5000, 5)

    # Board 1: 45x35, 2000g, 10 CHF (only fits in D2)
    board1 = CuttingBoard("B1", 45, 35, 2000, 1000)
    # Board 2: 25x15, 500g, 5 CHF (fits in both, but only one drawer can take it)
    board2 = CuttingBoard("B2", 25, 15, 501, 500)
    # Board 3: 25x15, 1200g, 5 CHF (fits in both, but too heavy for D1)
    board3 = CuttingBoard("B3", 26, 16, 1200, 500)

    optimizer = Optimizer([drawer1, drawer2], [board1, board2, board3], 10000, 10)
    result = optimizer.optimize()

    # Optimal should be:
    # B1 in D2 (Area 1575)
    # B1 in D2 (Area 1575)
    # B2 in D1 (Area 375)
    # Total area: 3525
    # (Total Weight in D2: 4000 <= 5000)
    # (Total Boards in D2: 2 <= 5)
    # (Total Cost: 2500 <= 10000)

    assert result[drawer2].count(board1) == 2
    assert board2 in result[drawer1]


def test_optimizer_optimize_tie_breaking():
    # Drawer: Large enough for all
    drawer = Drawer("D", 100, 100, 10000, 10)

    # All boards have same area (1000)
    # Board 1: Cost 1000, Weight 1000
    board1 = CuttingBoard("B1", 50, 20, 1000, 1000)
    # Board 2: Cost 1000, Weight 500
    board2 = CuttingBoard("B2", 50, 20, 500, 1000)
    # Board 3: Cost 500, Weight 1000
    board3 = CuttingBoard("B3", 50, 20, 1000, 500)

    # Case 1: Max 1 board. Should pick Board 3 (lowest cost)
    opt1 = Optimizer([drawer], [board1, board2, board3], 10000, 1)
    res1 = opt1.optimize()
    assert res1[drawer] == [board3]

    # Case 2: Max 1 board, but Board 3 not available. Should pick Board 2 (same cost as B1, lower weight)
    opt2 = Optimizer([drawer], [board1, board2], 10000, 1)
    res2 = opt2.optimize()
    assert res2[drawer] == [board2]


def test_optimizer_optimize_multiple_selection():
    # Drawer: Large enough for 2 boards
    drawer = Drawer("D", 100, 100, 10000, 2)

    # Board 1: Area 1000, Cost 10
    board1 = CuttingBoard("B1", 50, 20, 100, 1000)
    # Board 2: Area 500, Cost 5
    board2 = CuttingBoard("B2", 25, 20, 100, 500)

    # Target 2 boards, budget 2000.
    # Should pick Board 1 twice (Total Area 2000, Cost 2000)
    # if it only picked it once, it would pick Board 1 and Board 2 (Total Area 1500)
    opt = Optimizer([drawer], [board1, board2], 2000, 2)
    res = opt.optimize()

    assigned = res[drawer]
    assert len(assigned) == 2
    assert assigned.count(board1) == 2
