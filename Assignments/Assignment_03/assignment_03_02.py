import turtle
import math

outer_square_length = 218

def draw_square(length):
    corners = 4
    corner_angle = 90

    for i in range(corners):
        turtle.forward(length)
        turtle.right(corner_angle)

def draw_inner_square():
    turtle.penup()
    turtle.forward(outer_square_length / 2)
    turtle.right(45)
    turtle.pendown()
    draw_square(outer_square_length / 2**0.5)

turtle.speed(20)

draw_square(outer_square_length)
draw_inner_square()

turtle.done()