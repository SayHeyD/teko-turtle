import turtle

corners = 3
length = 144

inner_corner_angle = 60
turtle_rotation = 180 - inner_corner_angle

def get_height():
    adjacent_cathetus = length / 2
    return (length**2 - adjacent_cathetus**2) ** 0.5

def draw_height():
    turtle.penup()
    turtle.forward(length / 2)
    turtle.pendown()
    turtle.color("BlueViolet")
    turtle.left(90)
    turtle.forward(get_height())

for i in range(corners):
    turtle.forward(length)
    turtle.left(turtle_rotation)

draw_height()

turtle.done()