number = 1
for _ in range(26):
    print(number)
    number += number

    if number >= 100:
        number = 1