from cutting_board_drawers_optimizer.optimizer.cutting_board import CuttingBoard
from cutting_board_drawers_optimizer.optimizer.drawer import Drawer


class Optimizer:
    def __init__(
        self,
        drawers: list[Drawer],
        cutting_boards: list[CuttingBoard],
        max_budget: int,
        cutting_board_amount: int,
    ):
        self.__drawers = drawers
        self.__cutting_boards = cutting_boards
        self.__max_budget = max_budget
        self.__cutting_board_amount = cutting_board_amount

    @property
    def drawers(self) -> list[Drawer]:
        return self.__drawers

    @property
    def cutting_boards(self) -> list[CuttingBoard]:
        return self.__cutting_boards

    @property
    def max_budget(self) -> int:
        return self.__max_budget

    @property
    def cutting_board_amount(self) -> int:
        return self.__cutting_board_amount
