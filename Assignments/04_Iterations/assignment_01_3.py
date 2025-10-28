import math
import turtle

# Durchmesser eines Kreises mit forward(1) und right(1) ist 115
DEFAULT_CIRCLE_DIAMETER = 115

RIGHT_ANGLE = 90
HALF_TURN = 180
RADIUS = 100

DISTANCE_X1 = math.floor(RADIUS / 4)
DISTANCE_X2 = DISTANCE_X1 * 2

DISTANCE_X0_5 = DISTANCE_X1 / 2
DISTANCE_X0_25 = DISTANCE_X1 / 4

def draw_nose() -> None:
    turtle.right(RIGHT_ANGLE)
    turtle.penup()
    turtle.forward(RADIUS)
    turtle.pendown()
    turtle.forward(RADIUS / 2)
    turtle.left(RIGHT_ANGLE)

def draw_mouth() -> None:
    turtle.penup()
    turtle.forward(DISTANCE_X1)
    turtle.pendown()
    turtle.color('Red')
    turtle.right(RADIUS)
    # 180 degrees will create a slight unwanted angle of the turtle (haven't found out why)
    draw_circle(DISTANCE_X1, 170)
    turtle.right(RIGHT_ANGLE)
    turtle.color('Black')

def draw_eye():
    turtle.penup()
    turtle.forward(DISTANCE_X0_5)
    turtle.right(RIGHT_ANGLE)
    turtle.color('Blue')
    turtle.pendown()
    draw_circle(DISTANCE_X0_5)
    turtle.color('Black')
    turtle.left(RIGHT_ANGLE)

def draw_circle(circle_radius: int|float, degrees: int = 360) -> None:

    # Der size_factor ist nicht exakt, reicht für unsere Zwecke allerdings aus
    size_factor = circle_radius * 2 / DEFAULT_CIRCLE_DIAMETER

    for _ in range(degrees):
        turtle.forward(1 * size_factor)
        turtle.right(1)


# Helper zum herausfinden des Durchmessers
def draw_diameter(diameter: int|float = 115):
    turtle.right(RIGHT_ANGLE)
    turtle.color('Red')
    turtle.forward(diameter)
    turtle.right(HALF_TURN)
    turtle.forward(diameter)
    turtle.right(RIGHT_ANGLE)
    turtle.color('Black')

turtle.speed(200)

draw_circle(RADIUS)
draw_nose()
draw_mouth()

# Get in position for the first eye
turtle.penup()
turtle.left(RIGHT_ANGLE)
turtle.forward(DISTANCE_X2)
turtle.left(RIGHT_ANGLE)
turtle.forward(DISTANCE_X0_5)
turtle.right(HALF_TURN)
turtle.pendown()

draw_eye()

# Get in position for the second eye
turtle.penup()
turtle.forward(DISTANCE_X2)
turtle.forward(DISTANCE_X0_5)
turtle.pendown()

draw_eye()

# Move turtle out of the way
turtle.penup()
turtle.goto(-10_000, -10_000)
turtle.pendown()

turtle.done()