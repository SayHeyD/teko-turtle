def harmonic_mean(a, b):
    return 2 / (1 / a + 1 / b)


def get_input(descriptor):
    invalid_answer = True

    user_input = None

    while invalid_answer:
        user_input = input('Bitte gib die ' + descriptor + ' Zahl an:\n')

        try:
            if int(user_input) != 0:
                invalid_answer = False
        except ValueError:
            print('Die Zahl muss eine ganze zahl sein!')

    return int(user_input)

first_number = get_input('erste')
second_number = get_input('zweite')

print(harmonic_mean(first_number, second_number))