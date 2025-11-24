"""
Module containing the cutting board class
"""

class CuttingBoard:
    """
    For managing cutting boards inputted by the users
    """
    def __init__(self,
                 length: int = 0,
                 width: int = 0,
                 price: int = 0,
                 weight: int = 0
                 ):

        if length == 0 or width == 0 or price == 0 or weight == 0:
            raise ValueError(
                "Length, width, price, and weight must be greater than 0")

        # In centimeters
        self.__length: int = length
        # In centimeters
        self.__width: int = width
        # In "rappen"
        self.__price: int = price
        # In gramms
        self.__weight: int = weight

    def get_length(self) -> int:
        """
        Returns the length of the cutting board in centimeters
        """
        return self.__length

    def get_width(self) -> int:
        """
        Returns the width of the cutting board in centimeters
        """
        return self.__width

    def get_price(self) -> int:
        """
        Returns the price of the cutting board in centimeters
        """
        return self.__price

    def get_weight(self) -> int:
        """
        Returns the weight of the cutting board in centimeters
        """
        return self.__weight
