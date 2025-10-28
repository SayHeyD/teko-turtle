import turtle

RIGHT_ANGLE = 90
HALF_TURN = 180

def draw_step(step_length, step_height) -> None:
    turtle.left(RIGHT_ANGLE)
    turtle.forward(step_height)
    turtle.right(RIGHT_ANGLE)
    turtle.forward(step_length)

def draw_casing(step_count, step_length, step_height) -> None:
    turtle.right(RIGHT_ANGLE)
    turtle.forward(step_count * step_height)
    turtle.right(RIGHT_ANGLE)
    turtle.forward(step_count * step_length)
    turtle.right(HALF_TURN)

def get_number_input(prompt) -> int:

    error_message = 'Die Angabe muss eine Ganzzahl sein!'

    while True:
        user_input = input(prompt)

        try:
            user_input = int(user_input)

            if user_input <= 0:
                print(error_message)
                continue

        except ValueError:
            print(error_message)
            continue

        return user_input

    return 0

def draw(step_count, step_length, step_height) -> None:
    for step in range(step_count):
        draw_step(step_length, step_height)

    draw_casing(step_count, step_length, step_height)
    turtle.done()

length = get_number_input('Bitte gib die Länge der Treppenstufen an:\n')
height = get_number_input('Bitte gib die Höhe der Treppenstufen an:\n')
steps = get_number_input('Bitte gib die Anzahl der Treppenstufen an:\n')

turtle.speed(50)
draw(steps, length, height)