class Validator:
    """Helper class for validating input fields."""

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
