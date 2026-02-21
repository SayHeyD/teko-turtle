from cutting_board_drawers_optimizer.optimizer.cutting_board import CuttingBoard
from cutting_board_drawers_optimizer.optimizer.drawer import Drawer
from cutting_board_drawers_optimizer.optimizer.drawer_state import DrawerState


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
                if (board_len <= drawer_len and board_wid <= drawer_wid) or (
                    board_wid <= drawer_len and board_len <= drawer_wid
                ):
                    fitting_drawers.append(drawer)

            fits[board] = fitting_drawers
        return fits

    def optimize(self) -> dict[Drawer, list[CuttingBoard]]:
        """
        Maximizes the total area of selected cutting boards given:
        - Total costs <= max_budget.
        - Total selected boards <= cutting_board_amount.
        - For each drawer: total weight <= drawer.max_load AND count <= drawer.max_boards.
        - Boards must fit in assigned drawers.

        Tie-breaking:
        1. Lower total cost.
        2. Lower total weight.

        Returns:
            A dictionary mapping each Drawer to a list of CuttingBoards placed in it.
        """
        fits = self.fit_check()
        # Filter out boards that don't fit in any drawer
        eligible_boards = [board for board in self.__cutting_boards if fits[board]]

        # Current best solution tracking
        self.__best_area = -1
        self.__best_cost = float("inf")
        self.__best_weight = float("inf")
        self.__best_assignment: dict[Drawer, list[CuttingBoard]] = {d: [] for d in self.__drawers}

        drawer_states = [DrawerState(d) for d in self.__drawers]

        self.__solve(0, eligible_boards, fits, drawer_states, 0, 0, 0, 0)

        return self.__best_assignment

    def __solve(
        self,
        board_idx: int,
        eligible_boards: list[CuttingBoard],
        fits: dict[CuttingBoard, list[Drawer]],
        drawer_states: list[DrawerState],
        current_area: int,
        current_cost: int,
        current_weight: int,
        total_boards: int,
    ) -> None:
        """
        Private recursive method to find the optimal board-to-drawer assignment.
        """
        # Base case: reached end of boards or reached maximum board limit
        if total_boards == self.__cutting_board_amount or board_idx == len(eligible_boards):
            self.__update_best_solution(current_area, current_cost, current_weight, drawer_states)
            return

        board = eligible_boards[board_idx]
        price = board.get_price_in_centime()
        weight = board.get_weight_in_grams()
        area = board.area

        # Option 1: Try placing the board in each fitting drawer
        for ds in drawer_states:
            if ds.drawer in fits[board] and self.__can_place_board(ds, price, weight, current_cost):
                # Place board
                ds.current_load += weight
                ds.current_boards.append(board)

                self.__solve(
                    board_idx,
                    eligible_boards,
                    fits,
                    drawer_states,
                    current_area + area,
                    current_cost + price,
                    current_weight + weight,
                    total_boards + 1,
                )

                # Backtrack
                ds.current_boards.pop()
                ds.current_load -= weight

        # Option 2: Try skipping this board (move to next board type)
        self.__solve(
            board_idx + 1,
            eligible_boards,
            fits,
            drawer_states,
            current_area,
            current_cost,
            current_weight,
            total_boards,
        )

    def __can_place_board(self, ds: DrawerState, price: int, weight: int, current_cost: int) -> bool:
        """Check if a board can be placed in the given drawer state."""
        return (
            ds.current_load + weight <= ds.max_load
            and len(ds.current_boards) + 1 <= ds.max_boards
            and current_cost + price <= self.__max_budget
        )

    def __update_best_solution(
        self, current_area: int, current_cost: int, current_weight: int, drawer_states: list[DrawerState]
    ) -> None:
        """Compare current solution with the best one found so far and update if better."""
        if current_area > self.__best_area or (
            current_area == self.__best_area
            and (
                current_cost < self.__best_cost
                or (current_cost == self.__best_cost and current_weight < self.__best_weight)
            )
        ):
            self.__best_area = current_area
            self.__best_cost = float(current_cost)
            self.__best_weight = float(current_weight)
            self.__best_assignment = {ds.drawer: list(ds.current_boards) for ds in drawer_states}
