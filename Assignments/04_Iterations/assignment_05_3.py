participant_ages = [14, 35, 29, 20, 40, 38, 66, 17, 20, 26, 31, 49]

juniors = list(filter(lambda num: num <= 22, participant_ages))
seniors = list(filter(lambda num: num > 22, participant_ages))

oldest_junior = max(juniors)
youngest_senior = min(seniors)

juniors_count = len(juniors)
seniors_count = len(seniors)

print(f'Alle Junioren: {juniors} ({juniors_count} Teilnehmer)')
print(f'Alle Senioren: {seniors} ({seniors_count} Teilnehmer)')

print(f'Ältester Junior: {oldest_junior}')
print(f'Jüngster Senior: {youngest_senior}')
