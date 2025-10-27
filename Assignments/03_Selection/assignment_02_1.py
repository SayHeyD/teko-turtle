numbers = {
    'a': 0,
    'b': 5,
    'c': 10,
    'd': 15,
    'e': 20,
}

largest_number = max(numbers, key=numbers.get)

for key, number in numbers.items():
    if key == numbers[largest_number]:
        print('"' + str(key) + '" ist die grösste Zahl (' + str(number) + ')')