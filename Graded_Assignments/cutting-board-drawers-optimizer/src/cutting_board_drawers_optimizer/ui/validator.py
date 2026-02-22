from typing import ClassVar


class Validator:
    """
    Utility class for validating user input from the UI.
    Provides methods to check for common constraints like non-empty names,
    positive numeric values, and valid currency formats.
    """

    MAX_CURRENCY_DECIMALS: ClassVar[int] = 2

    @staticmethod
    def is_valid_name(name: str) -> tuple[bool, str | None]:
        """
        Validate that the name is not empty or just whitespace.

        Returns:
            A tuple (is_valid, error_message).
        """
        if not name.strip():
            return False, "Name is required."
        return True, None

    @staticmethod
    def is_positive_number(value: str, field_name: str) -> tuple[bool, str | None]:
        """
        Validate that the input string can be parsed as a positive number.

        Args:
            value: The string to validate.
            field_name: Name of the field for the error message.

        Returns:
            A tuple (is_valid, error_message).
        """
        try:
            val = float(value)
            if val <= 0:
                return False, f"{field_name} must be positive."
        except ValueError:
            return False, f"{field_name} must be a number."
        else:
            return True, None

    @staticmethod
    def is_valid_currency(value: str, field_name: str) -> tuple[bool, str | None]:
        """
        Validate that the input is a valid currency amount.
        - Must be a positive number.
        - Must have at most MAX_CURRENCY_DECIMALS (2) decimal places.

        Returns:
            A tuple (is_valid, error_message).
        """
        # First check if it is a positive number
        valid, err = Validator.is_positive_number(value, field_name)
        if not valid:
            return False, err

        # Check for max decimals
        if "." in value:
            decimals = value.split(".")[1]
            if len(decimals) > Validator.MAX_CURRENCY_DECIMALS:
                return (
                    False,
                    f"{field_name} can have at most {Validator.MAX_CURRENCY_DECIMALS} decimal places.",
                )

        return True, None
