import turtle

INNER_ANGLE = 120
ROTATION_PER_TURN = 180 - INNER_ANGLE

ELEMENT_LENGTH = 100
REDUCTION_PER_ELEMENT = 1

turtle.speed(50)

while True:
    turtle.forward(ELEMENT_LENGTH)
    turtle.right(ROTATION_PER_TURN)
    ELEMENT_LENGTH -= REDUCTION_PER_ELEMENT

    if ELEMENT_LENGTH <= 5:
        break

# Would be more sensible to do something like this
#
# while ELEMENT_LENGTH > 5:
#     turtle.forward(ELEMENT_LENGTH)
#     turtle.right(ROTATION_PER_TURN)
#     ELEMENT_LENGTH -= REDUCTION_PER_ELEMENT

turtle.done()