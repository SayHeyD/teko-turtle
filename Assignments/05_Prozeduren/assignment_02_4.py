def sum_of_list(number_list: list[int]) -> list[int]:
    number_list.append(sum(number_list))
    return number_list

print(sum_of_list([1, 2, 3]))