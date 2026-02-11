class Drawer:
    def __init__(self, name: str, length: int, width: int, max_load: int):
        self.__name: str = name
        self.__length: int = length
        self.__width: int = width
        self.__max_load: int = max_load

        self.__validate_construction_parameters()

    def __validate_construction_parameters(self):
        invalid_parameters = []

        if self.__length <= 0:
            invalid_parameters.append("length")

        if self.__width <= 0:
            invalid_parameters.append("width")

        if self.__max_load <= 0:
            invalid_parameters.append("max_load")

        if len(invalid_parameters) > 0:
            params = ", ".join(invalid_parameters)
            message = f"Invalid parameters: {params}"
            raise ValueError(message)

    def get_name(self) -> str:
        return self.__name

    def get_length_in_centimeters(self) -> int:
        return self.__length

    def get_width_in_centimeters(self) -> int:
        return self.__width

    def get_max_load_in_grams(self) -> int:
        return self.__max_load
