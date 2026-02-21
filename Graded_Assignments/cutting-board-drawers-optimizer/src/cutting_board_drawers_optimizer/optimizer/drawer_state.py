from typing import TYPE_CHECKING

from cutting_board_drawers_optimizer.optimizer.drawer import Drawer

if TYPE_CHECKING:
    from cutting_board_drawers_optimizer.optimizer.cutting_board import CuttingBoard


class DrawerState:
    def __init__(self, drawer: Drawer):
        self.drawer = drawer
        self.max_load = drawer.get_max_load_in_grams()
        self.max_boards = drawer.get_max_boards()
        self.current_load = 0
        self.current_boards: list[CuttingBoard] = []
