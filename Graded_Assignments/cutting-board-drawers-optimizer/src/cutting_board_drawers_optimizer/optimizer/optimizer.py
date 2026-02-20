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

    def fit_check(self) -> dict[CuttingBoard, list[Drawer]]:
        """
        Check which cutting boards fit into which drawers.
        A board fits if its (length <= drawer_length AND width <= drawer_width)
        OR if its (width <= drawer_length AND length <= drawer_width) after a 90-degree rotation.
        """
        fits = {}
        for board in self.__cutting_boards:
            fitting_drawers = []
            board_len = board.get_length_in_centimeters()
            board_wid = board.get_width_in_centimeters()

            for drawer in self.__drawers:
                drawer_len = drawer.get_length_in_centimeters()
                drawer_wid = drawer.get_width_in_centimeters()

                # Check original orientation
                if board_len <= drawer_len and board_wid <= drawer_wid:
                    fitting_drawers.append(drawer)
                # Check 90-degree rotation
                elif board_wid <= drawer_len and board_len <= drawer_wid:
                    fitting_drawers.append(drawer)

            fits[board] = fitting_drawers
        return fits
