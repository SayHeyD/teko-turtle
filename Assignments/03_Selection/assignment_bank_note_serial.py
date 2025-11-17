import re

class Serial:
    def __init__(self, serial_number: str):
        self.serial_number = serial_number
        self.country_index = self.__get_alphabet_index()
        self.check_digit = self.__get_check_digit()
        self.note_id = self.__verify_note_id()

    def __get_alphabet_index(self) -> str:
        letter_upper_case = self.serial_number[0].upper()

        char_pattern = re.compile(r"^[A-Z]$")
        if not char_pattern.match(letter_upper_case):
            raise ValueError("Invalid letter, must be uppercase letter from A - Z")

        # Use Unicode index as a base, since letters from A to Z are in the correct order
        # Return string as we want to easily handle multiple characters (ints complicate this)
        return str(ord(letter_upper_case) - ord("A") + 1)

    def __get_check_digit(self) -> int:
        try:
            return int(self.serial_number[-1])
        except ValueError:
            raise ValueError("Invalid check digit, must be a number from 0 - 9")

    def __verify_note_id(self) -> str:
        note_id = self.serial_number[1:-1]

        note_id_pattern = re.compile(r"^\d{10}$")

        if not note_id_pattern.match(note_id):
            raise ValueError("Invalid note number, must be a number from 1 - 999999")

        # Do not convert to int as we would lose leading zeros
        return note_id

    def validate(self) -> bool:
        digits = [int(char) for char in self.country_index]
        digits.extend([int(char) for char in self.note_id])

        print(digits)

        cross_sum = sum(digits)

        rest_of_division_by_nine = cross_sum % 9

        if rest_of_division_by_nine == 0 and self.check_digit == 9:
            return True
        else:
            difference = 8 - rest_of_division_by_nine

            return difference == self.check_digit


def get_serial_from_user() -> str:
    while True:
        user_input = input("Enter your serial number: ")

        serial_pattern = re.compile(r"^[A-Z]\d{11}$")

        if serial_pattern.match(user_input):
            return user_input
        else:
            print("Invalid serial number, must be in the format A1234567890")

serial = Serial(get_serial_from_user())

try:
    if serial.validate():
        print("Valid serial number!")
    else:
        print("Invalid serial number!")
except ValueError as e:
    print(e)

