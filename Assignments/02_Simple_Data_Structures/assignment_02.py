def get_resistance():
    # Infinite loops are generally bad, but in this case, whatever
    while True:
        user_input = input('Wiederstand (Ohm):\n')

        try:
            return int(user_input)
        except ValueError:
            print('Der Wiederstand muss als ganze Zahl angegeben werden!')

def print_tolerance_error_message():
    print('Die Toleranz muss ein Wert zwischen 0 und 1 sein!')
    print('(Kommazahlen erlaubt)')

def get_tolerance():
    # Infinite loops are generally bad, but in this case, whatever
    while True:
        user_input = input('Toleranz (%):\n')

        try:
            user_input = user_input.replace(',', '.')
            user_input = float(user_input)

            if user_input > 1 or user_input < 0:
                print_tolerance_error_message()
                continue

            return user_input

        except ValueError:
            print_tolerance_error_message()

def calculate_max_allowed_resistence(base_resistance, tolerance_percentage):
    return base_resistance + base_resistance * tolerance_percentage

def calculate_min_allowed_resistence(base_resistance, tolerance_percentage):
    return base_resistance - base_resistance * tolerance_percentage

resistance = get_resistance()
tolerance = get_tolerance()

max_resistence = calculate_max_allowed_resistence(resistance, tolerance)
min_resistence = calculate_min_allowed_resistence(resistance, tolerance)

print('Maximal erlaubter Wiederstand: ' + str(max_resistence))
print('Minimal erlaubter Wiederstand: ' + str(min_resistence))