import pytest
from cutting_board_drawers_optimizer.ui.validator import Validator

def test_validator_is_valid_name():
    # Valid names
    assert Validator.is_valid_name("Cutting Board")[0] is True
    assert Validator.is_valid_name("  Trimmed Name  ")[0] is True
    
    # Invalid names
    valid, error = Validator.is_valid_name("")
    assert valid is False
    assert error == "Name is required."
    
    valid, error = Validator.is_valid_name("   ")
    assert valid is False
    assert error == "Name is required."

def test_validator_is_positive_number():
    # Valid positive numbers
    assert Validator.is_positive_number("10", "Field")[0] is True
    assert Validator.is_positive_number("10.5", "Field")[0] is True
    assert Validator.is_positive_number("0.1", "Field")[0] is True
    
    # Non-numeric values
    valid, error = Validator.is_positive_number("abc", "Field")
    assert valid is False
    assert error == "Field must be a number."
    
    valid, error = Validator.is_positive_number("", "Field")
    assert valid is False
    assert error == "Field must be a number."
    
    # Zero and negative values
    valid, error = Validator.is_positive_number("0", "Field")
    assert valid is False
    assert error == "Field must be positive."
    
    valid, error = Validator.is_positive_number("-5", "Field")
    assert valid is False
    assert error == "Field must be positive."
