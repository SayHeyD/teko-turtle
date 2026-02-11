import random

import pytest

from cutting_board_drawers_optimizer.optimizer import CuttingBoard, Drawer

# It's ok that we import a private class here since we are testing
from cutting_board_drawers_optimizer.state._state_data import StateData


@pytest.fixture
def get_drawers() -> list[Drawer]:
    drawers = []

    for i in range(10):
        length = random.randint(80, 200)
        width = random.randint(40, 160)
        max_load = random.randint(1000, 40_000)

        drawers.append(Drawer(f"Drawer {i}", length, width, max_load))

    return drawers


@pytest.fixture
def get_cutting_boards() -> list[CuttingBoard]:
    cutting_boards = []

    for i in range(20):
        length = random.randint(80, 200)
        width = random.randint(40, 160)
        weight = random.randint(500, 3_500)
        price = random.randint(100, 80_000)

        cutting_boards.append(CuttingBoard(f"Board {i}", length, width, weight, price))

    return cutting_boards


def test_state_data_returns_correct_drawers(get_drawers, get_cutting_boards):
    state_data = StateData(get_drawers, get_cutting_boards)

    assert state_data.get_drawers() == get_drawers


def test_state_data_returns_correct_cutting_boards(get_drawers, get_cutting_boards):
    state_data = StateData(get_drawers, get_cutting_boards)

    assert state_data.get_cutting_boards() == get_cutting_boards
