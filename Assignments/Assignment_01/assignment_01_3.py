import turtle

corners = 4
length = 100
corner_angle = 120

# Set starting orientation
turtle.left(corner_angle / 4)

for i in range(corners):

    if i % 2 == 0:
        turtle.right(180 - corner_angle)
    else:
        turtle.right(corner_angle)

    turtle.forward(length)

input()