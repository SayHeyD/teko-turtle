# Limit the number of possible iterations
LIMIT = 10_000

for i in range(LIMIT + 1):
    if not i % 7 and i % 3:
        print(i)