while True:
    user_input = input('Wie geht es dir?\n')
    user_input = user_input.lower()

    if user_input == 'gut':
        print('Das freut mich 😁')
        exit()
    elif user_input == 'schlecht':
        print('Das tut mir leid 🥹')
        exit()
    else:
        print('DIR GEHT ES ENTWEDER "gut" ODER "schlecht"! 🤬')
        print('ALLE ANDEREN BEFINDUNGEN EXISTIEREN NICHT')