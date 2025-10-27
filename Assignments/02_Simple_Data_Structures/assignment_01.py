result_invalid = True

while result_invalid:

    value = input('Bitte geben Sie einen Wert ein:\n')
    try:
        value = float(value)
        result_invalid = False
    except ValueError:
        print('Der eigenebene Wert ist keine Zahl!')
        continue

    divided_result = round(value / 3)

    print('Das Resultat ist: ' + str(divided_result))