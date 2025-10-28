numbers = [
    1,
    2,
    4,
    6,
    120,
    1,
    1234,
    421344231,
    31456,
    987654,
    12312,
    143,
    2,
    3,
    1,
    2,
    4
]

number_sum = 0

for number in numbers:
    number_sum += number

average = number_sum / len(numbers)

print(f'Summe: {number_sum}')
print(f'Average: {average}')