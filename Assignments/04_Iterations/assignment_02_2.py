number = 24
divisors = []

for i in range(1, number):
    if number % i != 0:
        divisors.append(i)

print(f"{number} is not divisible by: {divisors}")