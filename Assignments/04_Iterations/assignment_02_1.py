import math

def get_number_input(prompt) -> int:

    error_message = 'Die Angabe muss eine Ganzzahl über 1 sein!'

    while True:
        user_input = input(prompt)

        try:
            user_input = int(user_input)

            if user_input <= 1:
                print(error_message)
                continue

        except ValueError:
            print(error_message)
            continue

        return user_input

    return 0

# Variable x is not necessary
FACTOR = get_number_input('Bitte gibt deinen Faktor ein:\n') # factor ist meine variable "a"

# Get the exact index of 1000
# This could be solved iteratively, but using the Factor as the base
# for a logarithm achieves the same thing without needing an iteration
index = math.log(1000, FACTOR)

# Calculate the value of the number at the next index that is an integer
next_number = FACTOR ** math.ceil(index)

# If the next number is exactly 1000, we want the next largest number,
# so we multiply the next_number again with the factor
if next_number == 1000:
    next_number *= FACTOR

print(next_number)

