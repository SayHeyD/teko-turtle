from typing import ClassVar


class Validator:
    """Helper class for validating input fields."""

    MAX_CURRENCY_DECIMALS: ClassVar[int] = 2

    @staticmethod
    def is_valid_name(name: str) -> tuple[bool, str | None]:
        """Validate that the name is not empty."""
        if not name.strip():
            return False, "Name is required."
        return True, None

    @staticmethod
    def is_positive_number(value: str, field_name: str) -> tuple[bool, str | None]:
        """Validate that the value is a positive number."""
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
        """Validate that the value is a valid currency amount (positive, max 2 decimals)."""
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
