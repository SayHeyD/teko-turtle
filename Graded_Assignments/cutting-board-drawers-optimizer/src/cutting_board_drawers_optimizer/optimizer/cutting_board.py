class CuttingBoard:
    def __init__(self, length: int, width: int, weight: int, price: int):
        self.__length: int = length
        self.__width: int = width
        self.__weight: int = weight
        self.__price: int = price

        self.__validate_construction_parameters()

    def __validate_construction_parameters(self):
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

    def get_length_in_centimeters(self) -> int:
        return self.__length

    def get_width_in_centimeters(self) -> int:
        return self.__width

    def get_weight_in_grams(self) -> int:
        return self.__weight

    def get_price_in_chf(self) -> str:
        return f"{self.__price / 100:.2f}"
