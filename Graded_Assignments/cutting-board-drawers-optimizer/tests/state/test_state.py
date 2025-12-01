import os
import pickle
import random
import tempfile
import uuid

import pytest

from cutting_board_drawers_optimizer.optimizer import CuttingBoard, Drawer
from cutting_board_drawers_optimizer.state import State
from cutting_board_drawers_optimizer.state._state_data import StateData


@pytest.fixture
def get_drawers() -> list[Drawer]:
    drawers = []

    for _ in range(10):
        length = random.randint(80, 200)
        width = random.randint(40, 160)
        max_load = random.randint(1000, 40_000)

        drawers.append(Drawer(length, width, max_load))

    return drawers


@pytest.fixture
def get_cutting_boards() -> list[CuttingBoard]:
    cutting_boards = []

    for _ in range(20):
        length = random.randint(80, 200)
        width = random.randint(40, 160)
        weight = random.randint(500, 3_500)
        price = random.randint(100, 80_000)

        cutting_boards.append(CuttingBoard(length, width, weight, price))

    return cutting_boards

# Tests with an empty state
def test_state_with_empty_lists_returns_correct_state_data():
    state = State()
    state_data: StateData = state._get_data()

    assert state_data.get_drawers() == []
    assert state_data.get_cutting_boards() == []

def test_state_with_empty_lists_returns_correct_drawers():
    state = State()
    assert state.get_drawers() == []

def test_state_with_empty_lists_returns_correct_cutting_boards():
    state = State()
    assert state.get_cutting_boards() == []

# Tests with a filled state
def test_state_returns_correct_state_data(get_drawers, get_cutting_boards):
    state = State(get_drawers, get_cutting_boards)
    state_data: StateData = state._get_data()

    assert state_data.get_drawers() == get_drawers
    assert state_data.get_cutting_boards() == get_cutting_boards

def test_state_returns_correct_drawers(get_drawers, get_cutting_boards):
    state = State(get_drawers, get_cutting_boards)
    assert state.get_drawers() == get_drawers

def test_state_returns_correct_cutting_boards(get_drawers, get_cutting_boards):
    state = State(get_drawers, get_cutting_boards)
    assert state.get_cutting_boards() == get_cutting_boards

# Tests hitting the filesystem
def test_state_can_be_written_to_disk_if_file_path_does_not_exist(get_drawers, get_cutting_boards):
    file_to_save_to = tempfile.mktemp()
    State(get_drawers, get_cutting_boards).save(file_to_save_to)

    assert os.path.exists(file_to_save_to)
    os.remove(file_to_save_to)

def test_state_can_be_written_to_disk_if_file_path_contains_directories_that_do_not_exist(get_drawers, get_cutting_boards):
    base_directory_to_save_to = os.path.join( os.path.dirname(tempfile.mktemp()), str(uuid.uuid4()) )
    file_to_save_to = os.path.join(base_directory_to_save_to, str(uuid.uuid4()) )

    State(get_drawers, get_cutting_boards).save(file_to_save_to)

    assert os.path.exists(file_to_save_to)
    os.remove(file_to_save_to)

def test_state_raises_exception_on_save_if_file_path_already_exists():
    file_to_save_to = tempfile.mktemp()
    open(file_to_save_to, "w").close()

    message = f"File '{file_to_save_to}' already exists"

    with pytest.raises(FileExistsError, match=message):
        State().save(file_to_save_to)

    assert os.path.exists(file_to_save_to)
    os.remove(file_to_save_to)

def test_state_raises_exception_on_save_if_directories_cannot_be_created(monkeypatch):
    base_directory_to_save_to = os.path.join( os.path.dirname(tempfile.mktemp()), str(uuid.uuid4()) )
    file_to_save_to = os.path.join(base_directory_to_save_to, str(uuid.uuid4()) )

    # Keep real os.path.exists available
    real_exists = os.path.exists

    def fake_exists(p: str | os.PathLike[str]) -> bool:
        # Return False only for the parent dir we care about; defer to real for others
        return False if str(p) == str(base_directory_to_save_to) else real_exists(p)

    monkeypatch.setattr(os.path, "exists", fake_exists)

    # Make os.makedirs fail
    def boom(_):
        raise OSError("disk is full")

    monkeypatch.setattr(os, "makedirs", boom)

    message_pattern = f"Creation of the directory '{base_directory_to_save_to}' failed"
    with pytest.raises(OSError, match=message_pattern):
        State().save(file_to_save_to)

def test_state_raises_exception_on_save_if_file_cannot_be_written(monkeypatch):
    file_to_save_to = tempfile.mktemp()

    def boom(*args, **kwargs):
        raise OSError("disk is full")

    monkeypatch.setattr(pickle, "dump", boom)

    message = "Failed saving data to disk"
    with pytest.raises(Exception, match=message):
        State().save(file_to_save_to)

def test_state_can_be_loaded_from_disk_if_path_exists(get_drawers, get_cutting_boards):
    drawers = get_drawers
    cutting_boards = get_cutting_boards

    file_to_save_to = tempfile.mktemp()
    State(drawers, cutting_boards).save(file_to_save_to)

    state = State().load(file_to_save_to)

    for idx, drawer in enumerate(drawers):
        assert state.get_drawers()[idx].get_length_in_centimeters() == drawer.get_length_in_centimeters()
        assert state.get_drawers()[idx].get_width_in_centimeters() == drawer.get_width_in_centimeters()
        assert state.get_drawers()[idx].get_max_load_in_grams() == drawer.get_max_load_in_grams()

    for idx, cutting_board in enumerate(cutting_boards):
        assert state.get_cutting_boards()[idx].get_length_in_centimeters() == cutting_board.get_length_in_centimeters()
        assert state.get_cutting_boards()[idx].get_width_in_centimeters() == cutting_board.get_width_in_centimeters()
        assert state.get_cutting_boards()[idx].get_weight_in_grams() == cutting_board.get_weight_in_grams()
        assert state.get_cutting_boards()[idx].get_price_in_chf() == cutting_board.get_price_in_chf()

    os.remove(file_to_save_to)

def tests_state_raises_exception_on_load_if_file_path_does_not_exist():
    file_that_does_not_exist = tempfile.mktemp()

    message = f"File '{file_that_does_not_exist}' does not exist"

    with pytest.raises(FileNotFoundError, match=message):
        State().load(file_that_does_not_exist)

def tests_state_raises_exception_on_load_if_file_data_cannot_be_loaded(get_drawers, get_cutting_boards, monkeypatch):
    file_to_save_to = tempfile.mktemp()
    State(get_drawers, get_cutting_boards).save(file_to_save_to)

    def boom(*args, **kwargs):
        raise pickle.PicklingError("Could not unpickle data")

    monkeypatch.setattr(pickle, "load", boom)

    message = "Failed loading data from disk"
    with pytest.raises(Exception, match=message):
        State().load(file_to_save_to)
