import math

square_product_number_limit = 1000

square_factor = math.floor(math.sqrt(square_product_number_limit))

square_numbers = [number * number for number in range(1, square_factor + 1)]

print(f'Letzte 10 Quadratzahlen: {square_numbers[-10:]}')
