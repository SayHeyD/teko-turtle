import json
import os
from typing import Self

from cutting_board_drawers_optimizer.optimizer import CuttingBoard, Drawer
from cutting_board_drawers_optimizer.state._state_data import StateData
from cutting_board_drawers_optimizer.state.loading_data_failed_error import LoadingDataFailedError
from cutting_board_drawers_optimizer.state.saving_data_failed_error import SavingDataFailedError


class State:
    """
    Main state controller that manages loading, saving, and accessing application data.
    Acts as a wrapper around the StateData DTO.
    """

    def __init__(
        self,
        drawers: list[Drawer] | None = None,
        cutting_boards: list[CuttingBoard] | None = None,
        budget_cents: int | None = None,
        cutting_board_amount: int | None = None,
    ):
        """Initializes the application state with optional initial data."""
        if drawers is None:
            drawers = []

        if cutting_boards is None:
            cutting_boards = []

        self.set_data(drawers, cutting_boards, budget_cents, cutting_board_amount)

    def _get_data(self) -> StateData:
        """Returns the internal StateData object."""
        return self.__data

    def get_drawers(self) -> list[Drawer]:
        """Returns the list of drawers from the current state."""
        return self.__data.get_drawers()

    def get_cutting_boards(self) -> list[CuttingBoard]:
        """Returns the list of cutting boards from the current state."""
        return self.__data.get_cutting_boards()

    def get_budget_cents(self) -> int | None:
        """Returns the current optimization budget in centimes."""
        return self.__data.get_budget_cents()

    def get_cutting_board_amount(self) -> int | None:
        """Returns the current target amount of cutting boards."""
        return self.__data.get_cutting_board_amount()

    def set_data(
        self,
        drawers: list[Drawer],
        cutting_boards: list[CuttingBoard],
        budget_cents: int | None = None,
        cutting_board_amount: int | None = None,
    ) -> None:
        """Updates the internal state with new data."""
        self.__data = StateData(drawers, cutting_boards, budget_cents, cutting_board_amount)

    def load(self, file_path: str) -> Self:
        """
        Loads state from a JSON file.

        Args:
            file_path: Path to the JSON file.

        Returns:
            The State instance (self) for method chaining.

        Raises:
            FileNotFoundError: If the file is not found.
            LoadingDataFailedError: If any error occurs during parsing or initialization.
        """
        # Check if the file exists
        if not os.path.exists(file_path):
            message = f"File '{file_path}' does not exist"
            raise FileNotFoundError(message)

        # Load the data from the file
        try:
            with open(file_path) as file:
                self.__data = StateData.from_dict(json.load(file))
        except Exception as e:
            # If the file cannot be read, wrap the original exception in our custom error
            message = "Failed loading data from disk"
            raise LoadingDataFailedError(message) from e

        return self

    def save(self, file_path: str) -> Self:
        """
        Saves the current state to a JSON file.
        Creates the necessary directories if they don't exist.

        Args:
            file_path: Path where the file should be saved.

        Returns:
            The State instance (self) for method chaining.

        Raises:
            FileExistsError: If the file already exists (preventing accidental overwrite).
            SavingDataFailedError: If any error occurs during serialization or file writing.
        """
        dir_path = os.path.dirname(file_path)

        # Check if the file already exists
        if os.path.exists(file_path):
            message = f"File '{file_path}' already exists"
            raise FileExistsError(message)

        # Check if the directory exists and create it if not
        if not os.path.exists(dir_path):
            # Create the directory recursively (including parents)
            try:
                os.makedirs(dir_path)
            except OSError as e:
                message = f"Creation of the directory '{dir_path}' failed"
                raise OSError(message) from e

        # Serialize and write the data to the file
        with open(file_path, "w") as file:
            try:
                # ensure_ascii=False ensures special characters (like German umlauts) are saved correctly
                json.dump(self.__data.to_dict(), file, ensure_ascii=False)
            except Exception as e:
                message = "Failed saving data to disk"
                raise SavingDataFailedError(message) from e

        return self
