import math
import turtle

hypotenuse_length = 185
radius = 45
gamma_radius = 90
side_length = hypotenuse_length / math.sqrt(2)

def triangle():
    turtle.forward(hypotenuse_length)
    turtle.left(180 - radius)

    turtle.forward(side_length)
    turtle.left(gamma_radius)

    turtle.forward(side_length)
    turtle.left(180 - radius)

turtle.speed(10)

# Draw roof
triangle()
turtle.right(gamma_radius)

# House body
for i in range(3):
    triangle()
    turtle.penup()
    turtle.forward(hypotenuse_length)
    turtle.pendown()
    turtle.left(gamma_radius)


turtle.done()