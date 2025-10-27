import turtle
import math

def draw_water():
    length = 2*30 + 80
    turtle.color("Blue")
    turtle.forward(length)
    turtle.penup()
    turtle.home()
    turtle.pendown()

def draw_boat_body():
    water_offset = 30
    body_base_length = 80
    body_side_length = 20
    railing_length = 100
    inner_base_angle = 60

    turtle.color("Brown")
    turtle.penup()
    turtle.goto(water_offset, 0)
    turtle.pendown()
    turtle.forward(body_base_length)
    turtle.left(inner_base_angle)
    turtle.forward(body_side_length)
    turtle.left(180 - inner_base_angle)
    turtle.forward(railing_length)
    turtle.left(180 - inner_base_angle)
    turtle.forward(body_side_length)
    turtle.left(inner_base_angle)

def draw_mast():
    body_base_length = 80
    mast_height = 100
    body_side_length = 20
    inner_base_angle = 60
    inner_base_radius = math.radians(inner_base_angle)
    gamma_radius = math.radians(90)

    # Calculate body height
    boat_body_height = (body_side_length * math.sin(inner_base_radius)) / math.sin(gamma_radius)

    turtle.color("Brown")
    turtle.penup()
    turtle.goto(body_base_length / 2 + 30, boat_body_height)
    turtle.left(90)
    turtle.pendown()
    turtle.forward(mast_height)

def draw_sail():
    corners = 3
    length = 100
    inner_corner_angle = 60
    turtle_rotation = 180 - inner_corner_angle

    # Set color and initial rotation
    turtle.color("Yellow")
    turtle.left(180 + 30)

    for i in range(corners):
        turtle.forward(length)
        turtle.right(turtle_rotation)

turtle.speed(20)

draw_water()
draw_boat_body()
draw_mast()
draw_sail()

turtle.done()