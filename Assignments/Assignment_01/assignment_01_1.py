import turtle

corners = 4
corner_angle = 90
length = 150

for i in range(corners):
    turtle.forward(length)
    turtle.right(corner_angle)

turtle.done()