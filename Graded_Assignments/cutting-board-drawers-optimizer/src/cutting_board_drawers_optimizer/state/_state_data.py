from cutting_board_drawers_optimizer.optimizer import CuttingBoard, Drawer


class StateData:
    def __init__(self, drawers: list[Drawer], cutting_boards: list[CuttingBoard]):
        self.__drawers = drawers
        self.__cutting_boards = cutting_boards

    def get_drawers(self) -> list[Drawer]:
        return self.__drawers

    def get_cutting_boards(self) -> list[CuttingBoard]:
        return self.__cutting_boards

    def to_dict(self) -> dict:
        return {
            "drawers": [
                {
                    "length": drawers.get_length_in_centimeters(),
                    "width": drawers.get_width_in_centimeters(),
                    "max_load": drawers.get_max_load_in_grams(),
                }
                for drawers in self.__drawers
            ],
            "cutting_boards": [
                {
                    "length": cutting_boards.get_length_in_centimeters(),
                    "width": cutting_boards.get_width_in_centimeters(),
                    "weight": cutting_boards.get_weight_in_grams(),
                    # Store exact cents derived from the public CHF string
                    "price_cents": cutting_boards.get_price_in_centime(),
                }
                for cutting_boards in self.__cutting_boards
            ],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "StateData":
        drawers = [
            Drawer(drawer["length"], drawer["width"], drawer["max_load"])  # ints
            for drawer in data.get("drawers", [])
        ]
        cutting_boards = [
            CuttingBoard(
                cutting_board["length"],
                cutting_board["width"],
                cutting_board["weight"],
                int(cutting_board["price_cents"])  # back to cents for constructor
            )
            for cutting_board in data.get("cutting_boards", [])
        ]
        return cls(drawers, cutting_boards)
