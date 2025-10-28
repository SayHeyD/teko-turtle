import math

def get_number_input(prompt) -> int:

    error_message = 'Die Angabe muss eine Ganzzahl grösser gleich 0 sein!'

    while True:
        user_input = input(prompt)

        try:
            user_input = int(user_input)

            if user_input < 1:
                print(error_message)
                continue

        except ValueError:
            print(error_message)
            continue

        return user_input

    return 0

def get_amount_of_halving(number):
    # No need for an iteration here
    return math.floor(math.log(number, 2))

first_factor = get_number_input('Erster Faktor:\n')
second_factor = get_number_input('Zweiter Faktor:\n')

halving_amount = get_amount_of_halving(first_factor)

# Multiply the second factor by the halving amount twice
doubling_value = second_factor * halving_amount * halving_amount

# Add the second factor once again and print to console
print(doubling_value + second_factor)
