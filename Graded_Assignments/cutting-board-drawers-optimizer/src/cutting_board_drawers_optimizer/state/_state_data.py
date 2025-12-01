from cutting_board_drawers_optimizer.optimizer import CuttingBoard, Drawer


class StateData:
    def __init__(self, drawers: list[Drawer], cutting_boards: list[CuttingBoard]):
        self.__drawers = drawers
        self.__cutting_boards = cutting_boards

    def get_drawers(self) -> list[Drawer]:
        return self.__drawers

    def get_cutting_boards(self) -> list[CuttingBoard]:
        return self.__cutting_boards
