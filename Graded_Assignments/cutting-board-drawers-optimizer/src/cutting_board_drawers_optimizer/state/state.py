import os

from typing import Self

from cutting_board_drawers_optimizer.optimizer import Drawer, CuttingBoard
from cutting_board_drawers_optimizer.state._state_data import StateData

import pickle

class State:
    def __init__(self, drawers: list[Drawer] = None, cutting_boards: list[CuttingBoard] = None):
        if drawers is None:
            drawers = []

        if cutting_boards is None:
            cutting_boards = []

        self.__data = StateData(drawers, cutting_boards)

    def _get_data(self) -> StateData:
        return self.__data

    def get_drawers(self) -> list[Drawer]:
        return self.__data.get_drawers()

    def get_cutting_boards(self) -> list[CuttingBoard]:
        return self.__data.get_cutting_boards()

    def load(self, file_path: str) -> Self:
        if not os.path.exists(file_path):
            message = f"File '{file_path}' does not exist"
            raise FileNotFoundError(message)

        try:
            with open(file_path, "rb") as file:
                self.__data = pickle.load(file)
        except Exception as e:
            message = f"Failed loading data from disk: {e}"
            raise Exception(message)

        return self

    def save(self, file_path: str) -> Self:

        dir_path = os.path.dirname(file_path)

        if os.path.exists(file_path):
            message = f"File '{file_path}' already exists"
            raise FileExistsError(message)

        if not os.path.exists(dir_path):
            try:
                os.makedirs(dir_path)
            except OSError as e:
                message = f"Creation of the directory '{dir_path}' failed: {e}"
                raise OSError(message)

        with open(file_path, "wb") as file:
            try:
                pickle.dump(self.__data, file, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                message = f"Failed saving data to disk: {e}"
                raise Exception(message)

        return self