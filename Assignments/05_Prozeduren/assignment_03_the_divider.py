def the_divider(dividers: list[int], number: int) -> bool:
    for divider in dividers:
        if divider == 0:
            return False

        if number % divider != 0:
            return False

    return True
print(the_divider(list(range(1, 11)), 2520))

# Alle kleineren Zahlen sind nicht mit allen Zahlen bis 20 teilbar
count = 2520
iterations = 0

# Lösung: 232_792_560
while True:
    iterations += 1
    print(f'Number: {count}', end='\r')
    if the_divider(list(range(1, 21)), count):
        print(f'Number divisible by all numbers from 1 to 20: {count}')
        exit(0)
    else:
        count += 1