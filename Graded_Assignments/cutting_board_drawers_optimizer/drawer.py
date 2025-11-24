"""
Drawer class module
"""
class Drawer:
    """
    For managing kitchen drawers inputted by the users
    """
    def __init__(self,
                 length: int = 0,
                 width: int = 0,
                 max_load: int = 0,
                 ):
        if length == 0 or width == 0 or max_load == 0:
            raise ValueError(
                "Length, width, and maximum load must be greater than 0")

        # In centimeters
        self.__length: int = length
        # In centimeters
        self.__width: int = width
        # In gramms
        self.__max_load: int = max_load

    def get_length(self) -> int:
        """
        Returns the length of the drawer in centimeters
        """
        return self.__length

    def get_width(self) -> int:
        """
        Returns the width of the drawer in centimeters
        """
        return self.__width

    def get_max_load(self) -> int:
        """
        Returns the maximum load of the drawer in grams
        """
        return self.__max_load
