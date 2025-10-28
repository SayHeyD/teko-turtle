import math

square_product_number_limit = 100

square_factor = math.floor(math.sqrt(square_product_number_limit))

square_numbers = [number * number for number in range(1, square_factor + 1)]

square_number_sum = 0

for number in square_numbers:
    square_number_sum += number

print(f'Summe aller Quadratzahlen: {square_number_sum}')