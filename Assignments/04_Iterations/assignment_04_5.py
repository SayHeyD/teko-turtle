import math

square_product_number_limit = 100

square_factor = math.floor(math.sqrt(square_product_number_limit))

square_numbers = [number * number for number in range(1, square_factor + 1)]

print([*square_numbers, *square_numbers[:-1]])