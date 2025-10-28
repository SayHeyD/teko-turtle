import math

first_number = 24
second_number = 54

def get_divisors(number):
    divisors = []
    for i in range(1, int(math.sqrt(number)) + 1):
        if number % i == 0:
            divisors.append(i)

            if i != number // i:
                divisors.append(number // i)

    return divisors

first_divisors = get_divisors(first_number)
second_divisors = get_divisors(second_number)

# not using an "if" with an "and" but there is an "&" 😁
common_divisors = list(set(first_divisors) & set(second_divisors))

print(f"Divisors of {first_number} and {second_number}: {common_divisors}")