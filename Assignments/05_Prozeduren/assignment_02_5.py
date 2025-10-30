def count_value(number_list: list[int], value: int) -> int:
    return number_list.count(value)

value = 3
value_count = count_value([1, 2, 3, 3, 3, 3, 3, 3, 4, 4, 4, 5], value)

print(f'Der Wert {value} kommt in der Liste {value_count} Mal vor.')