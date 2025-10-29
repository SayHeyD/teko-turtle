numbers = [
    5,
    3,
    7,
    6,
    1,
    10,
    2,
    14,
    1,
]

def bubble_sort(nums: list[int]) -> (int, int):
    switches = 0
    iterations = 0

    for key, number in enumerate(nums):

        if key == len(numbers) - 1:
            break

        iterations += 1

        if numbers[key + 1] < number:
            switches += 1
            numbers[key], numbers[key + 1] = numbers[key + 1], numbers[key]

    return switches, iterations

continue_sorting = True
total_iterations = 0
total_switches = 0

while continue_sorting:
    run_switches, run_iterations = bubble_sort(numbers)

    total_iterations += run_iterations
    total_switches += run_switches

    continue_sorting = run_switches != 0

print(f'Sorted list: {numbers}')
print(f'Total sorting iterations: {total_iterations}')
print(f'Total switches: {total_switches}')
