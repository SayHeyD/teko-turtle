from typing import TYPE_CHECKING

from cutting_board_drawers_optimizer.optimizer.drawer import Drawer

if TYPE_CHECKING:
    from cutting_board_drawers_optimizer.optimizer.cutting_board import CuttingBoard


class DrawerState:
    """
    Tracks the current state of a drawer during optimization.
    Helps keep track of the current weight load and the assigned boards.
    """

    def __init__(self, drawer: Drawer):
        """
        Initialize the drawer state based on its properties.

        Args:
            drawer: The Drawer object to track.
        """
        self.drawer = drawer
        self.max_load = drawer.get_max_load_in_grams()
        self.max_boards = drawer.get_max_boards()
        self.current_load = 0  # Tracks total weight in grams
        self.current_boards: list[CuttingBoard] = []  # List of boards currently placed
