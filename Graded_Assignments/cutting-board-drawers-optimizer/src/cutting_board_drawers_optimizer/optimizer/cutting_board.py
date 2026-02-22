class CuttingBoard:
    """Represents a cutting board with its dimensions, weight, and price."""

    def __init__(self, name: str, length: int, width: int, weight: int, price: int):
        """
        Initialize a CuttingBoard.

        Args:
            name: The name of the cutting board.
            length: Length in centimeters.
            width: Width in centimeters.
            weight: Weight in grams.
            price: Price in centimes (rappen).
        """
        self.__name: str = name
        self.__length: int = length
        self.__width: int = width
        self.__weight: int = weight
        self.__price: int = price

        self.__validate_construction_parameters()

    def __validate_construction_parameters(self):
        """Ensures all parameters are valid."""
        invalid_parameters = []

        if self.__length <= 0:
            invalid_parameters.append("length")

        if self.__width <= 0:
            invalid_parameters.append("width")

        if self.__weight <= 0:
            invalid_parameters.append("weight")

        if self.__price <= 0:
            invalid_parameters.append("price")

        if len(invalid_parameters) > 0:
            message = ", ".join(invalid_parameters)
            raise ValueError(message)

    def get_name(self) -> str:
        """Returns the name of the cutting board."""
        return self.__name

    def get_length_in_centimeters(self) -> int:
        """Returns the length in cm."""
        return self.__length

    def get_width_in_centimeters(self) -> int:
        """Returns the width in cm."""
        return self.__width

    def get_weight_in_grams(self) -> int:
        """Returns the weight in grams."""
        return self.__weight

    def get_price_in_chf(self) -> str:
        """Returns the price formatted as a CHF string (e.g., '10.50')."""
        return f"{self.__price / 100:.2f}"

    def get_price_in_centime(self) -> int:
        """Returns the raw price in centimes (rappen)."""
        return self.__price

    @property
    def area(self) -> int:
        """Calculates and returns the area of the cutting board in cm²."""
        return self.__length * self.__width
