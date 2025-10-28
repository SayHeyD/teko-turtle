numbers = [
    2134,
    234,
    1,
    23412345,
    -6,
    12344123,
    3412,
    2340891423,
    2,
    -6,
    11423,
    12,
    123444123,
    134124,
    1234,
]

smallest_value = min(numbers)
print(f'Kleinster Wert: {smallest_value}')

cleaned_numbers = list(filter(lambda num: num != smallest_value, numbers))
print(f'List without smallest value: {cleaned_numbers}')
