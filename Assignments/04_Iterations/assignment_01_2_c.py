import turtle

CORNERS = 5
INNER_ANGLE_TOTAL = 540
SIDE_LENGTH = 100
INNER_ANGLE = INNER_ANGLE_TOTAL / CORNERS

turtle_rotation = 180 - INNER_ANGLE

for i in range(CORNERS):
    turtle.forward(SIDE_LENGTH)
    turtle.right(turtle_rotation)

turtle.speed(50)
turtle.done()
