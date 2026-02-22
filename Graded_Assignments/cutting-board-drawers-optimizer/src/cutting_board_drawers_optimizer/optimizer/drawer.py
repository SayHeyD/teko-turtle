class Drawer:
    """Represents a drawer where cutting boards are stored."""

    def __init__(self, name: str, length: int, width: int, max_load: int, max_boards: int):
        """
        Initialize a Drawer.

        Args:
            name: The name of the drawer.
            length: Length in centimeters.
            width: Width in centimeters.
            max_load: Weight limit in grams.
            max_boards: Maximum number of cutting boards allowed in the drawer.
        """
        self.__name: str = name
        self.__length: int = length
        self.__width: int = width
        self.__max_load: int = max_load
        self.__max_boards: int = max_boards

        self.__validate_construction_parameters()

    def __validate_construction_parameters(self):
        """Ensures all parameters are valid."""
        invalid_parameters = []

        if self.__length <= 0:
            invalid_parameters.append("length")

        if self.__width <= 0:
            invalid_parameters.append("width")

        if self.__max_load <= 0:
            invalid_parameters.append("max_load")

        if self.__max_boards <= 0:
            invalid_parameters.append("max_boards")

        if len(invalid_parameters) > 0:
            params = ", ".join(invalid_parameters)
            message = f"Invalid parameters: {params}"
            raise ValueError(message)

    def get_name(self) -> str:
        """Returns the name of the drawer."""
        return self.__name

    def get_length_in_centimeters(self) -> int:
        """Returns the length in cm."""
        return self.__length

    def get_width_in_centimeters(self) -> int:
        """Returns the width in cm."""
        return self.__width

    def get_max_load_in_grams(self) -> int:
        """Returns the weight capacity in grams."""
        return self.__max_load

    def get_max_boards(self) -> int:
        """Returns the board count limit."""
        return self.__max_boards

    @property
    def area(self) -> int:
        """Calculates and returns the area of the drawer in cm²."""
        return self.__length * self.__width
