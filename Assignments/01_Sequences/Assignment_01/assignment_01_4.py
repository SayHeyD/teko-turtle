import turtle

corners = 3
primary_length = 100
secondary_length = 75
inner_rotation_angle = 40

# Set starting orientation
turtle.right(120)

for i in range(corners):

    if i % 2 == 0:
        turtle.forward(primary_length)
        turtle.left(180 - inner_rotation_angle)
    else:
        turtle.forward(secondary_length)
        turtle.right(180 - inner_rotation_angle)

input()