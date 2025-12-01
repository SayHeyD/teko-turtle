import json
import os
from typing import Self

from cutting_board_drawers_optimizer.optimizer import CuttingBoard, Drawer
from cutting_board_drawers_optimizer.state._state_data import StateData
from cutting_board_drawers_optimizer.state.loading_data_failed_error import LoadingDataFailedError
from cutting_board_drawers_optimizer.state.saving_data_failed_error import SavingDataFailedError


class State:
    def __init__(self, drawers: list[Drawer] | None = None, cutting_boards: list[CuttingBoard] | None = None):
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
            with open(file_path, "r") as file:
                self.__data = StateData.from_dict(json.load(file))
        except Exception as e:
            message = "Failed loading data from disk"
            raise LoadingDataFailedError(message) from e

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
                message = f"Creation of the directory '{dir_path}' failed"
                raise OSError(message) from e

        with open(file_path, "w") as file:
            try:
                json.dump(self.__data.to_dict(), file, ensure_ascii=False)
            except Exception as e:
                message = "Failed saving data to disk"
                raise SavingDataFailedError(message) from e

        return self
