def interval_even(number_list: list[int], start: int, end: int) -> list[int]:
    for number in range(start, end + 1):
        if number % 2 == 0:
            number_list.append(number)

    return number_list

even_numbers = []
interval_even(even_numbers, 2, 80)

print(even_numbers)