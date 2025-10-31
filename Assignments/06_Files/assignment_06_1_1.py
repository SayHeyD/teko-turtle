import os
import tempfile
import time

def normalize_file_name(filename: str) -> str:
    # Add a leading slash if not present
    if not filename.startswith(os.sep):
        return os.sep + filename

    return filename


def create_file(filename: str) -> None:

    filename = normalize_file_name(filename)

    try:
        with open(tempfile.gettempdir() + filename, 'x') as file:
            file.write('1')
    except FileExistsError:
        print('Skipping file creation: File already exists!')

def write_to_file(filename: str, content: str) -> None:

    filename = normalize_file_name(filename)

    try:
        with open(tempfile.gettempdir() + filename, 'w') as file:
            file.write(content)
    except FileNotFoundError:
        print('Could not write to file: File not found!')
        exit(1)

def read_from_file(filename: str) -> str:

    filename = normalize_file_name(filename)

    try:
        with open(tempfile.gettempdir() + filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print('Could not read file: File not found!')
        exit(1)

def get_last_prime(filename: str) -> int:
    try:
        content = int(read_from_file(filename))
    except ValueError:
        content = 1

    return content

def is_prime(number: int, current_iterations) -> (bool, int):
    current_iterations += 1

    # What the f**k is happening here?
    # ================================
    #
    # Basically, instead of calculating a lot of unnecessary divisions in
    # hopes of finding a magic divider that mathematically and logically
    # cannot exist, we just calculate the absolute minimum of options
    # required to safely determine if the given number is a prime.
    #
    # 1. If the number is even, it is divisible by 2 → not a prime number, return False
    # 2. Compute the integer square root; no divisor greater than sqrt(number) needs checking
    #     * A number cannot have two or more factors both greater than its square root because
    #       their product would exceed the original number
    # 3. Try only odd divisors from 3 up to that limit. If it divides evenly -> not a prime number, return False
    #    * All even numbers are excluded in step 1
    # 4. If no divisor was found in the previous steps -> is a prime number, return True
    if number % 2 == 0:
        return False, current_iterations

    sqrt_of_number = int(number**0.5)

    for d in range(3, sqrt_of_number + 1, 2):
        if number % d == 0:
            return False, current_iterations

    return True, current_iterations

def get_next_prime(start_number: int) -> (int, int):
    passed_iterations = 0

    # Our for loop only works for number greater than 1
    if start_number == 1:
        return 2, 1

    for number in range(start_number + 1, start_number * 2):
        is_prime_number, passed_iterations = is_prime(number, passed_iterations)
        print(f'Testing number: {number}', end='\r')
        if is_prime_number:
            print(f'Testing number: {number}')
            return number, passed_iterations

    raise Exception('No prime found!')

file_name = 'assignment_06_1_1.txt'

create_file(file_name)
last_prime = get_last_prime(file_name)
print(f'Last found prime: {last_prime}')
print('Continuing to search for next prime...')

calculation_start_time = time.time()
next_prime, iterations = get_next_prime(last_prime)
required_time = time.time() - calculation_start_time
last_prime = next_prime

write_to_file(file_name, str(next_prime))

print(f'Time required for finding next prime: {required_time} seconds')
print(f'Iteration count: {iterations}')
print(f'Next prime: {next_prime}')
file_name = normalize_file_name(file_name)
print(f'Results written to file: {tempfile.gettempdir() + file_name}')
