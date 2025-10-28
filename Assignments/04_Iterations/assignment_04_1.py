counter = 1
divider = 1

fraction_sum = 0

while fraction_sum + (counter / divider) < 5:
    fraction_sum += (counter / divider)
    divider += 1

print(f'Nenner: {divider}')
print(f'Summe: {fraction_sum}')
