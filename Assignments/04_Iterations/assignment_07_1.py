prime_search_limit = 10_000

found_primes = []
iterations = 0

def print_current_prime(prime_number):
    print(f'Found prime: {prime_number}', end='\r')

print('Searching for primes...')

for number in range(2, prime_search_limit):

    if len(found_primes) == 0:
        found_primes.append(number)
        print_current_prime(number)
        continue

    for key, prime in enumerate(found_primes):
        iterations += 1
        if number % prime == 0:
            break

        if key == len(found_primes) - 1:
            found_primes.append(number)
            print_current_prime(number)

print(f'Primes: {found_primes}')
print(f'Found {len(found_primes)} primes')
print(f'Iterations: {iterations}')