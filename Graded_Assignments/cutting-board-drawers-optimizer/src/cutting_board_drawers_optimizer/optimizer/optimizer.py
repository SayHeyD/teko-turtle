from cutting_board_drawers_optimizer.optimizer.cutting_board import CuttingBoard
from cutting_board_drawers_optimizer.optimizer.drawer import Drawer
from cutting_board_drawers_optimizer.optimizer.drawer_state import DrawerState


class Optimizer:
    """
    Optimizer class that determines the best distribution of cutting boards into drawers.
    It uses a backtracking algorithm to maximize the total surface area.
    """

    def __init__(
        self,
        drawers: list[Drawer],
        cutting_boards: list[CuttingBoard],
        max_budget: int,
        cutting_board_amount: int,
    ):
        """
        Initialize the Optimizer with constraints.

        Args:
            drawers: List of available Drawers.
            cutting_boards: List of available CuttingBoard types.
            max_budget: Maximum allowed cost in centimes.
            cutting_board_amount: Total number of boards to select.
        """
        self.__drawers = drawers
        self.__cutting_boards = cutting_boards
        self.__max_budget = max_budget
        self.__cutting_board_amount = cutting_board_amount

        # Field initialization
        self.__best_assignment = None
        self.__best_weight = None
        self.__best_cost = None
        self.__best_area = None

    @property
    def drawers(self) -> list[Drawer]:
        """Returns the list of drawers."""
        return self.__drawers

    @property
    def cutting_boards(self) -> list[CuttingBoard]:
        """Returns the list of cutting board types."""
        return self.__cutting_boards

    @property
    def max_budget(self) -> int:
        """Returns the maximum budget in centimes."""
        return self.__max_budget

    @property
    def cutting_board_amount(self) -> int:
        """Returns the total number of boards to select."""
        return self.__cutting_board_amount

    def fit_check(self) -> dict[CuttingBoard, list[Drawer]]:
        """
        Determines which drawers each cutting board type can physically fit into.
        A board fits if its (length <= drawer_length AND width <= drawer_width)
        OR if its (width <= drawer_length AND length <= drawer_width) after a 90-degree rotation.

        Returns:
            A dictionary mapping each CuttingBoard to a list of compatible Drawers.
        """
        fits = {}
        # Loop over each cutting board
        for board in self.__cutting_boards:
            fitting_drawers = []
            # Assign local variables to make code more readable
            board_len = board.get_length_in_centimeters()
            board_wid = board.get_width_in_centimeters()

            # Loop over each drawer
            for drawer in self.__drawers:
                # Assign local variables to make code more readable
                drawer_len = drawer.get_length_in_centimeters()
                drawer_wid = drawer.get_width_in_centimeters()

                # Check if the board fits into the drawer as-is or rotated 90 degrees
                if (board_len <= drawer_len and board_wid <= drawer_wid) or (
                    board_wid <= drawer_len and board_len <= drawer_wid
                ):
                    # Add the drawer to the list of compatible drawers
                    fitting_drawers.append(drawer)

            # Save the list of compatible drawers for this board to the dict
            fits[board] = fitting_drawers
        return fits

    def optimize(self) -> dict[Drawer, list[CuttingBoard]]:
        """
        Runs the optimization algorithm to find the combination with maximum area.

        Rules:
        - Total costs must not exceed max_budget.
        - Total selected boards must not exceed cutting_board_amount.
        - Per drawer: Total weight <= load capacity AND Total boards <= limit.
        - Boards must physically fit into their assigned drawers.

        Selection Strategy:
        1. Maximize Total Surface Area.
        2. Tie-break: Prefer lower Total Cost.
        3. Tie-break: Prefer lower Total Weight.

        Returns:
            A dictionary mapping each Drawer to the list of boards assigned to it.
        """
        # Determine which drawers each board type can physically fit into
        fits = self.fit_check()
        # Only consider boards that fit in at least one drawer
        eligible_boards = [board for board in self.__cutting_boards if fits[board]]

        # Keep track of the best solution found during recursive search
        # Set initial values to the worst possible option
        # float("inf") references infinity
        self.__best_area = -1
        self.__best_cost = float("inf")
        self.__best_weight = float("inf")
        # Generator statement create an emtpy array for each drawer
        self.__best_assignment: dict[Drawer, list[CuttingBoard]] = {d: [] for d in self.__drawers}

        # Initialize the internal state for each drawer to track the current load during the search
        # Generator statement create a DrawerState object for each drawer
        drawer_states = [DrawerState(d) for d in self.__drawers]

        # Start recursive search (Backtracking)
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
        Recursive backtracking solver. Explores all valid combinations of board placements.

        Args:
            board_idx: Index of the cutting board type currently being considered.
            eligible_boards: List of boards that fit in at least one drawer.
            fits: Compatibility mapping (board -> drawers).
            drawer_states: Current usage state of each drawer.
            current_area: Total area of boards selected so far.
            current_cost: Total cost of boards selected so far.
            current_weight: Total weight of boards selected so far.
            total_boards: Count of boards selected so far.
        """
        # Base case: Do not continue if we've used all allowed boards OR we've considered all board types
        if total_boards == self.__cutting_board_amount or board_idx == len(eligible_boards):
            self.__update_best_solution(current_area, current_cost, current_weight, drawer_states)
            return

        # Assign local variables to make code more readable
        board = eligible_boards[board_idx]
        price = board.get_price_in_centime()
        weight = board.get_weight_in_grams()
        area = board.area

        # Strategy 1: Attempt to place another instance of the CURRENT board type
        for ds in drawer_states:
            # Check if the board fits in this drawer and if we have budget/load capacity
            if ds.drawer in fits[board] and self.__can_place_board(ds, price, weight, current_cost):
                # Apply Placement
                ds.current_load += weight
                ds.current_boards.append(board)

                # Recurse: stay on the same board_idx to allow multiple selection of the same board
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

                # Backtrack: undo placement for next iterations
                ds.current_boards.pop()
                ds.current_load -= weight

        # Strategy 2: Skip to the NEXT board type
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
        """Validates if adding the board violates any drawer or budget constraints."""
        return (
            ds.current_load + weight <= ds.max_load
            and len(ds.current_boards) + 1 <= ds.max_boards
            and current_cost + price <= self.__max_budget
        )

    def __update_best_solution(
        self, current_area: int, current_cost: int, current_weight: int, drawer_states: list[DrawerState]
    ) -> None:
        """
        Updates the global best solution if the current one is superior based on the defined strategy.
        """
        # Preference: 1. Higher Area, 2. Lower Cost, 3. Lower Weight
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
            # Create a deep-ish copy of the current assignment
            self.__best_assignment = {ds.drawer: list(ds.current_boards) for ds in drawer_states}
