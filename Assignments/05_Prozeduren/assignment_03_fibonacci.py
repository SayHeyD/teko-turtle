def fibonacci(number: int):
    if number in {0, 1}:
        return number
    else:
        return fibonacci(number - 1) + fibonacci(number - 2)

print(fibonacci(15))