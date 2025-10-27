import turtle

corners = 3
length = 200

inner_corner_angle = 60

turtle_rotation = 180 - inner_corner_angle

for i in range(corners):
    turtle.forward(length)
    turtle.right(turtle_rotation)

turtle.done()