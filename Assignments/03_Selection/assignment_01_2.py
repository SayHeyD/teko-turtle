import turtle

def calculate_triangle_height(length):
    return (length**2 - (length / 2)**2)**0.5

def draw_triangle(length):
    corners = 3
    inner_corner_angle = 60

    turtle_rotation = 180 - inner_corner_angle

    turtle.right(60)

    for i in range(corners):
        turtle.forward(length)
        turtle.right(turtle_rotation)

    turtle.right(30)

def draw_stem():
    length = 50
    width = 20

    turtle.forward(width / 2)
    turtle.right(90)
    turtle.forward(length)
    turtle.right(90)
    turtle.forward(width)
    turtle.right(90)
    turtle.forward(length)

def draw_tree():
    turtle.speed(50)

    first_length = 50
    second_length = 75
    third_length = 100

    # Draw first triangle
    draw_triangle(first_length)
    # Position turtle for the second triangle
    turtle.penup()
    turtle.forward(calculate_triangle_height(first_length))
    turtle.pendown()
    turtle.left(90)
    # Draw the second triangle
    draw_triangle(second_length)
    # Position turtle for the third triangle
    turtle.penup()
    turtle.forward(calculate_triangle_height(second_length))
    turtle.pendown()
    turtle.left(90)
    # Draw the third triangle
    draw_triangle(third_length)
    # Position the turtle for the tree stem
    turtle.penup()
    turtle.forward(calculate_triangle_height(third_length))
    turtle.pendown()
    turtle.left(90)

    # Draw tree stem
    draw_stem()

    turtle.done()

def draw_star(points, length):
    if points % 2 == 0:
        raise Exception('Cannot draw stars with even number of points!')

    turtle.speed(50)

    outer_angle = 180 - 180 / points

    for i in range(points):
        turtle.right(outer_angle)
        turtle.forward(length)

while True:
    user_input = input('Soll ich einen Baum oder Stern zeichnen?\n')
    user_input = user_input.lower()

    if user_input == 'baum':
        draw_tree()
        turtle.done()
        exit()
    elif user_input == 'stern':
        draw_star(5, 200)
        turtle.done()
        exit()
    else:
        print('Ich kann nur einen Baum oder Stern zeichnen 😭')