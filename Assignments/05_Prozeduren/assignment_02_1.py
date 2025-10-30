import turtle

def polygon_circle(corners, circumference):

    if corners < 35:
        raise ValueError("The number of corners must be greater than 35.")

    if circumference < 100:
        raise ValueError("The circumference must be greater than 100.")

    for i in range(corners):
        turtle.forward(circumference / corners)
        turtle.right(360 / corners)

turtle.speed(50)

polygon_circle(35, 100)

turtle.done()